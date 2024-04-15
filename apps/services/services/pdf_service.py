import tempfile

from django.utils.html import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def draw_header(c, image_path, width, height, margin):
    image_width = 1.6 * inch
    image_height = inch
    image_x = width - margin - image_width
    image_y = height - margin - image_height + 50
    c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)


def draw_footer(c, page_number, width):
    c.setFont("Helvetica", 8)
    footer_text = f"Página {page_number}"
    text_width = c.stringWidth(footer_text, "Helvetica", 8)
    c.drawString((width - text_width) / 2, 0.5 * inch, footer_text)


def add_page(c, width, height, page_number, margin, company):
    c.showPage()
    page_number += 1
    draw_header(c, f"setup/images/logo_{company}.png", width, height, margin)
    draw_footer(c, page_number, width)
    return page_number, height - margin - 1.3 * inch


def generate_pdf(instance):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    margin = inch
    line_height = 14
    page_number = 1

    company = instance.company.lower()
    draw_header(c, f"setup/images/logo_{company}.png", width, height, margin)
    draw_footer(c, page_number, width)

    current_height = height - margin - inch

    c.setFont("Helvetica", 14)
    title = "Cotação de Serviço - Grupo Gimi"
    text_width = c.stringWidth(title, "Helvetica", 14)
    c.drawString((width - text_width) / 2, current_height, title)
    current_height -= line_height * 2

    c.line(margin, current_height, width - margin, current_height)
    current_height -= line_height * 2

    c.setFont("Helvetica", 10)

    formattedDate = instance.request_date.strftime("%d/%m/%Y")

    details = [
        f"Serviço: {escape(instance.service.description)}",
        f"Observações: {escape(instance.obs)}",
        f"Data da necessidade: {escape(formattedDate)}",
    ]

    for detail in details:
        if current_height <= margin + (2 * line_height):
            page_number, current_height = add_page(c, width, height, page_number, margin, company)
        c.drawString(margin, current_height, detail)
        current_height -= line_height

    c.save()
    return filename
