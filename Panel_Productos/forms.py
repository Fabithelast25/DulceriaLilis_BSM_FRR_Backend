import re
from django import forms
from Panel_Productos.choices import alertas_por_vencer, alertas_bajo_stock
from Panel_Productos.models import Categoria, UnidadMedida, Producto
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ProductoForm(forms.ModelForm):

    #Identificación
    sku = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'SKU-0001'}), max_length=15)
    ean_upc = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'7891234567890'}), min_length=12,max_length=13)
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Silla ergonómica'}), max_length=70)
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripción del producto'}), max_length=300)
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Seleccione...",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    marca = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'MarcaX'}), max_length=50)
    modelo = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'MX-200'}), max_length=50)

    #Unidades y precios
    uom_compra = forms.ModelChoiceField(
        queryset=UnidadMedida.objects.all(),
        empty_label="Seleccione...",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    uom_venta = forms.ModelChoiceField(
        queryset=UnidadMedida.objects.all(),
        empty_label="Seleccione...",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    factor_conversion = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'1'}),initial=1)
    costo_estandar = forms.CharField(required=False,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}), initial=0)
    costo_promedio = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}), initial=0)
    precio_venta = forms.CharField(required=False,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}), initial=0)
    impuesto_iva = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'19'}))

    #Stock y control
    stock_minimo = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'0'}))
    stock_maximo = forms.CharField(required=False,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}), initial=0)
    punto_reorden = forms.CharField(required=False,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}), initial=0)
    perishable = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), initial=False)
    control_por_lote = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), initial=False)
    control_por_serie = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), initial=False)

    #Relaciones y soporte
    imagen_url = forms.URLField(required=False,widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'https://.../foto.jpg'}), max_length=255)
    ficha_tecnica_url = forms.URLField(required=False,widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'https://.../ficha.pdf'}), max_length=255)

    #Derivados / solo lectura en vistas
    stock_actual = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'0'}))
    alerta_bajo_stock = forms.CharField(widget=forms.Select(choices=alertas_bajo_stock, attrs={'class':'form-select'}))
    alerta_por_vencer = forms.CharField(widget=forms.Select(choices=alertas_por_vencer, attrs={'class':'form-select'}))

    class Meta:
        model = Producto
        fields = [
            'sku', 'ean_upc', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo', 
            'uom_compra', 'uom_venta', 'factor_conversion', 'costo_estandar', 'costo_promedio', 
            'precio_venta', 'impuesto_iva', 'stock_minimo', 'stock_maximo', 'punto_reorden', 
            'perishable', 'control_por_lote', 'control_por_serie', 'imagen_url', 'ficha_tecnica_url',
            'stock_actual', 'alerta_bajo_stock', 'alerta_por_vencer'
        ]
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'ean_upc': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'uom_compra': forms.TextInput(attrs={'class': 'form-control'}),
            'uom_venta': forms.TextInput(attrs={'class': 'form-control'}),
            'factor_conversion': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'costo_estandar': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_promedio': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'impuesto_iva': forms.NumberInput(attrs={'class': 'form-control', 'value': 19}),

        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            numeric_fields = [
                'factor_conversion',
                'costo_estandar',
                'costo_promedio',
                'precio_venta',
                'stock_minimo',
                'stock_maximo',
                'punto_reorden',
                'stock_actual',
            ]

            for field in numeric_fields:
                if field in self.fields:
                    self.fields[field].widget.attrs.update({
                        'max': 999999,
                    })

            # Caso especial: impuesto_iva → solo hasta 100
            if 'impuesto_iva' in self.fields:
                self.fields['impuesto_iva'].widget.attrs.update({
                    'max': 100,
            })
     # SKU
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        if not re.match(r'^[A-Z0-9\-]+$', sku):
            raise forms.ValidationError("El SKU solo puede contener letras mayúsculas, números y guiones")
        if len(sku) >= 15:
            raise forms.ValidationError("El número debe tener menos de 15 caracteres")
        qs = Producto.objects.filter(sku=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con este SKU.")
        return sku

    # EAN/UPC
    def clean_ean_upc(self):
        ean_upc = self.cleaned_data.get('ean_upc')
        if not ean_upc:
            return ean_upc
        if not ean_upc.isdigit():
            raise forms.ValidationError("Este campo solo debe contener números.")
        if not (12 <= len(ean_upc) <= 13):
            raise forms.ValidationError("El número debe tener entre 12 y 13 caracteres.")
        qs = Producto.objects.filter(ean_upc=ean_upc)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con esta EAN/UPC.")
        return ean_upc

    # Nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        if not re.match(r'^[A-Za-z0-9áéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras, números y espacios, incluyendo acentos.")
        if len(nombre) >= 70:
            raise forms.ValidationError("El nombre debe tener menos de 70 caracteres")
        return nombre

    # Descripción
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion') or ''
        if len(descripcion) >= 300:
            raise forms.ValidationError("La descripción debe tener menos de 300 caracteres")
        return descripcion

    # Marca
    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if marca:
            if not re.match(r'^[A-Za-z0-9 ]+$', marca):
                raise forms.ValidationError("La marca solo puede contener letras, números y espacios")
            if len(marca) > 50:
                raise forms.ValidationError("La marca no puede tener más de 50 caracteres")
        return marca

    # Modelo
    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')
        if modelo:
            if not re.match(r'^[A-Za-z0-9 ]+$', modelo):
                raise forms.ValidationError("El modelo solo puede contener letras, números y espacios")
            if len(modelo) > 50:
                raise forms.ValidationError("El modelo no puede tener más de 50 caracteres")
        return modelo

    # Factor de conversión
    def clean_factor_conversion(self):
        factor = self.cleaned_data.get('factor_conversion')
        if factor is None:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        if factor < 0:
            raise forms.ValidationError("El factor de conversión no puede ser negativo.")
        return factor

    # Costos
    def clean_costo_estandar(self):
        costo = self.cleaned_data.get('costo_estandar')
        if costo in (None, ''):
            return None
        try:
            costo = float(costo)
        except ValueError:
            raise forms.ValidationError("El costo estándar debe ser un número")
        if costo < 0:
            raise forms.ValidationError("El costo estándar no puede ser negativo")
        if costo > 999999:
            raise forms.ValidationError("El costo estándar no puede superar 999.999")
        return costo

    def clean_costo_promedio(self):
        costo = self.cleaned_data.get('costo_promedio')
        if costo in (None, ''):
            return None
        try:
            costo = float(costo)
        except ValueError:
            raise forms.ValidationError("El costo promedio debe ser un número")
        if costo < 0:
            raise forms.ValidationError("El costo promedio no puede ser negativo")
        if costo > 999999:
            raise forms.ValidationError("El costo promedio no puede superar 999.999")
        return costo

    def clean_precio_venta(self):
        precio = self.cleaned_data.get('precio_venta')
        if precio in (None, ''):
            return None
        try:
            precio = float(precio)
        except ValueError:
            raise forms.ValidationError("El precio de venta debe ser un número")
        if precio < 0:
            raise forms.ValidationError("El precio de venta no puede ser negativo")
        if precio > 999999:
            raise forms.ValidationError("El precio de venta no puede superar 999.999")
        return precio

    # IVA
    def clean_impuesto_iva(self):
        iva = self.cleaned_data.get('impuesto_iva')
        if iva in (None, ''):
            raise forms.ValidationError("Este campo no puede estar vacío.")
        try:
            iva = float(iva)
        except ValueError:
            raise forms.ValidationError("El IVA debe ser un número")
        if not (0 <= iva <= 100):
            raise forms.ValidationError("El IVA debe estar entre 0 y 100")
        return iva

    # Stock
    def clean_stock_minimo(self):
        stock = self.cleaned_data.get('stock_minimo')
        if stock in (None, ''):
            raise forms.ValidationError("Este campo no puede estar vacío.")
        try:
            stock = int(stock)
        except ValueError:
            raise forms.ValidationError("El stock mínimo debe ser un número entero")
        if stock < 0:
            raise forms.ValidationError("El stock mínimo no puede ser negativo")
        if stock > 999999:
            raise forms.ValidationError("El stock mínimo no puede superar 999.999")
        return stock

    def clean_stock_maximo(self):
        stock = self.cleaned_data.get('stock_maximo')
        if stock in (None, ''):
            return None
        try:
            stock = int(stock)
        except ValueError:
            raise forms.ValidationError("El stock máximo debe ser un número entero")
        if stock < 0:
            raise forms.ValidationError("El stock máximo no puede ser negativo")
        if stock > 999999:
            raise forms.ValidationError("El stock máximo no puede superar 999.999")
        return stock

    def clean_stock_actual(self):
        stock = self.cleaned_data.get('stock_actual')
        if stock in (None, ''):
            raise forms.ValidationError("Este campo no puede estar vacío.")
        try:
            stock = int(stock)
        except ValueError:
            raise forms.ValidationError("El stock debe ser un número entero")
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo")
        if stock > 999999:
            raise forms.ValidationError("El stock no puede superar 999.999")
        return stock

    def clean_punto_reorden(self):
        punto = self.cleaned_data.get('punto_reorden')
        if punto in (None, ''):
            return None
        try:
            punto = int(punto)
        except ValueError:
            raise forms.ValidationError("El punto de reorden debe ser un número entero")
        if punto < 0:
            raise forms.ValidationError("El punto de reorden no puede ser negativo")
        if punto > 999999:
            raise forms.ValidationError("El punto de reorden no puede superar 999.999")
        return punto

    # URLs
    def clean_imagen_url(self):
        url = self.cleaned_data.get('imagen_url')
        if not url:
            return url
        if not url.startswith(('http://','https://')):
            raise forms.ValidationError("La URL debe iniciar con http:// o https://")
        return url

    def clean_ficha_tecnica_url(self):
        url = self.cleaned_data.get('ficha_tecnica_url')
        if not url:
            return url
        if not url.startswith(('http://','https://')):
            raise forms.ValidationError("La URL debe iniciar con http:// o https://")
        return url

    # Validación general
    def clean(self):
        cleaned_data = super().clean()

        stock_minimo = cleaned_data.get('stock_minimo')
        stock_maximo = cleaned_data.get('stock_maximo')
        punto_reorden = cleaned_data.get('punto_reorden')

        # Validación stock_min < stock_max
        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo > stock_maximo:
                self.add_error('stock_minimo', "El stock mínimo no puede ser mayor que el stock máximo.")
                self.add_error('stock_maximo', "El stock máximo no puede ser menor que el stock mínimo.")

        # Validación punto de reorden dentro del rango
        if (
            stock_minimo not in (None, 0) and
            stock_maximo not in (None, 0) and
            punto_reorden is not None
        ):
            if not (stock_minimo <= punto_reorden <= stock_maximo):
                self.add_error('punto_reorden', "El punto de reorden debe estar entre el stock mínimo y el stock máximo.")
                # Opcional: puedes mostrar también el error en los otros campos
                self.add_error('stock_minimo', "El punto de reorden debe estar dentro del rango definido.")
                self.add_error('stock_maximo', "El punto de reorden debe estar dentro del rango definido.")

        return cleaned_data


class CategoriaForm(forms.ModelForm):
    nombre_abreviado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'CH'}), max_length=3)
    nombre_completo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Chocolate'}), max_length=20)
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows':3,
            'placeholder':'Descripción de la categoría'
        }),
        max_length=240
    )

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'descripcion_categoria': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre_abreviado_categoria(self):
        nombre_abreviado = self.cleaned_data.get('nombre_abreviado')
        
        if not nombre_abreviado:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        
        if not all(c.isalpha() or c.isspace() for c in nombre_abreviado):
            raise forms.ValidationError("El nombre abreviado solo puede contener letras y espacios.")
        
        return nombre_abreviado
    
    def clean_nombre_completo_categoria(self):
        nombre_completo = self.cleaned_data.get('nombre_completo')
        
        if not nombre_completo:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        
        if not all(c.isalpha() or c.isspace() for c in nombre_completo):
            raise forms.ValidationError("El nombre completo solo puede contener letras y espacios.")
        
        return nombre_completo
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        if not descripcion:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        
        if len(descripcion) >= 200:
            raise forms.ValidationError('La descripción debe tener menos de 200 caracteres.')
        
        return descripcion

class UnidadMedidaForm(forms.ModelForm):
    nombre_abreviado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'UN'}),max_length=4)
    nombre_completo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Unidad'}),max_length=20)
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripción de la unidad de medida'}), max_length=200)
    class Meta:
        model = UnidadMedida
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    def clean_nombre_abreviado_categoria(self):
        nombre_abreviado = self.cleaned_data.get('nombre_abreviado')
        
        if not nombre_abreviado:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        
        if not all(c.isalpha() or c.isspace() for c in nombre_abreviado):
            raise forms.ValidationError("El nombre abreviado solo puede contener letras y espacios.")
        
        return nombre_abreviado
    
    def clean_nombre_completo_categoria(self):
        nombre_completo = self.cleaned_data.get('nombre_completo')
        
        if not nombre_completo:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        
        if not all(c.isalpha() or c.isspace() for c in nombre_completo):
            raise forms.ValidationError("El nombre completo solo puede contener letras y espacios.")
        
        return nombre_completo
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        if not descripcion:
            raise forms.ValidationError("Este campo no puede estar vacío.")
        
        if len(descripcion) >= 200:
            raise forms.ValidationError('La descripción debe tener menos de 200 caracteres.')
        
        return descripcion