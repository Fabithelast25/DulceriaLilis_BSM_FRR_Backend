from django.shortcuts import render, redirect, get_object_or_404
from Panel_Usuarios.forms import UsuarioForm
from Panel_Usuarios.models import Usuario, Area, Rol
from Panel_Usuarios.choices import estados

# Create your views here.
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
