from django.shortcuts import render, redirect
from .models import productos
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .models import Usuario, CodigoRecuperacion
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import datetime
from django.http import JsonResponse, HttpResponse
import csv
import io
from Panel_Productos.models import Producto
from Panel_Proveedores.models import Proveedor
from django.contrib.auth.decorators import login_required
import re
from django.contrib.sessions.models import Session

User = get_user_model()

def historia_empresa(request):
    return render(request, 'InfoEmpresa/historia_empresa.html')

def catalogo(request):
    categorias = list(productos.keys())
    return render(request, 'InfoEmpresa/catalogo.html', {'categorias' : categorias})

def subcatalogo(request, categoria):
    productoCategoria = productos.get(categoria, [])
    return render(request, 'InfoEmpresa/subcatalogo.html', {
        'categoria' : categoria,
        'productos' : productoCategoria
    })

def detalle(request, categoria, nombreProducto):
    categoriaProductos = productos.get(categoria, [])
    producto = next((producto for producto in categoriaProductos if producto["nombre"] == nombreProducto), None)
    return render(request, 'InfoEmpresa/producto.html', {
        'producto' : producto,
        'categoria' : categoria
    })

def rrss(request):
    return render(request, 'InfoEmpresa/rrss.html')

User = get_user_model()

def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:

            # 🔥 VALIDAR PRIMER ACCESO
            if not user.primer_acceso:
                request.session['primer_acceso_email'] = user.email
                return redirect('recuperarContraseña')

            # Si ya tiene primer acceso habilitado → entra normal
            auth_login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


def logout_view(request):
    # Cerrar sesión actual
    logout(request)

    # Borrar todas las sesiones del usuario (impide que Django lo mantenga “recordado”)
    request.session.flush()

    return redirect('login')


