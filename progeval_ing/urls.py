from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registrar_usuario.urls')),
    path('', include('progeval.urls')),
]
