from django.contrib import admin

from apps.employees.models import Position, Employee

# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    ordering = ["cost_center"]

admin.site.register(Position, PositionAdmin)
admin.site.register(Employee)