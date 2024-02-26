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
        "company",
        "department",
        "request_date",
        "requester",
        "provider",
        "service",
        "value",
        "status",
        "approver",
        "approval_date",
    )
    list_display_links = ("id",)
    search_fields = (
        "provider",
        "service",
    )
    list_filter = ("status",)
    list_per_page = 25
    ordering = ("request_date", "approval_date")


admin.site.register(ServiceType, ServiceTypes)
admin.site.register(Service, Services)
