from django.contrib import admin

from Panel_Usuarios.models import Rol, Usuario, Area

class RolAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "creado", "descripcion"]

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["username",
                    "email",
                    "first_name",
                    "last_name",
                    "telefono",
                    "rol",
                    "estado",
                    "mfa_habilitado",
                    "last_login",
                    "sesiones_activas",
                    "area",
                    "observaciones"]
    
class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "creado"]

admin.site.register(Rol, RolAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Area, AreaAdmin)


# Register your models here.
