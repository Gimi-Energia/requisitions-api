from datetime import date
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.providers.models import Transporter
from apps.departments.models import Department

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("GIR", "GIR")]
STATUS = [
    ("Opened", "Opened"),
    ("Pending", "Pending"),
    ("Denied", "Denied"),
    ("Approved", "Approved"),
]


class Freight(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    request_date = models.DateField(_("Request Date"), default=date.today)
    execution_date = models.DateField(_("Execution Date"), default=date.today)
    requester = models.ForeignKey(
        User,
        verbose_name=_("Requester"),
        on_delete=models.CASCADE,
        related_name="freight_requester",
    )
    motive = models.CharField(_("Motive"), max_length=50)
    obs = models.TextField(_("Observation"))
    status = models.CharField(_("Status"), choices=STATUS, default="Pending", max_length=8)
    quotations = models.ManyToManyField(
        Transporter, through="FreightQuotation", verbose_name=_("quotations")
    )
    approver = models.ForeignKey(
        User,
        verbose_name=_("Approver"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="freight_approver",
    )
    approval_date = models.DateField(_("Approval Date"), blank=True, null=True)
    cte_number = models.CharField(_("CTE Number"), max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class FreightQuotation(models.Model):
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Status"), choices=STATUS, default="Pending", max_length=8)

    def __str__(self):
        return f"{self.transporter} - {self.price}"

    class Meta:
        unique_together = ("freight", "transporter")
