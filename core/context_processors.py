"""Vitu vinavyoonekana kila ukurasa: logo, rangi, mawasiliano, menyu."""

from django.core.cache import cache

CACHE_SECONDS = 300


def site(request):
    data = cache.get("site_context")
    if data is None:
        from company.models import About
        from divisions.models import Division

        from .models import BusinessHour, ContactInfo, SectionSlide, SiteSettings, SocialLink

        divisions = list(
            Division.objects.filter(is_active=True).order_by("order", "id")
        )
        data = {
            "settings_obj": SiteSettings.load(),
            "contact": ContactInfo.load(),
            "about": About.load(),
            "hours": list(BusinessHour.objects.filter(is_active=True)),
            "socials": list(
                SocialLink.objects.filter(is_active=True).select_related("division")
            ),
            "footer_bg": SectionSlide.objects.filter(
                is_active=True, slot=SectionSlide.Slot.FOOTER
            ).first(),
            "nav_divisions": [d for d in divisions if d.is_live],
            "upcoming_divisions": [d for d in divisions if not d.is_live],
        }
        cache.set("site_context", data, CACHE_SECONDS)
    return data
