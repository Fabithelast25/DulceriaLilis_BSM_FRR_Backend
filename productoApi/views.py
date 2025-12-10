from django.shortcuts import render
from Panel_Productos.models import Producto
from django.http import JsonResponse
from productoApi.serializers import ProductoSerializar
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def productosApi(request):
    productos = Producto.objects.all()
    data = {
        'productos':list(
            productos.values('sku','ean_upc','nombre','descripcion','categoria','marca','modelo','uom_compra','uom_venta','factor_conversion',
                             'costo_estandar','costo_promedio','precio_venta','impuesto_iva','stock_minimo','stock_maximo','punto_reorden',
                             'perishable','control_por_lote','control_por_serie','imagen_url','ficha_tecnica_url','stock_actual',
                             'alerta_bajo_stock','alerta_por_vencer','creado')
        )
    }
    return JsonResponse(data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def producto_listado(request):
    if request.method == 'GET':
        if not request.user.rol.puede_ver_productos:
            return Response({'error': 'No tienes permiso para ver productos'}, status=status.HTTP_403_FORBIDDEN)
        productos = Producto.objects.all()
        serializer = ProductoSerializar(productos,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        if not request.user.rol.puede_gestionar_productos:
            return Response({'error': 'No tienes permiso para crear productos'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductoSerializar(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def producto_detalle(request,pk):
    try:
        producto = Producto.objects.get(id=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if not request.user.rol.puede_ver_productos:
            return Response({'error': 'No tienes permiso para ver este producto'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductoSerializar(producto)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        if not request.user.rol.puede_gestionar_productos:
            return Response({'error': 'No tienes permiso para editar este producto'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductoSerializar(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)