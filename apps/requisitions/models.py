from datetime import date
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.products.models import Product

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("GIR", "GIR")]


class Requisition(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    date = models.DateField(_("Date"), default=date.today)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    motive = models.CharField(_("Motive"), max_length=50)
    obs = models.TextField(_("Observation"))
    is_approved = models.BooleanField(_("Is Approved?"), default=False)
    products = models.ManyToManyField(
        Product, through="RequisitionProduct", verbose_name=_("Products")
    )

    def __str__(self):
        return self.id


class RequisitionProduct(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"))

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    class Meta:
        unique_together = ("requisition", "product")
