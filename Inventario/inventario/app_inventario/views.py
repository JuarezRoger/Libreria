from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'inicio.html')

def inventario_view(request):
    return render(request, 'inventario.html')

def reportes_view(request):
    return render(request, 'reportes.html')

def historial_tecnico_view(request):
    return render(request, 'historial_tecnico.html')

def lista_de_repuestos_view(request):
    return render(request, 'lista_de_repuestos.html')