import uuid
from http import HTTPStatus
from django.core.mail import EmailMessage, send_mail
from setup import settings
from functools import partial

from django.http import JsonResponse
from ninja.errors import HttpError

from apps.purchases.models import Purchase, PurchaseProduct
from apps.purchases.schema import (
    PurchaseBaseSchema,
    PurchaseInputCreateSchema,
    PurchaseProductInputSchema,
)
from apps.users.service import UserService
from utils.email import EmailUtils

class PurchasesService:
    @property
    def user_service(self):
        return UserService()

    @property
    def email_utils(self):
        return EmailUtils()
    
    def get_purchase_products_by_purchase_id(self, purchase_id: uuid.UUID):
        return PurchaseProduct.objects.filter(purchase_id=purchase_id)

    def get_purchase_product_by_status(self, purchase_id: uuid.UUID, status: str):
        return PurchaseProduct.objects.filter(purchase_id=purchase_id, status=status)

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
    
    #TODO Pensar se faz sentido manter aqui ou criar outro arquivo
    def get_purchase_product_with_coditional(self, purchase_id: uuid.UUID, approved_only: bool = True, generic_only: bool = False):
        purchase_product = self.get_purchase_product_by_status(purchase_id, "Approved")
        if not approved_only:
            return self.get_purchase_products_by_purchase_id(purchase_id)
        if generic_only:
            return purchase_product.filter(product__code__icontains="GENERIC")
        return purchase_product

    def mount_table_purchase_products(self, purchase_product: PurchaseProduct, price: bool):
        rows = f"<tr><td>{purchase_product.product.code}</td><td>{purchase_product.product.description}</td><td>{purchase_product.quantity}</td>"
        if price:
            rows += f"<td>R$ {purchase_product.price}</td>"
        rows += "</tr>"
        
        return rows

    def build_common_body(self, purchase: Purchase, table_html: str = ''):
        common_body = f"""
                Dados da solicitação:<br>
                Empresa: {purchase.company}<br>
                Departamento: {purchase.department}<br>
                Data solicitada: {purchase.request_date.strftime("%d/%m/%Y")}<br>
                Aprovador: {purchase.approver}<br>
                Número de controle: {purchase.control_number}<br>
                Motivo: {purchase.motive}<br>
                Obsevações: {purchase.obs}<br>
                Produtos: <br>{table_html}
            """
        return common_body
    
    def build_purchase_products_from_email(self, purchase_id: uuid.UUID, approved_only: bool = True, generic_only: bool = False, price: bool = True):
        list_purchase_products = self.get_purchase_product_with_coditional(purchase_id, approved_only, generic_only)
        data_rows = [self.mount_table_purchase_products(purchase_product, price) for purchase_product in list_purchase_products]

        if not data_rows:
            return False
        price_header = "<th>Preço Un.</th>" if price else ""
        
        return f"""
        <table border="1">
            <tr>
                <th>Código</th>
                <th>Descrição</th>
                <th>Quantidade</th>
                {price_header}
            </tr>
            {''.join(data_rows)}
        </table>
        """
    
    def mount_status_change_email(self, purchase: Purchase):
        emails = [purchase.requester]

        if purchase.status == "Approved":
            email_subject = "Solicitação de Compra Aprovada"
            email_body_intro = f"""
                        Olá, {purchase.requester.name}!<br>
                        Sua solicitação foi aprovada por {purchase.approver} 
                        em {purchase.approval_date.strftime("%d/%m/%Y")}<br>
                    """
            table_html = self.build_purchase_products_from_email(purchase.id)
            emails = list(self.user_service.get_user_by_contains_email().values_list('email', flat=True))
        elif purchase.status == "Denied":
            email_subject = "Solicitação de Compra Rejeitada"
            email_body_intro = f"""
                Olá, {purchase.requester.name}!<br>
                Sua solicitação foi rejeitada por {purchase.approver} 
                em {purchase.approval_date.strftime("%d/%m/%Y")}<br>
            """
            table_html = self.build_purchase_products_from_email(purchase.id, approved_only=False)
        elif purchase.status == "Opened":
            title = "Cotada" if purchase.has_quotation else "Criada"
            email_subject = f"Solicitação de Compra {title}"
            email_body_intro = f"""
                Olá, {purchase.requester.name}!<br>
                A requisição Nº {purchase.control_number} 
                já pode ser aprovada por {purchase.approver}<br>
            """
            table_html = self.build_purchase_products_from_email(purchase.id, approved_only=False)
            
            emails.append(purchase.approver)
        else:
            return
        common_body = self.build_common_body(purchase, table_html)
        content = {'common_body': common_body, 'email_body_intro': email_body_intro}
        html_message = self.email_utils.get_base_email(content=content)

        data = {
            'subject': email_subject,
            'message': "This is a plain text for email clients that don't support HTML",
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': emails,
            'html_message': html_message,
            'fail_silently': False
        }
        return data

    def purchase_send_email(self, purchase: Purchase, send_email_type: str):
        options_send_email = {
            'status_change': partial(self.mount_status_change_email, purchase=purchase),
            'purchase_quotation': ''
        }
        send_mail(**options_send_email[send_email_type]())
        return JsonResponse({"message": "Email sent successfully"})
    
    
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
