from django.urls import path
from . import views


urlpatterns = [
    path("stores/", views.show_listado_tiendas, name='stores'),
    path("storeMenu/<int:id>/", views.show_store_menu, name="show_store_menu"),
]