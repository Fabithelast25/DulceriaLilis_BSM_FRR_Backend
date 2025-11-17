from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Panel_Usuarios.forms import UsuarioForm, RolForm, AreaForm
from Panel_Usuarios.models import Usuario, Area, Rol
from Panel_Usuarios.choices import estados
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

#Importaciones para que cuando se cree un usuario se envie un email y contraseña automatica
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings
import string, random
# Create your views here.

#Generador de claves aleatorias
def generar_contrasenia():
    # Genera una contraseña aleatoria de 10 caracteres
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


#CRUD DE USUARIOS
@login_required(login_url='login')
def usuarioAdd(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            contrasenia = generar_contrasenia()
            usuario.password = make_password(contrasenia)  # Encripta la contraseña
            usuario.save()
            send_mail(
                "Bienvenido a Dulceria Lilis",
                f"Hola {usuario.first_name} {usuario.last_name}, tu contraseña temporal es: {contrasenia}\nPor favor cámbiala en la opción 'Recuperar contraseña'.",
                settings.DEFAULT_FROM_EMAIL,
                [usuario.email],
                fail_silently=False,
            )

            messages.success(request, "Usuario creado correctamente")
        else:
            messages.error(request, "Error al crear el usuario. Verifique que todos los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = UsuarioForm()
    
    return render(request, 'Usuarios/usuarioAdd.html', {'form':form})

@login_required(login_url='login')
def usuarioLista(request):
    def clean_param(param):
        if param is None:
            return ""
        return param.strip()

    username = clean_param(request.GET.get("username", ""))
    rol = clean_param(request.GET.get("rol", ""))
    estado = clean_param(request.GET.get("estado", ""))
    per_page = clean_param(request.GET.get("per_page", "10"))

    usuarios = Usuario.objects.all()

    # Filtrar Username
    if username:
        usuarios = usuarios.filter(username__icontains=username)

    # Filtrar Rol
    if rol:
        usuarios = usuarios.filter(rol_id=rol)

    # Filtrar Estado
    if estado:
        usuarios = usuarios.filter(estado=estado)

    # Paginación
    if per_page == "all":
        usuarios_page = usuarios
    else:
        try:
            per_page_int = int(per_page)
        except ValueError:
            per_page_int = 10
        paginator = Paginator(usuarios, per_page_int)
        page = request.GET.get("page")
        usuarios_page = paginator.get_page(page)

    # Obtener roles para el select
    roles = Rol.objects.all()

    # Obtener estados para el select (reutilizando tu variable de choices)
    return render(request, "Usuarios/usuarios.html", {
        "usuarios": usuarios_page,
        "roles": roles,
        "estados": estados,
        "username_actual": username,
        "rol_actual": rol,
        "estado_actual": estado,
        "per_page_actual": per_page,
    })
    
def usuarioDelete(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('usuarioLista')

@login_required(login_url='login')
def usuarioUpdate(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
       
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
        else:
            messages.error(request, "Hubo un error al actualizar, verifique que los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'Usuarios/usuarioUpdate.html', {'form': form})

#CRUD ROLES
@login_required(login_url='login')
def rolAdd(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rolLista')
        else:
            print(form.errors)
    else:
        form = RolForm()
    
    return render(request, 'Usuarios/roles/rolAdd.html', {'form':form})

def rolDelete(request, id):
    rol = get_object_or_404(Rol, id=id)
    rol.delete()
    return redirect('rolLista')

@login_required(login_url='login')
def rolUpdate(request, id):
    rol = get_object_or_404(Rol, id=id)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('rolLista')
        else:
            print(form.errors)
    else:
        form = RolForm(instance=rol)
    return render(request, 'Usuarios/roles/rolUpdate.html', {'form': form})

@login_required(login_url='login')
def rolLista(request):
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    roles = Rol.objects.all()

    if fecha_inicio:
        roles = roles.filter(creado__gte=fecha_inicio)  # mayor o igual a fecha_inicio
    if fecha_fin:
        roles = roles.filter(creado__lte=fecha_fin)  # menor o igual a fecha_fin

    return render(request, 'Usuarios/roles/roles.html', {
        'roles': roles,
    })
    
#CRUD AREAS
@login_required(login_url='login')
def areaAdd(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('areaLista')
        else:
            print(form.errors)
    else:
        form = AreaForm()
    
    return render(request, 'Usuarios/areas/areaAdd.html', {'form':form})

def areaDelete(request, id):
    area = get_object_or_404(Area, id=id)
    area.delete()
    return redirect('areaLista')

@login_required(login_url='login')
def areaUpdate(request, id):
    area = get_object_or_404(Area, id=id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('areaLista')
        else:
            print(form.errors)
    else:
        form = AreaForm(instance=area)
    return render(request, 'Usuarios/areas/areaUpdate.html', {'form': form})

@login_required(login_url='login')
def areaLista(request):
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    areas = Area.objects.all()
    
    if fecha_inicio:
        areas = areas.filter(creado__gte=fecha_inicio)  # mayor o igual a fecha_inicio
    if fecha_fin:
        areas = areas.filter(creado__lte=fecha_fin)  # menor o igual a fecha_fin

    return render(request, 'Usuarios/areas/areas.html', {
        'areas': areas,
    })
    