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
        verbose_name="Utangulizi",
        help_text="Aya moja au mbili za kuanzia ukurasa wa About.",
    )
    story = models.TextField(blank=True, verbose_name="Historia ya kampuni")
    story_image = models.ImageField(upload_to="about/", blank=True, verbose_name="Picha")

    vision_en = models.TextField(blank=True, verbose_name="Vision (English)")
    vision_sw = models.TextField(blank=True, verbose_name="Vision (Kiswahili)")
    mission_en = models.TextField(blank=True, verbose_name="Mission (English)")
    mission_sw = models.TextField(blank=True, verbose_name="Mission (Kiswahili)")

    class Meta:
        verbose_name = "Kuhusu kampuni"
        verbose_name_plural = "Kuhusu kampuni"

    def __str__(self):
        return "Kuhusu kampuni"


class CoreValue(Orderable):
    title = models.CharField(
        max_length=60, verbose_name="Thamani",
        help_text="Mfano: Integrity, Accountability.",
    )
    description = models.TextField(verbose_name="Maelezo")
    icon = models.ImageField(upload_to="values/", blank=True, verbose_name="Ikoni")

    class Meta(Orderable.Meta):
        verbose_name = "Thamani ya kampuni"
        verbose_name_plural = "Thamani za kampuni"

    def __str__(self):
        return self.title


class Milestone(Orderable):
    year = models.CharField(max_length=12, verbose_name="Mwaka")
    title = models.CharField(max_length=120, verbose_name="Kilichotokea")
    description = models.TextField(blank=True, verbose_name="Maelezo")

    class Meta(Orderable.Meta):
        verbose_name = "Hatua ya kihistoria"
        verbose_name_plural = "Historia kwa miaka"

    def __str__(self):
        return f"{self.year} — {self.title}"


class Person(Orderable, TimeStamped):
    """Wakurugenzi na timu. Hii hii ndiyo inatumika kwenye business cards."""

    full_name = models.CharField(max_length=120, verbose_name="Jina kamili")
    position = models.CharField(max_length=90, verbose_name="Cheo")
    bio = models.TextField(blank=True, verbose_name="Wasifu mfupi")
    photo = models.ImageField(upload_to="team/", blank=True, verbose_name="Picha")

    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Simu")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")

    is_director = models.BooleanField(default=False, verbose_name="Ni mkurugenzi")
    show_on_website = models.BooleanField(default=True, verbose_name="Aonekane kwenye website")
    on_business_card = models.BooleanField(default=False, verbose_name="Ana business card")

    class Meta(Orderable.Meta):
        verbose_name = "Mtu wa kampuni"
        verbose_name_plural = "Timu na wakurugenzi"

    def __str__(self):
        return f"{self.full_name} — {self.position}"


class Credential(Orderable):
    """BRELA, TIN, leseni na vyeti vingine."""

    class Kind(models.TextChoices):
        REGISTRATION = "registration", "Usajili (BRELA)"
        TIN = "tin", "TIN"
        LICENCE = "licence", "Leseni"
        CERTIFICATE = "certificate", "Cheti"

    kind = models.CharField(max_length=20, choices=Kind.choices, verbose_name="Aina")
    label = models.CharField(max_length=90, verbose_name="Jina")
    number = models.CharField(max_length=60, blank=True, verbose_name="Namba")
    issued_on = models.DateField(null=True, blank=True, verbose_name="Ilitolewa tarehe")
    document = models.FileField(upload_to="credentials/", blank=True, verbose_name="Faili")
    show_on_website = models.BooleanField(
        default=False,
        verbose_name="Ionekane kwenye website",
        help_text="Namba za usajili mara nyingi huwekwa footer tu.",
    )

    class Meta(Orderable.Meta):
        verbose_name = "Cheti au usajili"
        verbose_name_plural = "Vyeti na usajili"

    def __str__(self):
        return f"{self.label} {self.number}".strip()


class Client(Orderable):
    name = models.CharField(max_length=120, verbose_name="Jina la mteja")
    logo = models.ImageField(upload_to="clients/", blank=True, verbose_name="Logo")
    website = models.URLField(blank=True, verbose_name="Website")

    class Meta(Orderable.Meta):
        verbose_name = "Mteja au mshirika"
        verbose_name_plural = "Wateja na washirika"

    def __str__(self):
        return self.name
