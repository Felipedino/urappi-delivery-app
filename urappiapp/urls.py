from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.register_user, name='register_user'),
    path('login',views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
   
    path('comprador/', views.comprador, name='comprador'),
    path('repartidor/', views.repartidor_perfil, name='repartidor'),  
    path('vendedor/', views.vendedor, name='vendedor'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)