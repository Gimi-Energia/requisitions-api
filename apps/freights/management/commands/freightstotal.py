import locale

from django.core.management.base import BaseCommand
from django.db.models import Sum

from apps.contracts.models import Contract


class Command(BaseCommand):
    help = "Calcula o total de frete consumido"

    def handle(self, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        total_freight = Contract.objects.aggregate(total=Sum("freight_consumed"))["total"]
        total_freight_formatted = locale.currency(total_freight, grouping=True)
        self.stdout.write(
            self.style.SUCCESS(f"Total de frete consumido: {total_freight_formatted}")
        )
