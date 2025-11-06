from django.db import models
from Panel_Productos.choices import categorias, unidades_medidas
from django.utils import timezone

# Create your models here.
'''
Identificación
    • sku (requerido, único)
    • ean_upc (opcional, único si se usa)
    • nombre (requerido)
    • descripcion (opcional)
    • categoria (requerido)
    • marca (opcional)
    • modelo (opcional)
Unidades y precios
    • uom_compra (requerido; ej. UN, CAJA, KG)
    • uom_venta (requerido)
    • factor_conversion (requerido; default 1)
    • costo_estandar (opcional)
    • costo_promedio (solo lectura si calculas)
    • precio_venta (opcional)
    • impuesto_iva (requerido; ej. 19%)
Stock y control
    • stock_minimo (requerido; default 0)
    • stock_maximo (opcional)
    • punto_reorden (opcional; si no, usar mínimo)
    • perishable (requerido; default 0)
    • control_por_lote (requerido; default 0)
    • control_por_serie (requerido; default 0)
Relaciones y soporte
    • imagen_url (opcional)
    • ficha_tecnica_url (opcional)
Derivados / solo lectura en vistas
    • stock_actual (por bodega o total; calculado)
    • alerta_bajo_stock (calculado)
    • alerta_por_vencer (si perishable/lote)
'''

class Categoria(models.Model):
    nombre = models.CharField(max_length=3, choices=categorias, default="CH", unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=200, verbose_name="Descripción", blank=True)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "categoria" #Nombre de la tabla cuando se cree
        verbose_name = "Categoria" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Categorias" #Nombre en plural

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=4, choices=unidades_medidas, default="UN", unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=200, verbose_name="Descripción", blank=True)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "unidad_medida" #Nombre de la tabla cuando se cree
        verbose_name = "Unidad de Medida" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Unidades de Medida" #Nombre en plural

class Producto(models.Model):
    #Identificación
    sku = models.CharField(max_length=15, verbose_name="SKU",unique=True)
    ean_upc = models.PositiveIntegerField(verbose_name= "Código EAN/UPC", unique=True)
    nombre = models.CharField(max_length=70,verbose_name="Nombre")
    descripcion = models.TextField(max_length=300,verbose_name="Descripción", blank=True)
    categoria = models.ForeignKey(Categoria, on_delete= models.RESTRICT)
    marca = models.CharField(max_length=50,verbose_name="Marca")
    modelo = models.CharField(max_length=50,verbose_name="Modelo")

    #Unidades y precios
    uom_compra = models.ForeignKey(UnidadMedida, on_delete= models.RESTRICT, related_name='productos_compra')
    uom_venta = models.ForeignKey(UnidadMedida, on_delete= models.RESTRICT, related_name='productos_venta')
    factor_conversion = models.PositiveIntegerField(verbose_name="Factor de Conversión", default=1)
    costo_estandar = models.PositiveIntegerField(verbose_name="Costo Estandar", blank=True)
    costo_promedio = models.PositiveIntegerField(verbose_name="Costo Promedio", null=True, blank=True)
    precio_venta = models.PositiveIntegerField(verbose_name="Precio de Venta", blank=True)
    impuesto_iva = models.PositiveSmallIntegerField(verbose_name="Porcentaje de Iva (%)", default=19)

    #Stock y control
    stock_minimo = models.PositiveIntegerField(verbose_name="Stock Mínimo",default=0)
    stock_maximo = models.PositiveIntegerField(verbose_name="Stock Máximo",blank=True)
    punto_reorden = models.PositiveIntegerField(verbose_name="Punto de Reorden", blank=True)
    perishable = models.BooleanField(verbose_name="¿Es perecible?", default=False)
    control_por_lote = models.BooleanField(verbose_name="Control por lote", default=False)
    control_por_serie = models.BooleanField(verbose_name="Control por número de serie", default=False)

    #Relaciones y soporte
    imagen_url = models.URLField(max_length=300,verbose_name="URL Imagen", blank=True)
    ficha_tecnica_url = models.URLField(max_length=300,verbose_name="URL de la Ficha Técnica", blank=True)

    #Derivados / solo lectura en vistas
    stock_actual = models.PositiveIntegerField(verbose_name="Stock Actual")
    alerta_bajo_stock = models.CharField(max_length=2, verbose_name= "Alerta de Bajo Stock")
    alerta_por_vencer = models.CharField(max_length=2, verbose_name= "Alerta de Vencimiento")

    #Fecha de creación
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "producto" #Nombre de la tabla cuando se cree
        verbose_name = "Producto" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Productos" #Nombre en plural
