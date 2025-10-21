from django.contrib import admin
from django.urls import path
from Dulceria import views 

# Importaciones Usuario
from Panel_Usuarios import views as vista

# Importaciones Proveedores
from Panel_Proveedores import views as vista_proveedores

urlpatterns = [
    path('admin/', admin.site.urls),

    path('historia-empresa/', views.historia_empresa, name="historia-empresa"),
    path('rrss/', views.rrss, name='rrss'),
    path('', views.catalogo, name="catalogo"),
    path('catalogo/<str:categoria>/', views.subcatalogo, name="subcatalogo"),
    path('catalogo/<str:categoria>/<str:nombreProducto>/', views.detalle, name="detalle_producto"),
    
    # Rutas Usuario
    path('usuarioAdd/', vista.usuarioAdd, name="usuarioAdd"),
    path('usuarioLista/', vista.usuarioLista, name='usuarioLista'),
    path('usuarioLista/delete/<int:id>/', vista.usuarioDelete, name='usuarioDelete'),
    path('usuarioUpdate/<int:id>/', vista.usuarioUpdate, name='usuarioUpdate'),
    
    # Rutas Roles
    path('rolLista/', vista.rolLista, name="rolLista"),
    path('rolAdd/', vista.rolAdd, name='rolAdd'),
    path('rolLista/delete/<int:id>/', vista.rolDelete, name='rolDelete'),
    path('rolUpdate/<int:id>/', vista.rolUpdate, name='rolUpdate'),
    
    # Rutas Areas
    path('areaLista/', vista.areaLista, name="areaLista"),
    path('areaAdd/', vista.areaAdd, name='areaAdd'),
    path('areaLista/delete/<int:id>/', vista.areaDelete, name='areaDelete'),
    path('areaUpdate/<int:id>/', vista.areaUpdate, name='areaUpdate'),

    # Rutas Proveedores
    path('proveedores/', vista_proveedores.lista_proveedores, name='lista_proveedores'),
    path('proveedores/agregar/', vista_proveedores.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:pk>/', vista_proveedores.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', vista_proveedores.eliminar_proveedor, name='eliminar_proveedor'),

    # Rutas Ofertas de Proveedores
    path('ofertas/', vista_proveedores.lista_ofertas, name='lista_ofertas'),
    path('ofertas/agregar/', vista_proveedores.agregar_oferta, name='agregar_oferta'),
    path('ofertas/editar/<int:pk>/', vista_proveedores.editar_oferta, name='editar_oferta'),
    path('ofertas/eliminar/<int:pk>/', vista_proveedores.eliminar_oferta, name='eliminar_oferta'),

    #Rutas Productos
    path('gestion-producto/',productosAdd,name="gestion-producto"),
    path('productos/',mostrarProductos,name="productos"),
    path('producto-load/<int:producto_id>',cargarProductos,name='producto-load'),
    path('producto-modificado/<int:producto_id>',modificarProductos,name='producto-modificado'),

    #Rutas Categorías
    path('gestion-categoria/',categoriasAdd,name="gestion-categoria"),
    path('categorias/',mostrarCategorias,name="categorias"),
    path('categoria-load/<int:categoria_id>',cargarCategorias,name='categoria-load'),
    path('categoria-modificada/<int:categoria_id>',modificarCategorias,name='categoria-modificada'),

    #Rutas Unidades de Medida
    path('gestion-unidad-medida/',unidadesAdd,name="gestion-unidad-medida"),
    path('unidades-medidas/',mostrarUnidades,name="unidades-medida"),
    path('unidad-medida-load/<int:unidad_medida_id>',cargarUnidades,name='unidad-medida-load'),
    path('unidad-medida-modificada/<int:unidad_medida_id>',modificarUnidades,name='unidad-medida-modificada'),
]

