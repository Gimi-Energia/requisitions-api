from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage, send_mail

from apps.products.models import Product
from apps.purchases.models import PurchaseProduct
from apps.users.models import User

from .pdf_service import generate_pdf


def build_quotation_table(
    purchase_pk, include_approved_only=True, include_price=True, include_generic_only=False
):
    if include_approved_only:
        purchase_products = PurchaseProduct.objects.filter(purchase=purchase_pk, status="Approved")
    elif include_generic_only:
        purchase_products = PurchaseProduct.objects.filter(
            purchase=purchase_pk, status="Approved", product__code__icontains="GENERIC"
        )
    else:
        purchase_products = PurchaseProduct.objects.filter(purchase=purchase_pk)

    table_rows = []
    total_price = 0

    for purchase_product in purchase_products:
        product_code = purchase_product.product.code
        product = Product.objects.filter(code=product_code).first()
        product_description = product.description
        product_quantity = purchase_product.quantity
        product_obs = purchase_product.obs

        if include_price:
            product_price = purchase_product.price
            total_price += product_price * product_quantity
            price_cell = f"<td>R$ {product_price:.2f}</td>"
        else:
            price_cell = ""

        table_row = f"""
            <tr>
                <td>{product_code}</td>
                <td>{product_description}</td>
                <td>{product_quantity}</td>
                {price_cell}
                <td>{product_obs}</td>
                </tr>
        """
        table_rows.append(table_row)

    if not table_rows:
        return False

    price_header = "<th>Preço Un.</th>" if include_price else ""
    total_row = (
        f"<tr><td colspan='4'><b>Total</b></td><td><b>R$ {total_price:.2f}</b></td></tr>"
        if include_price
        else ""
    )

    return f"""
        <table border="1">
            <tr>
                <th>Código</th>
                <th>Descrição</th>
                <th>Quantidade</th>
                {price_header}
                <th>Observações</th>
            </tr>
            {''.join(table_rows)}
            {total_row}
        </table>
    """


def send_status_change_email(instance):
    email_subject = ""
    email_body_intro = ""
    table_html = ""

    emails = []

    if instance.status == "Approved":
        email_subject = "Solicitação de Compra Aprovada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi aprovada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}<br>
        """
        table_html = build_quotation_table(instance.id)
        
        purchase_group = Group.objects.get(name="Purchase Products")
        purchase_users = purchase_group.user_set.all().values_list("email", flat=True)
        emails = [*purchase_users]

    elif instance.status == "Denied":
        email_subject = "Solicitação de Compra Rejeitada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi rejeitada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}<br>
        """
        table_html = build_quotation_table(instance.id, include_approved_only=False)
    elif instance.status == "Opened":
        title = "Cotada" if instance.has_quotation else "Criada"
        email_subject = f"Solicitação de Compra {title}"
        print(email_subject)
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            A requisição Nº {instance.control_number} 
            já pode ser aprovada por {instance.approver}<br>
        """
        table_html = build_quotation_table(instance.id, include_approved_only=False)
        emails.append(instance.approver)
    else:
        return

    emails.append(instance.requester)

    if not table_html:
        return

    common_body = f"""
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Aprovador: {instance.approver}<br>
        Número de controle: {instance.control_number}<br>
        Motivo: {instance.motive}<br>
        Obsevações: {instance.obs}<br>
        Produtos: <br>{table_html}
    """

    button_html = '<a href="https://gimi-requisitions.vercel.app" target="_blank" class="btn">Acessar Webapp</a><br>'

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
        emails,
        fail_silently=False,
        html_message=html_message,
    )
    print(f"Status change email sent - current status: {instance.status}")
    print(f"Email sent to {emails}")


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

    purchase_group = Group.objects.get(name="Purchase Products")
    purchase_users = purchase_group.user_set.all().values_list("email", flat=True)
    emails = [*purchase_users]
    emails.append(instance.requester)
    print("Sending email to:")
    print(emails)

    if not table_html:
        return

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Aprovador: {instance.approver}<br>
        Número de controle: {instance.control_number}<br>
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
        emails,
        fail_silently=False,
        html_message=html_message,
    )


def send_quotation_email_with_pdf(instance):
    subject = f"Cotação de Compra Nº {instance.control_number} - Grupo Gimi"
    recipient_list = [email.strip() for email in instance.quotation_emails.split(",")]
    email_from = settings.EMAIL_HOST_USER
    emails_gimi = [user.email for user in User.objects.filter(email__icontains="compras")]
    purchase_group = Group.objects.get(name="Purchase Products")
    purchase_users = list(purchase_group.user_set.all().values_list("email", flat=True))

    pdf_file = generate_pdf(instance)

    if not pdf_file:
        return

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
        if recipient != "":
            all_recipients = [recipient, instance.requester] + emails_gimi + purchase_users

            email = EmailMessage(
                subject=subject,
                body=body_message,
                from_email=email_from,
                to=all_recipients,
            )
            email.attach(
                f"carta_cotacao_compra_{instance.control_number}.pdf",
                pdf_data,
                "application/pdf",
            )
            email.send()


def send_generic_product_email(instance):
    email_subject = "Cadastro de Produto Genérico"
    table_html = build_quotation_table(
        instance.id, include_approved_only=False, include_price=False, include_generic_only=True
    )

    if not table_html:
        return

    email_body = f"""
        Olá, {instance.requester.name}!<br>
        Sua requisição de compra Nº {instance.control_number} foi aprovada, 
        porém contém produtos genéricos.<br><br>

        Observações da requisição: {instance.obs}
        {table_html}<br>

        Para prosseguirmos com esse processo, será necessário 3 passos:<br> 
            1 - Solicite o cadastro do material<br>
            2 - Crie a requisição diretamente no Omie (incluindo todos os itens da requisição e não somente o item genérico)<br>
            3 - Inclua na observação interna da requisição dentro do OMIE que se trata da cotação Nº {instance.control_number} do App de Requisições.
    """

    html_message = f"""
        <html>
            <head>
                <style>
                    * {{ font-size: 1rem; }}
                    table {{ border-collapse: collapse; }}
                    th, td {{ border: 1px solid black; padding: 5px; text-align: left; font-size: 0.9rem; }}
                </style>
            </head>
            <body>
                <div>
                    {email_body}<br>
                </div>
            </body>
        </html>
    """

    send_mail(
        email_subject,
        "This is a plain text for email clients that don't support HTML",
        settings.EMAIL_HOST_USER,
        [instance.requester],
        fail_silently=False,
        html_message=html_message,
    )
