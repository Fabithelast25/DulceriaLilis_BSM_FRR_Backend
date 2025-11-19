from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from Panel_Usuarios.models import Usuario, Rol, Area

@receiver(post_migrate)
def crear_superusuario(sender, **kwargs):
    # Evitar ejecutar esto en apps que no sean Panel_Usuarios
    if sender.label != "Panel_Usuarios":
        return
    
    # Configura aquí tus datos
    username_default = "Administrador"
    email_default = "Admin954@dulcerialilis.cl"
    password_default = "DuLc3R!aL1l!s"
    
    # Si ya existe, no se crea otra vez
    if Usuario.objects.filter(username=username_default).exists():
        return

    # Crear o buscar Rol
    rol_admin, _ = Rol.objects.get_or_create(nombre="Administrador")

    # Crear o buscar un área
    area_default, _ = Area.objects.get_or_create(nombre="Administración")

    # Crear superusuario
    Usuario.objects.create(
        username = username_default,
        email = email_default,
        first_name = "Admin",
        last_name = "Root",
        telefono = "000000000",
        rol = rol_admin,
        area = area_default,
        estado = "A",
        is_superuser = True,
        is_staff = True,
        password = make_password(password_default),
    )
