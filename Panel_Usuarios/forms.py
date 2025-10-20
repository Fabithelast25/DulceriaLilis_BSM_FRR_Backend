from django import forms
from Panel_Usuarios.choices import estados
from Panel_Usuarios.models import Area, Rol, Usuario
from django.utils import timezone
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
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = forms.CharField(required=False,widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    #Estado y acceso
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        empty_label="Seleccione un rol",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    estado = forms.CharField(widget=forms.Select(choices=estados, attrs={'class':'form-select'}))
    mfa_habilitado = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    ultimo_acceso = forms.DateField(initial=timezone.now, widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'--------', 'readonly': True}))
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
        
    