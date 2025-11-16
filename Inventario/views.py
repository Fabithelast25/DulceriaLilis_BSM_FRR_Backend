from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import movimientoForm
from .models import Movimiento
from .choices import tipos
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def movimientoAdd(request):
    if request.method == 'POST':
        form = movimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.save()
            messages.success(request, "Movimiento creado correctamente")
        else:
            messages.error(request, "Error al crear el movimiento. Verifique que todos los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = movimientoForm()


    return render(request, 'Inventario/inventarioAdd.html', {'form': form})

@login_required(login_url='login')
def inventarioLista(request):
    movimientos = Movimiento.objects.all()
    
    return render(request, 'Inventario/inventarioLista.html', {
        'movimientos': movimientos,
    })

@login_required(login_url='login')
def movimientoUpdate(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    if request.method == 'POST':
        form = movimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, "Movimiento actualizado correctamente.")
        else:
            messages.error(request, "Hubo un error al actualizar, verifique que los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = movimientoForm(instance=movimiento)
    return render(request, 'Inventario/inventarioUpdate.html', {'form': form})

def movimientoDelete(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    movimiento.delete()
    return redirect('inventarioLista')