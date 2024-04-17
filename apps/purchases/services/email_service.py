from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from apps.products.models import Product
from apps.purchases.models import PurchaseProduct

from .pdf_service import generate_pdf


def build_quotation_table(purchase_pk, include_approved_only=True, include_price=True):
    if include_approved_only:
        purchase_products = PurchaseProduct.objects.filter(purchase=purchase_pk, status="Approved")
    else:
        purchase_products = PurchaseProduct.objects.filter(purchase=purchase_pk)

    table_rows = []

    for purchase_product in purchase_products:
        product_code = purchase_product.product.code
        product = Product.objects.filter(code=product_code).first()
        product_description = product.description
        product_quantity = purchase_product.quantity

        if include_price:
            product_price = f"<td>R$ {purchase_product.price}</td>"
        else:
            product_price = ""

        table_row = f"<tr><td>{product_code}</td><td>{product_description}</td><td>{product_quantity}</td>{product_price}</tr>"
        table_rows.append(table_row)

    if not table_rows:
        return ""

    price_header = "<th>Preço Un.</th>" if include_price else ""

    return f"""
        <table border="1">
            <tr>
                <th>Código</th>
                <th>Descrição</th>
                <th>Quantidade</th>
                {price_header}
            </tr>
            {''.join(table_rows)}
        </table>
    """


def send_status_change_email(instance):
    email_subject = ""
    email_body_intro = ""
    table_html = ""

    if instance.status == "Approved":
        email_subject = "Solicitação de Compra Aprovada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi aprovada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}<br>
        """
        table_html = build_quotation_table(instance.id)
    elif instance.status == "Denied":
        email_subject = "Solicitação de Compra Rejeitada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi rejeitada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}<br>
        """
        table_html = build_quotation_table(instance.id, include_approved_only=False)
    elif instance.status == "Opened":
        email_subject = "Solicitação de Compra Cotada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi cotada e já pode ser aprovada<br>
        """
        table_html = build_quotation_table(instance.id)

    common_body = f"""
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Motivo: {instance.motive}<br>
        Obsevações: {instance.obs}<br>
        Produtos: <br>{table_html}
    """

    html_message = f"""
        <html>
            <head>
                <style>
                    * {{ font-size: 1rem; }}
                    table {{ border-collapse: collapse; }}
                    th, td {{ border: 1px solid black; padding: 5px; text-align: left; font-size: 0.9rem; }}
                    .btn {{
                        display: inline-block;
                        background-color: #f0f0f0;
                        padding: 8px 16px;
                        text-align: center;
                        text-decoration: none;
                        font-size: 16px;
                        border-radius: 10px;
                        margin-top: 10px;
                        border: 2px solid black;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div>
                    {email_body_intro}<br>
                    {common_body}<br>
                </div>
            </body>
        </html>
    """

    send_mail(
        email_subject,
        "This is a plain text for email clients that don't support HTML",
        settings.EMAIL_HOST_USER,
        [instance.requester.email],
        fail_silently=False,
        html_message=html_message,
    )


def send_purchase_quotation_email(instance):
    email_subject = "Cotação de Compra Criada"
    email_body_intro = """
        Olá!<br>
        Uma solicitação está agora em cotação e precisa de mais informações antes de ser processada.<br>
    """
    button_html = '<a href="https://gimi-requisitions.vercel.app" target="_blank" class="btn">Acessar Webapp</a><br>'
    table_html = build_quotation_table(
        instance.id, include_approved_only=False, include_price=False
    )

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Motivo: {instance.motive}<br>
        Obsevações: {instance.obs}<br>
        Produtos: <br>{table_html}
    """

    html_message = f"""
        <html>
            <head>
                <style>
                    * {{ font-size: 1rem; }}
                    table {{ border-collapse: collapse; }}
                    th, td {{ border: 1px solid black; padding: 5px; text-align: left; font-size: 0.9rem; }}
                    .btn {{
                        display: inline-block;
                        background-color: #f0f0f0;
                        padding: 8px 16px;
                        text-align: center;
                        text-decoration: none;
                        font-size: 16px;
                        border-radius: 10px;
                        margin-top: 10px;
                        border: 2px solid black;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div>
                    {email_body_intro}<br>
                    {common_body}<br>
                    {button_html}
                </div>
            </body>
        </html>
    """

    send_mail(
        email_subject,
        "This is a plain text for email clients that don't support HTML",
        settings.EMAIL_HOST_USER,
        [instance.requester.email],
        fail_silently=False,
        html_message=html_message,
    )


def send_quotation_email_with_pdf(instance):
    subject = f"Cotação de Compra Nº {instance.control_number} - Grupo Gimi"
    recipient_list = instance.quotation_emails.split(", ")
    email_from = settings.EMAIL_HOST_USER

    pdf_file = generate_pdf(instance)
    with open(pdf_file, "rb") as pdf_file_content:
        pdf_data = pdf_file_content.read()

    body_message = f"""
        Prezado fornecedor,

        Anexo o arquivo PDF com a carta de cotação Nº {instance.control_number}

        Por favor, responder este e-mail com os valores e condições de pagamento de acordo 
        com a carta anexa.

        Atenciosamente,

        Grupo Gimi
    """

    for recipient in recipient_list:
        email = EmailMessage(
            subject=subject,
            body=body_message,
            from_email=email_from,
            to=[recipient, instance.requester],
        )
        email.attach(
            f"carta_cotacao_compra_{instance.control_number}.pdf",
            pdf_data,
            "application/pdf",
        )
        email.send()
