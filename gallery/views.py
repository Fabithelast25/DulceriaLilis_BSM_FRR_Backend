from django.shortcuts import render, redirect
from .models import GalleryImage
from .forms import ImageForm
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def gallery_view(request):

    # 1️⃣ Obtener imágenes de la BD ordenadas nuevas primero
    db_images = GalleryImage.objects.all().order_by('-uploaded_at')

    # 2️⃣ Obtener imágenes estáticas desde /static/gallery/default
    static_path = os.path.join(settings.BASE_DIR, 'static/gallery/default')
    static_images = []

    if os.path.exists(static_path):
        for file in os.listdir(static_path):
            static_images.append(f'/static/gallery/default/{file}')

    # 3️⃣ Procesar subida de imagen
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)  # crea el form con datos enviados

        if form.is_valid():  # valida el formulario
            form.save()      # guarda la imagen en BD y carpeta media
            return redirect('gallery')  # recarga la página (evita repost)

    else:
        form = ImageForm()  # si es GET, crea formulario vacío

    # 4️⃣ Renderizar template
    return render(request, 'gallery/gallery.html', {
        'db_images': db_images,
        'static_images': static_images,
        'form': form
    })