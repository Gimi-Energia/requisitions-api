from django.core.management.base import BaseCommand
from django.db.models import F

from apps.contracts.models import Contract
from apps.freights.models import Freight


class Command(BaseCommand):
    help = "Atualiza os fretes consumidos nos contratos correspondentes"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Iniciando a atualização dos fretes consumidos..."))

        contracts = Contract.objects.all()
        contracts.update(freight_consumed=0)
        self.stdout.write(self.style.SUCCESS("Frete consumido zerado para todos os contratos"))

        freights = Freight.objects.filter(status="Approved").select_related("contract")
        for freight in freights:
            approved_quotation = freight.freightquotation_set.filter(status="Approved").first()
            if approved_quotation and freight.contract:
                Contract.objects.filter(id=freight.contract.id).update(
                    freight_consumed=F("freight_consumed") + approved_quotation.price
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Frete atualizado para o {freight.contract.contract_number} ({freight.contract.company}) com o valor {approved_quotation.price}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Atualização dos fretes consumidos concluída."))
