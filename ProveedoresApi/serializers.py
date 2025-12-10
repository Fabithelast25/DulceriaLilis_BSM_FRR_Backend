# ProveedoresApi/serializers.py
from rest_framework import serializers
from Panel_Proveedores.models import Proveedor, OfertaProveedor


class ProveedorSerializer(serializers.ModelSerializer):
    # Opcional: ver cuántas ofertas tiene el proveedor
    total_ofertas = serializers.IntegerField(
        source='ofertas.count', read_only=True
    )

    class Meta:
        model = Proveedor
        fields = [
            'id',
            'rut_nif',
            'razon_social',
            'nombre_fantasia',
            'email',
            'telefono',
            'sitio_web',
            'direccion',
            'ciudad',
            'pais',
            'condiciones_pago',
            'moneda',
            'contacto_principal_nombre',
            'contacto_principal_email',
            'contacto_principal_telefono',
            'estado',
            'observaciones',
            'creado',
            'total_ofertas',
        ]
        read_only_fields = ['id', 'creado', 'total_ofertas']


class OfertaProveedorSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(
        source='proveedor.razon_social', read_only=True
    )
    producto_nombre = serializers.CharField(
        source='producto.nombre', read_only=True
    )

    class Meta:
        model = OfertaProveedor
        fields = [
            'id',
            'producto',
            'producto_nombre',
            'proveedor',
            'proveedor_nombre',
            'costo',
            'lead_time_dias',
            'min_lote',
            'descuento_pct',
            'preferente',
        ]
        read_only_fields = ['id']
