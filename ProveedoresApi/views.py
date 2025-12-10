# ProveedoresApi/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from Panel_Proveedores.models import Proveedor
from .serializers import ProveedorSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def proveedor_lista(request):
    """
    GET  -> lista todos los proveedores
    POST -> crea un proveedor nuevo
    """

    # ------- GET LISTA -------
    if request.method == 'GET':
        # Si tu modelo Rol tiene permisos específicos, descomenta y adapta:
        # if not getattr(request.user.rol, 'puede_ver_proveedores', False):
        #     return Response(
        #         {'error': 'No tienes permiso para ver proveedores'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)

    # ------- POST CREAR -------
    if request.method == 'POST':
        # if not getattr(request.user.rol, 'puede_gestionar_proveedores', False):
        #     return Response(
        #         {'error': 'No tienes permiso para crear proveedores'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = ProveedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # respeta validaciones y normalización del modelo
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def proveedor_detalle(request, pk):
    """
    GET    -> detalle de proveedor
    PUT    -> actualizar proveedor
    DELETE -> eliminar proveedor
    """
    try:
        proveedor = Proveedor.objects.get(pk=pk)
    except Proveedor.DoesNotExist:
        return Response(
            {'error': 'Proveedor no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

    # ------- GET DETALLE -------
    if request.method == 'GET':
        # if not getattr(request.user.rol, 'puede_ver_proveedores', False):
        #     return Response(
        #         {'error': 'No tienes permiso para ver este proveedor'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = ProveedorSerializer(proveedor)
        return Response(serializer.data)

    # ------- PUT EDITAR -------
    if request.method == 'PUT':
        # if not getattr(request.user.rol, 'puede_gestionar_proveedores', False):
        #     return Response(
        #         {'error': 'No tienes permiso para editar proveedores'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = ProveedorSerializer(proveedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ------- DELETE ELIMINAR -------
    if request.method == 'DELETE':
        # if not getattr(request.user.rol, 'puede_gestionar_proveedores', False):
        #     return Response(
        #         {'error': 'No tienes permiso para eliminar proveedores'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        proveedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
