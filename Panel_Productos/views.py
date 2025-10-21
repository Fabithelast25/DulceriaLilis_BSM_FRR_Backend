from django.shortcuts import render, redirect, get_object_or_404
from Panel_Productos.forms import ProductoForm,CategoriaForm,UnidadMedidaForm
from django.contrib import messages
from Panel_Productos.models import Producto,Categoria,UnidadMedida

# Create your views here.

#MANEJO DE PRODUCTOS
def productosAdd(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('gestion-producto')  # o a donde quieras redirigir
        messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = ProductoForm()
    return render(request, 'Productos/productos_add.html', {'form': form})

def mostrarProductos(request):
    productos = Producto.objects.all()
    data = {
        'productos' : productos,
    }

    return render(request,'Productos/productos.html',data)

def cargarProductos(request,producto_id):
    producto = get_object_or_404(Categoria,id=producto_id)
    form = ProductoForm(instance=producto)

    return render(request,'Productos/update_producto.html',{'form':form,'categoria':producto})

def modificarProductos(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST,instance=producto)
        if form.is_valid():
            form.save()
            return redirect('/productos/')
    else:
        form = ProductoForm()

    return render(request,'Productos/productos_add.html',{'form':form})


#MANEJO DE CATEGORÍAS
def categoriasAdd(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria creada correctamente.')
            return redirect('gestion-categoria')  # o a donde quieras redirigir
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

def modificarCategorias(request,categoria_id):
    categoria = get_object_or_404(Categoria,id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST,instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('/categorias/')
    else:
        form = CategoriaForm()

    return render(request,'Productos/categorias/categorias_add.html',{'form':form})


#MANEJO DE UNIDADES DE MEDIDA
def unidadesAdd(request):
    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidad de medida creada correctamente.')
            return redirect('gestion-unidad-medida')  # o a donde quieras redirigir
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

def modificarUnidades(request,unidad_medida_id):
    unidad_medida = get_object_or_404(UnidadMedida,id=unidad_medida_id)

    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST,instance=unidad_medida)
        if form.is_valid():
            form.save()
            return redirect('/unidades-medida/')
    else:
        form = UnidadMedidaForm()

    return render(request,'Productos/unidades-medida/unidades_medida_add.html',{'form':form})