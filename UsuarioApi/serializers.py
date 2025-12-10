from rest_framework import serializers
from Panel_Usuarios.models import Usuario

class UsuarioSeralizar(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','username','first_name','last_name','email','telefono','estado','area_id','rol_id']