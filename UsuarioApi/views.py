from django.shortcuts import render
from Panel_Usuarios.models import Usuario
from django.http import JsonResponse
from UsuarioApi.serializers import UsuarioSeralizar
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def usuariosApi(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios':list(
        usuarios.values('id','username','first_name','last_name','email','telefono','estado','area_id','rol_id')
    )}
    return JsonResponse(data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def usuario_lista(request):
    if request.method == 'GET':
        if not request.user.rol.puede_ver_usuarios:
            return Response({'error': 'No tienes permiso para ver usuarios'}, status=status.HTTP_403_FORBIDDEN)
        
        usuarios = Usuario.objects.all()
        serializer = UsuarioSeralizar(usuarios, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        if not request.user.rol.puede_gestionar_usuarios:
            return Response({'error': 'No tienes permiso para crear usuarios'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSeralizar(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def usuario_detalle(request, pk):
    try:
        usuario = Usuario.objects.get(id=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if not request.user.rol.puede_ver_usuarios:
            return Response({'error': 'No tienes permiso para ver este usuario'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSeralizar(usuario)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        if not request.user.rol.puede_gestionar_usuarios:
            return Response({'error': 'No tienes permiso para editar usuarios'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSeralizar(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if not request.user.rol.puede_gestionar_usuarios:
            return Response({'error': 'No tienes permiso para eliminar usuarios'}, status=status.HTTP_403_FORBIDDEN)
        
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    