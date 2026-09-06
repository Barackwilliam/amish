"""
core/models.py — AMISH Company Limited
Kila kitu hapa kinahaririwa kupitia Django admin. Hakuna maandishi
yaliyofichwa kwenye templates.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# Abstract base models
# ---------------------------------------------------------------------------

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Orderable(models.Model):
    """Mpangilio wa kuonekana kwenye site. Namba ndogo inatangulia."""
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Order",
        help_text="Lower numbers appear first.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Visible on the website",
    )

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class Singleton(models.Model):
    """Model yenye record moja tu. Admin inafungua moja kwa moja kwenye edit."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SEOFields(models.Model):
    """Huingizwa kwenye kila page inayohitaji SEO yake."""
    meta_title = models.CharField(
        max_length=70, blank=True,
        verbose_name="SEO title",
        help_text="Shown in Google results. Leave blank to use the normal title.",
    )
    meta_description = models.CharField(
        max_length=160, blank=True,
        verbose_name="SEO description",
        help_text="One or two sentences shown under the title in Google.",
    )
    og_image = models.ImageField(
        upload_to="seo/", blank=True,
        verbose_name="Share image",
        help_text="Shown when the link is shared on WhatsApp or Facebook. 1200x630px.",
    )

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Site settings
# ---------------------------------------------------------------------------

class SiteSettings(Singleton, SEOFields, TimeStamped):
    company_name = models.CharField(
        max_length=120, default="AMISH Company Limited",
        verbose_name="Company name",
    )
    slogan = models.CharField(
        max_length=160, default="Your Success, Our Commitment",
        verbose_name="Slogan",
    )
    short_intro = models.TextField(
        blank=True,
        verbose_name="Short introduction",
        help_text="Two or three sentences describing the company. Used in the footer and intro sections.",
    )

    logo = models.ImageField(
        upload_to="brand/", blank=True,
        verbose_name="Logo (for light backgrounds)",
    )
    logo_light = models.ImageField(
        upload_to="brand/", blank=True,
        verbose_name="Logo (for dark backgrounds)",
    )
    favicon = models.ImageField(
        upload_to="brand/", blank=True,
        verbose_name="Favicon",
        help_text="Small icon shown in the browser tab. 512x512px.",
    )

    # Rangi rasmi za kampuni
    color_primary = models.CharField(
        max_length=7, default="#142B6F",
        verbose_name="Primary colour",
    )
    color_ink = models.CharField(
        max_length=7, default="#000000",
        verbose_name="Text colour",
    )
    color_surface = models.CharField(
        max_length=7, default="#FFFFFF",
        verbose_name="Background colour",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.company_name

    def clean(self):
        for field in ("color_primary", "color_ink", "color_surface"):
            value = getattr(self, field, "")
            if value and not (value.startswith("#") and len(value) == 7):
                raise ValidationError({field: "Use hex format, for example #003ABC"})


class ContactInfo(Singleton, TimeStamped):
    """Mawasiliano. Yanatumika header, footer, contact page na schema ya Google."""
    phone_primary = models.CharField(max_length=30, blank=True, verbose_name="Primary phone")
    phone_secondary = models.CharField(max_length=30, blank=True, verbose_name="Second phone")
    whatsapp = models.CharField(
        max_length=30, blank=True,
        verbose_name="WhatsApp number",
        help_text="International format with no symbols, for example 255711686816",
    )
    email = models.EmailField(blank=True, verbose_name="Main email")
    email_sales = models.EmailField(blank=True, verbose_name="Sales email")

    street = models.CharField(max_length=160, blank=True, verbose_name="Street or building")
    ward = models.CharField(max_length=80, blank=True, default="Kigamboni", verbose_name="Ward")
    city = models.CharField(max_length=80, blank=True, default="Dar es Salaam", verbose_name="City")
    postal_address = models.CharField(max_length=80, blank=True, verbose_name="P.O. Box")

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude",
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude",
    )

    class Meta:
        verbose_name = "Contact details"
        verbose_name_plural = "Contact details"

    def __str__(self):
        return "Company contact details"

    @property
    def full_address(self):
        parts = [self.street, self.ward, self.city]
        return ", ".join(p for p in parts if p)

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.whatsapp}" if self.whatsapp else ""


class BusinessHour(Orderable):
    class Day(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUNDAY = 7, "Sunday"

    day = models.IntegerField(choices=Day.choices, unique=True, verbose_name="Day")
    opens_at = models.TimeField(null=True, blank=True, verbose_name="Opens at")
    closes_at = models.TimeField(null=True, blank=True, verbose_name="Closes at")
    is_closed = models.BooleanField(default=False, verbose_name="Closed on this day")
    note = models.CharField(
        max_length=80, blank=True,
        verbose_name="Note",
        help_text="For example: Half day, or By appointment only.",
    )

    class Meta:
        ordering = ["day"]
        verbose_name = "Opening hours"
        verbose_name_plural = "Opening hours"

    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_display()}: Closed"
        return f"{self.get_day_display()}: {self.opens_at:%H:%M} - {self.closes_at:%H:%M}"


