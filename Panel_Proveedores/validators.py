# Panel_Proveedores/validators.py
import re
from django.core.exceptions import ValidationError

# Patrón: 7–8 dígitos seguidos de - y un dígito verificador (0–9 o K)
RUT_PATTERN = re.compile(r'^\d{7,8}-[\dkK]$')

def _rut_dv(num: str) -> str:
    """
    Calcula el dígito verificador (DV) de un RUT chileno.
    """
    reversed_digits = map(int, reversed(num))
    factors = [2, 3, 4, 5, 6, 7]
    s = 0
    for i, d in enumerate(reversed_digits):
        s += d * factors[i % 6]
    res = 11 - (s % 11)
    if res == 11:
        return "0"
    if res == 10:
        return "K"
    return str(res)

def normalize_rut(value: str) -> str:
    """
    Limpia y normaliza el RUT:
    - Elimina puntos y espacios
    - Pasa a mayúsculas
    - Si falta guion, lo inserta antes del DV
    """
    value = (value or "").strip().replace(".", "").replace(" ", "").upper()
    if "-" not in value and value.isalnum() and 7 <= len(value) <= 9:
        value = f"{value[:-1]}-{value[-1]}"
    return value

def validate_rut_chile(value: str):
    """
    Valida estrictamente que el RUT chileno tenga formato válido y DV correcto.
    """
    v = normalize_rut(value)
    if not RUT_PATTERN.match(v):
        raise ValidationError("Formato de RUT inválido. Use 12345678-9 o 12345678-K.")
    num, dv = v.split("-")
    if _rut_dv(num) != dv:
        raise ValidationError("RUT inválido: el dígito verificador no coincide.")

# Alias para compatibilidad con migraciones antiguas
def validate_rut_chile_or_nif(value: str):
    """
    Alias que apunta al validador estricto de RUT.
    Se mantiene para compatibilidad con migraciones viejas.
    """
    return validate_rut_chile(value)
