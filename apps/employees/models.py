from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.departments.models import Department

# Create your models here.
class Position(models.Model):
    id = models.CharField(max_length=7, primary_key=True, unique=True, editable=False)
    name = models.CharField(_("Name"), max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)