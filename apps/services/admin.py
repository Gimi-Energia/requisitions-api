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
        "department",
        "request_date",
        "requester",
        "provider",
        "service",
        "value",
        "status",
    )
    list_display_links = ("id",)
    search_fields = (
        "provider",
        "service",
    )
    list_filter = ("status",)
    list_per_page = 25
    ordering = ("created_at",)


admin.site.register(ServiceType, ServiceTypes)
admin.site.register(Service, Services)
