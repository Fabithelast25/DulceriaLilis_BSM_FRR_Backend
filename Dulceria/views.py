from django.shortcuts import render


def redes(request):
    return render(request, 'InfoEmpresa/rrss.html')

def mision(request):
    return render(request, 'InfoEmpresa/mision.html')

def historia_empresa(request):
    return render(request, 'InfoEmpresa/historia_empresa.html')

def catalogo(request):
    return render(request, 'InfoEmpresa/catalogo.html')