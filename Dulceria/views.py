from django.shortcuts import render


def redes(request):
    return render(request, 'InfoEmpresa/rrss.html')

def mision(request):
    return render(request, 'InfoEmpresa/mision.html')