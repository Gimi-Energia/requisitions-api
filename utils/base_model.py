from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # created_at = models.DateTimeField(
    #     blank=True,
    #     null=True,
    #     verbose_name="data de cadastro no Sistema",
    #     auto_now_add=True,
    # )
    # updated_at = models.DateTimeField(
    #     blank=True,
    #     null=True,
    #     verbose_name="data de atualização no Sistema",
    #     auto_now=True,
    # )
