from datetime import date
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.departments.models import Department
from apps.users.models import User

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS")]
REQUEST_STATUS = [
    ("Opened", "Opened"),
    ("Scheduled", "Scheduled"),
    ("Completed", "Completed"),
    ("Denied", "Denied"),
    ("Canceled", "Canceled"),
]
APPROVER_STATUS = [
    ("Checking", "Checking"),
    ("Completed", "Completed"),
]


class Maintenance(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    name = models.CharField(_("Name"), max_length=50)
    extension = models.CharField(_("Extension"), max_length=10)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    object = models.CharField(_("Object"), max_length=50)
    url = models.URLField(_("Attachment URL"), max_length=200, blank=True, null=True)
    obs = models.TextField(_("Observation"), blank=True, null=True)

    requester = models.ForeignKey(
        User,
        verbose_name=_("Requester"),
        on_delete=models.CASCADE,
        related_name="maintenance_requester",
    )
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    request_date = models.DateField(_("Request Date"), default=date.today)
    status = models.CharField(_("Status"), choices=REQUEST_STATUS, default="Opened", max_length=9)

    approver = models.ForeignKey(
        User,
        verbose_name=_("Approver"),
        on_delete=models.CASCADE,
        related_name="maintenance_approver",
        blank=True,
        null=True,
    )
    forecast_date = models.DateField(_("Forecast Date"), blank=True, null=True)
    approver_obs = models.TextField(_("Approver Observation"), blank=True, null=True)
    approver_status = models.CharField(
        _("Approver Status"), choices=APPROVER_STATUS, max_length=9, blank=True, null=True
    )
    end_date = models.DateTimeField(_("End Date"), blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Responsible(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    phone = models.CharField(_("Phone"), max_length=15)
    extension = models.CharField(_("Extension"), max_length=10)

    def save(self, *args, **kwargs):
        if not self.pk and Responsible.objects.exists():
            raise ValidationError("Só pode haver um responsável pela manutenção interna.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.phone} {self.extension}"
