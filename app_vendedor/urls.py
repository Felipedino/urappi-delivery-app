from django.urls import path

from . import views

app_name = 'app_vendedor'
urlpatterns = [
    path("mystore/", views.show_my_store, name="show_my_store"),
    path("add_product/", views.addNewProduct, name="addNewProduct"),
    path("editarProducto/<int:productID>/", views.editProduct, name="editProduct"),
    path("editStore/", views.editStore, name="editStore"),
]