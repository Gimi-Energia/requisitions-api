from django.contrib import admin
from apps.freights.models import Freight, FreightQuotation


class Freights(admin.ModelAdmin):
    list_display = (
        "id",
        "control_number",
        "company",
        "department",
        "request_date",
        "requester",
        "status",
    )
    list_display_links = ("id",)
    search_fields = (
        "requester",
        "approver",
    )
    list_filter = ("status",)
    list_per_page = 25
    ordering = ("created_at",)


class FreightQuotations(admin.ModelAdmin):
    list_display = ("freight", "transporter", "name_other", "price", "status")
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
