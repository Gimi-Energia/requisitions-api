import pytz
from django.conf import settings
from django.core.mail import send_mail

from apps.users.models import User


def send_status_change_email(instance):
    email_subject = ""
    email_body_intro = ""
    emails = []

    print(instance.status)

    if instance.status == "Scheduled":
        email_subject = "Solicitação de Manutenção Interna Programada"
        email_body_intro = f"""
            Olá, {instance.requester}!<br>
            Sua solicitação foi programada
            para {instance.forecast_date.strftime("%d/%m/%Y")}.<br>
        """
        emails.append(instance.requester)
    elif instance.status == "Opened":
        print("preparing email for Opened status")
        local_timezone = pytz.timezone("America/Sao_Paulo")
        local_created_at = instance.created_at.astimezone(local_timezone)
        formatted_created_at = local_created_at.strftime("%d/%m/%Y às %H:%M:%S")
        print(formatted_created_at)
        email_subject = "Solicitação de Manutenção Interna Criada"
        email_body_intro = f"""
            Olá!<br>
            Uma solicitação foi criada em {formatted_created_at}<br>
            De {instance.requester}.<br>
        """
        print("getting emails")
        emails = [user.email for user in User.objects.filter(groups__name="Maintenance")]
        emails.append(instance.requester.email)
        print(f"email list {emails}")
    elif instance.status == "Completed":
        local_timezone = pytz.timezone("America/Sao_Paulo")
        local_end_date = instance.end_date.astimezone(local_timezone)
        formatted_end_date = local_end_date.strftime("%d/%m/%Y às %H:%M:%S")
        email_subject = "Solicitação de Manutenção Interna Encerrada"
        email_body_intro = f"""
            Olá {instance.requester}!<br>
            Sua solicitação foi encerrada em {formatted_end_date}<br>
        """
        emails.append(instance.requester)
    elif instance.status == "Denied":
        local_timezone = pytz.timezone("America/Sao_Paulo")
        local_end_date = instance.end_date.astimezone(local_timezone)
        formatted_end_date = local_end_date.strftime("%d/%m/%Y às %H:%M:%S")
        email_subject = "Solicitação de Manutenção Interna Negada"
        email_body_intro = f"""
            Olá {instance.requester}!<br>
            Sua solicitação foi negada em {formatted_end_date}<br>
        """
        emails.append(instance.requester)
    else:
        return

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {instance.company}<br>
        Nome do requisitante: {instance.name}<br>
        Email do requisitante: {instance.requester}<br>
        Ramal do requisitante: {instance.extension}<br>
        Local da manutenção: {instance.department}<br>
        Objeto a receber manutenção: {instance.object}<br>
        Anexo (Link): {instance.url}<br>
        Observação do requisitante: {instance.obs}<br>
        Data da solicitação: {instance.request_date.strftime("%d/%m/%Y")}<br>
    """
    print("email body created")

    if instance.status in ["Scheduled", "Completed"]:
        common_body += f"Data de previsão: {instance.forecast_date.strftime('%d/%m/%Y')}<br>"
        if instance.approver_obs:
            common_body += f"Observação do executor: {instance.approver_obs}<br>"
        if instance.approver_status:
            common_body += f"Status do executor: {translate_status(instance.approver_status)}<br>"

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
                    {common_body}
                    {button_html}
                </div>
            </body>
        </html>
    """
    print("start sending email")
    send_mail(
        email_subject,
        "This is a plain text for email clients that don't support HTML",
        settings.EMAIL_HOST_USER,
        emails,
        fail_silently=False,
        html_message=html_message,
    )
    print(f"email sent to {emails}")


def translate_status(status: str) -> str:
    options = {"Checking": "Verificando", "Completed": "Finalizado"}

    translated = options.get(status)

    return translated
