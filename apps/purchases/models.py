from datetime import date
from uuid import uuid4

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.departments.models import Department
from apps.products.models import Product
from apps.users.models import User

COMPANIES = [
    ("Gimi", "Gimi"),
    ("GBL", "GBL"),
    ("GPB", "GPB"),
    ("GS", "GS"),
    ("GIR", "GIR"),
    ("Filial", "Filial"),
]
STATUS = [
    ("Opened", "Opened"),
    ("Approved", "Approved"),
    ("Denied", "Denied"),
    ("Canceled", "Canceled"),
    ("Quotation", "Quotation"),
]


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=6)
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    request_date = models.DateField(_("Request Date"), default=date.today)
    requester = models.ForeignKey(
        User, verbose_name=_("Requester"), on_delete=models.CASCADE, related_name="Requester"
    )
    motive = models.TextField(_("Motive"))
    obs = models.TextField(_("Observation"))
    status = models.CharField(_("Status"), choices=STATUS, default="Opened", max_length=9)
    products = models.ManyToManyField(
        Product, through="PurchaseProduct", verbose_name=_("Products")
    )
    approver = models.ForeignKey(
        User,
        verbose_name=_("Approver"),
        on_delete=models.CASCADE,
        related_name="Approver",
    )
    approval_date = models.DateTimeField(_("Approval Date"), blank=True, null=True)
    has_quotation = models.BooleanField(_("Has Quotation?"), default=True)
    quotation_emails = models.TextField(_("Purchase Quotation Emails"), blank=True, null=True)
    quotation_date = models.DateTimeField(
        _("Quotation Date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    control_number = models.IntegerField(_("Control Number"), default=0)
    motive_denied = models.TextField(_("Motive Denied"), blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        exists = Purchase.objects.filter(id=self.pk).exists()
        if not exists:
            with transaction.atomic():
                last = Purchase.objects.select_for_update().order_by("-control_number").first()
                if last:
                    self.control_number = last.control_number + 1
                else:
                    self.control_number = 1

        super(Purchase, self).save(*args, **kwargs)


class PurchaseProduct(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(_("Quantity"), max_digits=12, decimal_places=5)
    price = models.DecimalField(_("Price"), max_digits=12, decimal_places=5, blank=True, null=True)
    status = models.CharField(_("Status"), choices=STATUS, default="Opened", max_length=9)
    obs = models.TextField(_("Observation"), blank=True, null=True)

    def __str__(self):
        return f"{self.product} - {self.quantity} x R$ {self.price}"

