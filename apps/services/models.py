from datetime import date
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.departments.models import Department
from apps.providers.models import Provider
from apps.users.models import User

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("GIR", "GIR")]
STATUS = [("Opened", "Opened"), ("Approved", "Approved"), ("Denied", "Denied")]


class ServiceType(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    description = models.CharField(_("Description"), max_length=120)

    def __str__(self):
        return self.description


class Service(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    request_date = models.DateField(_("Request Date"), default=date.today)
    requester = models.ForeignKey(
        User,
        verbose_name=_("Requester"),
        on_delete=models.CASCADE,
        related_name="service_requester",
    )
    motive = models.CharField(_("Motive"), max_length=50)
    obs = models.TextField(_("Observation"))
    provider = models.ForeignKey(Provider, verbose_name=_("Provider"), on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceType, verbose_name=_("Service"), on_delete=models.CASCADE)
    value = models.DecimalField(_("Value"), max_digits=7, decimal_places=2)
    status = models.CharField(_("Status"), choices=STATUS, default="Pending", max_length=8)
    approver = models.ForeignKey(
        User,
        verbose_name=_("Approver"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="service_approver",
    )
    approval_date = models.DateField(_("Approval Date"), blank=True, null=True)

    def __str__(self):
        return self.id
