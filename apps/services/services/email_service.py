from django.conf import settings
from django.core.mail import send_mail


def check_status_and_send_email(old_status, new_instance):
    if old_status == new_instance.status:
        return

    email_subject = ""
    email_body_intro = ""

    if new_instance.status == "Approved":
        email_subject = "Solicitação de Serviço Aprovada"
        email_body_intro = f"""
            Olá, {new_instance.requester.name}!<br>
            Sua solicitação foi aprovada por {new_instance.approver} 
            em {new_instance.approval_date.strftime("%d/%m/%Y")}<br>
        """
    elif new_instance.status == "Denied":
        email_subject = "Solicitação de Serviço Rejeitada"
        email_body_intro = f"""
            Olá, {new_instance.requester.name}!<br>
            Sua solicitação foi rejeitada por {new_instance.approver}<br>
        """
    elif new_instance.status == "Opened":
        email_subject = "Solicitação de Serviço Cotada"
        email_body_intro = f"""
            Olá, {new_instance.requester.name}!<br>
            Sua solicitação foi cotada e já pode ser aprovada<br>
        """

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {new_instance.company}<br>
        Departamento: {new_instance.department}<br>
        Data solicitada: {new_instance.request_date.strftime("%d/%m/%Y")}<br>
        Motivo: {new_instance.motive}<br>
        Obsevações: {new_instance.obs}<br>
        Prestador: {new_instance.provider}<br>
        Serviço: {new_instance.service.description}<br>
        Valor: R$ {new_instance.value}
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
        [new_instance.requester.email],
        fail_silently=False,
        html_message=html_message,
    )


def send_service_quotation_email(new_instance):
    email_subject = "Cotação de Serviço Criada"
    email_body_intro = """
        Olá!<br>
        Uma solicitação está agora em cotação e precisa de mais informações antes de ser processada.<br>
    """
    button_html = '<a href="https://gimi-requisitions.vercel.app" target="_blank" class="btn">Acessar Webapp</a><br>'

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {new_instance.company}<br>
        Departamento: {new_instance.department}<br>
        Data solicitada: {new_instance.request_date.strftime("%d/%m/%Y")}<br>
        Motivo: {new_instance.motive}<br>
        Observações: {new_instance.obs}<br>
        Serviço: {new_instance.service.description}<br>
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
        [new_instance.requester.email],
        fail_silently=False,
        html_message=html_message,
    )
