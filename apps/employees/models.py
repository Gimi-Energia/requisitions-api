from datetime import date
from uuid import uuid4
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.departments.models import Department
from apps.users.models import User

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("Group", "Group")]
STATUS = [
    ("Opened", "Opened"),
    ("Canceled", "Canceled"),
    ("Pending", "Pending"),
    ("Denied", "Denied"),
    ("Approved", "Approved"),
]

# Create your models here.
class Position(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    position = models.CharField(_("Position"), max_length=50)
    cost_center = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=5)

    def __str__(self):
        return f"{self.cost_center.name} - {self.position}"
    
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=5)
    cost_center = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    request_date = models.DateField(_("Request Date"), default=date.today)
    position = models.CharField(_("Position"), max_length=50)
    is_replacement = models.BooleanField(_("Is Replacement"))
    has_pc = models.BooleanField(_("Has Pc"))
    needs_phone = models.BooleanField(_("Needs Phone"))
    needs_tablet = models.BooleanField(_("Needs Tablet"))
    needs_software = models.BooleanField(_("Needs Software"))
    software_names = models.TextField(_("Software Names"), blank=True, null=True)
    has_workstation = models.BooleanField(_("Has Workstation"))
    motive = models.TextField(_("Motive"))
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="requester")
    status = models.CharField(_("Status"), choices=STATUS, default="Opened", max_length=9)
    obs = models.TextField(_("Obs"), blank=True, null=True)
    replaced_email = models.CharField(_("Replacement Email"), max_length=60, blank=True, null=True)
    complete_name = models.CharField(_("Complete Name"), max_length=60, blank=True, null=True)
    start_date = models.DateField(_("Start Date"), blank=True, null=True)
    approver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="approver")
    approval_date =models.DateTimeField(_("Approval Date"), null=True, blank=True)
    control_number = models.IntegerField(_("Control Number"), default=0)

    def __str__(self):
        return f"{self.complete_name} - {self.position}"

    def save(self, *args, **kwargs):
        exists = Employee.objects.filter(id=self.pk).exists()
        if not exists:
            with transaction.atomic():
                last = Employee.objects.select_for_update().order_by("-control_number").first()
                if last:
                    self.control_number = last.control_number + 1
                else:
                    self.control_number = 1

        super(Employee, self).save(*args, **kwargs)