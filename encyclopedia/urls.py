from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    # Homepage
    path("", views.index, name="index"),

    # For viewing detailed entry
    path("wiki/<str:title>/", views.entry, name="entry"),
]
