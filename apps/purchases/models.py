from datetime import date
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.departments.models import Department
from apps.products.models import Product
from apps.users.models import User

COMPANIES = [("Gimi", "Gimi"), ("GBL", "GBL"), ("GPB", "GPB"), ("GS", "GS"), ("GIR", "GIR")]
STATUS = [("Opened", "Opened"), ("Approved", "Approved"), ("Denied", "Denied")]


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    request_date = models.DateField(_("Request Date"), default=date.today)
    requester = models.ForeignKey(
        User, verbose_name=_("Requester"), on_delete=models.CASCADE, related_name="Requester"
    )
    motive = models.CharField(_("Motive"), max_length=50)
    obs = models.TextField(_("Observation"))
    status = models.CharField(_("Status"), choices=STATUS, default="Opened", max_length=8)
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
    approval_date = models.DateTimeField(_("Approval Date"), blank=True, null=True)

    def __str__(self):
        return str(self.id)


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(_("Quantity"), max_digits=10, decimal_places=2)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Status"), choices=STATUS, default="Opened", max_length=8)

    def __str__(self):
        return f"{self.product} - {self.quantity} x R$ {self.price}"

    class Meta:
        unique_together = ("purchase", "product")
