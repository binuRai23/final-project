
from django.contrib import admin
from django.urls import path,include
from knox import views as knox_views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Djangoapp.urls')),
    path('api/auth/',include('knox.urls')),
   
    path('logout/',knox_views.LogoutView.as_view(),name='knox_logout'),
    path('api/password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset')),
]
 
