from django.contrib import admin
from django.urls import path
from Dulceria import views
from Panel_Productos.views import productosAdd,categoriasAdd,unidadesAdd,mostrarCategorias,cargarCategorias,modificarCategorias,mostrarUnidades,cargarUnidades,modificarUnidades,mostrarProductos,cargarProductos,modificarProductos,productoDelete,categoriaDelete,unidadesDelete, exportar_productos_excel
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ProveedoresApi import views as proveedores_api_views
# Importaciones Usuario
from Panel_Usuarios import views as vista

# Importaciones Proveedores
from Panel_Proveedores import views as vista_proveedores

#Importaciones Inventario
from Inventario import views as vista_inventario

from UsuarioApi import views as vistaUsuarioApi

urlpatterns = [
    path('admin/', admin.site.urls),

    path('historia-empresa/', views.historia_empresa, name="historia-empresa"),
    path('rrss/', views.rrss, name='rrss'),
    path('', views.catalogo, name="catalogo"),
    path('catalogo/<str:categoria>/', views.subcatalogo, name="subcatalogo"),
    path('catalogo/<str:categoria>/<str:nombreProducto>/', views.detalle, name="detalle_producto"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('recuperarContraseña/', views.recuperarContraseña, name="recuperarContraseña"),
    path('verificarCodigo/', views.verificarCodigo, name="verificarCodigo"),
    path('crearContraseña/', views.crearContraseña, name="crearContraseña"),
    
    #Rutas token
    path('api/token/', TokenObtainPairView.as_view(), name='obtener_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    
    # Rutas Usuario
    path('usuarioAdd/', vista.usuarioAdd, name="usuarioAdd"),
    path('usuarioLista/', vista.usuarioLista, name='usuarioLista'),
    path('usuarioLista/delete/<int:id>/', vista.usuarioDelete, name='usuarioDelete'),
    path('usuarioUpdate/<int:id>/', vista.usuarioUpdate, name='usuarioUpdate'),
    path("usuarios/exportar-excel/", vista.exportar_usuarios_excel, name="exportar_usuarios_excel"),
    
    #Rutas Usuario API
    path('usuariosApi/', vistaUsuarioApi.usuariosApi, name='usuariosApi'),
    path('usuariosListApi/', vistaUsuarioApi.usuario_lista, name='usuariosListApi'),
    path('usuariosListApi/<int:pk>', vistaUsuarioApi.usuario_detalle, name='usuariosDetalleApi'),
    
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
    path('proveedores/', include('Panel_Proveedores.urls')),
    path("proveedores/exportar-excel/", vista_proveedores.exportar_proveedores_excel, name="exportar_proveedores_excel"),

    path('api/proveedores/', proveedores_api_views.proveedor_lista, name='proveedor_lista'),
    path('api/proveedores/<int:pk>/', proveedores_api_views.proveedor_detalle, name='proveedor_detalle'),


    # Rutas Ofertas de Proveedores
    path('ofertas/', vista_proveedores.lista_ofertas, name='lista_ofertas'),
    path('ofertas/agregar/', vista_proveedores.agregar_oferta, name='agregar_oferta'),
    path('ofertas/editar/<int:pk>/', vista_proveedores.editar_oferta, name='editar_oferta'),
    path('ofertas/eliminar/<int:pk>/', vista_proveedores.eliminar_oferta, name='eliminar_oferta'),
    path('ofertas/fragment/', vista_proveedores.lista_ofertas_fragment, name='lista_ofertas_fragment'),


    #Rutas Productos
    path('gestion-producto/',productosAdd,name="gestion-producto"),
    path('productos/',mostrarProductos,name="productos"),
    path('producto-load/<int:producto_id>',cargarProductos,name='producto-load'),
    path('producto-eliminado/<int:producto_id>', productoDelete, name='producto-eliminado'),
    path('producto-modificado/<int:id>/',modificarProductos,name='producto-modificado'),
    path("productos/exportar-excel/", exportar_productos_excel, name="exportar_productos_excel"),


    #Rutas Categorías
    path('gestion-categoria/',categoriasAdd,name="gestion-categoria"),
    path('categorias/',mostrarCategorias,name="categorias"),
    path('categoria-load/<int:categoria_id>',cargarCategorias,name='categoria-load'),
    path('categoria-eliminada/<int:categoria_id>', categoriaDelete, name='categoria-eliminada'),
    path('categoria-modificada/<int:id>/',modificarCategorias,name='categoria-modificada'),

    #Rutas Unidades de Medida
    path('gestion-unidad-medida/',unidadesAdd,name="gestion-unidad-medida"),
    path('unidades-medidas/',mostrarUnidades,name="unidades-medida"),
    path('unidad-medida-load/<int:unidad_medida_id>',cargarUnidades,name='unidad-medida-load'),
    path('unidad-medida-eliminada/<int:unidad_medida_id>', unidadesDelete, name='unidad-medida-eliminada'),
    path('unidad-medida-modificada/<int:id>/',modificarUnidades,name='unidad-medida-modificada'),

    #Rutas Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # APIs para gráficas y tablas
    path('api/stats/summary/', views.api_summary, name='api_summary'),
    path('api/stats/products_by_category/', views.api_products_by_category, name='api_products_by_category'),
    path('api/stats/products_monthly/', views.api_products_monthly, name='api_products_monthly'),
    path('api/stats/providers_monthly/', views.api_providers_monthly, name='api_providers_monthly'),
    path('api/stats/users_monthly/', views.api_users_monthly, name='api_users_monthly'),
    path('api/table/low_stock/', views.api_low_stock, name='api_low_stock'),

    # Exportaciones
    path('export/excel/<str:resource>/', views.export_excel, name='export_excel'),
    path('export/csv/<str:resource>/', views.export_csv, name='export_csv'),
    
    #Inventario
    path('inventarioAdd/', vista_inventario.movimientoAdd, name='inventarioAdd'),
    path('inventarioLista/', vista_inventario.inventarioLista, name='inventarioLista'),
    path('inventarioLista/delete/<int:id>/', vista_inventario.movimientoDelete, name='inventarioDelete'),
    path('inventarioUpdate/<int:id>/', vista_inventario.movimientoUpdate, name='inventarioUpdate'),
    path("inventario/exportar-excel/", vista_inventario.exportar_movimientos_excel, name="exportar_movimientos_excel"),

    path("no_autorizado/", views.no_autorizado, name='no_autorizado'),
]

