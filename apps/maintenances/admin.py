from django.contrib import admin

from apps.maintenances.models import Maintenance, Responsible


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "company",
        "object",
        "status",
        "department",
        "requester",
        "approver",
        "created_at",
        "request_date",
        "forecast_date",
        "end_date",
    )
    list_filter = ("company", "status", "department", "request_date", "forecast_date")
    search_fields = ("name", "object", "requester__email", "approver__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "company",
                    "name",
                    "extension",
                    "department",
                    "object",
                    "url",
                    "obs",
                )
            },
        ),
        (
            "Requester Details",
            {
                "fields": (
                    "requester",
                    "request_date",
                    "status",
                )
            },
        ),
        (
            "Approver Details",
            {
                "fields": (
                    "approver",
                    "forecast_date",
                    "approver_obs",
                    "approver_status",
                    "end_date",
                    "motive_denied",
                )
            },
        ),
    )


@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "extension")
    search_fields = ("name", "email", "phone", "extension")
    ordering = ("name",)
