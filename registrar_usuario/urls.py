from django.urls import path,include, re_path
from . import views

urlpatterns = [
    path('', views.user_login, name='usuario_login'), #login to app
    path('registro/', views.first_user, name='first_user'), #first user registration to app
    path('logout/', views.user_logout, name='usuario_logout'), #login to app
    path('usuario/registrar/', views.usuario_register, name='usuario_insert'), #get data to register a new user
    path('usuario/registrar/<int:id>/', views.usuario_update, name='usuario_update'), #edit existing user
    path('delete/<int:id>/', views.user_delete, name='usuario_delete'), #delete an existing user
    path('usuario/listar/', views.user_list, name='usuario_list') #retrieve registered users in db
]