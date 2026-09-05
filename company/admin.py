"""company/admin.py — AMISH Company Limited"""

from django.contrib import admin

from core.admin import ImagePreviewMixin, SingletonAdmin

from .models import About, Client, CoreValue, Credential, Milestone, Person


@admin.register(About)
class AboutAdmin(SingletonAdmin):
    fieldsets = (
        ("Utangulizi", {"fields": ("intro", "story", "story_image")}),
        ("Vision", {"fields": ("vision_en", "vision_sw")}),
        ("Mission", {"fields": ("mission_en", "mission_sw")}),
        ("Google", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "is_active", "order")
    list_editable = ("title", "is_active", "order")


@admin.register(Person)
class PersonAdmin(ImagePreviewMixin, admin.ModelAdmin):
    preview_field = "photo"
    list_display = ("preview", "full_name", "position", "is_director",
                    "on_business_card", "show_on_website", "order")
    list_editable = ("is_director", "on_business_card", "show_on_website", "order")
    search_fields = ("full_name", "position")
    fieldsets = (
        ("Msingi", {"fields": ("full_name", "position", "bio", "photo")}),
        ("Mawasiliano", {
            "fields": ("email", "phone", "linkedin"),
            "description": "Haya haya ndiyo yanayochapishwa kwenye business card yake.",
        }),
        ("Wapi aonekane", {
            "fields": ("is_director", "show_on_website", "on_business_card", "order", "is_active"),
        }),
    )


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ("label", "kind", "number", "show_on_website", "order")
    list_editable = ("show_on_website", "order")
    list_filter = ("kind",)


@admin.register(Client)
class ClientAdmin(ImagePreviewMixin, admin.ModelAdmin):
    preview_field = "logo"
    list_display = ("preview", "name", "is_active", "order")
    list_editable = ("is_active", "order")
