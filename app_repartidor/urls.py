from django.contrib import admin
from django.urls import path
from . import views

# Agregamos los urls de las vistas dentro de la lógica repartidor.
app_name = 'app_repartidor'
urlpatterns = [
    path('deliverer/', views.repartidor_perfil, name='repartidor_perfil'),
    path('accepted-order/', views.accepted_order, name='accepted_order'),
    path('order_selected/<str:order_id>/', views.order_details, name='order_selected'),
    path('estado_order/<str:order_id>/', views.estado_order, name='estado_order'),
    path('delivery-action/', views.delivery_action, name='delivery_action'),




]