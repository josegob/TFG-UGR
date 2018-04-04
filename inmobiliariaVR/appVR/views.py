from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Casa, ImagenesHabitaciones, BotonLink
from .forms import CasaForm
import tempfile
import requests
from django.conf import settings
from django.core import files

# Create your views here.

class NuevaCasa(View):
    @staticmethod
    def post(request):
        data = {}
        form = CasaForm(request.POST, request.POST)
        if form.is_valid():
            casas = Casa.objects.filter(nombre_casa=request.POST['nombre_casa'].lower()).count()
            if(casas > 0):
                data["creado"] = False
                data["mensaje"] = "Ya existe una casa con ese nombre"
            else:
                Casa.objects.create(nombre_casa=request.POST['nombre_casa'].lower(), numero_habitaciones=request.POST['numero_habitaciones'])
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
        array_tmp = []

        for j in range(0, int(request.POST["numero_ficheros"])):
            tmp = request.POST["nombre_habitacion"+str(j)]
            if tmp in array_tmp:
                data["creada"] = False
                data['message'] = "No puede haber dos habitaciones con el mismo nombre"
                return JsonResponse(data)
            else:
                array_tmp.append(tmp)

        for i in range(0, int(request.POST["numero_ficheros"])):
            nueva_habitacion = ImagenesHabitaciones(imagen_habitacion=request.FILES["file_to_upload"+str(i)], nombre_habitacion=request.POST["nombre_habitacion"+str(i)].lower(), nombre_casa=request.POST["nombre_casa"].lower())
            if nueva_habitacion:
                nueva_habitacion.save()
                data["creada"] = True
                data['message'] = 'Casa creada correctamente'
                data["casa_creada"] = request.POST["nombre_casa"]
            else:
                data["creada"] = False
                data['message'] = 'Error al procesar las habitaciones'
                return JsonResponse(data)

        casas = Casa.objects.all()
        lista_casas = []
        for casa in casas:
            lista_casas.append(casa.nombre_casa)

        data["casas"] = lista_casas

        return JsonResponse(data)

class SaveButton(View):
    @staticmethod
    def post(request):
        data = {}
        hab = request.POST.get('habitacion_seleccionada_2', '')

        if hab == '':
            data["mensaje"] = "Debe seleccionar una habitacion como enlace"
            data["creado"] = False
            return JsonResponse(data)

        image_url = "https://dabuttonfactory.com/button.png?t={}&f=Calibri-Bold&ts=49&tc=fff&tshs=1&tshc=000&hp=20&vp=8&c=5&bgt=gradient&bgc=3d85c6&ebgc=073763".format(request.POST["nombre_boton"])

        enlace = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada_3"], nombre_habitacion=request.POST["habitacion_seleccionada_2"])
        for a in enlace:
            link = a.get_download_link()

        if (BotonLink.objects.filter(nombre_boton=request.POST["nombre_boton"].lower(), nombre_habitacion=request.POST["habitacion_select_2"].lower())).count() > 0:
            data["mensaje"] = "Ya existe un boton con ese nombre para esta habitacion"
            data["creado"] = False
            return JsonResponse(data)

        tmp = requests.get(image_url, stream=True)
        if tmp.status_code != requests.codes.ok:
            data["mensaje"] = "Error procesando la imagen del boton"
            data["creado"] = False
            return JsonResponse(data)

        file_tmp = tempfile.NamedTemporaryFile(dir=settings.TMP_ROOT, suffix='.jpg')

        for block in tmp.iter_content(1024 * 8):
            if not block:
                break
            file_tmp.write(block)

        nuevo_boton = BotonLink(imagen_boton=files.File(file_tmp), nombre_boton=request.POST["nombre_boton"].lower(), nombre_habitacion=request.POST["habitacion_select_2"].lower(), nombre_casa=request.POST["casa_seleccionada_3"].lower(),
                                coordenada_x_position=float(request.POST["coord_x_p"]), coordenada_y_position=float(request.POST["coord_y_p"]), coordenada_z_position=float(request.POST["coord_z_p"]),
                                coordenada_x_rotation=float(request.POST["coord_x_r"]), coordenada_y_rotation=float(request.POST["coord_y_r"]), coordenada_z_rotation=float(request.POST["coord_z_r"]),
                                enlace_habitacion=link)

        if nuevo_boton:
            nuevo_boton.save()
            data["mensaje"] = "Boton creado correctamente"
            data["creado"] = True

        return JsonResponse(data)

class DeleteHouse(View):
    @staticmethod
    def post(request):
        data = {}
        casa = request.POST.get('seleccion', '')
        print(casa)
        Casa.objects.filter(nombre_casa=casa).delete()
        ImagenesHabitaciones.objects.filter(nombre_casa=casa).delete()
        BotonLink.objects.filter(nombre_casa=casa).delete()
        print("ASD")
        casas = Casa.objects.all()
        lista_casas = []
        for casa in casas:
            lista_casas.append(casa.nombre_casa)

        data["casas"] = lista_casas
        return JsonResponse(data)
