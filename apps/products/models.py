from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

UN_CHOICES = [
    ("UN", "Unit"),
    ("KG", "Kilogram"),
    ("M", "Meter"),
    ("L", "Litre"),
    ("RL", "Roll"),
    ("PCT", "Package"),
]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    code = models.CharField(_("Code"), max_length=30)
    un = models.CharField(_("Measurement Unit"), choices=UN_CHOICES, max_length=3, default="UN")
    description = models.CharField(_("Description"), max_length=120)
    icms = models.DecimalField(_("ICMS"), max_digits=5, decimal_places=2, null=True, blank=True)
    ipi = models.DecimalField(_("IPI"), max_digits=5, decimal_places=2, null=True, blank=True)
    st = models.DecimalField(_("ST"), max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.code
