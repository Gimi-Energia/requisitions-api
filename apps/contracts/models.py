from django.db import models
from django.utils.translation import gettext_lazy as _

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GIR", "GIR")]


class Contract(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=6)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    contract_number = models.CharField(_("Contract Number"), max_length=10)
    control_number = models.CharField(_("Control Number"), max_length=8, null=True, blank=True)
    client_name = models.CharField(_("Client Name"), max_length=120)
    project_name = models.CharField(_("Project Name"), max_length=120, null=True, blank=True)
    freight_value = models.FloatField(_("Freight Value"), null=True, blank=True)

    def __str__(self):
        return self.contract_number
