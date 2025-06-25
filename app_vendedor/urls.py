from django.urls import path

from . import views


urlpatterns = [
    path("mystore/", views.show_my_store, name="mystore"),
]