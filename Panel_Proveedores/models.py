# Panel_Proveedores/models.py
from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from Panel_Productos.models import Producto
from .validators import validate_rut_chile, normalize_rut  # RUT chileno estricto
from django.utils import timezone

ESTADO_PROVEEDOR = (("ACTIVO", "Activo"), ("BLOQUEADO", "Bloqueado"))

MONEDA_CHOICES = (
    ("CLP", "Peso Chileno (CLP)"),
    ("USD", "Dólar (USD)"),
    ("EUR", "Euro (EUR)"),
)

CONDICIONES_PAGO_CHOICES = (
    ("CONTADO", "Contado"),
    ("15D", "15 días"),
    ("30D", "30 días"),
    ("45D", "45 días"),
    ("60D", "60 días"),
    ("TRANSFERENCIA", "Transferencia inmediata"),
)

telefono_validator = RegexValidator(
    regex=r'^\+?\d{8,15}$',
    message="El teléfono debe tener 8 a 15 dígitos y opcionalmente un + al inicio."
)

ciudad_pais_validator = RegexValidator(
    regex=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ .'-]{2,}$",
    message="Solo letras, espacios y .'- (mínimo 2 caracteres)."
)


class Proveedor(models.Model):
    # Solo RUT chileno válido (estricto)
    rut_nif = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_rut_chile],
        verbose_name="RUT",
        help_text="Formato: 12345678-9 o 12345678-K",
    )
    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, blank=True, null=True)

    email = models.EmailField(validators=[EmailValidator()])
    telefono = models.CharField(max_length=30, blank=True, null=True, validators=[telefono_validator])
    sitio_web = models.URLField(blank=True, null=True)

    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=128, blank=True, null=True, validators=[ciudad_pais_validator])
    pais = models.CharField(max_length=64, default="Chile", validators=[ciudad_pais_validator])

    condiciones_pago = models.CharField(
        max_length=120, choices=CONDICIONES_PAGO_CHOICES, default="30D"
    )
    moneda = models.CharField(max_length=8, choices=MONEDA_CHOICES, default="CLP")

    contacto_principal_nombre = models.CharField(max_length=120, blank=True, null=True)
    contacto_principal_email = models.EmailField(blank=True, null=True)
    contacto_principal_telefono = models.CharField(
        max_length=30, blank=True, null=True, validators=[telefono_validator]
    )

    estado = models.CharField(max_length=10, choices=ESTADO_PROVEEDOR, default="ACTIVO")
    observaciones = models.TextField(blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["razon_social"]

    def __str__(self):
        return f"{self.razon_social} ({self.rut_nif})"

    def save(self, *args, **kwargs):
        # Normalizaciones suaves para mantener datos limpios
        if self.rut_nif:
            self.rut_nif = normalize_rut(self.rut_nif)
        if self.razon_social:
            self.razon_social = self.razon_social.strip()
        if self.nombre_fantasia:
            self.nombre_fantasia = self.nombre_fantasia.strip()
        if self.pais:
            self.pais = self.pais.strip().title()
        if self.ciudad:
            self.ciudad = self.ciudad.strip().title()
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)


class OfertaProveedor(models.Model):
    """Relación Producto–Proveedor con condiciones comerciales."""
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="ofertas_proveedor"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name="ofertas"
    )
    # Validación a nivel de campo (evita negativos)
    costo = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    lead_time_dias = models.PositiveIntegerField(
        default=7, validators=[MinValueValidator(0)]
    )
    min_lote = models.DecimalField(
        max_digits=12, decimal_places=2, default=1, validators=[MinValueValidator(0.01)]
    )
    descuento_pct = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    preferente = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Oferta de Proveedor"
        verbose_name_plural = "Ofertas de Proveedor"
        unique_together = ("producto", "proveedor")
        constraints = [
            # Red de seguridad a nivel BD
            models.CheckConstraint(
                check=models.Q(costo__gte=0), name="oferta_costo_no_negativo"
            ),
            models.CheckConstraint(
                check=models.Q(lead_time_dias__gte=0), name="oferta_lead_time_no_negativo"
            ),
            models.CheckConstraint(
                check=models.Q(min_lote__gt=0), name="oferta_min_lote_gt_0"
            ),
            models.CheckConstraint(
                check=(models.Q(descuento_pct__gte=0) & models.Q(descuento_pct__lte=100)) |
                      models.Q(descuento_pct__isnull=True),
                name="oferta_descuento_pct_0_100_or_null",
            ),
        ]

    def __str__(self):
        return f"{self.proveedor.razon_social} → {self.producto} (${self.costo})"

    # Validación de modelo (mensajes claros en formularios/admin)
    def clean(self):
        errors = {}
        if self.costo is not None and self.costo < 0:
            errors["costo"] = "El costo no puede ser negativo."
        if self.lead_time_dias is not None and self.lead_time_dias < 0:
            errors["lead_time_dias"] = "El lead time (días) no puede ser negativo."
        if self.min_lote is not None and self.min_lote <= 0:
            errors["min_lote"] = "El mínimo de lote debe ser mayor que 0."
        if self.descuento_pct is not None and self.descuento_pct < 0:
            errors["descuento_pct"] = "El descuento no puede ser negativo."
        if errors:
            raise ValidationError(errors)

    # Forzar validación siempre, incluso guardados manuales
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
