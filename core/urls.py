from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.inicio, name="login"),
    path("salir/", views.salir, name="logout"),
    path("registro-egresado/", views.registro, name="registro-egresado"),
    path("registro-administrativo/", views.registro, name="registro-administrativo"),
    path("perfil/<int:id>", views.perfil, name="perfil"),
    path("informacion-basica/<int:id>", views.infoBasica, name="info-basica"),
    path("formacionUPN/", views.formacionUPN, name="formacionUPN"),
    path('get_programas', views.get_programas, name='get_programas'),
]
