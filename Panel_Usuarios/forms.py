from django import forms
from Panel_Usuarios.choices import estados
from Panel_Usuarios.models import Area, Rol, Usuario
from django.utils import timezone
from .validators import validar_telefono_chileno
"""    #Identificación
    username = models.CharField(max_length=50, verbose_name="Username", unique=True)
    email = models.EmailField(max_length=70, verbose_name="Email", unique=True)
    nombres = models.CharField(max_length=50, verbose_name="Nombres")
    apellidos = models.CharField(max_length=60, verbose_name="Apellidos")
    telefono = models.CharField(max_length=15, verbose_name="Telefono", blank=True)

    #Estado y acceso
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT)
    estado = models.CharField(max_length=1, choices=estados, default="A")
    mfa_habilitado = models.BooleanField(default=True, verbose_name="MFA_Habilitado")
    ultimo_acceso = models.DateField(default=timezone.now)
    sesiones_activas = models.PositiveIntegerField(default=0)

    #Metadatos
    area = models.ForeignKey(Area, on_delete=models.RESTRICT)
    observaciones = models.TextField(max_length=200, verbose_name="Observaciones", blank=True)"""
class UsuarioForm(forms.ModelForm):
    #Identificación
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(max_length=70, widget=forms.EmailInput(attrs={'class':'form-control'}))
    telefono = forms.CharField(max_length=11, required=False,validators=[validar_telefono_chileno],widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    #Estado y acceso
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        empty_label="Seleccione un rol",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    estado = forms.CharField(widget=forms.Select(choices=estados, attrs={'class':'form-select'}))
    mfa_habilitado = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    last_login = forms.DateTimeField(initial = timezone.now(),
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )
    sesiones_activas = forms.CharField(required=False, empty_value=0, widget=forms.NumberInput(attrs={'class':'form_control', 'readonly':True, 'placeholder':'0'}))
    
    #Metadatos
    area = forms.ModelChoiceField(
        required=False,
        queryset=Area.objects.all(),
        empty_label="Seleccione un área",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    observaciones= forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'(Max: 500 carácteres)'}), max_length=500)
    
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ["password", "date_joined"]
        
class AreaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Area
        fields = '__all__'
    
    