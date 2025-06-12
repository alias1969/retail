from django.contrib import admin

from products.models import Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """Админка контрагентов"""

    list_display = (
        "name",
        "item",
        "release_at",
    )
