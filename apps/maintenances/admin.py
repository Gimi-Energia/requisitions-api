from django.contrib import admin

from apps.maintenances.models import Maintenance

class Maintenances(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "requester",
        "created_at",
        "status",
    )
    list_display_links = ("id",)
    search_fields = (
        "name",
        "status",
        "requester",
    )
    list_filter = ("requester",)
    list_per_page = 25
    ordering = ("-created_at",)

admin.site.register(Maintenance, Maintenances)
