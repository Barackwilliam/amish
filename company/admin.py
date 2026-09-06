"""company/admin.py — AMISH Company Limited"""

from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline as UnfoldTabularInline

from core.admin import ImagePreviewMixin, SingletonAdmin

from .models import About, Client, CoreValue, Credential, Milestone, Person


@admin.register(About)
class AboutAdmin(SingletonAdmin):
    fieldsets = (
        ("Introduction", {"fields": ("intro", "story", "story_image")}),
        ("Vision", {"fields": ("vision_en", "vision_sw")}),
        ("Mission", {"fields": ("mission_en", "mission_sw")}),
        ("Search", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )


@admin.register(CoreValue)
class CoreValueAdmin(UnfoldModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(Milestone)
class MilestoneAdmin(UnfoldModelAdmin):
    list_display = ("year", "title", "is_active", "order")
    list_editable = ("title", "is_active", "order")


@admin.register(Person)
class PersonAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    preview_field = "photo"
    list_display = ("preview", "full_name", "position", "is_director",
                    "on_business_card", "show_on_website", "order")
    list_editable = ("is_director", "on_business_card", "show_on_website", "order")
    search_fields = ("full_name", "position")
    fieldsets = (
        ("Basics", {"fields": ("full_name", "position", "bio", "photo")}),
        ("Contact details", {
            "fields": ("email", "phone", "linkedin"),
            "description": "These are the details printed on this person's business card.",
        }),
        ("Where they appear", {
            "fields": ("is_director", "show_on_website", "on_business_card", "order", "is_active"),
        }),
    )


@admin.register(Credential)
class CredentialAdmin(UnfoldModelAdmin):
    list_display = ("label", "kind", "number", "show_on_website", "order")
    list_editable = ("show_on_website", "order")
    list_filter = ("kind",)


@admin.register(Client)
class ClientAdmin(ImagePreviewMixin, UnfoldModelAdmin):
    preview_field = "logo"
    list_display = ("preview", "name", "is_active", "order")
    list_editable = ("is_active", "order")
