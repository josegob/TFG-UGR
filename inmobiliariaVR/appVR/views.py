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
            Casa.objects.create(nombre_casa=request.POST['nombre_casa'], numero_habitaciones=request.POST['numero_habitaciones'])
            data["creado"] = True
            data["habitaciones"] = request.POST['numero_habitaciones']
        else:
            data["creado"] = False

        return JsonResponse(data, safe=False)
