from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

DAY_SHORT = {
    1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
    5: "Friday", 6: "Saturday", 7: "Sunday",
}


@register.filter
def tsh(value):
    if value is None:
        return ""
    return f"TSh {value:,.0f}"


@register.simple_tag
def whatsapp(contact, text=""):
    if not contact or not contact.whatsapp:
        return ""
    base = f"https://wa.me/{contact.whatsapp}"
    if text:
        from urllib.parse import quote
        return mark_safe(f"{base}?text={quote(text)}")
    return mark_safe(base)


@register.filter
def open_days(hours):
    """'Monday - Saturday' instead of listing six separate days."""
    working = [h for h in hours if not h.is_closed]
    if not working:
        return ""
    if len(working) == 1:
        return DAY_SHORT.get(working[0].day, "")
    days = [h.day for h in working]
    if days == list(range(min(days), max(days) + 1)):
        return f"{DAY_SHORT.get(min(days))} - {DAY_SHORT.get(max(days))}"
    return ", ".join(DAY_SHORT.get(d, "") for d in days)


@register.filter
def open_time(hours):
    working = [h for h in hours if not h.is_closed and h.opens_at and h.closes_at]
    if not working:
        return ""
    first = working[0]
    return f"{first.opens_at:%H:%M} - {first.closes_at:%H:%M}"


@register.simple_tag
def bg(image, fallback):
    """Picha ya database ikiwepo; la sivyo picha ya default kwenye static."""
    try:
        if image and image.url:
            return image.url
    except (ValueError, AttributeError):
        pass
    return static(f"img/defaults/{fallback}")


@register.filter
def nth(sequence, index):
    """Kipengele cha n kwenye orodha, bila kuvunjika ikiwa haipo."""
    try:
        return list(sequence)[index]
    except (IndexError, TypeError, ValueError):
        return None


@register.simple_tag(takes_context=True)
def absurl(context, url):
    """URL kamili kwa sitemap — inaacha za Cloudinary kama zilivyo."""
    if not url:
        return ""
    if url.startswith("http"):
        return url
    request = context.get("request")
    if request is None:
        return url
    return request.build_absolute_uri(url)
