"""
URL configuration for DulceríaLilis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Dulceria import views
from Panel_Productos.views import productosAdd,categoriasAdd,unidadesAdd,mostrarCategorias,cargarCategorias,modificarCategorias,mostrarUnidades,cargarUnidades,modificarUnidades,mostrarProductos,cargarProductos,modificarProductos

urlpatterns = [
    path('admin/', admin.site.urls),

    path('historia-empresa/',views.historia_empresa, name="historia-empresa"),
    path('rrss/', views.rrss, name='rrss'),
    path('',views.catalogo, name="catalogo"),
    path('catalogo/<str:categoria>/',views.subcatalogo, name="subcatalogo"),
    path('catalogo/<str:categoria>/<str:nombreProducto>/',views.detalle, name="detalle_producto"),
    path('gestion-producto/',productosAdd,name="gestion-producto"),
    path('gestion-categoria/',categoriasAdd,name="gestion-categoria"),
    path('gestion-unidad-medida/',unidadesAdd,name="gestion-unidad-medida"),
    path('categorias/',mostrarCategorias,name="categorias"),
    path('categoria-load/<int:categoria_id>',cargarCategorias,name='categoria-load'),
    path('categoria-modificada/<int:categoria_id>',modificarCategorias,name='categoria-modificada'),
    path('unidades-medidas/',mostrarUnidades,name="unidades-medida"),
    path('unidad-medida-load/<int:unidad_medida_id>',cargarUnidades,name='unidad-medida-load'),
    path('unidad-medida-modificada/<int:unidad_medida_id>',modificarUnidades,name='unidad-medida-modificada'),
    path('productos/',mostrarProductos,name="productos"),
    path('producto-load/<int:producto_id>',cargarProductos,name='producto-load'),
    path('producto-modificado/<int:producto_id>',modificarProductos,name='producto-modificado'),

]

