from datetime import date
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.contracts.models import Contract
from apps.departments.models import Department
from apps.providers.models import Transporter
from apps.users.models import User

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("GIR", "GIR")]
STATUS_FREIGHTS = [
    ("Opened", "Opened"),
    ("Canceled", "Canceled"),
    ("Pending", "Pending"),
    ("Denied", "Denied"),
    ("Approved", "Approved"),
]
STATUS_QUOTATIONS = [
    ("Opened", "Opened"),
    ("Denied", "Denied"),
    ("Approved", "Approved"),
]


class Freight(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    request_date = models.DateField(_("Request Date"), default=date.today)
    requester = models.ForeignKey(
        User,
        verbose_name=_("Requester"),
        on_delete=models.CASCADE,
        related_name="freight_requester",
    )
    motive = models.TextField(_("Motive"))
    obs = models.TextField(_("Observation"))
    status = models.CharField(_("Status"), choices=STATUS_FREIGHTS, default="Opened", max_length=8)
    quotations = models.ManyToManyField(
        Transporter, through="FreightQuotation", verbose_name=_("Quotations")
    )
    approver = models.ForeignKey(
        User,
        verbose_name=_("Approver"),
        on_delete=models.CASCADE,
        related_name="freight_approver",
    )
    approval_date = models.DateTimeField(_("Approval Date"), blank=True, null=True)
    cte_number = models.CharField(_("CTE Number"), max_length=20, blank=True, null=True)
    contract = models.ForeignKey(
        Contract,
        verbose_name=_("Contract"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    motive_denied = models.TextField(_("Motive Denied"), blank=True, null=True)
    due_date = models.DateTimeField(_("Due Date"), blank=True, null=True)
    is_internal = models.BooleanField(_("Is Internal"), default=False)

    def __str__(self):
        return str(self.id)


class FreightQuotation(models.Model):
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Status"), choices=STATUS_QUOTATIONS, default="Opened", max_length=8
    )
    name_other = models.CharField(_("Name Other"), max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.transporter} - {self.price}"

    class Meta:
        unique_together = ("freight", "transporter")


class ExportLog(models.Model):
    export_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Exportação realizada em {self.export_date}"
