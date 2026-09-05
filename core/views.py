from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from company.models import Client, CoreValue, Milestone, Person
from divisions.models import Division, GalleryImage, Product

from .forms import EnquiryForm
from .models import FAQ, HeroSlide, Page, Reason, SectionSlide, Stat, Testimonial


def _handle_enquiry(request, redirect_to):
    form = EnquiryForm(request.POST)
    if form.is_valid():
        enquiry = form.save()
        _notify(enquiry)
        messages.success(
            request,
            "Thank you — your message has reached us. We will call or reply "
            "within a few working hours.",
        )
        return redirect(redirect_to), None
    messages.error(
        request,
        "Your message was not sent. Please check the fields marked below.",
    )
    return None, form


def _notify(enquiry):
    if not django_settings.ENQUIRY_NOTIFY_EMAIL:
        return
    try:
        send_mail(
            subject=f"New enquiry from {enquiry.name}",
            message=(
                f"Name: {enquiry.name}\n"
                f"Phone: {enquiry.phone}\n"
                f"Email: {enquiry.email}\n"
                f"Subject: {enquiry.subject}\n\n"
                f"{enquiry.message}"
            ),
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            recipient_list=[django_settings.ENQUIRY_NOTIFY_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


def home(request):
    divisions = list(
        Division.objects.filter(is_active=True).prefetch_related("slides", "categories")
    )
    context = {
        "slides": HeroSlide.objects.filter(is_active=True)[:4],
        "live_divisions": [d for d in divisions if d.is_live],
        "upcoming": [d for d in divisions if not d.is_live],
        "featured": Product.objects.filter(
            is_active=True, is_featured=True, division__is_active=True
        ).select_related("division")[:8],
        "stats": Stat.objects.filter(is_active=True),
        "reasons": Reason.objects.filter(is_active=True)[:4],
        "band_slides": SectionSlide.objects.filter(
            is_active=True, slot=SectionSlide.Slot.BAND
        )[:4],
        "strip": GalleryImage.objects.filter(is_active=True)[:10],
        "values": CoreValue.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_active=True),
        "clients": Client.objects.filter(is_active=True),
        "form": EnquiryForm(),
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html", {
        "values": CoreValue.objects.filter(is_active=True),
        "milestones": Milestone.objects.filter(is_active=True),
        "team": Person.objects.filter(is_active=True, show_on_website=True),
        "stats": Stat.objects.filter(is_active=True),
        "reasons": Reason.objects.filter(is_active=True)[:4],
        "band_slides": SectionSlide.objects.filter(
            is_active=True, slot=SectionSlide.Slot.BAND
        )[:4],
        "strip": GalleryImage.objects.filter(is_active=True)[:10],
        "clients": Client.objects.filter(is_active=True),
    })


def contact(request):
    form = EnquiryForm()
    if request.method == "POST":
        response, form = _handle_enquiry(request, "core:contact")
        if response:
            return response
    return render(request, "pages/contact.html", {
        "form": form,
        "faqs": FAQ.objects.filter(is_active=True),
    })


def gallery(request):
    return render(request, "pages/gallery.html", {
        "images": GalleryImage.objects.filter(is_active=True).select_related("division"),
    })


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, "pages/page.html", {"page": page})


def not_found(request, exception=None):
    return render(request, "404.html", status=404)


def robots(request):
    """Inaruhusu Googlebot-Image na kuonyesha sitemap."""
    site = request.build_absolute_uri("/").rstrip("/")
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "",
        "User-agent: Googlebot-Image",
        "Allow: /",
        "",
        f"Sitemap: {site}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
