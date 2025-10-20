# Panel_Proveedores/admin.py
from django.contrib import admin
from .models import Proveedor, OfertaProveedor

class OfertaProveedorInline(admin.TabularInline):
    """Permite gestionar ofertas directamente desde la vista de un proveedor"""
    model = OfertaProveedor
    extra = 1
    fields = ('producto', 'costo', 'lead_time_dias', 'min_lote', 'descuento_pct', 'preferente')
    raw_id_fields = ['producto']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'rut_nif', 'razon_social', 'nombre_fantasia',
        'email', 'telefono', 'ciudad', 'pais',
        'estado', 'moneda', 'condiciones_pago'
    )
    search_fields = (
        'rut_nif', 'razon_social', 'nombre_fantasia',
        'email', 'ciudad', 'pais'
    )
    list_filter = (
        'estado', 'moneda', 'condiciones_pago', 'pais'
    )
    ordering = ('razon_social',)
    inlines = [OfertaProveedorInline]

@admin.register(OfertaProveedor)
class OfertaProveedorAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'producto', 'costo', 'min_lote', 'descuento_pct', 'preferente')
    search_fields = ('proveedor__razon_social', 'producto__nombre', 'producto__sku')
    list_filter = ('preferente', 'proveedor__estado', 'proveedor__moneda')
    #autocomplete_fields = ['proveedor', 'producto']
    raw_id_fields = ['proveedor','producto']

