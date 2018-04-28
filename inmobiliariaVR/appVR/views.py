from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Casa, ImagenesHabitaciones, BotonLink
from .forms import CasaForm
import tempfile
import requests
from django.conf import settings
from django.core import files
import os
import zipfile
from os.path import basename
from django.http import HttpResponse



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
        botones = []
        hab = request.POST.get('habitacion_seleccionada_2', '')

        if hab == '':
            data["mensaje"] = "Debe seleccionar una habitacion como enlace"
            data["creado"] = False
            return JsonResponse(data)

        image_url = "https://dabuttonfactory.com/button.png?t={}&f=Calibri-Bold&ts=49&tc=fff&tshs=1&tshc=000&hp=20&vp=8&c=5&bgt=gradient&bgc=3d85c6&ebgc=073763".format(request.POST["nombre_boton"])

        enlace = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada_3"], nombre_habitacion=request.POST["habitacion_seleccionada_2"])
        for a in enlace:
            link = a.get_download_link()

        if (BotonLink.objects.filter(nombre_casa=request.POST["casa_seleccionada_3"], nombre_boton=request.POST["nombre_boton"].lower(), nombre_habitacion=request.POST["habitacion_select_2"].lower())).count() > 0:
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
            c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada_3"], nombre_habitacion=request.POST["habitacion_select_2"])
            for a in c:
                data["link_habitacion"] = a.get_download_link()

            data["casa_actual"] = request.POST["casa_seleccionada_3"]
            data["habitacion_actual"] = request.POST["habitacion_select_2"]

            c = BotonLink.objects.filter(nombre_casa=request.POST["casa_seleccionada_3"], nombre_habitacion=request.POST["habitacion_select_2"])
            for a in c:
                botones.append(a.nombre_boton)
                data["botones"] = botones

        return JsonResponse(data)

class DeleteHouse(View):
    @staticmethod
    def post(request):
        data = {}
        casa = request.POST.get('seleccion', '')
        Casa.objects.filter(nombre_casa=casa).delete()
        ImagenesHabitaciones.objects.filter(nombre_casa=casa).delete()
        BotonLink.objects.filter(nombre_casa=casa).delete()
        casas = Casa.objects.all()
        lista_casas = []
        for casa in casas:
            lista_casas.append(casa.nombre_casa)

        data["casas"] = lista_casas
        return JsonResponse(data)

class RotateView(View):
    @staticmethod
    def post(request):
        data = {}
        botones = BotonLink.objects.filter(nombre_casa=request.POST["casa"], nombre_habitacion=request.POST["habitacion"], nombre_boton=request.POST["boton"])

        lista_coordenadas = []
        for boton in botones:
            lista_coordenadas.append(boton.coordenada_x_rotation)
            lista_coordenadas.append(boton.coordenada_y_rotation)
            lista_coordenadas.append(boton.coordenada_z_rotation)

        data["coordenadas"] = lista_coordenadas

        c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa"], nombre_habitacion=request.POST["habitacion"])
        for a in c:
            data["link"] = a.get_download_link()

        return JsonResponse(data)


class Deletebutton(View):
    @staticmethod
    def post(request):
        data = {}
        casa = request.POST.get('seleccion', '')
        BotonLink.objects.filter(nombre_boton=request.POST["boton"], nombre_casa=request.POST["casa"], nombre_habitacion=request.POST["habitacion"]).delete()
        botones = BotonLink.objects.filter(nombre_casa=request.POST["casa"], nombre_habitacion=request.POST["habitacion"])
        lista_botones = []
        for boton in botones:
            lista_botones.append(boton.nombre_boton)

        c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa"], nombre_habitacion=request.POST["habitacion"])
        for a in c:
            data["link"] = a.get_download_link()

        data["botones"] = lista_botones
        return JsonResponse(data)


class GenerateZip(View):
    @staticmethod
    def post(request):
        data = {}
        if request.POST["habitacion"] == 'Selecciona una habitacion':
            data["aviso"] = "Debes seleccionar una habitacion"
            data["error"] = True
            return JsonResponse(data)

        if request.POST["HTML"] == 'False':
            c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa"], nombre_habitacion=request.POST["habitacion"])
            for a in c:
                data["link"] = a.get_download_link()

        else:
            imagenes_habitaciones = []
            imagenes_botones = []
            habitaciones = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa"])
            botones = BotonLink.objects.filter(nombre_casa=request.POST["casa"])
            for boton in botones:
                imagenes_botones.append(boton.get_download_link())
            for habitacion in habitaciones:
                imagenes_habitaciones.append(habitacion.get_download_link())

            ruta = settings.MEDIA_ROOT + '/casaVR.html'
            with open(ruta, 'wb') as f:
                f.write(bytearray(request.POST["data_html"], 'utf8'))

            js_ruta_1 = settings.JS_ROOT + '/jquery.js'
            js_ruta_2 = settings.JS_ROOT + '/materialize.js'
            js_ruta_3 = settings.JS_ROOT + '/set-image.js'
            js_ruta_4 = settings.JS_ROOT + '/custom.js'

            with zipfile.ZipFile('FicherosVR' + '.zip', 'w') as myzip:
                myzip.write(ruta, basename(ruta))
                myzip.write(js_ruta_1, "/static/js/" + basename(js_ruta_1))
                myzip.write(js_ruta_2, "/static/js/" + basename(js_ruta_2))
                myzip.write(js_ruta_3, "/static/js/" + basename(js_ruta_3))
                myzip.write(js_ruta_4, "/static/js/" + basename(js_ruta_4))
                for i in range(0, len(imagenes_habitaciones)):
                    ruta = settings.MEDIA_ROOT + (imagenes_habitaciones[i])[6:]
                    myzip.write(ruta, "/media/" + basename(ruta))
                for i in range(0, len(imagenes_botones)):
                    ruta = settings.TMP_ROOT + (imagenes_botones[i])[-23:]
                    myzip.write(ruta, "/media/imagenes_botones/" + basename(ruta))

            os.replace(settings.BASE_DIR + '/FicherosVR.zip', settings.MEDIA_ROOT + '/FicherosVR.zip')
            data["enlace"] = '/media/FicherosVR.zip'

        return JsonResponse(data)


