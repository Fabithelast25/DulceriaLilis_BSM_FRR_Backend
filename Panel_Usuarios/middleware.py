from django.shortcuts import redirect
from django.contrib import messages

def role_required(
    gestionar_usuarios=False,
    gestionar_productos=False,
    gestionar_proveedores=False,
    gestionar_inventario=False,
    ver_reportes=False,
    ver_usuarios=False,
    ver_productos=False,
    ver_proveedores=False,
):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            rol = getattr(request.user, "rol", None)
            if not rol:
                messages.error(request, "No tienes un rol asignado.")
                return redirect("no_autorizado")

            # Guardamos permisos requeridos
            permisos_requeridos = {
                "puede_gestionar_usuarios": gestionar_usuarios,
                "puede_gestionar_productos": gestionar_productos,
                "puede_gestionar_proveedores": gestionar_proveedores,
                "puede_gestionar_inventario": gestionar_inventario,
                "puede_ver_reportes": ver_reportes,
                "puede_ver_usuarios": ver_usuarios,
                "puede_ver_productos": ver_productos,
                "puede_ver_proveedores": ver_proveedores,
            }

            # Si NO se pidió ningún permiso → permitir
            if not any(permisos_requeridos.values()):
                return view_func(request, *args, **kwargs)

            # Verificar si el usuario cumple al menos un permiso
            for perm_name, required in permisos_requeridos.items():
                if required and getattr(rol, perm_name):
                    return view_func(request, *args, **kwargs)

            # Si no cumple ninguno
            messages.error(request, "No tienes permisos para acceder a esta página.")
            return redirect("no_autorizado")

        return wrapper
    return decorator

