import re
from django import forms
from Panel_Productos.choices import categorias, unidades_medidas
from Panel_Productos.models import Categoria, UnidadMedida, Producto

class ProductoForm(forms.ModelForm):

    #Identificación
    sku = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'SKU-0001'}))
    ean_upc = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'7891234567890'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Silla ergonómica'}))
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripción del producto'}))
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Seleccione...",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    marca = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'MarcaX'}))
    modelo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'MX-200'}))

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
    factor_conversion = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'1'}))
    costo_estandar = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}))
    costo_promedio = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}))
    precio_venta = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}))
    impuesto_iva = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'19'}))

    #Stock y control
    stock_minimo = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'0'}))
    stock_maximo = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}))
    punto_reorden = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':''}))
    perishable = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    control_por_lote = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    control_por_serie = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

    #Relaciones y soporte
    url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'https://.../foto.jpg'}))
    ficha_tecnica_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'https://.../ficha.pdf'}))

    #Derivados / solo lectura en vistas
    stock_actual = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'0'}))
    alerta_bajo_stock = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'SI'}))
    alerta_por_vencer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'NO'}))

    class Meta:
        model = Producto
        fields = '__all__'
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
    # Validación de SKU
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not re.match(r'^[A-Z0-9\-]+$', sku):
            raise forms.ValidationError("El SKU solo puede contener letras mayúsculas, números y guiones")
        return sku

    # Validación de nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and not all(c.isalpha() or c.isspace() for c in nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios")
        return nombre

    # Validación de costos y precios
    def clean_costo_estandar(self):
        costo = self.cleaned_data.get('costo_estandar')
        try:
            costo = float(costo)
        except ValueError:
            raise forms.ValidationError("El costo estándar debe ser un número")
        if costo < 0:
            raise forms.ValidationError("El costo estándar no puede ser negativo")
        return costo

    def clean_costo_promedio(self):
        costo = self.cleaned_data.get('costo_promedio')
        try:
            costo = float(costo)
        except ValueError:
            raise forms.ValidationError("El costo promedio debe ser un número")
        if costo < 0:
            raise forms.ValidationError("El costo promedio no puede ser negativo")
        return costo

    def clean_precio_venta(self):
        precio = self.cleaned_data.get('precio_venta')
        try:
            precio = float(precio)
        except ValueError:
            raise forms.ValidationError("El precio de venta debe ser un número")
        if precio < 0:
            raise forms.ValidationError("El precio de venta no puede ser negativo")
        return precio

    def clean_impuesto_iva(self):
        iva = self.cleaned_data.get('impuesto_iva')
        try:
            iva = float(iva)
        except ValueError:
            raise forms.ValidationError("El IVA debe ser un número")
        if not (0 <= iva <= 100):
            raise forms.ValidationError("El IVA debe estar entre 0 y 100")
        return iva

    # Validación de stock
    def clean_stock_minimo(self):
        stock = self.cleaned_data.get('stock_minimo')
        try:
            stock = int(stock)
        except ValueError:
            raise forms.ValidationError("El stock mínimo debe ser un número entero")
        if stock < 0:
            raise forms.ValidationError("El stock mínimo no puede ser negativo")
        return stock

    def clean_stock_maximo(self):
        stock = self.cleaned_data.get('stock_maximo')
        try:
            stock = int(stock)
        except ValueError:
            raise forms.ValidationError("El stock máximo debe ser un número entero")
        if stock < 0:
            raise forms.ValidationError("El stock máximo no puede ser negativo")
        return stock

    def clean_punto_reorden(self):
        punto = self.cleaned_data.get('punto_reorden')
        try:
            punto = int(punto)
        except ValueError:
            raise forms.ValidationError("El punto de reorden debe ser un número entero")
        if punto < 0:
            raise forms.ValidationError("El punto de reorden no puede ser negativo")
        return punto

    # Validación de URLs
    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith(('http://', 'https://')):
            raise forms.ValidationError("La URL debe iniciar con http:// o https://")
        return url

    def clean_ficha_tecnica_url(self):
        url = self.cleaned_data.get('ficha_tecnica_url')
        if url and not url.startswith(('http://', 'https://')):
            raise forms.ValidationError("La URL de la ficha técnica debe iniciar con http:// o https://")
        return url

class CategoriaForm(forms.ModelForm):
    nombre = forms.ChoiceField(
        choices=categorias,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows':3,
            'placeholder':'Descripción del producto'
        })
    )

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'descripcion_categoria': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre_categoria(self):
        nombre = self.cleaned_data.get('nombre_categoria')
        if nombre and not all(c.isalpha() or c.isspace() for c in nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios")
        return nombre


class UnidadMedidaForm(forms.ModelForm):
    nombre = forms.ChoiceField(
        choices=unidades_medidas,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripción del producto'}))
    class Meta:
        model = UnidadMedida
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and not all(c.isalpha() or c.isspace() for c in nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios")
        return nombre