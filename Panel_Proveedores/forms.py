# Panel_Proveedores/forms.py
from django import forms
from .models import Proveedor, MONEDA_CHOICES, ESTADO_PROVEEDOR, CONDICIONES_PAGO_CHOICES, OfertaProveedor
from .validators import normalize_rut, RUT_PATTERN, _rut_dv

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            "rut_nif", "razon_social", "nombre_fantasia",
            "email", "telefono", "sitio_web",
            "direccion", "ciudad", "pais",
            "condiciones_pago", "moneda",
            "contacto_principal_nombre", "contacto_principal_email", "contacto_principal_telefono",
            "estado", "observaciones",
        ]
        widgets = {
            "rut_nif": forms.TextInput(attrs={"class": "form-control", "placeholder": "12.345.678-K"}),
            "razon_social": forms.TextInput(attrs={"class": "form-control", "maxlength": 255}),
            "nombre_fantasia": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "proveedor@correo.cl"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "+56912345678", "inputmode": "tel"}),
            "sitio_web": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://www.ejemplo.cl"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control"}),
            "pais": forms.TextInput(attrs={"class": "form-control"}),
            "condiciones_pago": forms.Select(attrs={"class": "form-select"}, choices=CONDICIONES_PAGO_CHOICES),
            "moneda": forms.Select(attrs={"class": "form-select"}, choices=MONEDA_CHOICES),
            "contacto_principal_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "contacto_principal_email": forms.EmailInput(attrs={"class": "form-control"}),
            "contacto_principal_telefono": forms.TextInput(attrs={"class": "form-control", "inputmode": "tel"}),
            "estado": forms.Select(attrs={"class": "form-select"}, choices=ESTADO_PROVEEDOR),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class OfertaProveedorForm(forms.ModelForm):
    class Meta:
        model = OfertaProveedor
        fields = ["producto", "proveedor", "costo", "lead_time_dias", "min_lote", "descuento_pct", "preferente"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-select"}),
            "proveedor": forms.Select(attrs={"class": "form-select"}),
            "costo": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
            "lead_time_dias": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "1"}),
            "min_lote": forms.NumberInput(attrs={"class": "form-control", "min": "0.01", "step": "0.01"}),
            "descuento_pct": forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "100", "step": "0.01"}),
            "preferente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    # --- Limpiezas & validaciones de campo ---
    def clean_rut_nif(self):
        v = normalize_rut(self.cleaned_data.get("rut_nif"))
        # Si cumple formato RUT chileno, verificar DV aquí también (doble capa con el model)
        if RUT_PATTERN.match(v):
            num, dv = v.split("-")
            if _rut_dv(num) != dv:
                raise forms.ValidationError("RUT inválido: el dígito verificador no coincide.")
        return v

    def clean_razon_social(self):
        v = (self.cleaned_data.get("razon_social") or "").strip()
        if len(v) < 3:
            raise forms.ValidationError("La razón social debe tener al menos 3 caracteres.")
        return v

    def clean_email(self):
        v = (self.cleaned_data.get("email") or "").strip().lower()
        # bloquea dominios obviamente inválidos
        if v.endswith("@example.com"):
            raise forms.ValidationError("Usa un email real, no dominios de ejemplo.")
        return v

    def clean_sitio_web(self):
        v = self.cleaned_data.get("sitio_web")
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise forms.ValidationError("La URL debe comenzar con http:// o https://")
        return v

    # --- Validación cruzada ---
    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get("contacto_principal_nombre")
        email = cleaned.get("contacto_principal_email")
        tel = cleaned.get("contacto_principal_telefono")

        if nombre and not (email or tel):
            raise forms.ValidationError(
                "Si indicas un nombre de contacto, debes ingresar email o teléfono del contacto."
            )
        return cleaned
