from datetime import date
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.products.models import Product
from apps.departments.models import Department

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("GIR", "GIR")]
STATUS = [("Pending", "Pending"), ("Approved", "Approved"), ("Denied", "Denied")]


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    request_date = models.DateField(_("Request Date"), default=date.today)
    requester = models.ForeignKey(
        User, verbose_name=_("Requester"), on_delete=models.CASCADE, related_name="Requester"
    )
    motive = models.CharField(_("Motive"), max_length=50)
    obs = models.TextField(_("Observation"))
    status = models.CharField(_("Status"), choices=STATUS, default="Pending", max_length=8)
    products = models.ManyToManyField(
        Product, through="PurchaseProduct", verbose_name=_("Products")
    )
    approver = models.ForeignKey(
        User,
        verbose_name=_("Approver"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="Approver",
    )
    approval_date = models.DateField(_("Approval Date"), blank=True, null=True)

    def __str__(self):
        return self.id


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"))
    status = models.CharField(_("Status"), choices=STATUS, default="Pending", max_length=8)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    class Meta:
        unique_together = ("purchase", "product")
