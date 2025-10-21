from django.contrib import admin

# Register your models here.
from Panel_Productos.models import Producto, UnidadMedida, Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["id","nombre","creado","descripcion"]

class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ["id","nombre","creado","descripcion"]

class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        "sku",
        "ean_upc",
        "nombre",
        "descripcion",
        "categoria",
        "marca",
        "modelo",
        "uom_compra",
        "uom_venta",
        "factor_conversion",
        "costo_estandar",
        "costo_promedio",
        "precio_venta",
        "impuesto_iva",
        "stock_minimo",
        "stock_maximo",
        "punto_reorden",
        "perishable",
        "control_por_lote",
        "control_por_serie",
        "imagen_url",
        "ficha_tecnica_url",
        "stock_actual",
        "alerta_bajo_stock",
        "alerta_por_vencer",
        "creado"
    ]

admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(UnidadMedida,UnidadMedidaAdmin)
admin.site.register(Producto,ProductoAdmin)