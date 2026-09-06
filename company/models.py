"""
company/models.py — AMISH Company Limited

Kila kitu kinachoingia kwenye ukurasa wa About na kwenye company profile
kinatoka hapa. Ukibadilisha hapa, PDF ya company profile pia inabadilika.
"""

from django.db import models

from core.models import Orderable, SEOFields, Singleton, TimeStamped


class About(Singleton, SEOFields, TimeStamped):
    intro = models.TextField(
        blank=True,
        verbose_name="Introduction",
        help_text="One or two opening paragraphs for the About page.",
    )
    story = models.TextField(blank=True, verbose_name="Company story")
    story_image = models.ImageField(upload_to="about/", blank=True, verbose_name="Photo")

    vision_en = models.TextField(blank=True, verbose_name="Vision (English)")
    vision_sw = models.TextField(blank=True, verbose_name="Vision (Kiswahili)")
    mission_en = models.TextField(blank=True, verbose_name="Mission (English)")
    mission_sw = models.TextField(blank=True, verbose_name="Mission (Kiswahili)")

    class Meta:
        verbose_name = "About the company"
        verbose_name_plural = "About the company"

    def __str__(self):
        return "About the company"


class CoreValue(Orderable):
    title = models.CharField(
        max_length=60, verbose_name="Value",
        help_text="For example: Integrity, Accountability.",
    )
    description = models.TextField(verbose_name="Description")
    icon = models.ImageField(upload_to="values/", blank=True, verbose_name="Icon")

    class Meta(Orderable.Meta):
        verbose_name = "Core value"
        verbose_name_plural = "Core values"

    def __str__(self):
        return self.title


class Milestone(Orderable):
    year = models.CharField(max_length=12, verbose_name="Year")
    title = models.CharField(max_length=120, verbose_name="What happened")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta(Orderable.Meta):
        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"

    def __str__(self):
        return f"{self.year} — {self.title}"


class Person(Orderable, TimeStamped):
    """Directors and team. The same record is used for the business cards."""

    full_name = models.CharField(max_length=120, verbose_name="Full name")
    position = models.CharField(max_length=90, verbose_name="Position")
    bio = models.TextField(blank=True, verbose_name="Short biography")
    photo = models.ImageField(upload_to="team/", blank=True, verbose_name="Photo")

    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")

    is_director = models.BooleanField(default=False, verbose_name="Is a director")
    show_on_website = models.BooleanField(default=True, verbose_name="Show on the website")
    on_business_card = models.BooleanField(default=False, verbose_name="Has a business card")

    class Meta(Orderable.Meta):
        verbose_name = "Person"
        verbose_name_plural = "Team and directors"

    def __str__(self):
        return f"{self.full_name} — {self.position}"


class Credential(Orderable):
    """BRELA, TIN, licences and other certificates."""

    class Kind(models.TextChoices):
        REGISTRATION = "registration", "Business registration (BRELA)"
        TIN = "tin", "TIN"
        LICENCE = "licence", "Licence"
        CERTIFICATE = "certificate", "Certificate"

    kind = models.CharField(max_length=20, choices=Kind.choices, verbose_name="Type")
    label = models.CharField(max_length=90, verbose_name="Label")
    number = models.CharField(max_length=60, blank=True, verbose_name="Number")
    issued_on = models.DateField(null=True, blank=True, verbose_name="Issued on")
    document = models.FileField(upload_to="credentials/", blank=True, verbose_name="Document")
    show_on_website = models.BooleanField(
        default=False,
        verbose_name="Show on the website",
        help_text="Registration numbers are usually shown in the footer only.",
    )

    class Meta(Orderable.Meta):
        verbose_name = "Registration or certificate"
        verbose_name_plural = "Registration and certificates"

    def __str__(self):
        return f"{self.label} {self.number}".strip()


class Client(Orderable):
    name = models.CharField(max_length=120, verbose_name="Client name")
    logo = models.ImageField(upload_to="clients/", blank=True, verbose_name="Logo")
    website = models.URLField(blank=True, verbose_name="Website")

    class Meta(Orderable.Meta):
        verbose_name = "Client or partner"
        verbose_name_plural = "Clients and partners"

    def __str__(self):
        return self.name
