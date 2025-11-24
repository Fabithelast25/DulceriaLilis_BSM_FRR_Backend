from django.db import models
from django.utils import timezone #Importación para obtener fecha y hora
from Panel_Usuarios.choices import estados
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


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
    creado = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=200, verbose_name="Descripcion", blank=True)
    puede_gestionar_usuarios = models.BooleanField(default=False)
    puede_gestionar_productos = models.BooleanField(default=False)
    puede_gestionar_proveedores = models.BooleanField(default=False)
    puede_gestionar_inventario = models.BooleanField(default=False)
    puede_ver_usuarios = models.BooleanField(default=False)
    puede_ver_productos = models.BooleanField(default=False)
    puede_ver_proveedores = models.BooleanField(default=False)
    puede_ver_reportes = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "rol" #Nombre de la tabla cuando se cree
        verbose_name = "Rol" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Roles" #Nombre en plural

class Area(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Area")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = "area" #Nombre de la tabla cuando se cree
        verbose_name = "Area" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Areas" #Nombre en plural


class Usuario(AbstractUser):
    #Estos valores se heredan de AbstractUser
    """
    • username (requerido, único)
    • email (requerido, único)
    • nombres (requerido)
    • apellidos (requerido)
    """
    #Identificación
    telefono = models.CharField(max_length=11, verbose_name="Telefono", blank=True)

    #Estado y acceso
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=estados, default="A")
    mfa_habilitado = models.BooleanField(default=False, verbose_name="MFA_Habilitado")
    sesiones_activas = models.PositiveIntegerField(default=0)

    #Metadatos
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True)
    observaciones = models.TextField(max_length=500, verbose_name="Observaciones", blank=True)
    primer_acceso = models.BooleanField(default=False)
    class Meta:
        db_table = "usuario" #Nombre de la tabla cuando se cree
        verbose_name = "Usuario" #Nombre de la tabla en el panel Admin
        verbose_name_plural = "Usuarios" #Nombre en plural
    
    def save(self, *args, **kwargs):
        # Sincroniza estado con is_active
        if self.estado == "A":
            self.is_active = True
        else:
            self.is_active = False
        super().save(*args, **kwargs)
