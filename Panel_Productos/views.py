from django.shortcuts import render, redirect, get_object_or_404
from openpyxl import Workbook
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from Panel_Productos.forms import ProductoForm,CategoriaForm,UnidadMedidaForm
from django.contrib import messages
from django.core.paginator import Paginator
from Panel_Productos.models import Producto,Categoria,UnidadMedida
from django.contrib.auth.decorators import login_required
from Panel_Usuarios.middleware import role_required
# Create your views here.

#MANEJO DE PRODUCTOS
@login_required(login_url='login')
@role_required(gestionar_productos=True)
def productosAdd(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            # Si 'punto_reorden' está vacío, asignamos stock_minimo
            if not form.cleaned_data['punto_reorden']:
                form.cleaned_data['punto_reorden'] = form.cleaned_data.get('stock_minimo', 0)

            form.save()
            messages.success(request, 'Producto agregado correctamente.')

        # ❗ IMPORTANTE: si es inválido, NO crear un nuevo form.
        # El mismo form con errores se envía de vuelta
        return render(request, 'Productos/productos_add.html', {'form': form})

    else:
        # GET → crear formulario vacío
        form = ProductoForm()

    return render(request, 'Productos/productos_add.html', {'form': form})


@login_required(login_url='login')
@role_required(gestionar_productos=True)
def mostrarProductos(request):
    def clean_param(param):
        if param is None:
            return ""
        return param.strip()

    # Capturar los filtros
    buscar = request.GET.get("nombres", "")
    selected_categoria = request.GET.get("categoria", "")
    selected_unidad = request.GET.get("unidad_medida", "")
    per_page = clean_param(request.GET.get("per_page", "10"))

    productos =  Producto.objects.all().order_by('id') 

    # Aplicar los filtros
    if buscar:
        productos = productos.filter(Q(nombre__icontains=buscar) | Q(sku__icontains=buscar))
    if selected_categoria:
        productos = productos.filter(categoria_id=selected_categoria)
    if selected_unidad:
        productos = productos.filter(Q(uom_compra_id=selected_unidad) | Q(uom_venta_id=selected_unidad))

     # Verificar el estado de "bajo stock" en cada producto
    for producto in productos:
        if producto.stock_actual <= producto.punto_reorden:
            producto.bajo_stock = True
        else:
            producto.bajo_stock = False

    # Paginación
    hide_pagination = False
    if per_page == "all":
        productos_page = productos
        hide_pagination = True  # No mostrar paginador si se muestran todos los productos
    else:
        try:
            per_page_int = int(per_page)
        except ValueError:
            per_page_int = 10  # Valor predeterminado de paginación
        paginator = Paginator(productos, per_page_int)
        page = request.GET.get("page")
        productos_page = paginator.get_page(page)

        # Si solo hay una página, ocultamos la paginación
        if productos_page.paginator.num_pages == 1:
            hide_pagination = True


    # Si es AJAX → solo renderizamos la tabla
    if request.GET.get("ajax") == "1":
        return render(request, "Productos/partial_tabla_productos.html", {
            "productos": productos_page,
            "nombres": buscar,
            "categoria": selected_categoria,
            "unidad_medida": selected_unidad,
            "per_page_actual": per_page,
            "hide_pagination": hide_pagination
        })

    # Renderizar la vista completa
    return render(request, "Productos/productos.html", {
        "productos": productos_page,
        "categorias": Categoria.objects.all(),
        "unidades_medida": UnidadMedida.objects.all(),
        "nombres": buscar,
        "categoria": selected_categoria,
        "unidad_medida": selected_unidad,
        "per_page_actual": per_page,
        "hide_pagination": hide_pagination  # Añadir esto para controlar la visibilidad del paginador
    })


def cargarProductos(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)
    form = ProductoForm(instance=producto)

    return render(request,'Productos/update_producto.html',{'form':form,'categoria':producto})

@login_required(login_url='login')
@role_required(gestionar_productos=True)
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
                # Convertimos errores a dict simple
                errors = {k: [str(m) for m in v] for k,v in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
            messages.error(request, "Hubo un error al actualizar el producto.")
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'Productos/update_producto.html', {'form': form, 'producto': producto})

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
@login_required(login_url='login')
@role_required(gestionar_productos=True)
def categoriasAdd(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
        else:
            # NO SE USA messages.error
            return render(request, 'Productos/categorias/categorias_add.html', {'form': form})
    else:
        form = CategoriaForm()

    return render(request, 'Productos/categorias/categorias_add.html', {'form': form})


def mostrarCategorias(request):
    categorias = Categoria.objects.all()
    data = {
        'categorias' : categorias,
    }

    return render(request,'Productos/categorias/categorias.html',data)

@login_required(login_url='login')
@role_required(gestionar_productos=True)
def cargarCategorias(request,categoria_id):
    categoria = get_object_or_404(Categoria,id=categoria_id)
    form = CategoriaForm(instance=categoria)

    return render(request,'Productos/categorias/update_categoria.html',{'form':form,'categoria':categoria})

@login_required(login_url='login')
@role_required(gestionar_productos=True)
def modificarCategorias(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    mensaje_exito = False  # <- bandera para JS
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            mensaje_exito = True
        else:
            messages.error(request, "Revisa los campos, hay errores en el formulario.")
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'Productos/categorias/update_categoria.html', {
        'form': form,
        'mensaje_exito': mensaje_exito
    })


def categoriaDelete(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('categorias')

#MANEJO DE UNIDADES DE MEDIDA
@login_required(login_url='login')
@role_required(gestionar_productos=True)
def unidadesAdd(request):
    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidad de medida creada correctamente.')
        else:
            return render(request, 'Productos/unidades_medida/unidad_medida_add.html', {'form': form})
    else:
        form = UnidadMedidaForm()
    return render(request, 'Productos/unidades_medida/unidad_medida_add.html', {'form': form})

@login_required(login_url='login')
@role_required(gestionar_productos=True)
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
@login_required(login_url='login')
@role_required(gestionar_productos=True)
def modificarUnidades(request,id):
    unidad_medida = get_object_or_404(UnidadMedida, id=id)
    mensaje_exito = False  # <- bandera para JS

    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST, instance=unidad_medida)
        if form.is_valid():
            form.save()
            mensaje_exito = True
        else:
            messages.error(request, "Revisa los campos, hay errores en el formulario.")
    else:
        form = UnidadMedidaForm(instance=unidad_medida)

    return render(request, 'Productos/unidades_medida/update_unidad_medida.html', {
        'form': form,
        'mensaje_exito': mensaje_exito
    })

def unidadesDelete(request, unidad_medida_id):
    unidad_medida = get_object_or_404(UnidadMedida, id=unidad_medida_id)
    unidad_medida.delete()
    return redirect('unidades-medida')


