from django.urls import path

from machine import views

urlpatterns = [
    path("inventory", views.inventory_list),
]