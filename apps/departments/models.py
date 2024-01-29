from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    code = models.CharField(_("Code"), max_length=7)
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name
