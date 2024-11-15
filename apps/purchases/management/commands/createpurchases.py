from django.core.management.base import BaseCommand
from apps.purchases.models import Purchase
from apps.purchases.services.omie_service import include_purchase_requisition


class Command(BaseCommand):
    help = "Enviar requisições de compra para Omie com base nos control_numbers fornecidos"

    def add_arguments(self, parser):
        parser.add_argument("control_numbers", nargs="+", type=str, help="Lista de control_numbers")

    def handle(self, *args, **kwargs):
        control_numbers = kwargs["control_numbers"]
        for control_number in control_numbers:
            try:
                purchase = Purchase.objects.get(control_number=control_number)
                response = include_purchase_requisition(purchase)
                http_code = response.status_code
                if response and http_code == 200:
                    self.stdout.write(
                        self.style.SUCCESS(f"Requisição enviada com sucesso para {control_number}")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Erro {http_code} ao enviar requisição para {control_number}"
                        )
                    )
            except Purchase.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Purchase com control_number {control_number} não encontrado")
                )
