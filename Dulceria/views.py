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

        # Intentar autenticación por username directo
        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                # Si no encuentra por username, buscar por email
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            auth_login(request, user)
            return redirect('usuarioLista')  # redirige donde quieras
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


#Views para recuperar contraseña
def recuperarContraseña(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
            codigo = get_random_string(length=6, allowed_chars='0123456789')

            # Guardar código en la BD
            CodigoRecuperacion.objects.create(usuario=usuario, codigo=codigo)

            # Enviar correo
            send_mail(
                'Código de recuperación',
                f'Tu código de recuperación es: {codigo}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Se ha enviado un código de recuperación a tu correo.")
            return redirect('verificarCodigo')
        except Usuario.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")
    return render(request, 'recuperarContraseña.html')

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
    email = request.session.get('email_recuperacion')
    if not email:
        messages.error(request, "Sesión inválida.")
        return redirect('recuperarContraseña')

    if request.method == "POST":
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')
        if password == confirmar:
            usuario = Usuario.objects.get(email=email)
            usuario.password = make_password(password)
            usuario.save()
            del request.session['email_recuperacion']
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect('login')
        else:
            messages.error(request, "Las contraseñas no coinciden.")
    return render(request, 'crearContraseña.html')