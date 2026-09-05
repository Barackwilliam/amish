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
        verbose_name="Mpangilio",
        help_text="Namba ndogo inaonekana kwanza.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Inaonekana kwenye website",
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
        verbose_name="Kichwa cha SEO",
        help_text="Kinachoonekana Google. Ukikiacha wazi, jina la kawaida litatumika.",
    )
    meta_description = models.CharField(
        max_length=160, blank=True,
        verbose_name="Maelezo ya SEO",
        help_text="Sentensi 1-2 zinazoonekana chini ya kichwa kwenye Google.",
    )
    og_image = models.ImageField(
        upload_to="seo/", blank=True,
        verbose_name="Picha ya kushare",
        help_text="Inayoonekana link ikishirikishwa WhatsApp au Facebook. 1200x630px.",
    )

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Site settings
# ---------------------------------------------------------------------------

class SiteSettings(Singleton, SEOFields, TimeStamped):
    company_name = models.CharField(
        max_length=120, default="AMISH Company Limited",
        verbose_name="Jina la kampuni",
    )
    slogan = models.CharField(
        max_length=160, default="Your Success, Our Commitment",
        verbose_name="Slogan",
    )
    short_intro = models.TextField(
        blank=True,
        verbose_name="Utangulizi mfupi",
        help_text="Sentensi 2-3 zinazoelezea kampuni. Zinatumika footer na sehemu za utangulizi.",
    )

    logo = models.ImageField(
        upload_to="brand/", blank=True,
        verbose_name="Logo (background nyeupe)",
    )
    logo_light = models.ImageField(
        upload_to="brand/", blank=True,
        verbose_name="Logo ya background nyeusi",
    )
    favicon = models.ImageField(
        upload_to="brand/", blank=True,
        verbose_name="Favicon",
        help_text="Alama ndogo ya browser tab. 512x512px.",
    )

    # Rangi rasmi za kampuni
    color_primary = models.CharField(
        max_length=7, default="#142B6F",
        verbose_name="Rangi kuu (dark blue)",
    )
    color_ink = models.CharField(
        max_length=7, default="#000000",
        verbose_name="Rangi ya maandishi (black)",
    )
    color_surface = models.CharField(
        max_length=7, default="#FFFFFF",
        verbose_name="Rangi ya background (white)",
    )

    class Meta:
        verbose_name = "Mipangilio ya website"
        verbose_name_plural = "Mipangilio ya website"

    def __str__(self):
        return self.company_name

    def clean(self):
        for field in ("color_primary", "color_ink", "color_surface"):
            value = getattr(self, field, "")
            if value and not (value.startswith("#") and len(value) == 7):
                raise ValidationError({field: "Tumia muundo wa hex, mfano #142B6F"})


class ContactInfo(Singleton, TimeStamped):
    """Mawasiliano. Yanatumika header, footer, contact page na schema ya Google."""
    phone_primary = models.CharField(max_length=30, blank=True, verbose_name="Simu ya kwanza")
    phone_secondary = models.CharField(max_length=30, blank=True, verbose_name="Simu ya pili")
    whatsapp = models.CharField(
        max_length=30, blank=True,
        verbose_name="Namba ya WhatsApp",
        help_text="Muundo wa kimataifa bila alama, mfano 255628601130",
    )
    email = models.EmailField(blank=True, verbose_name="Email kuu")
    email_sales = models.EmailField(blank=True, verbose_name="Email ya mauzo")

    street = models.CharField(max_length=160, blank=True, verbose_name="Mtaa / jengo")
    ward = models.CharField(max_length=80, blank=True, default="Kigamboni", verbose_name="Kata")
    city = models.CharField(max_length=80, blank=True, default="Dar es Salaam", verbose_name="Jiji")
    postal_address = models.CharField(max_length=80, blank=True, verbose_name="S.L.P")

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude",
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude",
    )

    class Meta:
        verbose_name = "Mawasiliano"
        verbose_name_plural = "Mawasiliano"

    def __str__(self):
        return "Mawasiliano ya kampuni"

    @property
    def full_address(self):
        parts = [self.street, self.ward, self.city]
        return ", ".join(p for p in parts if p)

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.whatsapp}" if self.whatsapp else ""


class BusinessHour(Orderable):
    class Day(models.IntegerChoices):
        MONDAY = 1, "Jumatatu"
        TUESDAY = 2, "Jumanne"
        WEDNESDAY = 3, "Jumatano"
        THURSDAY = 4, "Alhamisi"
        FRIDAY = 5, "Ijumaa"
        SATURDAY = 6, "Jumamosi"
        SUNDAY = 7, "Jumapili"

    day = models.IntegerField(choices=Day.choices, unique=True, verbose_name="Siku")
    opens_at = models.TimeField(null=True, blank=True, verbose_name="Kufungua")
    closes_at = models.TimeField(null=True, blank=True, verbose_name="Kufunga")
    is_closed = models.BooleanField(default=False, verbose_name="Imefungwa siku hii")
    note = models.CharField(
        max_length=80, blank=True,
        verbose_name="Maelezo",
        help_text="Mfano: Nusu siku, au Kwa miadi tu.",
    )

    class Meta:
        ordering = ["day"]
        verbose_name = "Saa za kazi"
        verbose_name_plural = "Saa za kazi"

    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_display()}: Imefungwa"
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
        verbose_name="Jina la page",
        help_text="Mfano: AMISH Hardware",
    )
    url = models.URLField(verbose_name="Link")
    division = models.ForeignKey(
        "divisions.Division", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="social_links",
        verbose_name="Ni ya idara gani",
        help_text="Iache wazi kama ni page ya kampuni nzima.",
    )

    class Meta(Orderable.Meta):
        verbose_name = "Link ya social media"
        verbose_name_plural = "Links za social media"

    def __str__(self):
        return f"{self.get_platform_display()} — {self.handle or self.url}"


