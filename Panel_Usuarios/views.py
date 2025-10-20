from django.shortcuts import render, redirect, get_object_or_404
from Panel_Usuarios.forms import UsuarioForm, RolForm, AreaForm
from Panel_Usuarios.models import Usuario, Area, Rol
from Panel_Usuarios.choices import estados

# Create your views here.

#CRUD DE USUARIOS
def usuarioAdd(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarioLista')
        else:
            print(form.errors)
    else:
        form = UsuarioForm()
    
    return render(request, 'Usuarios/usuarioAdd.html', {'form':form})

def usuarioLista(request):
    nombres = request.GET.get('nombres', '')
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
        'usuarios': usuarios,
        'roles': roles,
        'areas': areas,
        'estados': estados,
        'nombres': nombres,
        'estado': estado,
        'rol': rol,
        'area': area,
    })

def usuarioDelete(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('usuarioLista')

def usuarioUpdate(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarioLista')
        else:
            print(form.errors)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'Usuarios/usuarioUpdate.html', {'form': form})

#CRUD ROLES
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
    