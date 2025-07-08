# flake8: noqa
from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:id>/", views.add, name="add"),
    path("addall/", views.addall, name="addall"),
    path("viewall/", views.view_all_batches, name="view_all_batches"),
    path("batch/<int:id>/", views.view_batch, name="view_batch"),
    path("data/<int:id>/", views.data, name="data"),
]
