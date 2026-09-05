"""
divisions/models.py — AMISH Company Limited

Division ndiyo kiini cha website. AMISH ni kampuni mama yenye matawi:
Hardware na Nguo zipo hewani, na migahawa, usafiri na furniture zinakuja.

Kuongeza tawi jipya ni kuongeza record moja kwenye admin. Tawi lililo
"linakuja" linaonekana kama teaser; likianza kufanya kazi, unabadilisha
status peke yake na kurasa zake zote zinafunguka.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import Orderable, SEOFields, TimeStamped


class Division(Orderable, SEOFields, TimeStamped):
    class Status(models.TextChoices):
        ACTIVE = "active", "Inafanya kazi"
        COMING_SOON = "coming_soon", "Inakuja hivi karibuni"

    class Kind(models.TextChoices):
        PRODUCTS = "products", "Inauza bidhaa"
        SERVICES = "services", "Inatoa huduma"

    name = models.CharField(max_length=90, verbose_name="Jina la tawi")
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    tagline = models.CharField(
        max_length=140, blank=True,
        verbose_name="Maelezo ya mstari mmoja",
        help_text="Mfano: Vifaa vya ujenzi vya kuaminika kwa bei ya jumla.",
    )
    description = models.TextField(blank=True, verbose_name="Maelezo kamili")

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE,
        verbose_name="Hali",
        help_text="Ikiwa 'inakuja', tawi linaonekana lakini bidhaa zake hazionyeshwi.",
    )
    kind = models.CharField(
        max_length=20, choices=Kind.choices, default=Kind.PRODUCTS,
        verbose_name="Aina",
    )
    launch_note = models.CharField(
        max_length=90, blank=True,
        verbose_name="Lini linaanza",
        help_text="Kinachoonekana kwenye tawi linalokuja. Mfano: Inatarajiwa 2027.",
    )

    icon = models.ImageField(upload_to="divisions/icons/", blank=True, verbose_name="Ikoni")
    cover = models.ImageField(
        upload_to="divisions/", blank=True,
        verbose_name="Picha kubwa",
        help_text="Inayoonekana juu ya ukurasa wa tawi. Upana wa angalau 1600px.",
    )
    accent_color = models.CharField(
        max_length=7, blank=True,
        verbose_name="Rangi ya tawi",
        help_text="Iache wazi ili itumie rangi kuu ya kampuni.",
    )

    class Meta(Orderable.Meta):
        verbose_name = "Tawi la kampuni"
        verbose_name_plural = "Matawi ya kampuni"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("divisions:detail", kwargs={"slug": self.slug})

    @property
    def is_live(self):
        return self.status == self.Status.ACTIVE

    @property
    def sitemap_images(self):
        urls = []
        if self.cover:
            urls.append(self.cover.url)
        urls += [s.image.url for s in self.slides.filter(is_active=True)]
        return urls


class Category(Orderable, TimeStamped):
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="categories",
        verbose_name="Tawi",
    )
    name = models.CharField(max_length=90, verbose_name="Jina la kundi")
    slug = models.SlugField(max_length=110, blank=True)
    description = models.CharField(max_length=200, blank=True, verbose_name="Maelezo mafupi")
    image = models.ImageField(upload_to="categories/", blank=True, verbose_name="Picha")

    class Meta(Orderable.Meta):
        unique_together = [("division", "slug")]
        verbose_name = "Kundi la bidhaa"
        verbose_name_plural = "Makundi ya bidhaa"

    def __str__(self):
        return f"{self.division.name} — {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(Orderable, SEOFields, TimeStamped):
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="products", verbose_name="Tawi",
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="products", verbose_name="Kundi",
    )

    name = models.CharField(max_length=140, verbose_name="Jina la bidhaa")
    slug = models.SlugField(max_length=160, blank=True)
    summary = models.CharField(max_length=200, blank=True, verbose_name="Maelezo mafupi")
    description = models.TextField(blank=True, verbose_name="Maelezo kamili")
    image = models.ImageField(upload_to="products/", blank=True, verbose_name="Picha kuu")

    price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Bei (TSh)",
    )
    show_price = models.BooleanField(
        default=False,
        verbose_name="Onyesha bei kwenye website",
        help_text="Ikizimwa, mteja anaona kitufe cha kuuliza bei badala ya namba.",
    )
    unit = models.CharField(
        max_length=30, blank=True,
        verbose_name="Kipimo", help_text="Mfano: kwa mfuko, kwa mita, kwa kipande.",
    )
    in_stock = models.BooleanField(default=True, verbose_name="Ipo dukani")
    is_featured = models.BooleanField(default=False, verbose_name="Ionekane homepage")

    class Meta(Orderable.Meta):
        unique_together = [("division", "slug")]
        verbose_name = "Bidhaa"
        verbose_name_plural = "Bidhaa"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "divisions:product",
            kwargs={"division_slug": self.division.slug, "slug": self.slug},
        )

    @property
    def sitemap_images(self):
        urls = [self.image.url] if self.image else []
        urls += [i.image.url for i in self.images.filter(is_active=True)]
        return urls


class ProductImage(Orderable):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Bidhaa",
    )
    image = models.ImageField(upload_to="products/gallery/", verbose_name="Picha")
    caption = models.CharField(max_length=120, blank=True, verbose_name="Maelezo")

    class Meta(Orderable.Meta):
        verbose_name = "Picha ya ziada"
        verbose_name_plural = "Picha za ziada"

    def __str__(self):
        return f"{self.product.name} — picha {self.order}"


class Service(Orderable, TimeStamped):
    """Kwa matawi yanayotoa huduma badala ya bidhaa, mfano usafiri."""
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="services", verbose_name="Tawi",
    )
    name = models.CharField(max_length=120, verbose_name="Jina la huduma")
    summary = models.CharField(max_length=200, blank=True, verbose_name="Maelezo mafupi")
    description = models.TextField(blank=True, verbose_name="Maelezo kamili")
    icon = models.ImageField(upload_to="services/", blank=True, verbose_name="Ikoni")

    class Meta(Orderable.Meta):
        verbose_name = "Huduma"
        verbose_name_plural = "Huduma"

    def __str__(self):
        return self.name


class GalleryImage(Orderable):
    division = models.ForeignKey(
        Division, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="gallery", verbose_name="Tawi",
        help_text="Iache wazi kama ni picha ya kampuni kwa ujumla.",
    )
    image = models.ImageField(upload_to="gallery/", verbose_name="Picha")
    caption = models.CharField(max_length=140, blank=True, verbose_name="Maelezo")

    class Meta(Orderable.Meta):
        verbose_name = "Picha ya gallery"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return self.caption or f"Picha {self.pk}"


class DivisionImage(Orderable):
    """Picha zinazopita kwenye paneli ya tawi kwenye homepage."""

    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="slides", verbose_name="Tawi",
    )
    image = models.ImageField(upload_to="divisions/slides/", verbose_name="Picha")
    caption = models.CharField(max_length=120, blank=True, verbose_name="Maelezo")

    class Meta(Orderable.Meta):
        verbose_name = "Picha ya paneli"
        verbose_name_plural = "Picha za paneli"

    def __str__(self):
        return f"{self.division.name} — slide {self.order}"
