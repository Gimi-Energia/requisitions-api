from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    code = models.CharField(_("Code"), max_length=30)
    un = models.CharField(_("Measurement Unit"), max_length=30)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.code