def recuperarContraseña(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()
        
    email_session = request.session.get('primer_acceso_email')
    ocultar_email = False

    if email_session:
        ocultar_email = True

    if request.method == "POST":
        email = email_session if email_session else request.POST.get('email')

        try:
            usuario = Usuario.objects.get(email=email)
            codigo = get_random_string(length=6, allowed_chars='0123456789')

            CodigoRecuperacion.objects.create(usuario=usuario, codigo=codigo)

            send_mail(
                'Código de recuperación',
                f'Tu código de recuperación es: {codigo}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Se ha enviado un código a tu correo.")
            return redirect('verificarCodigo')

        except Usuario.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")

    return render(request, 'recuperarContraseña.html', {
        'ocultar_email': ocultar_email,
        'email_session': email_session
    })

def verificarCodigo(request):
    if request.method == "POST":
        email = request.POST.get('email')
        codigo = request.POST.get('codigo')

        try:
            usuario = Usuario.objects.get(email=email)
            registro = CodigoRecuperacion.objects.filter(usuario=usuario, codigo=codigo).last()

            if registro and not registro.expirado():
                request.session['email_recuperacion'] = email
                registro.delete()  # se borra el código al validarlo
                return redirect('crearContraseña')
            else:
                messages.error(request, "Código inválido o expirado.")
        except Usuario.DoesNotExist:
            messages.error(request, "Correo no válido.")
    return render(request, 'verificarCodigo.html')

def crearContraseña(request):
    # Obtiene el email guardado en la sesión
    email = request.session.get('email_recuperacion')

    # Si no hay email, redirige a recuperar contraseña
    if not email:
        return redirect('recuperarContraseña')

    # Obtiene al usuario asociado al email
    usuario = Usuario.objects.get(email=email)

    # Si se envió el formulario por POST
    if request.method == "POST":
        # Captura de valores del formulario
        nueva = request.POST.get('password')
        confirmar = request.POST.get('confirmar')

        # Compara que ambas contraseñas sean iguales
        if nueva != confirmar:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'crearContraseña.html')

        # ----------- VALIDACIÓN ROBUSTA -----------
        # Expresión regular para validar fortaleza
        patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{12,}$'

        # Verifica si la contraseña NO cumple el patrón
        if not re.match(patron, nueva):
            messages.error(request,
                "La contraseña debe tener al menos 12 caracteres, una mayúscula, una minúscula y un símbolo."
            )
            return render(request, 'crearContraseña.html')
        # -------------------------------------------

        # Asigna la nueva contraseña usando hashing
        usuario.set_password(nueva)

        # Marca primer acceso como habilitado
        usuario.primer_acceso = True

        # Guarda los cambios en el usuario
        usuario.save()

        # Limpia los datos de recuperación en sesión
        request.session.pop('email_recuperacion', None)
        request.session.pop('primer_acceso_email', None)

        # Mensaje de éxito
        messages.success(request, "Contraseña actualizada. Ahora puedes iniciar sesión.")
        return redirect('login')

    # Si es GET, simplemente muestra el formulario
    return render(request, 'crearContraseña.html')


# Views para el Dashboard
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

# ---------- Helpers ----------
def _last_12_month_labels():
    base = now().date().replace(day=1)
    months = []
    for i in range(11, -1, -1):
        y = base.year if base.month - i > 0 else base.year - 1
        m = (base.month - i) if (base.month - i) > 0 else (12 + (base.month - i))
        months.append((y, m))
    labels = [f"{y}-{m:02d}" for y, m in months]
    return months, labels

def _month_range(y, m):
    from calendar import monthrange
    start = datetime(y, m, 1)
    end = datetime(y, m, monthrange(y, m)[1], 23, 59, 59)
    return start, end

# ---------- APIs ----------
def api_summary(request):
    total_productos = Producto.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_usuarios = User.objects.count()

    try:
        umbral = int(request.GET.get('umbral', '10'))
    except ValueError:
        umbral = 10

    low_stock = Producto.objects.filter(stock_actual__lt=umbral).count()

    return JsonResponse({
        "total_productos": total_productos,
        "total_proveedores": total_proveedores,
        "total_usuarios": total_usuarios,
        "productos_stock_bajo": low_stock,
    })

def api_products_by_category(request):
    qs = (
        Producto.objects
        .values('categoria__nombre_completo')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    values = [x['total'] for x in qs]
    # ¡OJO! El comp de arriba debe ser una list comprehension:
    labels = [x['categoria__nombre_completo'] or 'Sin categoría' for x in qs]
    return JsonResponse({"labels": labels, "values": values})

def api_products_monthly(request):
    months, labels = _last_12_month_labels()
    series = []
    for y, m in months:
        start, end = _month_range(y, m)
        series.append(Producto.objects.filter(creado__range=(start, end)).count())
    return JsonResponse({"labels": labels, "values": series})

def api_providers_monthly(request):
    """
    Requiere que Proveedor tenga un campo DateTime `creado`.
    Si aún no lo tienes, agrega en Panel_Proveedores.models.Proveedor:
        creado = models.DateTimeField(auto_now_add=True)
    y corre makemigrations/migrate.
    """
    months, labels = _last_12_month_labels()
    # Si no tienes 'creado', te devuelvo 0s para no romper la UI
    if not hasattr(Proveedor, 'creado'):
        return JsonResponse({"labels": labels, "values": [0]*12})

    series = []
    for y, m in months:
        start, end = _month_range(y, m)
        series.append(Proveedor.objects.filter(creado__range=(start, end)).count())
    return JsonResponse({"labels": labels, "values": series})

def api_users_monthly(request):
    months, labels = _last_12_month_labels()
    series = []
    for y, m in months:
        start, end = _month_range(y, m)
        series.append(User.objects.filter(date_joined__range=(start, end)).count())
    return JsonResponse({"labels": labels, "values": series})

def api_low_stock(request):
    umbral = int(request.GET.get('umbral', 10))
    qs = (
        Producto.objects
        .filter(stock_actual__lt=umbral)
        .values('id', 'nombre', 'categoria__nombre_completo', 'stock_actual')
    )
    # Normalizo claves para calzar con el template
    rows = [{
        "id": x["id"],
        "nombre": x["nombre"],
        "categoria": x["categoria__nombre_completo"],
        "stock": x["stock_actual"],
    } for x in qs]
    return JsonResponse({"rows": rows})

# ---------- Exportaciones ----------
def export_csv(request, resource: str):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{resource}.csv"'
    writer = csv.writer(response)

    if resource == 'productos':
        writer.writerow(['ID', 'SKU', 'Nombre', 'Categoría', 'Stock', 'Precio Venta', 'Creado'])
        for p in Producto.objects.select_related('categoria').all():
            writer.writerow([
                p.id, p.sku, p.nombre,
                getattr(p.categoria, 'nombre_completo', ''),
                p.stock_actual,
                p.precio_venta or '',
                p.creado,
            ])

    elif resource == 'proveedores':
        # Si agregas `creado` se exporta; si no, queda vacío
        writer.writerow(['ID', 'RUT', 'Razón Social', 'Email', 'Teléfono', 'Ciudad', 'País', 'Estado', 'Creado'])
        for pr in Proveedor.objects.all():
            writer.writerow([
                pr.id, pr.rut_nif, pr.razon_social, pr.email or '', pr.telefono or '',
                pr.ciudad or '', pr.pais or '', pr.estado,
                getattr(pr, 'creado', ''),  # soporta ambos casos
            ])

    elif resource == 'usuarios':
        writer.writerow(['ID', 'Username', 'Email', 'Rol', 'Estado', 'Fecha Registro', 'Staff'])
        for u in User.objects.select_related(getattr(User, 'rol', None)).all():
            rol = getattr(u, 'rol', None)
            writer.writerow([u.id, u.username, u.email, getattr(rol, 'nombre', ''), getattr(u, 'estado', ''), u.date_joined, u.is_staff])

    elif resource == 'low_stock':
        umbral = int(request.GET.get('umbral', 10))
        writer.writerow(['ID', 'Nombre', 'Categoría', 'Stock'])
        for p in Producto.objects.filter(stock_actual__lt=umbral).select_related('categoria'):
            writer.writerow([p.id, p.nombre, getattr(p.categoria, 'nombre_completo', ''), p.stock_actual])

    else:
        return HttpResponse("Recurso no válido", status=400)

    return response

def export_excel(request, resource: str):
    try:
        import openpyxl
    except ImportError:
        return HttpResponse("Instala openpyxl: pip install openpyxl", status=500)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = resource.upper()

    if resource == 'productos':
        ws.append(['ID', 'SKU', 'Nombre', 'Categoría', 'Stock', 'Precio Venta', 'Creado'])
        for p in Producto.objects.select_related('categoria').all():
            ws.append([
                p.id, p.sku, p.nombre,
                getattr(p.categoria, 'nombre_completo', ''),
                p.stock_actual,
                p.precio_venta or '',
                p.creado,
            ])

    elif resource == 'proveedores':
        ws.append(['ID', 'RUT', 'Razón Social', 'Email', 'Teléfono', 'Ciudad', 'País', 'Estado', 'Creado'])
        for pr in Proveedor.objects.all():
            ws.append([
                pr.id, pr.rut_nif, pr.razon_social, pr.email or '', pr.telefono or '',
                pr.ciudad or '', pr.pais or '', pr.estado,
                getattr(pr, 'creado', ''),
            ])

    elif resource == 'usuarios':
        ws.append(['ID', 'Username', 'Email', 'Rol', 'Estado', 'Fecha Registro', 'Staff'])
        for u in User.objects.all():
            rol = getattr(u, 'rol', None)
            ws.append([u.id, u.username, u.email, getattr(rol, 'nombre', ''), getattr(u, 'estado', ''), u.date_joined, u.is_staff])

    elif resource == 'low_stock':
        umbral = int(request.GET.get('umbral', 10))
        ws.append(['ID', 'Nombre', 'Categoría', 'Stock'])
        for p in Producto.objects.filter(stock_actual__lt=umbral).select_related('categoria'):
            ws.append([p.id, p.nombre, getattr(p.categoria, 'nombre_completo', ''), p.stock_actual])
    else:
        return HttpResponse("Recurso no válido", status=400)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    resp = HttpResponse(
        buf.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = f'attachment; filename="{resource}.xlsx"'
    return resp

def no_autorizado(request):
    return render(request, "no_autorizado.html")
