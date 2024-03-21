from django.contrib import admin
from apps.contracts.models import Contract


class Contracts(admin.ModelAdmin):
    list_display = (
        "id",
        "company",
        "contract_number",
        "control_number",
        "client_name",
        "project_name",
        "freight_estimated",
        "freight_consumed",
    )
    list_display_links = ("id",)
    search_fields = (
        "contract_number",
        "control_number",
        "company"
    )
    list_per_page = 25
    ordering = ("contract_number", "control_number")


admin.site.register(Contract, Contracts)
