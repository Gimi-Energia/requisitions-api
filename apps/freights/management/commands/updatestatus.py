from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.freights.models import Freight


class Command(BaseCommand):
    help = "Atualiza o status dos fretes pendentes anteriores a janeiro de 2025 para 'Approved' e define o campo CTE como 'Reset-CTE não informado'"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Iniciando a atualização dos status dos fretes..."))

        cutoff_date = timezone.datetime(2025, 1, 1)
        freights = Freight.objects.filter(status="Pending", created_at__lt=cutoff_date)

        updated_count = 0
        for freight in freights:
            freight.status = "Approved"
            freight.cte_number = "RESET-CTE NÃO INFO"
            freight.save()
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f"Frete {freight.id} atualizado."))

        self.stdout.write(self.style.SUCCESS(f"{updated_count} fretes atualizados com sucesso."))
        self.stdout.write(self.style.SUCCESS("Atualização dos status dos fretes concluída."))
