from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.validators.superuser import *


class UserManager(BaseUserManager):
    def create_user(
        self, name, email, document, cell_phone, fixed_phone, password=None
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            name=name,
            document=document,
            email=self.normalize_email(email),
            cell_phone=cell_phone,
            fixed_phone=fixed_phone,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, name, email, document, cell_phone, fixed_phone=None, password=None
    ):
        user = self.create_user(
            name=name,
            document=document,
            email=email,
            cell_phone=cell_phone,
            fixed_phone=fixed_phone,
            password=password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    username = None
    name = models.CharField(_("Complete Name"), max_length=100, validators=[valid_name])
    document = models.CharField(
        _("CNPJ/CPF"), unique=True, max_length=14, validators=[valid_document]
    )
    email = models.EmailField(
        _("E-mail"), unique=True, max_length=100, validators=[valid_email]
    )
    cell_phone = models.CharField(
        _("Cell Phone"), max_length=11, validators=[valid_phone]
    )
    fixed_phone = models.CharField(
        _("Fixed Phone"), max_length=10, null=True, blank=True, validators=[valid_phone]
    )
    is_active = models.BooleanField(_("Active Account"), default=True)
    is_admin = models.BooleanField(_("Administrator"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "document", "cell_phone"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_first_name(self):
        return self.name.split()[0].title()

    def get_last_name(self):
        return self.name.split()[-1].title()

    def get_first_last(self):
        name_split = self.name.split()
        return f"{name_split[0].title()} {name_split[-1].title()}"

    def get_short_name(self):
        name_split = self.name.split()
        return name_split[0][0] + name_split[-1][0]

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        permissions = (
            ("admin_user", "Can Admin Users"),
            ("disable_user", "Can disable User"),
        )
