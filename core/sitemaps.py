from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from divisions.models import Division, Product

from .models import Page


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["core:home", "core:about", "core:contact", "core:gallery"]

    def location(self, item):
        return reverse(item)


class DivisionSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Division.objects.filter(is_active=True)


class ProductSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(is_active=True, division__is_active=True)


class PageSitemap(Sitemap):
    priority = 0.3

    def items(self):
        return Page.objects.filter(is_active=True)

    def location(self, item):
        return reverse("core:page", kwargs={"slug": item.slug})


SITEMAPS = {
    "static": StaticSitemap,
    "divisions": DivisionSitemap,
    "products": ProductSitemap,
    "pages": PageSitemap,
}
