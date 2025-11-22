from django.contrib import admin
from goods.models import Categories, Products


# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    # list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "category",
        "price",
        "discount",
        "quantity",
        "brand",
        "burner_count",
        "is_portable",
    )
    list_editable = ["discount"]
    search_fields = (
        "name",
        "description",
        "brand",
        "body_material",
        "color",
    )
    list_filter = (
        "category",
        "discount",
        "quantity",
        "brand",
        "body_material",
        "color",
        "has_thermometer",
        "has_side_burner",
        "is_portable",
    )
    fields = [
        "name",
        "slug",
        "category",
        "brand",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
        # Характеристики
        ("grilling_area_sq_inch", "power_kw", "burner_count"),
        ("body_material", "color", "warranty_years"),
        # Логистика
        ("weight_kg", "dimensions_cm"),
        # Булевы поля
        ("has_thermometer", "has_side_burner", "is_portable"),
    ]
