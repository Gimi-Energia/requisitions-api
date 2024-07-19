from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.base_model import BaseModel


class Product(BaseModel):
    code = models.CharField(_("Code"), max_length=40, unique=True)
    un = models.CharField(_("Measurement Unit"), max_length=30)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.code
