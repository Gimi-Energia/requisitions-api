import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from apps.purchases.models import Purchase, PurchaseProduct


class Command(BaseCommand):
    help = "Exporta dados de compras para um arquivo CSV"

    def add_arguments(self, parser):
        parser.add_argument("--start_date", type=str, help="Data de início no formato YYYY-MM-DD")
        parser.add_argument("--end_date", type=str, help="Data de término no formato YYYY-MM-DD")

    def handle(self, *args, **kwargs):
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")

        output_file = "purchases_export.csv"
        fields_csv = [
            "UID",
            "Empresa",
            "Departamento",
            "Criado Em",
            "Data da Requisição",
            "Requisitante",
            "Status",
            "Aprovador Diretor",
            "Data da Aprovação Diretor",
            "Aprovador Gerente",
            "Data da Aprovação Gerente",
            "Motivo",
            "Observação",
            "Tem Cotação",
            "Emails Cotação",
            "Data Cotação",
            "Link Cotação",
            "Número de Controle",
            "Motivo Recusa",
            "Total Pedido Omie",
            "Produto",
            "Quantidade",
            "Preço",
            "Status do Produto",
            "Obervação Produto",
        ]

        rows = []

        purchases = Purchase.objects.all()
        if start_date:
            purchases = purchases.filter(created_at__gte=parse_date(start_date))
        if end_date:
            purchases = purchases.filter(created_at__lte=parse_date(end_date))

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields_csv)
            writer.writeheader()

            for purchase in purchases:
                created_at_date = purchase.created_at.date().isoformat()
                approval_date_director = (
                    purchase.approval_date_director.date().isoformat()
                    if purchase.approval_date_director
                    else ""
                )
                approval_date_manager = (
                    purchase.approval_date_manager.date().isoformat()
                    if purchase.approval_date_manager
                    else ""
                )

                approved_products = PurchaseProduct.objects.filter(
                    purchase=purchase, status="Approved"
                )

                for product in approved_products:
                    row = {
                        "UID": purchase.id,
                        "Empresa": purchase.company,
                        "Departamento": purchase.department.name,
                        "Criado Em": created_at_date,
                        "Data da Requisição": purchase.request_date,
                        "Requisitante": purchase.requester.email,
                        "Status": self.translate_status(purchase.status),
                        "Aprovador Diretor": purchase.approver_director.email
                        if purchase.approver_director
                        else "",
                        "Data da Aprovação Diretor": approval_date_director,
                        "Aprovador Gerente": purchase.approver_manager.email
                        if purchase.approver_manager
                        else "",
                        "Data da Aprovação Gerente": approval_date_manager,
                        "Motivo": purchase.motive,
                        "Observação": purchase.obs,
                        "Tem Cotação": purchase.has_quotation,
                        "Emails Cotação": purchase.quotation_emails,
                        "Data Cotação": purchase.quotation_date,
                        "Link Cotação": purchase.quotation_link,
                        "Número de Controle": purchase.control_number,
                        "Motivo Recusa": purchase.motive_denied,
                        "Total Pedido Omie": str(purchase.omie_total).replace(".", ","),
                        "Produto": product.product.code,
                        "Quantidade": str(product.quantity).replace(".", ","),
                        "Preço": str(product.price).replace(".", ",") if product.price else "",
                        "Status do Produto": self.translate_status(product.status),
                        "Obervação Produto": product.obs,
                    }
                    rows.append(row)

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields_csv)
            writer.writeheader()
            writer.writerows(rows)

        self.stdout.write(self.style.SUCCESS(f"Arquivo CSV {output_file} gerado com sucesso."))

    def translate_status(self, status):
        translations = {
            "Pending": "Pendente",
            "Approved": "Aprovado",
            "Opened": "Aberto",
            "Denied": "Negado",
            "Canceled": "Cancelado",
            "Quotation": "Cotação",
            "Validation": "Validação",
        }
        return translations.get(status, status)
