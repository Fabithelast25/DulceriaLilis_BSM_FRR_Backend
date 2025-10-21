from django.shortcuts import render
from .models import productos

def historia_empresa(request):
    return render(request, 'InfoEmpresa/historia_empresa.html')

def catalogo(request):
    categorias = list(productos.keys())
    return render(request, 'InfoEmpresa/catalogo.html', {'categorias' : categorias})

def subcatalogo(request, categoria):
    productoCategoria = productos.get(categoria, [])
    return render(request, 'InfoEmpresa/subcatalogo.html', {
        'categoria' : categoria,
        'productos' : productoCategoria
    })

def detalle(request, categoria, nombreProducto):
    categoriaProductos = productos.get(categoria, [])
    producto = next((producto for producto in categoriaProductos if producto["nombre"] == nombreProducto), None)
    return render(request, 'InfoEmpresa/producto.html', {
        'producto' : producto,
        'categoria' : categoria
    })

def rrss(request):
    return render(request, 'InfoEmpresa/rrss.html')

def login(request):
    return render(request, "login.html")

def recuperarContraseña(request):
    return render(request, 'recuperarContraseña.html')

def crearContraseña(request):
    return render(request, 'crearContraseña.html')