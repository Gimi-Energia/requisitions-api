import csv

from django.core.management.base import BaseCommand

from apps.freights.models import Freight


class Command(BaseCommand):
    help = "Exporta dados de fretes para um arquivo CSV"

    def handle(self, *args, **kwargs):
        output_file = "freights_export.csv"

        fields_csv = [
            "UID",
            "Empresa",
            "Departamento",
            "Criado Em",
            "Data da Requisição",
            "Requisitante",
            "Status",
            "Aprovador",
            "Data da aprovação",
            "CTE",
            "Transportadora",
            "Valor Frete",
            "E",
            "G",
            "Frete Estimado",
            "Frete Consumido",
        ]

        rows = []

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields_csv)
            writer.writeheader()

            freights = Freight.objects.all()

            for freight in freights:
                created_at_date = freight.created_at.date().isoformat()
                approval_date_date = (
                    freight.approval_date.date().isoformat() if freight.approval_date else ""
                )

                approved_quotation = freight.freightquotation_set.filter(status="Approved").first()

                row = {
                    "UID": freight.id,
                    "Empresa": freight.company,
                    "Departamento": freight.department.name,
                    "Criado Em": created_at_date,
                    "Data da Requisição": freight.request_date,
                    "Requisitante": freight.requester.email,
                    "Status": self.translate_status(freight.status),
                    "Aprovador": freight.approver.email if freight.approver else "",
                    "Data da aprovação": approval_date_date,
                    "CTE": freight.cte_number,
                    "Transportadora": approved_quotation.transporter.name
                    if approved_quotation
                    else "",
                    "Valor Frete": str(approved_quotation.price).replace(".", ",")
                    if approved_quotation
                    else "",
                }

                if freight.contract:
                    row["E"] = freight.contract.contract_number.replace(".", ",")
                    row["G"] = freight.contract.control_number.replace(".", ",")
                    row["Frete Estimado"] = str(freight.contract.freight_estimated).replace(
                        ".", ","
                    )
                    row["Frete Consumido"] = str(freight.contract.freight_consumed).replace(
                        ".", ","
                    )
                else:
                    row["E"] = ""
                    row["G"] = ""
                    row["Frete Estimado"] = ""
                    row["Frete Consumido"] = ""

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
        }
        return translations.get(status, status)
