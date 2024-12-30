from django.contrib import admin
from apps.services.models import Service, ServiceType


class ServiceTypes(admin.ModelAdmin):
    list_display = ("id", "description")
    list_display_links = ("id",)
    search_fields = ("description",)
    list_per_page = 25
    ordering = ("description",)


class Services(admin.ModelAdmin):
    list_display = (
        "id",
        "control_number",
        "company",
        "status",
        "department",
        "requester",
        "provider",
        "service",
        "value",
        "created_at",
    )
    list_display_links = ("id",)
    search_fields = (
        "provider",
        "service__description",
        "control_number",
        "requester__email",
        "approver__email",
    )
    list_filter = ("status", "company")
    list_per_page = 25
    ordering = ("-created_at",)


admin.site.register(ServiceType, ServiceTypes)
admin.site.register(Service, Services)
