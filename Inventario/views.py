import openpyxl
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import movimientoForm
from .models import Movimiento
from .choices import tipos
from django.contrib.auth.decorators import login_required
from Panel_Productos.models import Producto
from django.db import transaction
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from Panel_Usuarios.middleware import role_required
# Create your views here.
@login_required(login_url='login')
@role_required(gestionar_inventario=True)
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
                        if producto.stock_actual > producto.stock_maximo:
                            messages.error(request, "No puede superar el stock maximo del producto")
                            return render(request, 'Inventario/inventarioAdd.html', {'form': form})
                            

                    elif movimiento.tipo == "S":  # Salida
                        if producto.stock_actual < cantidad:
                            messages.error(request, f"Stock insuficiente. Stock actual: {producto.stock_actual}")
                            return render(request, "Inventario/inventarioAdd.html", {"form": form})
                        producto.stock_actual -= cantidad

                    elif movimiento.tipo == "D":  # Devolución
                        producto.stock_actual += cantidad
                        if producto.stock_actual > producto.stock_maximo:
                            messages.error(request, "No puede superar el stock maximo del producto")
                            return render(request, 'Inventario/inventarioAdd.html', {'form': form})

                    elif movimiento.tipo == "A":  # Ajuste
                        # Puedes decidir aquí si permites negativo o no
                        producto.stock_actual += cantidad  # Si permites ajustar con signos positivos/negativos
                        if producto.stock_actual > producto.stock_maximo:
                            messages.error(request, "No puede superar el stock maximo del producto")
                            return render(request, 'Inventario/inventarioAdd.html', {'form': form})

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
@role_required(gestionar_inventario=True, ver_reportes=True)
def inventarioLista(request):
    # 1️⃣ Obtener queryset base
    movimientos = Movimiento.objects.all().order_by('-fecha')

    # 2️⃣ Obtener filtros GET
    busqueda = request.GET.get('busqueda', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    fecha_desde_str = request.GET.get('fecha_desde', '').strip()
    fecha_hasta_str = request.GET.get('fecha_hasta', '').strip()

    # 3️⃣ Aplicar filtros de búsqueda y tipo
    if busqueda:
        movimientos = movimientos.filter(producto__nombre__icontains=busqueda)
    if tipo:
        movimientos = movimientos.filter(tipo=tipo)

    # 4️⃣ Filtrar fechas (convertir a datetime y crear rango)
    if fecha_desde_str:
        try:
            fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d')
            movimientos = movimientos.filter(fecha__gte=fecha_desde)
        except ValueError:
            pass  # ignorar si la fecha está mal escrita

    if fecha_hasta_str:
        try:
            # sumamos un día para incluir todo el día seleccionado
            fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d') + timedelta(days=1)
            movimientos = movimientos.filter(fecha__lt=fecha_hasta)
        except ValueError:
            pass  # ignorar si la fecha está mal escrita

    # 5️⃣ Paginación
    per_page = request.GET.get('per_page', '10')  # traer como string para comparar
    if per_page == '1000':  # opción "Todos"
        movimientos_paginados = list(movimientos)  # no paginar
    else:
        paginator = Paginator(movimientos, int(per_page))
        page_number = request.GET.get('page')
        movimientos_paginados = paginator.get_page(page_number)

    # 6️⃣ Pasar variables al template
    context = {
        'movimientos': movimientos_paginados,
        'busqueda_actual': busqueda,
        'tipo_actual': tipo,
        'fecha_desde_actual': fecha_desde_str,
        'fecha_hasta_actual': fecha_hasta_str,
        'per_page_actual': per_page,  # siempre como string
    }

    return render(request, 'Inventario/inventarioLista.html', context)

@login_required(login_url='login')
@role_required(gestionar_inventario=True)
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
                if producto_nuevo.stock_actual > producto_nuevo.stock_maximo:
                    messages.error(request, "No puede superar el stock maximo del producto")
                    return render(request, 'Inventario/inventarioUpdate.html', {'form': form})
            elif nuevo_tipo == "S":
                if producto_nuevo.stock_actual < nueva_cantidad:
                    messages.error(request, "Stock insuficiente para aplicar la salida.")
                    return render(request, 'Inventario/inventarioUpdate.html', {'form': form})
                producto_nuevo.stock_actual -= nueva_cantidad
            elif nuevo_tipo == "D":
                producto_nuevo.stock_actual += nueva_cantidad
                if producto.stock_actual > producto.stock_maximo:
                            messages.error(request, "No puede superar el stock maximo del producto")
                            return render(request, 'Inventario/inventarioUpdate.html', {'form': form})
            elif nuevo_tipo == "A":
                producto_nuevo.stock_actual += nueva_cantidad  # Si manejas ajustes +/-
                if producto.stock_actual > producto.stock_maximo:
                            messages.error(request, "No puede superar el stock maximo del producto")
                            return render(request, 'Inventario/inventarioUpdate.html', {'form': form})
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

@login_required(login_url='login')
@role_required(gestionar_inventario=True)
def movimientoDelete(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    movimiento.delete()
    return redirect('inventarioLista')

def exportar_movimientos_excel(request):
    # ----------------------------------------------------------------------
    # 1) CAPTURAR FILTROS DESDE LA URL (GET)
    # ----------------------------------------------------------------------
    tipo = request.GET.get("tipo", "").strip()              # Obtiene el tipo (I, S, A, D)
    fecha_desde = request.GET.get("fecha_desde", "").strip() # Fecha inicial
    fecha_hasta = request.GET.get("fecha_hasta", "").strip() # Fecha final

    # ----------------------------------------------------------------------
    # 2) CONSULTA BASE: TRAE TODOS LOS MOVIMIENTOS CON SUS RELACIONES
    # ----------------------------------------------------------------------
    movimientos = Movimiento.objects.select_related(
        "producto", "proveedor", "bodega"
    ).all()

    # ----------------------------------------------------------------------
    # 3) FILTRO POR TIPO DE MOVIMIENTO
    # ----------------------------------------------------------------------
    if tipo:
        movimientos = movimientos.filter(tipo__iexact=tipo)  
        # Si viene "I", filtra solo Ingresos; si viene "S", solo Salidas, etc.

    # ----------------------------------------------------------------------
    # 4) FILTRO POR FECHA DESDE
    # ----------------------------------------------------------------------
    if fecha_desde:
        movimientos = movimientos.filter(fecha__date__gte=fecha_desde)
        # Trae movimientos cuya fecha sea >= fecha_desde

    # ----------------------------------------------------------------------
    # 5) FILTRO POR FECHA HASTA
    # ----------------------------------------------------------------------
    if fecha_hasta:
        movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)
        # Trae movimientos cuya fecha sea <= fecha_hasta

    # ----------------------------------------------------------------------
    # 6) CREAR ARCHIVO EXCEL
    # ----------------------------------------------------------------------
    wb = openpyxl.Workbook()   # Crea libro
    ws = wb.active             # Hoja activa
    ws.title = "Movimientos"   # Nombre de la hoja

    # Encabezados del Excel
    headers = [
        "Fecha",
        "Tipo",
        "Cantidad",
        "Producto",
        "Proveedor",
        "Bodega",
        "Lote",
        "Serie",
        "Fecha Vencimiento",
        "Documento Referencia",
        "Motivo",
        "Observaciones",
    ]
    ws.append(headers)  # Coloca la fila de encabezados

    # ----------------------------------------------------------------------
    # 7) LLENAR EXCEL FILA POR FILA
    # ----------------------------------------------------------------------
    for m in movimientos:
        ws.append([
            m.fecha.strftime("%Y-%m-%d %H:%M"),                       # Fecha formateada
            dict(m._meta.get_field("tipo").choices).get(m.tipo, m.tipo),  # Traduce I,S,A,D a palabras
            m.cantidad,                                               # Cantidad movida
            m.producto.nombre if m.producto else "—",                 # Producto
            m.proveedor.razon_social if m.proveedor else "—",         # Proveedor
            m.bodega.nombre if m.bodega else "—",                     # Bodega
            m.lote or "",                                             # Lote si existe
            m.serie or "",                                            # Serie si existe
            m.fechaVencimiento.strftime("%Y-%m-%d") if m.fechaVencimiento else "",
            m.doc_referencia,                                         # Documento referencia
            m.motivo,                                                 # Motivo
            m.observaciones or "",                                    # Observaciones
        ])

    # ----------------------------------------------------------------------
    # 8) RESPUESTA HTTP PARA DESCARGAR EXCEL
    # ----------------------------------------------------------------------
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="movimientos_filtrados.xlsx"'

    wb.save(response)  # Guarda el archivo en la respuesta
    return response    # Devuelve el Excel
