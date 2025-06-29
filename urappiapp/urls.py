from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register_user, name="register_user"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("comprador/", views.comprador, name="comprador"),
    path("repartidor/", views.repartidor_perfil, name="repartidor"),
    path("vendedor/", views.vendedor, name="vendedor"),
    path("profile/", views.profile, name="profile"),
    path("recharge_upuntos/", views.recharge_upuntos, name="recharge_upuntos"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
