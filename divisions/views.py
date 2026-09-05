from django.shortcuts import get_object_or_404, redirect, render

from core.forms import EnquiryForm
from core.views import _handle_enquiry

from .models import Category, Division, Product


def division_list(request):
    divisions = Division.objects.filter(is_active=True)
    return render(request, "pages/division_list.html", {
        "live_divisions": [d for d in divisions if d.is_live],
        "upcoming": [d for d in divisions if not d.is_live],
    })


def division_detail(request, slug):
    division = get_object_or_404(Division, slug=slug, is_active=True)

    products = Product.objects.filter(
        division=division, is_active=True
    ).select_related("category")

    active_category = None
    category_slug = request.GET.get("category")
    if category_slug:
        active_category = Category.objects.filter(
            division=division, slug=category_slug, is_active=True
        ).first()
        if active_category:
            products = products.filter(category=active_category)

    return render(request, "pages/division_detail.html", {
        "division": division,
        "categories": division.categories.filter(is_active=True),
        "active_category": active_category,
        "products": products,
        "services": division.services.filter(is_active=True),
        "gallery": division.gallery.filter(is_active=True)[:12],
        "slides": division.slides.filter(is_active=True),
        "form": EnquiryForm(initial={"division": division}),
    })


def product_detail(request, division_slug, slug):
    product = get_object_or_404(
        Product.objects.select_related("division", "category"),
        slug=slug, division__slug=division_slug, is_active=True,
    )

    form = EnquiryForm(initial={
        "division": product.division,
        "product": product,
        "subject": f"Uliza kuhusu {product.name}",
    })
    if request.method == "POST":
        response, posted = _handle_enquiry(request, product.get_absolute_url())
        if response:
            return response
        form = posted

    related = Product.objects.filter(
        division=product.division, is_active=True
    ).exclude(pk=product.pk)[:4]

    return render(request, "pages/product_detail.html", {
        "product": product,
        "division": product.division,
        "related": related,
        "form": form,
    })
