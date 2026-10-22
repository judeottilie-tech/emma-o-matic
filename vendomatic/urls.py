from django.urls import path

from machine import views

urlpatterns = [
    path("inventory", views.inventory_list),
    path("inventory/<int:item_id>", views.inventory_item),
    path("", views.handle_coins),
]
