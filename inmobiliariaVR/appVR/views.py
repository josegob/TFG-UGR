from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Casa
from .forms import CasaForm
# Create your views here.

class NuevaCasa(View):
    @staticmethod
    def post(request):
        data = {}
        form = CasaForm(request.POST, request.POST)
        if form.is_valid():
            casas = Casa.objects.filter(nombre_casa=request.POST['nombre_casa']).count()
            if(casas > 0):
                data["creado"] = False
                data["mensaje"] = "Ya existe una casa con ese nombre"
            else:
                Casa.objects.create(nombre_casa=request.POST['nombre_casa'], numero_habitaciones=request.POST['numero_habitaciones'])
                data["creado"] = True
                data["habitaciones"] = request.POST['numero_habitaciones']
        else:
            data["creado"] = False
            data["mensaje"] = "Revisa el formulario"

        return JsonResponse(data, safe=False)
