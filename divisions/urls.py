from django.urls import path

from . import views

app_name = "divisions"

urlpatterns = [
    path("divisions/", views.division_list, name="list"),
    path("divisions/<slug:slug>/", views.division_detail, name="detail"),
    path("divisions/<slug:division_slug>/<slug:slug>/", views.product_detail, name="product"),
]
