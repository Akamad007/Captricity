# flake8: noqa
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("edit/<int:id>/", views.create, name="edit"),
]
