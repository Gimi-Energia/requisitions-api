from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from apps.employees.services.email_service_templates import generate_email_templates

STATUS = {
    "Opened": "Opened",
    "Pending": "Pending",
    "Approved": "Approved",
    "Denied": "Denied",
    "Canceled": "Canceled",
}


def get_group_emails(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group.user_set.values_list("email", flat=True)
    except Group.DoesNotExist:
        print(f"Grupo {group_name} não encontrado.")
        return []


def send_status_change_email(instance):
    print("Iniciando envio de email para mudança de status.")

    ti_emails = list(get_group_emails("TI"))
    rh_emails = list(get_group_emails("RH"))
    print("Emails de TI e RH recuperados com sucesso.")

    status_configs = {
        STATUS["Opened"]: {
            "subject": f"Nova requisição de funcionário Nº {instance.control_number}",
            "emails": [instance.requester.email, instance.approver.email],
        },
        STATUS["Pending"]: {
            "subject": f"Requisição Nº {instance.control_number} de funcionário pendente",
            "emails": [instance.requester.email, *rh_emails, *ti_emails],
        },
        STATUS["Approved"]: {
            "subject": f"Requisição Nº {instance.control_number} de funcionário aprovada",
            "emails": [instance.requester.email, *ti_emails],
        },
        STATUS["Denied"]: {
            "subject": f"Requisição Nº {instance.control_number} de funcionário negada",
            "emails": [instance.requester.email],
        },
        STATUS["Canceled"]: None,
    }

    config = status_configs.get(instance.status)

    if not config:
        print(f"Sem envio de email para o status {instance.status}.")
        return

    TEMPLATES = generate_email_templates(instance=instance)
    email_body_intro = TEMPLATES["email_body_intro"][instance.status]
    summary_body = TEMPLATES["summary_body"]
    rh_content = TEMPLATES["RH"].get(instance.status, "")
    ti_content = TEMPLATES["TI"].get(instance.status, "")

    if not config["emails"]:
        print("Nenhum email encontrado para envio. Usando fallback.")
        config["emails"] = ["dev2@engenhadev.com"]
        summary_body = (
            f"Houve um erro ao identificar os destinatários (Nº {instance.control_number})."
        )

    button_html = '<a href="https://gimi-requisitions.vercel.app" target="_blank" class="btn">Acessar Webapp</a>'

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
                    ul {{
                        list-style: none;
                        margin: 0;
                        padding: 0;
                    }}
                    li {{
                        margin-left: 10px;
                    }}
                </style>
            </head>
            <body>
                <div>
                    {email_body_intro}<br>
                    {summary_body}<br>
                    {rh_content}
                    {ti_content}
                    {button_html}
                </div>
            </body>
        </html>
    """

    try:
        print(f"Enviando email para: {config['emails']}")
        send_mail(
            config["subject"],
            "Este é um texto para clientes de email que não suportam HTML.",
            settings.EMAIL_HOST_USER,
            config["emails"],
            fail_silently=False,
            html_message=html_message,
        )
        print("Email enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
