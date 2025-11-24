from django.core.exceptions import ValidationError

def cantidad_positivo(cantidad):
    if int(cantidad) <= 0:
        raise ValidationError("La cantidad no puede ser menor o igual a 0.")