from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.departments.models import Department

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("Grupo", "Grupo")]

# Create your models here.
class Position(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    position = models.CharField(_("Position"), max_length=50)
    cost_center = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=5)

    def __str__(self):
        return f"{self.cost_center.name} - {self.position}"