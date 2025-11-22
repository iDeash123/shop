from dis import disco
from email.mime import image
from os import name
from tabnanny import verbose
from unicodedata import category
from django.core.validators import slug_re
from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Category name")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name="URL",
    )

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Product name")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name="URL",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="Image"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Price"
    )
    discount = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2, verbose_name="Discount %"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")

    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name="Category"
    )

    brand = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Brand"
    )
    grilling_area_sq_inch = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Grilling Area (e.g. sq. in / cm²)",
    )
    power_kw = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Power (kW/BTU)",
    )
    burner_count = models.PositiveSmallIntegerField(
        default=0, verbose_name="Number of Burners"
    )
    body_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Body Material"
    )
    color = models.CharField(max_length=50, default="Black", verbose_name="Color")
    warranty_years = models.PositiveSmallIntegerField(
        default=1, verbose_name="Warranty (Years)"
    )

    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Weight (kg)",
    )
    dimensions_cm = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Dimensions (W x H x D cm)"
    )

    has_thermometer = models.BooleanField(
        default=False, verbose_name="Built-in Thermometer"
    )
    has_side_burner = models.BooleanField(default=False, verbose_name="Side Burner")
    is_portable = models.BooleanField(default=False, verbose_name="Portable")

    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} Quantity {self.quantity}"

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price