class SocialLink(Orderable):
    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        TIKTOK = "tiktok", "TikTok"
        WHATSAPP_CHANNEL = "whatsapp_channel", "WhatsApp Channel"
        LINKEDIN = "linkedin", "LinkedIn"
        YOUTUBE = "youtube", "YouTube"
        X = "x", "X (Twitter)"

    platform = models.CharField(max_length=30, choices=Platform.choices, verbose_name="Platform")
    handle = models.CharField(
        max_length=80, blank=True,
        verbose_name="Page name",
        help_text="For example: AMISH Hardware",
    )
    url = models.URLField(verbose_name="Link")
    division = models.ForeignKey(
        "divisions.Division", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="social_links",
        verbose_name="Which division",
        help_text="Leave blank if this is a company-wide page.",
    )

    class Meta(Orderable.Meta):
        verbose_name = "Social media link"
        verbose_name_plural = "Social media links"

    def __str__(self):
        return f"{self.get_platform_display()} — {self.handle or self.url}"


# ---------------------------------------------------------------------------
# Homepage content
# ---------------------------------------------------------------------------

class HeroSlide(Orderable):
    """The large slides at the very top of the home page."""
    headline = models.CharField(max_length=90, verbose_name="Headline")
    subline = models.CharField(max_length=180, blank=True, verbose_name="Supporting text")
    image = models.ImageField(
        upload_to="hero/",
        verbose_name="Image",
        help_text="At least 2000px wide, good quality.",
    )
    cta_label = models.CharField(max_length=40, blank=True, verbose_name="Button label")
    cta_url = models.CharField(max_length=200, blank=True, verbose_name="Button link")

    class Meta(Orderable.Meta):
        verbose_name = "Home page slide"
        verbose_name_plural = "Home page slides"

    def __str__(self):
        return self.headline


class Stat(Orderable):
    """Key figures shown on the home page."""
    value = models.CharField(max_length=20, verbose_name="Figure", help_text="For example: 12, 500+, 98%")
    label = models.CharField(max_length=60, verbose_name="Label", help_text="For example: Years of experience")

    class Meta(Orderable.Meta):
        verbose_name = "Key figure"
        verbose_name_plural = "Key figures"

    def __str__(self):
        return f"{self.value} {self.label}"


class Testimonial(Orderable):
    author = models.CharField(max_length=90, verbose_name="Customer name")
    role = models.CharField(max_length=90, blank=True, verbose_name="Role or company")
    quote = models.TextField(verbose_name="What they said")
    photo = models.ImageField(upload_to="testimonials/", blank=True, verbose_name="Photo")

    class Meta(Orderable.Meta):
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.author


class FAQ(Orderable):
    question = models.CharField(max_length=200, verbose_name="Question")
    answer = models.TextField(verbose_name="Answer")

    class Meta(Orderable.Meta):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


# ---------------------------------------------------------------------------
# Kurasa za maandishi (Privacy, Terms, n.k.)
# ---------------------------------------------------------------------------

class Page(SEOFields, TimeStamped):
    title = models.CharField(max_length=120, verbose_name="Title")
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    body = models.TextField(verbose_name="Body text")
    is_active = models.BooleanField(default=True, verbose_name="Visible")

    class Meta:
        ordering = ["title"]
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Ujumbe kutoka kwa wateja
# ---------------------------------------------------------------------------

class Enquiry(TimeStamped):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=90, verbose_name="Name")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone")
    email = models.EmailField(blank=True, verbose_name="Email")
    subject = models.CharField(max_length=140, blank=True, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")

    division = models.ForeignKey(
        "divisions.Division", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="enquiries",
        verbose_name="Division",
    )
    product = models.ForeignKey(
        "divisions.Product", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="enquiries",
        verbose_name="Product",
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Status",
    )
    internal_note = models.TextField(blank=True, verbose_name="Internal note")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer enquiry"
        verbose_name_plural = "Customer enquiries"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d/%m/%Y}"


class SectionSlide(Orderable):
    """Picha za nyuma zinazobadilika kwenye sehemu maalum za ukurasa."""

    class Slot(models.TextChoices):
        BAND = "band", "Vision and Mission band"
        FOOTER = "footer", "Footer background"

    slot = models.CharField(
        max_length=20, choices=Slot.choices, default=Slot.BAND, verbose_name="Section",
    )
    image = models.ImageField(upload_to="sections/", verbose_name="Photo")
    caption = models.CharField(max_length=120, blank=True, verbose_name="Internal note")

    class Meta(Orderable.Meta):
        verbose_name = "Background image"
        verbose_name_plural = "Background images"

    def __str__(self):
        return f"{self.get_slot_display()} — {self.order}"


class Reason(Orderable):
    """Sababu za kununua AMISH — sehemu ya "Kwa nini AMISH" homepage."""

    title = models.CharField(max_length=70, verbose_name="Title")
    description = models.TextField(verbose_name="Description")

    class Meta(Orderable.Meta):
        verbose_name = "Reason to buy here"
        verbose_name_plural = "Why AMISH"

    def __str__(self):
        return self.title
