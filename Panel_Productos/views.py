from django.shortcuts import render, redirect, get_object_or_404
from openpyxl import Workbook
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from Panel_Productos.forms import ProductoForm,CategoriaForm,UnidadMedidaForm
from django.contrib import messages
from Panel_Productos.models import Producto,Categoria,UnidadMedida
from django.contrib.auth.decorators import login_required
# Create your views here.

#MANEJO DE PRODUCTOS
def productosAdd(request):
    form = ProductoForm(request.POST)
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Si 'punto_reorden' está vacío, asignamos el valor de 'stock_minimo'
            if not form.cleaned_data['punto_reorden']:
                form.cleaned_data['punto_reorden'] = form.cleaned_data.get('stock_minimo', 0)  # Asigna 'stock_minimo' si está vacío
            form.save()
            messages.success(request, 'Producto agregado correctamente.')
        else:
            print(form.errors)
    else:
        form = ProductoForm()
    return render(request, 'Productos/productos_add.html', {'form': form})


from django.db.models import Q
from .models import Producto, Categoria, UnidadMedida  # ajusta nombres si los tienes diferentes

def mostrarProductos(request):
    # Capturar búsqueda desde el input "nombres"
    buscar = request.GET.get("nombres", "")

    # capturar filtros actuales (para mantener el select seleccionado en el template)
    selected_categoria = request.GET.get("categoria", "")
    selected_unidad = request.GET.get("unidad_medida", "")

    # Construir queryset base y aplicar búsqueda
    productos = Producto.objects.all()
    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) |
            Q(sku__icontains=buscar)
        )

    # Aplicar filtros de categoria / unidad si vienen (opcional, sigue funcionando el botón Filtrar)
    if selected_categoria:
        productos = productos.filter(categoria_id=selected_categoria)
    if selected_unidad:
        # dependiendo de tu modelo puedes tener uom_compra_id o uom_venta_id; aquí filtramos en ambas
        productos = productos.filter(Q(uom_compra_id=selected_unidad) | Q(uom_venta_id=selected_unidad))

    # Mantén tu lógica EXACTA de bajo_stock (no la modifiqué)
    for producto in productos:
        if producto.stock_actual <= producto.punto_reorden:
            producto.bajo_stock = True
        else:
            producto.bajo_stock = False

    # Obtener listas para los selects
    categorias = Categoria.objects.all()
    unidades_medida = UnidadMedida.objects.all()

    # Si la petición es AJAX, devuelve solo las filas de la tabla
    if request.GET.get("ajax") == "1":
        return render(request, "Productos/partial_tabla_productos.html", {"productos": productos})

    # Render normal cuando no es AJAX (incluimos las listas para los selects)
    ctx = {
        "productos": productos,
        "categorias": categorias,
        "unidades_medida": unidades_medida,
        "nombres": buscar,
        "categoria": selected_categoria,
        "unidad_medida": selected_unidad,
    }
    return render(request, "Productos/productos.html", ctx)


def cargarProductos(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)
    form = ProductoForm(instance=producto)

    return render(request,'Productos/update_producto.html',{'form':form,'categoria':producto})


def modificarProductos(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            form.save()
            # Si es AJAX, devolvemos JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            # Si no es AJAX, redirige normalmente
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productos')
        else:
            # Errores
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            messages.error(request, "Hubo un error al actualizar el producto.")
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'Productos/update_producto.html', {'form': form})

