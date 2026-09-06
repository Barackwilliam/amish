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
        ACTIVE = "active", "Trading"
        COMING_SOON = "coming_soon", "In preparation"

    class Kind(models.TextChoices):
        PRODUCTS = "products", "Sells products"
        SERVICES = "services", "Provides services"

    name = models.CharField(max_length=90, verbose_name="Division name")
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    tagline = models.CharField(
        max_length=140, blank=True,
        verbose_name="One-line description",
        help_text="For example: Reliable building materials at wholesale prices.",
    )
    description = models.TextField(blank=True, verbose_name="Full description")

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE,
        verbose_name="Status",
        help_text="If set to 'In preparation', the division is listed but its products are hidden.",
    )
    kind = models.CharField(
        max_length=20, choices=Kind.choices, default=Kind.PRODUCTS,
        verbose_name="Type",
    )
    launch_note = models.CharField(
        max_length=90, blank=True,
        verbose_name="Launch note",
        help_text="Shown on a division in preparation. For example: Expected 2027.",
    )

    icon = models.ImageField(upload_to="divisions/icons/", blank=True, verbose_name="Icon")
    cover = models.ImageField(
        upload_to="divisions/", blank=True,
        verbose_name="Cover image",
        help_text="Shown at the top of the division page. At least 1600px wide.",
    )
    accent_color = models.CharField(
        max_length=7, blank=True,
        verbose_name="Division colour",
        help_text="Leave blank to use the company primary colour.",
    )

    class Meta(Orderable.Meta):
        verbose_name = "Division"
        verbose_name_plural = "Divisions"

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
        verbose_name="Division",
    )
    name = models.CharField(max_length=90, verbose_name="Category name")
    slug = models.SlugField(max_length=110, blank=True)
    description = models.CharField(max_length=200, blank=True, verbose_name="Short description")
    image = models.ImageField(upload_to="categories/", blank=True, verbose_name="Image")

    class Meta(Orderable.Meta):
        unique_together = [("division", "slug")]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.division.name} — {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(Orderable, SEOFields, TimeStamped):
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="products", verbose_name="Division",
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="products", verbose_name="Category",
    )

    name = models.CharField(max_length=140, verbose_name="Product name")
    slug = models.SlugField(max_length=160, blank=True)
    summary = models.CharField(max_length=200, blank=True, verbose_name="Short description")
    description = models.TextField(blank=True, verbose_name="Full description")
    image = models.ImageField(upload_to="products/", blank=True, verbose_name="Main photo")

    price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Price (TSh)",
    )
    show_price = models.BooleanField(
        default=False,
        verbose_name="Show price on the website",
        help_text="When off, customers see an 'Ask for price' link instead of a figure.",
    )
    unit = models.CharField(
        max_length=30, blank=True,
        verbose_name="Unit", help_text="For example: per bag, per metre, per piece.",
    )
    in_stock = models.BooleanField(default=True, verbose_name="In stock")
    is_featured = models.BooleanField(default=False, verbose_name="Feature on the home page")

    class Meta(Orderable.Meta):
        unique_together = [("division", "slug")]
        verbose_name = "Product"
        verbose_name_plural = "Products"

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
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Product",
    )
    image = models.ImageField(upload_to="products/gallery/", verbose_name="Image")
    caption = models.CharField(max_length=120, blank=True, verbose_name="Caption")

    class Meta(Orderable.Meta):
        verbose_name = "Extra photo"
        verbose_name_plural = "Extra photos"

    def __str__(self):
        return f"{self.product.name} — photo {self.order}"


class Service(Orderable, TimeStamped):
    """Kwa matawi yanayotoa huduma badala ya bidhaa, mfano usafiri."""
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="services", verbose_name="Division",
    )
    name = models.CharField(max_length=120, verbose_name="Service name")
    summary = models.CharField(max_length=200, blank=True, verbose_name="Short description")
    description = models.TextField(blank=True, verbose_name="Full description")
    icon = models.ImageField(upload_to="services/", blank=True, verbose_name="Icon")

    class Meta(Orderable.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


class GalleryImage(Orderable):
    division = models.ForeignKey(
        Division, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="gallery", verbose_name="Division",
        help_text="Iache wazi kama ni picha ya kampuni kwa ujumla.",
    )
    image = models.ImageField(upload_to="gallery/", verbose_name="Image")
    caption = models.CharField(max_length=140, blank=True, verbose_name="Caption")

    class Meta(Orderable.Meta):
        verbose_name = "Gallery photo"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return self.caption or f"Photo {self.pk}"


class DivisionImage(Orderable):
    """Picha zinazopita kwenye paneli ya tawi kwenye homepage."""

    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="slides", verbose_name="Division",
    )
    image = models.ImageField(upload_to="divisions/slides/", verbose_name="Image")
    caption = models.CharField(max_length=120, blank=True, verbose_name="Caption")

    class Meta(Orderable.Meta):
        verbose_name = "Panel photo"
        verbose_name_plural = "Panel photos"

    def __str__(self):
        return f"{self.division.name} — slide {self.order}"
