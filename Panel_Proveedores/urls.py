# Panel_Proveedores/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proveedores, name='lista_proveedores'),
    path('fragment/', views.lista_proveedores_fragment, name='lista_proveedores_fragment'),
]
