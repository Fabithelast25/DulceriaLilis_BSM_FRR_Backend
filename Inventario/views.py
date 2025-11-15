from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import movimientoForm
from .models import Movimiento
from .choices import tipos
from django.contrib.auth.decorators import login_required

# Create your views here.
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

def inventarioLista(request):
    movimientos = Movimiento.objects.all()
    
    return render(request, 'Inventario/inventarioLista.html', {
        'movimientos': movimientos,
    })