def productoDelete(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('productos')

def exportar_productos_excel(request):

    # --------- FILTROS EXACTOS DE TU VISTA mostrarProductos ---------
    buscar = request.GET.get("nombres", "")
    selected_categoria = request.GET.get("categoria", "")
    selected_unidad = request.GET.get("unidad_medida", "")

    productos = Producto.objects.all()

    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) |
            Q(sku__icontains=buscar)
        )

    if selected_categoria:
        productos = productos.filter(categoria_id=selected_categoria)

    if selected_unidad:
        productos = productos.filter(
            Q(uom_compra_id=selected_unidad) |
            Q(uom_venta_id=selected_unidad)
        )

    # --------- LÓGICA DE BAJO STOCK ---------
    for producto in productos:
        producto.bajo_stock = (
            producto.stock_actual <= (producto.punto_reorden or 0)
        )

    # --------- CREAR ARCHIVO EXCEL ---------
    wb = Workbook()
    ws = wb.active
    ws.title = "Productos"

    # --------- ENCABEZADOS ---------
    ws.append([
        "SKU",
        "Nombre",
        "Descripción",
        "Categoría",
        "Marca",
        "Modelo",
        "UOM Compra",
        "UOM Venta",
        "Factor Conversión",
        "Costo Estándar",
        "Costo Promedio",
        "Precio Venta",
        "IVA (%)",
        "Stock Mínimo",
        "Stock Máximo",
        "Punto Reorden",
        "Stock Actual",
        "Bajo Stock",
        "Perecible",
        "Control por lote",
        "Control por serie",
        "Imagen URL",
        "Ficha técnica URL",
    ])

    # --------- LLENAR DATOS ---------
    for p in productos:
        ws.append([
            p.sku,
            p.nombre,
            p.descripcion,
            p.categoria.nombre_completo if p.categoria else "",
            p.marca,
            p.modelo,
            p.uom_compra.nombre_completo if p.uom_compra else "",
            p.uom_venta.nombre_completo if p.uom_venta else "",
            p.factor_conversion,
            p.costo_estandar,
            p.costo_promedio,
            p.precio_venta,
            p.impuesto_iva,
            p.stock_minimo,
            p.stock_maximo,
            p.punto_reorden,
            p.stock_actual,
            "Sí" if p.bajo_stock else "No",
            "Sí" if p.perishable else "No",
            "Sí" if p.control_por_lote else "No",
            "Sí" if p.control_por_serie else "No",
            p.imagen_url,
            p.ficha_tecnica_url,
        ])

    # --------- RESPUESTA HTTP ---------
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="productos_filtrados.xlsx"'

    wb.save(response)
    return response


#MANEJO DE CATEGORÍAS
def categoriasAdd(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria creada correctamente.')
        else:
            print(form.errors)
            messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = CategoriaForm()
    return render(request, 'Productos/categorias/categorias_add.html', {'form': form})


def mostrarCategorias(request):
    categorias = Categoria.objects.all()
    data = {
        'categorias' : categorias,
    }

    return render(request,'Productos/categorias/categorias.html',data)


def cargarCategorias(request,categoria_id):
    categoria = get_object_or_404(Categoria,id=categoria_id)
    form = CategoriaForm(instance=categoria)

    return render(request,'Productos/categorias/update_categoria.html',{'form':form,'categoria':categoria})


def modificarCategorias(request,id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
       
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('categoria-modificada', id=id)
        else:
            messages.error(request, "Hubo un error al actualizar, verifique que los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'Productos/categorias/update_categoria.html', {'form': form})

def categoriaDelete(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('categorias')

#MANEJO DE UNIDADES DE MEDIDA
def unidadesAdd(request):
    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidad de medida creada correctamente.')
        else:
            print(form.errors)
            messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = UnidadMedidaForm()
    return render(request, 'Productos/unidades_medida/unidad_medida_add.html', {'form': form})


def mostrarUnidades(request):
    unidades = UnidadMedida.objects.all()
    data = {
        'unidades' : unidades,
    }

    return render(request,'Productos/unidades_medida/unidades_medida.html',data)

def cargarUnidades(request,unidad_medida_id):
    unidad_medida = get_object_or_404(UnidadMedida,id=unidad_medida_id)
    form = UnidadMedidaForm(instance=unidad_medida)

    return render(request,'Productos/unidades_medida/update_unidad_medida.html',{'form':form,'unidad_medida':unidad_medida})

def modificarUnidades(request,id):
    unidad_medida = get_object_or_404(UnidadMedida, id=id)
    if request.method == 'POST':
       
        form = UnidadMedidaForm(request.POST, instance=unidad_medida)
        if form.is_valid():
            form.save()
            messages.success(request, "Unidad de medida actualizada correctamente.")
            return redirect('unidad-medida-modificada', id=id)
        else:
            messages.error(request, "Hubo un error al actualizar, verifique que los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = UnidadMedidaForm(instance=unidad_medida)
    return render(request, 'Productos/unidades_medida/update_unidad_medida.html', {'form': form})

def unidadesDelete(request, unidad_medida_id):
    unidad_medida = get_object_or_404(UnidadMedida, id=unidad_medida_id)
    unidad_medida.delete()
    return redirect('unidades-medida')


