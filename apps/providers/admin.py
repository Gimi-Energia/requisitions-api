from django.contrib import admin
from apps.providers.models import Provider, Transporter


class BaseCompany(admin.ModelAdmin):
    list_display = ("id", "name", "cnpj", "email", "phone")
    list_display_links = ("id",)
    search_fields = (
        "name",
        "cnpj",
        "email",
    )
    list_per_page = 25
    ordering = ("name", "email", "cnpj")


admin.site.register(Provider, BaseCompany)
admin.site.register(Transporter, BaseCompany)
