from django.core.exceptions import ValidationError
import re

def validar_telefono_chileno(value):
    # Verifica que el número de teléfono comience con '569' y tenga exactamente 11 caracteres según formato.
    if not re.match(r'^\d+$', value):
        raise ValidationError('El número de teléfono solo debe contener números.')

    # 2️⃣ Verificamos que empiece con 569
    if not value.startswith('569'):
        raise ValidationError('El número de teléfono debe comenzar con 569.')