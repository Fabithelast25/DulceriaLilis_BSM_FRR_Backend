from django.shortcuts import render, redirect, get_object_or_404
from Panel_Productos.forms import ProductoForm,CategoriaForm,UnidadMedidaForm
from django.contrib import messages
from Panel_Productos.models import Producto,Categoria,UnidadMedida

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
            messages.success(request, 'Producto creado correctamente.')
        else:
            print(form.errors)
            messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = ProductoForm()
    return render(request, 'Productos/productos_add.html', {'form': form})

def mostrarProductos(request):
    productos = Producto.objects.all()
    for producto in productos:
        if producto.stock_actual <= producto.punto_reorden:
            producto.bajo_stock = True
        else:
            producto.bajo_stock = False
    data = {
        'productos' : productos,
    }

    return render(request,'Productos/productos.html',data)

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
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('producto-modificado', id=id)
        else:
            messages.error(request, "Hubo un error al actualizar, verifique que los campos se hayan ingresado correctamente")
            print(form.errors)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'Productos/update_producto.html', {'form': form})

def productoDelete(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('productos')

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
