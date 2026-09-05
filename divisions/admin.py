"""divisions/admin.py — AMISH Company Limited"""

from django.contrib import admin
from django.utils.html import format_html

from core.admin import ImagePreviewMixin

from .models import (
    Category, Division, DivisionImage, GalleryImage, Product, ProductImage, Service,
)


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    fields = ("name", "description", "image", "order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


class DivisionImageInline(admin.TabularInline):
    model = DivisionImage
    extra = 1
    fields = ("image", "caption", "order", "is_active")
    verbose_name = "Picha ya paneli"
    verbose_name_plural = "Picha zinazopita kwenye paneli ya homepage"


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ("name", "summary", "icon", "order", "is_active")


@admin.register(Division)
class DivisionAdmin(ImagePreviewMixin, admin.ModelAdmin):
    preview_field = "cover"
    list_display = ("preview", "name", "status", "kind", "product_count", "is_active", "order")
    list_editable = ("status", "is_active", "order")
    list_filter = ("status", "kind")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [DivisionImageInline, CategoryInline, ServiceInline]
    fieldsets = (
        ("Msingi", {"fields": ("name", "slug", "tagline", "description")}),
        ("Hali", {
            "fields": ("status", "kind", "launch_note"),
            "description": "Tawi linalokuja linaonekana kwenye website lakini bidhaa zake hazionyeshwi. "
                           "Likianza kufanya kazi, badilisha hali kuwa 'Inafanya kazi' — hakuna kingine kinachohitajika.",
        }),
        ("Muonekano", {"fields": ("icon", "cover", "accent_color", "order", "is_active")}),
        ("Google", {"fields": ("meta_title", "meta_description", "og_image"),
                    "classes": ("collapse",)}),
    )

    @admin.display(description="Bidhaa")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "division", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("division",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "caption", "order")


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "name", "division", "category",
                    "price_display", "in_stock", "is_featured", "is_active")
    list_editable = ("in_stock", "is_featured", "is_active")
    list_filter = ("division", "category", "in_stock", "is_featured", "is_active")
    search_fields = ("name", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    list_select_related = ("division", "category")
    fieldsets = (
        ("Msingi", {"fields": ("division", "category", "name", "slug", "summary", "description")}),
        ("Picha", {"fields": ("image",)}),
        ("Bei", {
            "fields": ("price", "unit", "show_price"),
            "description": "Ukizima 'Onyesha bei', mteja anaona kitufe cha kuuliza bei badala ya namba.",
        }),
        ("Hali", {"fields": ("in_stock", "is_featured", "is_active", "order")}),
        ("Google", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )

    @admin.display(description="Bei")
    def price_display(self, obj):
        if obj.price is None:
            return "—"
        label = f"TSh {obj.price:,.0f}"
        if not obj.show_price:
            return format_html('<span style="opacity:.5;">{} (imefichwa)</span>', label)
        return label


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "division", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("division",)


@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "caption", "division", "is_active", "order")
    list_editable = ("caption", "is_active", "order")
    list_filter = ("division",)
