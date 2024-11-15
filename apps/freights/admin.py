from django.contrib import admin
from apps.freights.models import Freight, FreightQuotation


class Freights(admin.ModelAdmin):
    list_display = (
        "id",
        "company",
        "status",
        "department",
        "requester",
        "created_at",
    )
    list_display_links = ("id",)
    search_fields = ("requester__email", "approver__email", "contract__contract_number")
    list_filter = ("status", "company")
    list_per_page = 25
    ordering = ("-created_at",)


class FreightQuotations(admin.ModelAdmin):
    list_display = ("freight", "transporter", "price", "status")
    list_display_links = ("freight", "transporter")
    search_fields = (
        "freight",
        "transporter",
    )
    list_filter = ("status",)
    list_per_page = 25
    ordering = ("freight", "transporter")


admin.site.register(Freight, Freights)
admin.site.register(FreightQuotation, FreightQuotations)
