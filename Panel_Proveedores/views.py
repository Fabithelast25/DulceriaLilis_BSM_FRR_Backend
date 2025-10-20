# Panel_Proveedores/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django import forms
from django.db import IntegrityError

from .models import Proveedor, ESTADO_PROVEEDOR, MONEDA_CHOICES, CONDICIONES_PAGO_CHOICES, OfertaProveedor
from .forms import OfertaProveedorForm

# =========================
# Formulario (ModelForm)
# =========================
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'rut_nif', 'razon_social', 'nombre_fantasia',
            'email', 'telefono', 'sitio_web',
            'direccion', 'ciudad', 'pais',
            'condiciones_pago', 'moneda',
            'contacto_principal_nombre', 'contacto_principal_email', 'contacto_principal_telefono',
            'estado', 'observaciones'
        ]
        widgets = {
            'rut_nif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-K o NIF'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'proveedor@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'value': 'Chile'}),
            'condiciones_pago': forms.Select(attrs={'class': 'form-select'}, choices=CONDICIONES_PAGO_CHOICES),
            'moneda': forms.Select(attrs={'class': 'form-select'}, choices=MONEDA_CHOICES),
            'contacto_principal_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_principal_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_principal_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'estado': forms.Select(attrs={'class': 'form-select'}, choices=ESTADO_PROVEEDOR),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # Normalizaciones suaves extra (el modelo ya valida, esto mejora UX)
    def clean_rut_nif(self):
        v = self.cleaned_data['rut_nif']
        return v.replace(' ', '').upper() if v else v

    def clean_pais(self):
        v = self.cleaned_data.get('pais')
        return v.strip().title() if v else v

    def clean_ciudad(self):
        v = self.cleaned_data.get('ciudad')
        return v.strip().title() if v else v


# =========================
# Vistas CRUD + Listado
# =========================
def lista_proveedores(request):
    """
    Listado con búsqueda y filtros:
    - q: busca por rut_nif, razón social, nombre_fantasia, email, ciudad, país
    - estado: ACTIVO/BLOQUEADO
    - moneda: CLP/USD/EUR...
    Paginación de 10 por página (param 'page').
    """
    qs = Proveedor.objects.all()

    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    moneda = request.GET.get('moneda', '').strip()

    if q:
        qs = qs.filter(
            Q(rut_nif__icontains=q) |
            Q(razon_social__icontains=q) |
            Q(nombre_fantasia__icontains=q) |
            Q(email__icontains=q) |
            Q(ciudad__icontains=q) |
            Q(pais__icontains=q)
        )

    if estado:
        qs = qs.filter(estado=estado)

    if moneda:
        qs = qs.filter(moneda=moneda)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'q': q,
        'estado': estado,
        'moneda': moneda,
        'ESTADO_PROVEEDOR': ESTADO_PROVEEDOR,
        'MONEDA_CHOICES': MONEDA_CHOICES,
    }
    return render(request, 'proveedores/lista.html', context)


def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect('lista_proveedores')
        messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/form.html', {'form': form, 'accion': 'Agregar'})


def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('lista_proveedores')
        messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/form.html', {'form': form, 'accion': 'Editar'})


def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado.')
        return redirect('lista_proveedores')
    return render(request, 'proveedores/eliminar.html', {'proveedor': proveedor})

# ---------- OFERTAS: LISTA ----------
def lista_ofertas(request):
    q = (request.GET.get("q") or "").strip()
    preferente = request.GET.get("preferente")  # '1', '0' o None

    ofertas = OfertaProveedor.objects.select_related("producto", "proveedor")

    if q:
        ofertas = ofertas.filter(
            Q(producto__nombre__icontains=q) |
            Q(producto__sku__icontains=q) |
            Q(proveedor__razon_social__icontains=q)
        )
    if preferente in ("0", "1"):
        ofertas = ofertas.filter(preferente=(preferente == "1"))

    ofertas = ofertas.order_by("proveedor__razon_social", "producto__nombre")

    paginator = Paginator(ofertas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "proveedores/ofertas_lista.html",
        {"page_obj": page_obj, "q": q, "preferente": preferente},
    )

# ---------- OFERTAS: AGREGAR ----------
def agregar_oferta(request):
    if request.method == "POST":
        form = OfertaProveedorForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # ejecuta full_clean() del modelo y respeta unique_together
                messages.success(request, "Oferta creada correctamente.")
                return redirect("lista_ofertas")
            except IntegrityError:
                form.add_error(None, "Ya existe una oferta para ese producto con ese proveedor.")
    else:
        form = OfertaProveedorForm()

    return render(
        request,
        "proveedores/ofertas_form.html",
        {"form": form, "accion": "Agregar"},
    )

# ---------- OFERTAS: EDITAR ----------
def editar_oferta(request, pk):
    oferta = get_object_or_404(OfertaProveedor, pk=pk)
    if request.method == "POST":
        form = OfertaProveedorForm(request.POST, instance=oferta)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Oferta actualizada correctamente.")
                return redirect("lista_ofertas")
            except IntegrityError:
                form.add_error(None, "Ya existe una oferta para ese producto con ese proveedor.")
    else:
        form = OfertaProveedorForm(instance=oferta)

    return render(
        request,
        "proveedores/ofertas_form.html",
        {"form": form, "accion": "Editar"},
    )

# ---------- OFERTAS: ELIMINAR ----------
def eliminar_oferta(request, pk):
    oferta = get_object_or_404(OfertaProveedor, pk=pk)
    if request.method == "POST":
        oferta.delete()
        messages.success(request, "Oferta eliminada correctamente.")
        return redirect("lista_ofertas")

    return render(
        request,
        "proveedores/ofertas_eliminar.html",
        {"oferta": oferta},
    )