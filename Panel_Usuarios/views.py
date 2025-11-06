from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Panel_Usuarios.forms import UsuarioForm, RolForm, AreaForm
from Panel_Usuarios.models import Usuario, Area, Rol
from Panel_Usuarios.choices import estados
from django.contrib.auth.decorators import login_required

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
    nombres = request.GET.get('first_name', '')
    estado = request.GET.get('estado', '')
    rol = request.GET.get('rol', '')
    area = request.GET.get('area', '')

    usuarios = Usuario.objects.all()

    if nombres:
        usuarios = usuarios.filter(nombres__icontains=nombres)
    if estado and estado != "None":
        usuarios = usuarios.filter(estado=estado)
    if rol and rol != "None":
        usuarios = usuarios.filter(rol__id=rol)
    if area and area != "None":
        usuarios = usuarios.filter(area__id=area)

    roles = Rol.objects.all()
    areas = Area.objects.all()

    return render(request, 'Usuarios/usuarios.html', {
        'usuario': usuarios,
        'roles': roles,
        'areas': areas,
        'estados': estados,
        'first_name': nombres,
        'estado': estado,
        'rol': rol,
        'area': area,
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
            return redirect('usuarioUpdate', id=id)
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
    