from django.contrib import admin

from .models import Employee, Position, Software


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("position", "cost_center", "company")
    search_fields = ("position", "cost_center__name", "company")
    list_filter = ("company", "cost_center")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "control_number",
        "company",
        "status",
        "cost_center",
        "position",
        "requester",
        "created_at",
    )
    search_fields = ("complete_name", "position__position", "company", "replaced_email")
    list_filter = (
        "status",
        "company",
        "cost_center__name",
        "position__position",
        "request_date",
        "approval_date",
    )
    readonly_fields = ("control_number", "created_at")
    date_hierarchy = "request_date"
    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "complete_name",
                    "position",
                    "company",
                    "cost_center",
                    "motive",
                    "requester",
                    "status",
                    "obs",
                )
            },
        ),
        (
            "Additional Details",
            {
                "fields": (
                    "is_replacement",
                    "replaced_email",
                    "has_pc",
                    "needs_phone",
                    "needs_tablet",
                    "has_workstation",
                    "needs_software",
                    "software_names",
                )
            },
        ),
        (
            "Approval Information",
            {
                "fields": ("approver", "approval_date"),
            },
        ),
        (
            "Control and Dates",
            {
                "fields": ("control_number", "request_date", "start_date", "created_at"),
            },
        ),
    )


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
