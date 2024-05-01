from django.contrib import admin
from apps.users.models import User


class Users(admin.ModelAdmin):
    list_display = ("id", "name", "email", "company", "department", "type")
    list_display_links = ("id",)
    search_fields = (
        "name",
        "email",
    )
    list_filter = ("is_admin", "type")
    list_per_page = 25
    ordering = ("name", "email")


admin.site.register(User, Users)
