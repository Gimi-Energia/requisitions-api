import uuid
from http import HTTPStatus

from django.db import transaction
from django.http import JsonResponse
from ninja.errors import HttpError

from apps.products.models import Product
from apps.products.schema import ProductSchemaInput
from apps.products.services.iapp_service import get_iapp_products


class ProductService:
    def get_all_products(self):
        return Product.objects.all()

    def get_product_by_id(self, product_id: uuid.UUID):
        return Product.objects.filter(id=product_id).first()

    def list_products_by_list_code(self, list_code: list[str]):
        return Product.objects.filter(code__in=list_code)

    def get_product_by_code(self, code: str):
        return Product.objects.filter(code=code).first()

    def bulk_create_product(self, list_products: list[Product]):
        with transaction.atomic():
            return Product.objects.bulk_create(list_products)

    def __filter_products(self, products: Product, **kwargs):
        if code := kwargs.get("code"):
            if not products:
                products = Product.objects.filter(code=code)
            else:
                products = products.filter(code=code)
        if un := kwargs.get("un"):
            if not products:
                products = Product.objects.filter(un=un)
            else:
                products = products.filter(un=un)
        if description := kwargs.get("description"):
            if not products:
                products = Product.objects.filter(description=description)
            else:
                products = products.filter(description=description)

        return products

    def list(self, **kwargs):
        if not kwargs.get("code") and not kwargs.get("un") and not kwargs.get("description"):
            products = self.get_all_products()
        else:
            products = self.__filter_products(None, **kwargs)
        orderby = kwargs.get("orderby", "code")
        products = products.order_by(orderby)
        total = products.count()
        offset_max = int(kwargs.get("offset_max"))
        offset_min = int(kwargs.get("offset_min"))
        data = {"total": total, "products": products[offset_min:offset_max]}
        return data

    def get(self, product_id: uuid.UUID):
        if not (product := self.get_product_by_id(product_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Product not found")
        return product

    def create(self, input_data: ProductSchemaInput):
        if self.get_product_by_code(input_data.code):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Product already exists")

        product = Product.objects.create(**input_data.dict())
        return product

    def update(self, product_id: uuid.UUID, input_data: ProductSchemaInput):
        product = self.get_product_by_id(product_id)
        if not product:
            raise HttpError(HTTPStatus.NOT_FOUND, "Product not found")

        for attr, value in input_data.model_dump(exclude_defaults=True, exclude_unset=True).items():
            print(attr, value)
            setattr(product, attr, value)
        product.save()
        product.refresh_from_db()
        return product

    def delete(self, product_id: uuid.UUID):
        product = self.get_product_by_id(product_id)
        if not product:
            raise HttpError(HTTPStatus.NOT_FOUND, "Product not found")
        product.delete()
        return JsonResponse({"message": "Product deleted successfully"})

    def sync_iapp(self):
        try:
            iapp_products = get_iapp_products()
            if not iapp_products:
                raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Error finding products")

            list_product_exists = self.list_products_by_list_code(
                [iapp_product["code"] for iapp_product in iapp_products]
            )
            list_product_exists = list_product_exists.values_list("code", flat=True)
            list_product_for_create = []

            for product in iapp_products:
                if (
                    product["code"] not in list_product_exists
                    and product["code"] not in list_product_for_create
                ):
                    list_product_for_create.append(Product(**product))

            self.bulk_create_product(list_product_for_create)
            return {"message": "Data entered successfully"}
        except Exception as e:
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Error inserting data: " + str(e))
