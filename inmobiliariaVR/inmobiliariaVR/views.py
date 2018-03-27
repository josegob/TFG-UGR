from django.shortcuts import render
from appVR.models import ImagenesHabitaciones
from appVR.models import Casa
from django.views import View
from django.http import JsonResponse

def main_page(request):
    return render(request, 'inmobiliariaVR/main_page.html')


def sample(request, path):
    return render(request, 'inmobiliariaVR/habitacion_basica.html', {'link': path})


def previa(request):

    lista_casas = []
    c = Casa.objects.all()
    for a in c:
        lista_casas.append(a.nombre_casa)
    return render(request, 'inmobiliariaVR/previa_habitaciones.html', {'casas': lista_casas})

class GetHabitaciones(View):
    @staticmethod
    def post(request):
        data = {}
        habitaciones = []
        seleccionada = request.POST.get('casa_seleccionada', '')
        if seleccionada == '':
            data["seleccionada"] = False
            data["mensaje"] = "Debe seleccionar una opcion de la lista"
        else:
            c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada"])
            for a in c:
                habitaciones.append(a.nombre_habitacion)
                data["seleccionada"] = True
                data["habitaciones"] = habitaciones

        return JsonResponse(data, safe=False)


class GetLinkHabitacion(View):
    @staticmethod
    def post(request):
        data = {}
        seleccionada = request.POST.get('habitacion_seleccionada', '')

        if seleccionada == '':
            data["seleccionada"] = False
            data["mensaje"] = "Debe seleccionar una opcion de la lista"
            return JsonResponse(data, safe=False)
        else:
            c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada_2"], nombre_habitacion=request.POST["habitacion_seleccionada"])
            for a in c:
                data["seleccionada"] = True
                data["link"] = a.get_download_link()

        return JsonResponse(data, safe=False)

