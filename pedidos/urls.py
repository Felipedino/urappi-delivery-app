from django.urls import path

from . import views

urlpatterns = [
    path("stores/", views.show_listado_tiendas, name="stores"),
    path("storeMenu/<int:id>/", views.show_store_menu, name="show_store_menu"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("cart", views.show_cart, name="cart"),
    path(
        "remove_from_cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "update_cart/<int:item_id>/<str:action>/", views.update_cart, name="update_cart"
    ),
]
