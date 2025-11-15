from django import forms
from Inventario.choices import tipos
from Inventario.models import Movimiento, Bodega
from Panel_Productos.models import Producto
from Panel_Proveedores.models import Proveedor
from django.utils import timezone
from django.utils.safestring import mark_safe
""" #Datos movimiento
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=tipos, default="I")
    cantidad = models.IntegerField(max_length=5)
    
    #Foraneo
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL)
    proveedor = models.ForeignKey(Producto, on_delete=models.SET_NULL)
    bodega = models.CharField(max_length=6, choices=bodegas, default="BOD_01")
    
    #Control Avanzdo:
    manejoPorLotes = models.BooleanField(default=False)
    manejoPorSerie = models.BooleanField(default=False)
    perecible = models.DateTimeField()
    
    lote = models.CharField(max_length=10, null=True, blank=True)
    serie = models.CharField(max_length=10, null=True, blank=True)
    fechaVencimiento = models.DateField(null=True, blank=True)
    
    #Referencias/Observacioes:
    doc_referencia = models.CharField(max_length=10)
    motivo = models.CharField(max_length=50)
    observaciones = models.TextField(max_length=500, blank=True)
    """

class movimientoForm(forms.ModelForm):
    #Datos movimiento
    fecha = forms.DateTimeField(initial= timezone.now(), widget=forms.DateTimeInput(attrs={'class':'form-control','readonly':'readonly'}))
    tipo = forms.CharField(widget=forms.Select(choices=tipos, attrs={'class':'form-select'}))
    cantidad = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    #Foraneo
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(),
                                       empty_label="Seleccione un Proveedor",
                                       widget=forms.Select(attrs={'class':'form-control'}))
    bodega = forms.ModelChoiceField(queryset=Bodega.objects.all(),
                                    empty_label="Seleccione una Bodega",
                                    widget=forms.Select(attrs={'class':'form-control'}))
    
    #Control Avanzado
    control_por_lote = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'disabled':'disabled'}))
    control_por_serie = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'disabled':'disabled'}))
    perishable = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'disabled':'disabled'}))

    lote = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'disabled':'disabled'}))
    serie = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'disabled':'disabled'}))
    fechaVencimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'form-control', 'type':'date', 'disabled':'disabled'}))
    
    #Referencias/Observaciones
    doc_referencia  = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    motivo = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    observaciones = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'(Max: 500 carácteres)'}), max_length=500)
    
    class Meta:
        model = Movimiento
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener todos los productos
        productos = Producto.objects.all()

        # Crear las opciones manualmente con data-*
        opciones = [("", "Seleccione un producto")]  # placeholder REAL

        for p in productos:
            opciones.append((
                p.id,
                f"{p.nombre}"
            ))

        # Aplicamos las opciones al field
        self.fields['producto'].choices = opciones

        # Agregamos data-* a cada opción desde el widget
        self.fields['producto'].widget.attrs.update({'class': 'form-select', 'id': 'id_producto'})
        self.fields['producto'].widget.choices = opciones

        # Guardamos los datos para procesarlos en el template
        self.producto_data = {
            str(p.id): {
                "lote": str(p.control_por_lote),
                "serie": str(p.control_por_serie),
                "perecible": str(p.perishable)
            }
            for p in productos
        }

            
        

class bodegaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    creado = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control'}))
    descripcion = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Bodega
        fields = '__all__'