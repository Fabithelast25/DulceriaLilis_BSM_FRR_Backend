from django.db import models
from django.utils import timezone #Importación para obtener fecha y hora
from Panel_Usuarios.choices import estados

# Create your models here.
'''
Modelo: 
    Identificación
        • username (requerido, único)
        • email (requerido, único)
        • nombres (requerido)
        • apellidos (requerido)
        • telefono (opcional)
    Estado y acceso
        • rol (requerido)
        • estado (requerido; default ACTIVO)
        • mfa_habilitado (requerido; default 0)
        • ultimo_acceso (solo lectura)
        • sesiones_activas (contador/solo lectura si lo muestras)
    Metadatos
        • area/unidad (opcional)
        • observaciones (opcional)
'''
class Rol(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Rol")
    creado = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(max_length=200, verbose_name="Descripcion", blank=True)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "rol" #Nombre de la tabla cuando se cree
        verbose_name = "Rol" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Roles" #Nombre en plural

class Area(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Area")
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "area" #Nombre de la tabla cuando se cree
        verbose_name = "Area" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Areas" #Nombre en plural

class Usuario(models.Model):
    #Identificación
    username = models.CharField(max_length=50, verbose_name="Username", unique=True)
    email = models.EmailField(max_length=70, verbose_name="Email", unique=True)
    nombres = models.CharField(max_length=50, verbose_name="Nombres")
    apellidos = models.CharField(max_length=60, verbose_name="Apellidos")
    telefono = models.CharField(max_length=15, verbose_name="Telefono", blank=True)

    #Estado y acceso
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT)
    estado = models.CharField(max_length=1, choices=estados, default="A")
    mfa_habilitado = models.BooleanField(default=False, verbose_name="MFA_Habilitado")
    ultimo_acceso = models.DateField(default=timezone.now)
    sesiones_activas = models.PositiveIntegerField(default=0)

    #Metadatos
    area = models.ForeignKey(Area, on_delete=models.RESTRICT)
    observaciones = models.TextField(max_length=200, verbose_name="Observaciones", blank=True)
    
    class Meta:
        db_table = "usuario" #Nombre de la tabla cuando se cree
        verbose_name = "Usuario" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Usuarios" #Nombre en plural
