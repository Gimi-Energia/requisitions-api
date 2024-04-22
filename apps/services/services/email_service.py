from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from apps.users.models import User

from .pdf_service import generate_pdf


def send_status_change_email(instance):
    email_subject = ""
    email_body_intro = ""
    emails = [instance.requester]

    if instance.status == "Approved":
        email_subject = "Solicitação de Serviço Aprovada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi aprovada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}<br>
        """
    elif instance.status == "Denied":
        email_subject = "Solicitação de Serviço Rejeitada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi rejeitada por {instance.approver}<br>
        """
    elif instance.status == "Opened":
        email_subject = "Solicitação de Serviço Cotada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi cotada e já pode ser aprovada por {instance.approver}<br>
        """
        emails.append(instance.approver)
    else:
        return

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Aprovador: {instance.approver}<br>
        Número de controle: {instance.control_number}<br>
        Serviço: {instance.service.description}<br>
        Prestador: {instance.provider}<br>
        Valor: R$ {instance.value}<br>
        Motivo: {instance.motive}<br>
        Obsevações: {instance.obs}<br>
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
        emails,
        fail_silently=False,
        html_message=html_message,
    )


def send_service_quotation_email(instance):
    email_subject = "Cotação de Serviço Criada"
    email_body_intro = """
        Olá!<br>
        Uma solicitação está agora em cotação e precisa de mais informações antes de ser processada.<br>
    """
    button_html = '<a href="https://gimi-requisitions.vercel.app" target="_blank" class="btn">Acessar Webapp</a><br>'

    emails = [user.email for user in User.objects.filter(email__icontains="dev")]
    emails.append(instance.requester)

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Aprovador: {instance.approver}<br>
        Número de controle: {instance.control_number}<br>
        Serviço: {instance.service.description}<br>
        Motivo: {instance.motive}<br>
        Observações: {instance.obs}<br>
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
    subject = f"Cotação de Serviço Nº {instance.control_number} - Grupo Gimi"
    recipient_list = instance.quotation_emails.split(", ")
    email_from = settings.EMAIL_HOST_USER
    emails_gimi = [user.email for user in User.objects.filter(email__icontains="dev")]

    pdf_file = generate_pdf(instance)
    with open(pdf_file, "rb") as pdf_file_content:
        pdf_data = pdf_file_content.read()

    body_message = f"""
        Prezado prestador,

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
            to=[recipient, instance.requester].extend(emails_gimi),
        )
        email.attach(
            f"carta_cotacao_servico_{instance.control_number}.pdf",
            pdf_data,
            "application/pdf",
        )
        email.send()
