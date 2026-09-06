"""
core/admin.py — AMISH Company Limited

Lengo: Moh'd afungue admin aone menyu ya Kiswahili, si majina ya models.
Kila kitu kimepangwa kwa vikundi na kila field ina maelezo.
"""

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import (
    FAQ, BusinessHour, ContactInfo, Enquiry, HeroSlide, Page,
    Reason, SectionSlide, SiteSettings, SocialLink, Stat, Testimonial,
)

admin.site.site_header = "AMISH Company Limited"
admin.site.site_title = "AMISH"
admin.site.index_title = "Website management"


class SingletonAdmin(UnfoldModelAdmin):
    """Blocks add and delete: there is only ever one record to edit."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse
        obj = self.model.load()
        return redirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[obj.pk],
            )
        )


class ImagePreviewMixin:
    preview_field = "image"

    @admin.display(description="Photo")
    def preview(self, obj):
        image = getattr(obj, self.preview_field, None)
        if image:
            return format_html(
                '<img src="{}" style="height:46px;border-radius:4px;object-fit:cover;">',
                image.url,
            )
        return "—"


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Identity", {"fields": ("company_name", "slogan", "short_intro")}),
        ("Branding", {"fields": ("logo", "logo_light", "favicon")}),
        ("Brand colours", {
            "fields": ("color_primary", "color_ink", "color_surface"),
            "description": "These colours are used across the whole website. Change them here and the entire site follows.",
        }),
        ("Search and sharing", {
            "fields": ("meta_title", "meta_description", "og_image"),
            "classes": ("collapse",),
        }),
    )


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonAdmin):
    fieldsets = (
        ("Phone and email", {
            "fields": ("phone_primary", "phone_secondary", "whatsapp", "email", "email_sales"),
        }),
        ("Shop address", {"fields": ("street", "ward", "city", "postal_address")}),
        ("Map location", {
            "fields": ("latitude", "longitude"),
            "description": "Open Google Maps, press and hold on the shop location, then copy the two numbers shown.",
            "classes": ("collapse",),
        }),
    )


@admin.register(BusinessHour)
class BusinessHourAdmin(UnfoldModelAdmin):
    list_display = ("get_day_display", "opens_at", "closes_at", "is_closed", "note")
    list_editable = ("opens_at", "closes_at", "is_closed", "note")
    list_display_links = None


@admin.register(SocialLink)
class SocialLinkAdmin(UnfoldModelAdmin):
    list_display = ("platform", "handle", "division", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("platform", "division", "is_active")


@admin.register(HeroSlide)
class HeroSlideAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    list_display = ("preview", "headline", "is_active", "order")
    list_editable = ("is_active", "order")
    fields = ("headline", "subline", "image", ("cta_label", "cta_url"), "is_active", "order")


@admin.register(Reason)
class ReasonAdmin(UnfoldModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(SectionSlide)
class SectionSlideAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    list_display = ("preview", "slot", "caption", "is_active", "order")
    list_editable = ("caption", "is_active", "order")
    list_filter = ("slot",)


@admin.register(Stat)
class StatAdmin(UnfoldModelAdmin):
    list_display = ("value", "label", "is_active", "order")
    list_editable = ("label", "is_active", "order")


@admin.register(Testimonial)
class TestimonialAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    preview_field = "photo"
    list_display = ("preview", "author", "role", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(FAQ)
class FAQAdmin(UnfoldModelAdmin):
    list_display = ("question", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(Page)
class PageAdmin(UnfoldModelAdmin):
    list_display = ("title", "slug", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "body", "is_active")}),
        ("Search", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )


@admin.register(Enquiry)
class EnquiryAdmin(UnfoldModelAdmin):
    list_display = ("name", "phone", "subject", "division", "status", "created_at")
    list_filter = ("status", "division", "created_at")
    search_fields = ("name", "phone", "email", "message")
    readonly_fields = ("name", "phone", "email", "subject", "message",
                       "division", "product", "created_at")
    fieldsets = (
        ("Enquiry", {"fields": ("name", "phone", "email", "subject", "message",
                               "division", "product", "created_at")}),
        ("Follow-up", {"fields": ("status", "internal_note")}),
    )

    def has_add_permission(self, request):
        return False
