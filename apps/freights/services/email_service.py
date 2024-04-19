from django.conf import settings
from django.core.mail import send_mail

from apps.freights.models import FreightQuotation


def build_quotation_table(freight_pk, include_approved_only=False):
    if include_approved_only:
        freight_quotations = FreightQuotation.objects.filter(freight=freight_pk, status="Approved")
    else:
        freight_quotations = FreightQuotation.objects.filter(freight=freight_pk)

    table_rows = []
    for fq in freight_quotations:
        transporter = fq.name_other if fq.transporter.name == "Outro" else fq.transporter.name
        table_rows.append(f"<tr><td>{transporter}</td><td>R$ {fq.price}</td></tr>")

    if not table_rows:
        return ""

    return f"""
        <table border="1">
            <tr>
                <th>Transportadora</th>
                <th>Preço</th>
            </tr>
            {''.join(table_rows)}
        </table>
    """


def send_status_change_email(instance):
    email_subject = ""
    email_body_intro = ""
    table_html = ""
    important_note = ""

    if instance.status == "Pending":
        email_subject = "Solicitação de Frete Aprovada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi aprovada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}.
        """
        table_html = build_quotation_table(instance.id, include_approved_only=True)
        important_note = "IMPORTANTE: Acessar a ferramenta para inserir o número do CTE assim que receber da transportadora, o pagamento da NF estará vinculado a este número de controle."
    elif instance.status == "Denied":
        email_subject = "Solicitação de Frete Rejeitada"
        email_body_intro = f"""
            Olá, {instance.requester.name}!<br>
            Sua solicitação foi rejeitada por {instance.approver} 
            em {instance.approval_date.strftime("%d/%m/%Y")}.
        """
        table_html = build_quotation_table(instance.id, include_approved_only=False)
        important_note = "Por favor, verifique as informações e, se necessário, ajuste sua solicitação e submeta novamente."
    else:
        return

    common_body = f"""
        Dados da solicitação:<br>
        Empresa: {instance.company}<br>
        Departamento: {instance.department}<br>
        Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
        Aprovador: {instance.approver}<br>
        Motivo: {instance.motive}<br>
        Obsevações: {instance.obs}<br>
        Cotação:<br>{table_html}
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
                    {email_body_intro}<br>
                    {common_body}
                    <p><strong>{important_note}</strong></p>
                </div>
            </body>
        </html>
    """

    send_mail(
        email_subject,
        "This is a plain text for email clients that don't support HTML",
        settings.EMAIL_HOST_USER,
        [instance.requester, instance.approver],
        fail_silently=False,
        html_message=html_message,
    )
