from django.db import models

# Create your models here.
from django.db import models
from .choices import tipos
from Panel_Productos.models import Producto
from Panel_Proveedores.models import Proveedor

# Create your models here.
'''
Modelo: 
    Datos de movimiento:
        fecha/hora [DATE, readonly]
        tipo: (Ingreso/Salida)
        Cantidad [INT]
        Producto: ID Producto [Select]
        Proveedor: Rut o Razon social [Select]
        Bodega : [Select Bodegas]
    
    Control avanzado:
        Manejo por lotes: (Si, no)
        Manejo por series: (Si, no)
        
        Desde productos:
            Perecible (Vencimiento): (Si, no)
            Lote: Codigo Lote
            Serie: Codigo Serie
            
            Fecha Vencimiento [DATE]
        
    Referencias/Observaciones:
        Doc_Referencia: Nombre documento
        Motivo (Ajuste/Devoluciones)
        Observaciones: Text
'''

class Bodega(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Bodega")
    creado = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=200, verbose_name="Descripcion", blank=True)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "bodega" #Nombre de la tabla cuando se cree
        verbose_name = "Bodega" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Bodegas" #Nombre en plural

class Movimiento(models.Model):
    #Datos movimiento
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=1, choices=tipos, default="I")
    cantidad = models.PositiveIntegerField()
    
    #Foraneo
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True)
    
    lote = models.CharField(max_length=10, null=True, blank=True)
    serie = models.CharField(max_length=10, null=True, blank=True) 
    fechaVencimiento = models.DateField(null=True, blank=True)
    
    #Referencias/Observacioes:
    doc_referencia = models.CharField(max_length=10)
    motivo = models.CharField(max_length=50)
    observaciones = models.TextField(max_length=500, blank=True)
    
    class Meta:
        db_table = "movimiento" #Nombre de la tabla cuando se cree
        verbose_name = "Movimiento" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Movimientos" #Nombre en plural
