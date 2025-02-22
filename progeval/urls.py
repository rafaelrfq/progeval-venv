from django.urls import path,include
from . import views

urlpatterns = [
    #home and profile
    path('', include('registrar_usuario.urls')), #include all urls of registrar_usuario app
    path('profile/', views.profile, name='profile'), #user profile
    path('coord_home/', views.coord_home, name='coord_home'), #home for coordinators
    path('jurado_home/', views.jurado_home, name='jurado_home'), #home for jury
    #programacion
    path('coord/programacion/', views.programacion, name='coord_prog'), #program presentation
    path('coord/programacion/<int:id>/', views.programacion, name='prog_update'), #edit existing program
    path('coord/programacion/delete/<int:id>/', views.delete_prog, name='prog_delete'), #delete existing
    path('coord/programacion/listar', views.listar_prog, name='prog_list'), #program listing
    #evaluaciones
    path('coord/prog_evaluadas', views.listar_prog_eval, name='coord_prog_eval'), #prog eval listing
    path('coord/evaluaciones', views.listar_eval_coord, name='coord_eval_list'), #evaluation listing
    #proyecto
    path('coord/proyecto', views.insertar_proyecto, name='coord_proyecto'), #project creation
    path('coord/proyecto/<int:id>/', views.insertar_proyecto, name='proyecto_update'), #edit existing project
    path('coord/proyecto/delete/<int:id>/', views.delete_proyecto, name='proyecto_delete'), #delete existing
    path('coord/proyecto/listar', views.listar_proyecto, name='proyecto_list'), #project listing
    #clasificacion
    path('coord/proyecto/clasificacion', views.insertar_clasificacion, name='proyecto_clasif'), #project listing
    path('coord/proyecto/clasificacion/<int:id>/', views.insertar_clasificacion, name='clasif_update'), #project listing
    path('coord/proyecto/clasificacion/delete/<int:id>/', views.delete_clasif, name='clasif_delete'), #delete existing
    path('coord/proyecto/clasificacion/listar', views.listar_clasificacion, name='clasif_list'), #project listing
    #estudiante
    path('coord/estudiante', views.insertar_estudiante, name='coord_estudiante'), #student creation
    path('coord/estudiante/<int:id>/', views.insertar_estudiante, name='estudiante_update'), #edit existing student
    path('coord/estudiante/delete/<int:id>/', views.delete_estudiante, name='estudiante_delete'), #delete existing
    path('coord/estudiante/listar', views.listar_estudiante, name='estudiante_list'), #student listing
    # clase
    path('coord/clase', views.insertar_clase, name='coord_clase'), #class creation
    path('coord/clase/<int:id>/', views.insertar_clase, name='clase_update'), #edit existing class
    path('coord/clase/delete/<int:id>/', views.delete_clase, name='clase_delete'), #delete existing class
    path('coord/clase/listar', views.listar_clase, name='clase_list'), #class listing
    #carrera
    path('coord/carrera', views.insertar_carrera, name='coord_carrera'), #career creation
    path('coord/carrera/<int:id>/', views.insertar_carrera, name='carrera_update'), #edit existing career
    path('coord/carrera/delete/<int:id>/', views.delete_carrera, name='carrera_delete'), #delete existing career
    path('coord/carrera/listar', views.listar_carrera, name='carrera_list'), #career listing
    #rubrica
    path('coord/rubrica', views.insertar_rubrica, name='coord_rub'), #rubrica creation
    path('coord/rubrica/<int:id>/', views.insertar_rubrica, name='rubrica_update'), #edit existing
    path('coord/rubrica/delete/<int:id>/', views.delete_rub, name='rubrica_delete'), #delete existing
    path('coord/rubrica/listar', views.listar_rubrica, name='rubrica_list'), #rubrica listing
    #item
    path('coord/rubrica/item', views.insertar_item, name='coord_rubitem'), #item creation
    path('coord/rubrica/item/<int:id>/', views.insertar_item, name='item_update'), #edit existing item
    path('coord/rubrica/item/delete/<int:id>/', views.delete_item, name='item_delete'), #delete existing
    path('coord/rubrica/item/listar', views.listar_item, name='item_list'), #item listing
    #paths del jurado
    path('jurado/eval_disp', views.evaluaciones_disp, name='eval_disp'), #available evaluations
    path('jurado/evaluacion/<int:id>/', views.evaluacion, name='evaluacion'), #evaluation
    path('jurado/evaluacion_r/<int:id>/', views.evaluacion_reporte, name='evaluacion_reporte'), #report evaluation
    path('jurado/evaluacion/listar', views.listar_evaluacion, name='eval_list'), #evaluation
    path('jurado/evaluacion/ficha/<int:id>', views.ficha_evaluacion, name='eval_ficha'), #evaluation
    #path de PDF
    path('jurado/evaluacion/listar/pdf/<int:id>/', views.GeneratePdf.as_view(), name='pdf_view'), #pdf ficha evaluacion

]