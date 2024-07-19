from django.contrib import admin

from apps.products.models import Product


class Products(admin.ModelAdmin):
    list_display = ("id", "code", "un", "description")
    list_display_links = ("id",)
    search_fields = (
        "code",
        "description",
    )
    list_per_page = 25
    ordering = ("code", "un")


admin.site.register(Product, Products)
