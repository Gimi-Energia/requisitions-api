from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage, send_mail

from apps.users.models import User

from .pdf_service import generate_pdf

STATUS = {
    "Opened": "Opened",
    "Canceled": "Canceled",
    "Pending": "Pending",
    "Denied": "Denied",
    "Approved": "Approved",
}


def send_status_change_email(instance):
    # Get the TI and RH groups
    ti_group = Group.objects.get(name="TI")
    rh_group = Group.objects.get(name="RH")
    print("Grupos acessados com sucesso")

    # Get users from each group
    ti_users = ti_group.user_set.all()
    rh_users = rh_group.user_set.all()
    print("usuários recuperados com sucesso")
    print(f"TI: {ti_users}")
    print(f"RH: {rh_users}")

    # Get emails from both groups
    ti_emails = ti_users.values_list("email", flat=True)
    rh_emails = rh_users.values_list("email", flat=True)
    print("emails recuperados com sucesso")
    print(f"TI: {ti_users}")
    print(f"RH: {rh_users}")

    email_subject = ""
    email_body_intro = ""

    emails = []

    if instance.status == STATUS["Opened"]:
        email_subject = "Nova requisição de funcionário"
        email_body_intro = (
            f"Foi criada uma nova requisição de funcionário por {instance.requester.name}"
        )
        emails = [instance.requester, instance.approver]
        print("Dados de email criados para status Opened")

    if instance.status == STATUS["Approved"]:
        email_subject = "Requisição de funcionário aprovada"
        email_body_intro = f"A requisição de funcionário foi aprovada por {instance.approver.name}. O processo pode seguir."
        emails = [instance.requester, *rh_emails, *ti_emails]
        print("Dados de email criados para status Approved")

    if instance.status == STATUS["Denied"]:
        email_subject = "Requisição de novo funcionário negada"
        email_body_intro = f"A requisição foi negada por {instance.approver}"
        emails = [instance.requester, instance.approver]

    if instance.status == STATUS["Canceled"]:
        email_subject = "Requisição de novo funcionário negada"
        email_body_intro = "A requisição de novo funcionário foi cancelada."
        emails = [instance.requester, instance.approver]

    if instance.status == STATUS["Pending"]:
        email_subject = "Requisição de novo funcionário pendente"
        email_body_intro = "Há uma requisição de novo funcionário pendente."
        emails = [instance.requester, instance.approver]

    common_body = f"""
        <h2>Dados da solicitação:</h2>
        Empresa: {instance.company}<br>
        Departamento: {instance.cost_center.id} - {instance.cost_center.name}<br>
        Cargo: {instance.position.position}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Número de controle: {instance.control_number}<br>
        Motivo: {instance.motive}<br>
        Requisitante: {instance.requester}<br>
        Aprovador: {instance.approver}<br>
        Obsevações: {instance.obs}<br>
    """

    if len(emails) == 0:
        emails = ["dev3.engenhadev@gmail.com"]
        common_body = "Houve um erro"
        print("Não encontrei emails para enviar")

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
    print(f"Preparando para enviar o email para {emails}")
    send_mail(
        email_subject,
        "This is a plain text for email clients that don't support HTML",
        settings.EMAIL_HOST_USER,
        emails,
        fail_silently=False,
        html_message=html_message,
    )
    print("Email enviado com sucesso!")


# def send_service_quotation_email(instance):
#     email_subject = "Cotação de Serviço Criada"
#     email_body_intro = """
#         Olá!<br>
#         Uma solicitação está agora em cotação e precisa de mais informações antes de ser processada.<br>
#     """
#     button_html = '<a href="https://gimi-requisitions.vercel.app" target="_blank" class="btn">Acessar Webapp</a><br>'

#     emails = [user.email for user in User.objects.filter(email__icontains="compras")]
#     emails.append(instance.requester)

#     common_body = f"""
#         Dados da solicitação:<br>
#         Empresa: {instance.company}<br>
#         Departamento: {instance.department}<br>
#         Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
#         Aprovador: {instance.approver}<br>
#         Número de controle: {instance.control_number}<br>
#         Serviço: {instance.service.description}<br>
#         Motivo: {instance.motive}<br>
#         Observações: {instance.obs}<br>
#     """

#     html_message = f"""
#         <html>
#             <head>
#                 <style>
#                     * {{ font-size: 1rem; }}
#                     table {{ border-collapse: collapse; }}
#                     th, td {{ border: 1px solid black; padding: 5px; text-align: left; font-size: 0.9rem; }}
#                     .btn {{
#                         display: inline-block;
#                         background-color: #f0f0f0;
#                         padding: 8px 16px;
#                         text-align: center;
#                         text-decoration: none;
#                         font-size: 16px;
#                         border-radius: 10px;
#                         margin-top: 10px;
#                         border: 2px solid black;
#                         font-weight: bold;
#                     }}
#                 </style>
#             </head>
#             <body>
#                 <div>
#                     {email_body_intro}<br>
#                     {common_body}<br>
#                     {button_html}
#                 </div>
#             </body>
#         </html>
#     """

#     send_mail(
#         email_subject,
#         "This is a plain text for email clients that don't support HTML",
#         settings.EMAIL_HOST_USER,
#         emails,
#         fail_silently=False,
#         html_message=html_message,
#     )


# def send_quotation_email_with_pdf(instance):
#     subject = f"Cotação de Serviço Nº {instance.control_number} - Grupo Gimi"
#     recipient_list = [email.strip() for email in instance.quotation_emails.split(",")]
#     email_from = settings.EMAIL_HOST_USER
#     emails_gimi = [user.email for user in User.objects.filter(email__icontains="compras")]

#     pdf_file = generate_pdf(instance)
#     with open(pdf_file, "rb") as pdf_file_content:
#         pdf_data = pdf_file_content.read()

#     body_message = f"""
#         Prezado prestador,

#         Anexo o arquivo PDF com a carta de cotação Nº {instance.control_number}

#         Por favor, responder este e-mail com os valores e condições de pagamento de acordo 
#         com a carta anexa.

#         Atenciosamente,

#         Grupo Gimi
#     """

#     for recipient in recipient_list:
#         if recipient != "":
#             all_recipients = [recipient, instance.requester] + emails_gimi

#             email = EmailMessage(
#                 subject=subject,
#                 body=body_message,
#                 from_email=email_from,
#                 to=all_recipients,
#             )
#             email.attach(
#                 f"carta_cotacao_servico_{instance.control_number}.pdf",
#                 pdf_data,
#                 "application/pdf",
#             )
#             email.send()
