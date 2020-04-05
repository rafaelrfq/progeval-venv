from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registrar_usuario.urls')),
    path('', include('progeval.urls')),
     url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
]
