from django.contrib import admin
from apps.purchases.models import Purchase, PurchaseProduct


class Purchases(admin.ModelAdmin):
    list_display = (
        "id",
        "control_number",
        "company",
        "department",
        "request_date",
        "requester",
        "status",
    )
    list_display_links = ("id",)
    search_fields = (
        "requester",
        "approver",
    )
    list_filter = ("status",)
    list_per_page = 25
    ordering = ("created_at",)


class PurchaseProducts(admin.ModelAdmin):
    list_display = ("purchase", "product", "quantity", "price", "status")
    list_display_links = ("purchase", "product")
    search_fields = (
        "purchase",
        "product",
    )
    list_filter = ("status",)
    list_per_page = 25
    ordering = ("purchase", "product")


admin.site.register(Purchase, Purchases)
admin.site.register(PurchaseProduct, PurchaseProducts)
