from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import movimientoForm
from .models import Movimiento
from .choices import tipos
from django.contrib.auth.decorators import login_required
from Panel_Productos.models import Producto
from django.db import transaction
# Create your views here.
@login_required(login_url='login')
def movimientoAdd(request):
    if request.method == "POST":
        form = movimientoForm(request.POST)

        if form.is_valid() :
            try:
                with transaction.atomic():

                    # 1. Guardamos el movimiento SIN grabarlo aún en base de datos
                    movimiento = form.save(commit=False)

                    # 2. Obtenemos el producto
                    producto = Producto.objects.get(id=request.POST.get("producto"))

                    # 3. Obtenemos la cantidad
                    cantidad = int(form.cleaned_data["cantidad"])

                    if movimiento.tipo == "I":  # Ingreso
                        producto.stock_actual += cantidad

                    elif movimiento.tipo == "S":  # Salida
                        if producto.stock_actual < cantidad:
                            messages.error(request, f"Stock insuficiente. Stock actual: {producto.stock_actual}")
                            return render(request, "Inventario/inventarioAdd.html", {"form": form})
                        producto.stock_actual -= cantidad

                    elif movimiento.tipo == "D":  # Devolución
                        producto.stock_actual += cantidad

                    elif movimiento.tipo == "A":  # Ajuste
                        # Puedes decidir aquí si permites negativo o no
                        producto.stock_actual += cantidad  # Si permites ajustar con signos positivos/negativos

                    # 6. Guardamos stock actualizado
                    producto.save()

                    # 7. Guardamos el movimiento ahora sí
                    movimiento.producto = producto
                    movimiento.save()

                    messages.success(request, "Movimiento registrado correctamente")

            except Exception as e:
                messages.error(request, f"Error al guardar movimiento: {e}")

    else:
        form = movimientoForm()

    return render(request, "Inventario/inventarioAdd.html", {"form": form})

@login_required(login_url='login')
def inventarioLista(request):
    movimientos = Movimiento.objects.all()
    
    return render(request, 'Inventario/inventarioLista.html', {
        'movimientos': movimientos,
    })

@login_required(login_url='login')
@login_required(login_url='login')
def movimientoUpdate(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)

    # Guardamos la información anterior
    producto_original = movimiento.producto
    tipo_original = movimiento.tipo
    cantidad_original = movimiento.cantidad

    if request.method == 'POST':
        form = movimientoForm(request.POST, instance=movimiento)
        if form.is_valid():

            # === 1) REVERTIR MOVIMIENTO ANTERIOR ===
            producto = producto_original

            if tipo_original == "I":  # Ingreso
                producto.stock_actual -= cantidad_original
            elif tipo_original == "S":  # Salida
                producto.stock_actual += cantidad_original
            elif tipo_original == "D":  # Devolución
                producto.stock_actual -= cantidad_original
            elif tipo_original == "A":  # Ajuste
                producto.stock_actual -= cantidad_original  # Ajuste positivo o negativo
            # T = Transferencia aún no implementada

            producto.save()

            # === 2) GUARDAR NUEVO MOVIMIENTO ===
            movimiento_nuevo = form.save(commit=False)
            producto_nuevo = movimiento_nuevo.producto
            nueva_cantidad = movimiento_nuevo.cantidad
            nuevo_tipo = movimiento_nuevo.tipo

            # === 3) APLICAR NUEVO EFECTO EN STOCK ===
            if nuevo_tipo == "I":
                producto_nuevo.stock_actual += nueva_cantidad
            elif nuevo_tipo == "S":
                if producto_nuevo.stock_actual < nueva_cantidad:
                    messages.error(request, "Stock insuficiente para aplicar la salida.")
                    return render(request, 'Inventario/inventarioUpdate.html', {'form': form})
                producto_nuevo.stock_actual -= nueva_cantidad
            elif nuevo_tipo == "D":
                producto_nuevo.stock_actual += nueva_cantidad
            elif nuevo_tipo == "A":
                producto_nuevo.stock_actual += nueva_cantidad  # Si manejas ajustes +/-
            # T = Transferencia pendiente

            producto_nuevo.save()
            movimiento_nuevo.save()

            messages.success(request, "Movimiento actualizado correctamente.")
        else:
            messages.error(request, "Hubo un error al actualizar.")
            print(form.errors)
    else:
        form = movimientoForm(instance=movimiento)

    return render(request, 'Inventario/inventarioUpdate.html', {'form': form})


def movimientoDelete(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    movimiento.delete()
    return redirect('inventarioLista')