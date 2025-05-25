from django.contrib import admin
from django.urls import path
from . import views

app_name = 'app_repartidor'
urlpatterns = [
    path('deliverer/', views.repartidor_perfil, name='repartidor_perfil'),
    path('accepted-order/', views.accepted_order, name='accepted_order'),
    path('order_selected/', views.order_details, name='order_selected'),


]