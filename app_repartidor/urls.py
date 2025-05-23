from django.contrib import admin
from django.urls import path
from . import views
import views 


urlpatterns = [
    path('repartidor/', views.repartidor_perfil, name='repartidor_perfil'),
]