# ---------------------------------------------------------------------------
# Homepage content
# ---------------------------------------------------------------------------

class HeroSlide(Orderable):
    """Sehemu ya juu kabisa ya homepage."""
    headline = models.CharField(max_length=90, verbose_name="Kichwa kikubwa")
    subline = models.CharField(max_length=180, blank=True, verbose_name="Maelezo ya chini")
    image = models.ImageField(
        upload_to="hero/",
        verbose_name="Picha",
        help_text="Upana wa angalau 2000px, ubora mzuri.",
    )
    cta_label = models.CharField(max_length=40, blank=True, verbose_name="Maandishi ya kitufe")
    cta_url = models.CharField(max_length=200, blank=True, verbose_name="Link ya kitufe")

    class Meta(Orderable.Meta):
        verbose_name = "Slide ya homepage"
        verbose_name_plural = "Slides za homepage"

    def __str__(self):
        return self.headline


class Stat(Orderable):
    """Takwimu za kuonyesha uzoefu wa kampuni."""
    value = models.CharField(max_length=20, verbose_name="Namba", help_text="Mfano: 12, 500+, 98%")
    label = models.CharField(max_length=60, verbose_name="Maelezo", help_text="Mfano: Miaka ya uzoefu")

    class Meta(Orderable.Meta):
        verbose_name = "Takwimu"
        verbose_name_plural = "Takwimu"

    def __str__(self):
        return f"{self.value} {self.label}"


class Testimonial(Orderable):
    author = models.CharField(max_length=90, verbose_name="Jina la mteja")
    role = models.CharField(max_length=90, blank=True, verbose_name="Cheo au kampuni")
    quote = models.TextField(verbose_name="Alichosema")
    photo = models.ImageField(upload_to="testimonials/", blank=True, verbose_name="Picha")

    class Meta(Orderable.Meta):
        verbose_name = "Ushuhuda wa mteja"
        verbose_name_plural = "Ushuhuda wa wateja"

    def __str__(self):
        return self.author


class FAQ(Orderable):
    question = models.CharField(max_length=200, verbose_name="Swali")
    answer = models.TextField(verbose_name="Jibu")

    class Meta(Orderable.Meta):
        verbose_name = "Swali la mara kwa mara"
        verbose_name_plural = "Maswali ya mara kwa mara"

    def __str__(self):
        return self.question


# ---------------------------------------------------------------------------
# Kurasa za maandishi (Privacy, Terms, n.k.)
# ---------------------------------------------------------------------------

class Page(SEOFields, TimeStamped):
    title = models.CharField(max_length=120, verbose_name="Kichwa")
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    body = models.TextField(verbose_name="Maandishi")
    is_active = models.BooleanField(default=True, verbose_name="Inaonekana")

    class Meta:
        ordering = ["title"]
        verbose_name = "Ukurasa"
        verbose_name_plural = "Kurasa"

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
        NEW = "new", "Mpya"
        IN_PROGRESS = "in_progress", "Inashughulikiwa"
        CLOSED = "closed", "Imekamilika"

    name = models.CharField(max_length=90, verbose_name="Jina")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Simu")
    email = models.EmailField(blank=True, verbose_name="Email")
    subject = models.CharField(max_length=140, blank=True, verbose_name="Mada")
    message = models.TextField(verbose_name="Ujumbe")

    division = models.ForeignKey(
        "divisions.Division", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="enquiries",
        verbose_name="Idara husika",
    )
    product = models.ForeignKey(
        "divisions.Product", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="enquiries",
        verbose_name="Bidhaa husika",
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Hali",
    )
    internal_note = models.TextField(blank=True, verbose_name="Maelezo ya ndani")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ujumbe wa mteja"
        verbose_name_plural = "Ujumbe wa wateja"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d/%m/%Y}"


class SectionSlide(Orderable):
    """Picha za nyuma zinazobadilika kwenye sehemu maalum za ukurasa."""

    class Slot(models.TextChoices):
        BAND = "band", "Ukanda wa Vision na Mission"

    slot = models.CharField(
        max_length=20, choices=Slot.choices, default=Slot.BAND, verbose_name="Sehemu",
    )
    image = models.ImageField(upload_to="sections/", verbose_name="Picha")
    caption = models.CharField(max_length=120, blank=True, verbose_name="Maelezo ya ndani")

    class Meta(Orderable.Meta):
        verbose_name = "Picha ya nyuma"
        verbose_name_plural = "Picha za nyuma"

    def __str__(self):
        return f"{self.get_slot_display()} — {self.order}"


class Reason(Orderable):
    """Sababu za kununua AMISH — sehemu ya "Kwa nini AMISH" homepage."""

    title = models.CharField(max_length=70, verbose_name="Kichwa")
    description = models.TextField(verbose_name="Maelezo")

    class Meta(Orderable.Meta):
        verbose_name = "Sababu ya kununua hapa"
        verbose_name_plural = "Kwa nini AMISH"

    def __str__(self):
        return self.title
