import os
import tempfile

import pytz
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.products.models import Product
from apps.purchases.models import PurchaseProduct


def generate_pdf(instance):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    small_style = ParagraphStyle("SmallStyle", parent=styles["Normal"], fontSize=8, leading=10)

    company_info_dict = {
        "GIMI": [
            "IND MONTAGEM E INSTALACOES GIMI",
            "https://www.gimi.com.br/",
            "43.030.931/0001-45",
            "Estrada Portão Honda, 3530 - Jardim Revista",
            "08694-080",
            "(11) 4752-9900",
        ],
        "GBL": [
            "GIMI BONOMI LATIN AMERICA",
            "https://www.gimibonomi.com.br/",
            "41.517.310/0001-65",
            "Estrada Portão do Ronda, 3.500 (galpão unidades 1a e 1b) - Jardim Revista",
            "08694-080",
            "(11) 2500-4550",
        ],
        "GPB": [
            "GIMI POGLIANO BLINDOSBARRA",
            "https://www.gimipogliano.com.br/",
            "21.046.295/0001-07",
            "Estrada Portão do Ronda, 3.500 (galpão 2) - Jardim Revista",
            "08694-080",
            "(11) 4752-9900",
        ],
        "GIR": [
            "GIR-GIMI ITAIPU RENOVAVEIS",
            "https://www.grupogimi.com.br/",
            "50.791.922/0001-32",
            "Rua Maria de Lourdes Vessoni Porto Francischetti, 750 - Distrito Industrial II",
            "14900-000",
            "(16) 3263-9400",
        ],
    }

    company_details = company_info_dict.get(instance.company.upper())
    city = "Itápolis" if instance.company == "GIR" else "Suzano"

    company_details_content = "<br/>".join(
        [
            f"<b>{company_details[0]}</b>",
            f"<link href='{company_details[1]}'>{company_details[1]}</link>",
            f"CNPJ: {company_details[2]}",
            f"{company_details[3]}",
            f"{city} - SP - CEP: {company_details[4]}",
            f"Telefone: {company_details[5]}",
        ]
    )
    company_details_paragraph = Paragraph(company_details_content, small_style)

    logo_path = f"setup/images/logo_{instance.company.lower()}.png"
    logo = (
        Image(logo_path, width=2 * inch, height=1 * inch)
        if os.path.exists(logo_path)
        else Spacer(1, 2 * inch)
    )

    header_data = [[logo, company_details_paragraph]]
    header_table = Table(header_data, colWidths=[2 * inch, 5 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (1, 0), (1, 0), 14),
            ]
        )
    )

    elements = [header_table, Spacer(1, 0.25 * inch)]

    elements.append(Spacer(1, 0.25 * inch))

    title = f"Cotação de Compra Nº {instance.control_number}"
    title_para = Paragraph(title, styles["Title"])
    elements.append(title_para)
    elements.append(Spacer(1, 0.2 * inch))

    data = [["Item", "Código", "Descrição", "Quantidade"]]
    purchase_products = PurchaseProduct.objects.filter(purchase=instance.id)
    item_number = 1

    if not purchase_products:
        return False

    for purchase_product in purchase_products:
        product = Product.objects.filter(code=purchase_product.product.code).first()
        row = [
            str(item_number),
            purchase_product.product.code,
            product.description,
            f"{purchase_product.quantity} {product.un}",
        ]
        data.append(row)
        item_number += 1

    background_color_header = HexColor("#FF6666")
    background_color_rows = HexColor("#FFCCCC")
    text_color_header = colors.whitesmoke
    line_color = colors.black

    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), background_color_header),
                ("TEXTCOLOR", (0, 0), (-1, 0), text_color_header),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), background_color_rows),
                ("GRID", (0, 0), (-1, -1), 1, line_color),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ]
        )
    )
    elements.append(table)

    elements.append(Spacer(1, 0.25 * inch))

    local_timezone = pytz.timezone("America/Sao_Paulo")
    local_quotation_date = instance.quotation_date.astimezone(local_timezone)
    formatted_quotation_date = local_quotation_date.strftime("%d/%m/%Y às %H:%M:%S")

    formatted_request_date = instance.request_date.strftime("%d/%m/%Y")

    details = [
        Paragraph(f"Observações: {instance.obs}", styles["Normal"]),
        Paragraph(f"Sugestão de entrega: {formatted_request_date}", styles["Normal"]),
        Paragraph(f"Carta de cotação - incluído em: {formatted_quotation_date}", styles["Normal"]),
    ]
    for detail in details:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    document.build(elements)
    return filename
