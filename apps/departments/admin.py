from django.contrib import admin
from apps.departments.models import Department


class Departments(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id",)
    search_fields = ("name",)
    list_per_page = 25
    ordering = ("name",)


admin.site.register(Department, Departments)
