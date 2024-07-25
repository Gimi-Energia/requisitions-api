import uuid
from apps.purchases.models import Purchase, PurchaseProduct
from setup import settings
from utils.email import EmailUtils
from .pdf_service import generate_pdf


class PurchaseEmailService:

    @property
    def email_utils(self):
        return EmailUtils()
    
    @property
    def purchase_service(self):
        from apps.purchases.services.purchases_service import PurchasesService
        return PurchasesService()
    
    @property
    def user_service(self):
        from apps.users.service import UserService
        return UserService()
    
      #TODO Pensar se faz sentido manter aqui ou criar outro arquivo
    def get_purchase_product_with_coditional(self, purchase_id: uuid.UUID, approved_only: bool = True, generic_only: bool = False):
        purchase_product = self.purchase_service.get_purchase_product_by_status(purchase_id, "Approved")
        if not approved_only and not generic_only:
            return self.purchase_service.get_purchase_products_by_purchase_id(purchase_id)
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

    def mount_purchase_quotation_email(self, purchase: Purchase):
        emails = [purchase.requester]
        email_subject = "Cotação de Compra Criada"
        email_body_intro = """
            Olá!<br>
            Uma solicitação está agora em cotação e precisa de mais informações antes de ser processada.<br>
        """
        
        table_html = self.build_purchase_products_from_email(purchase.id, approved_only=False, price=False)
        common_body = self.build_common_body(purchase, table_html)
        content = {'common_body': common_body, 'email_body_intro': email_body_intro}
        emails += list(self.user_service.get_user_by_contains_email().values_list('email', flat=True))

        data = {
            'subject': email_subject,
            'message': "This is a plain text for email clients that don't support HTML",
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': emails,
            'html_message': self.email_utils.get_base_email(content=content),
            'fail_silently': False
        }
        return data
    
    def mount_generic_product_email(self, purchase: Purchase):
        emails = [purchase.requester]
        email_subject = "Cadastro de Produto Genérico"
        table_html = self.build_purchase_products_from_email(purchase.id, 
                                                             approved_only=False, 
                                                             price=False, 
                                                             generic_only=True)
        
        email_body_intro = f'''Olá, {purchase.requester.name}!<br>
            Sua requisição de compra Nº {purchase.control_number} foi aprovada, 
            porém contém produtos genéricos.<br><br>
        '''
        common_body = f'''Observações da requisição: {purchase.obs}
            {table_html}<br>

            Para prosseguirmos com esse processo, será necessário 3 passos:<br> 
                1 - Solicite o cadastro do material<br>
                2 - Crie a requisição diretamente no Omie (incluindo todos os itens da requisição e não somente o item genérico)<br>
                3 - Inclua na observação interna da requisição dentro do OMIE que se trata da cotação Nº {purchase.control_number} do App de Requisições.
        '''
        content = {'common_body': common_body, 'email_body_intro': email_body_intro}

        data = {
            'subject': email_subject,
            'message': "This is a plain text for email clients that don't support HTML",
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': emails,
            'html_message': self.email_utils.get_base_email(content=content),
            'fail_silently': False
        }
        return data
    
    def mount_quotation_email_with_pdf(self, purchase: Purchase):
        subject = f"Cotação de Compra Nº {purchase.control_number} - Grupo Gimi"
        recipient_list = purchase.quotation_emails.replace(" ", "").split(",")
        email_from = settings.EMAIL_HOST_USER
        emails_gimi = list(self.user_service.get_user_by_contains_email().values_list('email', flat=True))
        pdf_file = generate_pdf(purchase)
        with open(pdf_file, "rb") as pdf_file_content:
            pdf_data = pdf_file_content.read()
        body_message = f"""Prezado fornecedor,

            Anexo o arquivo PDF com a carta de cotação Nº {purchase.control_number}

            Por favor, responder este e-mail com os valores e condições de pagamento de acordo 
            com a carta anexa.

            Atenciosamente,

            Grupo Gimi
        """
        list_send_email = []
        data_attach = {
            "filename": f"carta_cotacao_compra_{purchase.control_number}.pdf",
            "content": pdf_data,
            "mimetype": "application/pdf"
        }
        
        for recipient in recipient_list:
            if recipient != "":
                all_recipients = [recipient, purchase.requester] + emails_gimi
                data_recipient = {
                    "subject": subject,
                    "body": body_message,
                    "from_email": email_from,
                    "to": all_recipients
                }
                list_send_email.append({"data_email":data_recipient, "data_attach": data_attach})
        return list_send_email