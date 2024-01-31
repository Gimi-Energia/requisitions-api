from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    id = models.CharField(max_length=7, primary_key=True, unique=True)
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return f"{self.id} - {self.name}"
