from django.shortcuts import render, redirect
from Panel_Usuarios.forms import UsuarioForm
from Panel_Usuarios.models import Usuario, Area, Rol

# Create your views here.
def usuarioAdd(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('usuarioAdd')
        else:
            print(form.errors)
    else:
        print("hola")
        form = UsuarioForm()
    
    return render(request, 'Usuarios/usuarioAdd.html', {'form':form})    