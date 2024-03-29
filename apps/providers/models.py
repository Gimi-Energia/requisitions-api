from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseCompany(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=50)
    cnpj = models.CharField(_("CNPJ"), max_length=14)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=11, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Provider(BaseCompany):
    pass


class Transporter(BaseCompany):
    pass
