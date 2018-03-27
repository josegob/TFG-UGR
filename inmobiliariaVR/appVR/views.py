from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Casa, ImagenesHabitaciones
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


class FileUploadView(View):
    @staticmethod
    def post(request):
        data = {}
        # data["asd"] = a.get_download_link()

        for i in range(0, int(request.POST["numero_ficheros"])):
            nueva_habitacion = ImagenesHabitaciones(imagen_habitacion=request.FILES["file_to_upload"+str(i)], nombre_habitacion=request.POST["nombre_habitacion"+str(i)], nombre_casa=request.POST["nombre_casa"])
            if nueva_habitacion:
                nueva_habitacion.save()
                data['message'] = 'Habitacion guardada correctamente'
            else:
                data['message'] = 'Error al procesar las habitaciones'
                return JsonResponse(data)

        return JsonResponse(data)
