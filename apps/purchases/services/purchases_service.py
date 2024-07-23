import uuid
from http import HTTPStatus

from django.http import JsonResponse
from ninja.errors import HttpError

from apps.purchases.models import Purchase, PurchaseProduct
from apps.purchases.schema import (
    PurchaseBaseSchema,
    PurchaseInputCreateSchema,
    PurchaseProductInputSchema,
)
from apps.users.service import UserService


class PurchasesService:
    @property
    def user_service(self):
        return UserService()

    def get_purchase_products_by_purchase_id(self, purchase_id: uuid.UUID):
        return PurchaseProduct.objects.filter(purchase_id=purchase_id)

    def get_purchase_products_by_purchase_id_and_product_id(
        self, purchase_id: uuid.UUID, product_id: uuid.UUID
    ):
        return PurchaseProduct.objects.filter(
            purchase_id=purchase_id, product_id=product_id
        ).first()

    def get_purchase_by_id(self, purchase_id: uuid.UUID):
        return Purchase.objects.filter(id=purchase_id).first()

    def delete_purchase_product_by_purchase_id_and_product_id(
        self, purchase_id: uuid.UUID, product_id: uuid.UUID
    ):
        return self.get_purchase_products_by_purchase_id_and_product_id(
            purchase_id, product_id
        ).delete()

    def update_purchase_product_by_purchase_id_and_product_id(
        self, purchase_id: uuid.UUID, product_id: uuid.UUID, input_data: PurchaseProductInputSchema
    ):
        purchase_product = self.get_purchase_products_by_purchase_id_and_product_id(
            purchase_id, product_id
        )
        for key, value in input_data.dict(exclude_defaults=True, exclude_unset=True).items():
            setattr(purchase_product, key, value)
        purchase_product.save()
        return purchase_product

    def build_purchases_products(self, purchase_id: uuid.UUID):
        data = []
        for purchase_product in self.get_purchase_products_by_purchase_id(purchase_id):
            data.append(
                {
                    "id": purchase_product.product.id,
                    "un": purchase_product.product.un,
                    "description": purchase_product.product.description,
                    "code": purchase_product.product.code,
                    "quantity": purchase_product.quantity,
                    "price": purchase_product.price,
                    "status": purchase_product.status,
                }
            )
        return data

    def build_purchase_data(self, purchases: Purchase):
        data = PurchaseBaseSchema.from_orm(purchases).dict()
        data["id"] = purchases.id
        data["products"] = self.build_purchases_products(purchases.id)
        data["requester"] = purchases.requester
        data["approver"] = purchases.approver
        data["department"] = purchases.department
        data["created_at"] = purchases.created_at
        return data

    def create_purchase(self, input_data: PurchaseInputCreateSchema):
        data = input_data.dict()
        data.pop("products")
        purchase = Purchase.objects.create(**data)
        return purchase

    def create_purchase_product(
        self, purchase_id: uuid.UUID, input_data: PurchaseProductInputSchema
    ):
        return PurchaseProduct.objects.create(purchase_id=purchase_id, **input_data.dict())

    def create_purchase_products_in_list(
        self, purchase_id: uuid.UUID, list_purchase_product: list[PurchaseProductInputSchema]
    ):
        for purchase_product in list_purchase_product:
            self.create_purchase_product(purchase_id, purchase_product)
        return self.get_purchase_products_by_purchase_id(purchase_id)

    def create(self, input_data: PurchaseInputCreateSchema):
        purchase = self.create_purchase(input_data)
        self.create_purchase_products_in_list(purchase.id, input_data.products)
        return self.build_purchase_data(purchase)

    def add_product(self, purchase_id: uuid.UUID, input_data: PurchaseProductInputSchema):
        if not (purchase := self.get_purchase_by_id(purchase_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Purchase not found")
        self.create_purchase_product(purchase_id, input_data)
        return self.build_purchase_data(purchase)

    def delete_product(self, purchase_id: uuid.UUID, product_id: uuid.UUID):
        if not (self.get_purchase_by_id(purchase_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Purchase not found")
        if not (self.get_purchase_products_by_purchase_id_and_product_id(purchase_id, product_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Product not found")

        self.delete_purchase_product_by_purchase_id_and_product_id(purchase_id, product_id)

        return JsonResponse({"message": "Product deleted successfully"})

    def update_product(
        self, purchase_id: uuid.UUID, product_id: uuid.UUID, input_data: PurchaseProductInputSchema
    ):
        if not (purchase := self.get_purchase_by_id(purchase_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Purchase not found")
        if not (self.get_purchase_products_by_purchase_id_and_product_id(purchase_id, product_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Product not found")

        self.update_purchase_product_by_purchase_id_and_product_id(
            purchase_id, product_id, input_data
        )

        return self.build_purchase_data(purchase)

    def list(self):
        list_data = []
        list_purchases = Purchase.objects.all()
        for purchases in list_purchases:
            list_data.append(self.build_purchase_data(purchases))
        return list_data

    def delete(self, purchase_id: uuid.UUID):
        purchase = self.get_purchase_by_id(purchase_id)
        if not purchase:
            raise HttpError(HTTPStatus.NOT_FOUND, "Purchase not found")
        purchase.delete()
        return JsonResponse({"message": "Purchase deleted successfully"})

    def get(self, purchase_id: uuid.UUID):
        if not (purchase := self.get_purchase_by_id(purchase_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Purchase not found")
        return self.build_purchase_data(purchase)

    def update(self, purchase_id: uuid.UUID, input_data: PurchaseInputCreateSchema):
        if not (purchase := self.get_purchase_by_id(purchase_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Purchase not found")

        for attr, value in input_data.model_dump(exclude_defaults=True, exclude_unset=True).items():
            print(attr, value)
            setattr(purchase, attr, value)

        purchase.save()
        purchase.refresh_from_db()

        return purchase
