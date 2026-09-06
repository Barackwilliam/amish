"""divisions/admin.py — AMISH Company Limited"""

from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline as UnfoldTabularInline
from django.utils.html import format_html

from core.admin import ImagePreviewMixin

from .models import (
    Category, Division, DivisionImage, GalleryImage, Product, ProductImage, Service,
)


class CategoryInline(UnfoldTabularInline):
    model = Category
    extra = 0
    # slug haipo hapa kwa makusudi: inajitengeneza kwenye Category.save().
    # Ikiwekwa prepopulated_fields bila shamba lenyewe, admin inavunjika.
    fields = ("name", "description", "image", "order", "is_active")


class DivisionImageInline(UnfoldTabularInline):
    model = DivisionImage
    extra = 1
    fields = ("image", "caption", "order", "is_active")
    verbose_name = "Panel photo"
    verbose_name_plural = "Photos that rotate on the home page panel"


class ServiceInline(UnfoldTabularInline):
    model = Service
    extra = 0
    fields = ("name", "summary", "icon", "order", "is_active")


@admin.register(Division)
class DivisionAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    preview_field = "cover"
    list_display = ("preview", "name", "status", "kind", "product_count", "is_active", "order")
    list_editable = ("status", "is_active", "order")
    list_filter = ("status", "kind")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [DivisionImageInline, CategoryInline, ServiceInline]
    fieldsets = (
        ("Basics", {"fields": ("name", "slug", "tagline", "description")}),
        ("Status", {
            "fields": ("status", "kind", "launch_note"),
            "description": "A division in preparation is listed on the website but its products stay hidden. "
                           "When it opens, switch the status to 'Trading' — nothing else is needed.",
        }),
        ("Appearance", {"fields": ("icon", "cover", "accent_color", "order", "is_active")}),
        ("Search", {"fields": ("meta_title", "meta_description", "og_image"),
                    "classes": ("collapse",)}),
    )

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Category)
class CategoryAdmin(UnfoldModelAdmin):
    list_display = ("name", "division", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("division",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(UnfoldTabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "caption", "order")


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    list_display = ("preview", "name", "division", "category",
                    "price_display", "in_stock", "is_featured", "is_active")
    list_editable = ("in_stock", "is_featured", "is_active")
    list_filter = ("division", "category", "in_stock", "is_featured", "is_active")
    search_fields = ("name", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    list_select_related = ("division", "category")
    fieldsets = (
        ("Basics", {"fields": ("division", "category", "name", "slug", "summary", "description")}),
        ("Photo", {"fields": ("image",)}),
        ("Price", {
            "fields": ("price", "unit", "show_price"),
            "description": "Turn off 'Show price' and customers see an 'Ask for price' link instead of a figure.",
        }),
        ("Status", {"fields": ("in_stock", "is_featured", "is_active", "order")}),
        ("Search", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )

    @admin.display(description="Price")
    def price_display(self, obj):
        if obj.price is None:
            return "—"
        label = f"TSh {obj.price:,.0f}"
        if not obj.show_price:
            return format_html('<span style="opacity:.5;">{} (hidden)</span>', label)
        return label


@admin.register(Service)
class ServiceAdmin(UnfoldModelAdmin):
    list_display = ("name", "division", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("division",)


@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    list_display = ("preview", "caption", "division", "is_active", "order")
    list_editable = ("caption", "is_active", "order")
    list_filter = ("division",)
