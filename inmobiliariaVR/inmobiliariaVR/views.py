from django.shortcuts import render
from appVR.models import ImagenesHabitaciones, Casa, BotonLink
from django.views import View
from django.http import JsonResponse
from django import template


register = template.Library()

def main_page(request):
    lista_casas = []
    casas = Casa.objects.all()
    for casa in casas:
        lista_casas.append(casa.nombre_casa)

    return render(request, 'inmobiliariaVR/main_page.html', {'casas': lista_casas})


def sample_butons(request, path, casa, habitacion):
    array_links = []
    array_nombres_botones = []
    array_contadores = []
    i = 0

    array_enlaces = []
    array_nombe_habitaciones = []

    array_pos_x = []
    array_rot_x = []

    array_pos_y = []
    array_rot_y = []

    array_pos_z = []
    array_rot_z = []

    botones = BotonLink.objects.filter(nombre_casa=casa)

    for boton in botones:
        array_nombres_botones.append(boton.nombre_boton.replace(' ', '_'))
        link = boton.get_download_link()
        array_links.append(link[link.index('VR/') + 2:])
        array_contadores.append(i)
        i += 1

        array_nombe_habitaciones.append(boton.nombre_habitacion)
        array_enlaces.append(boton.enlace_habitacion)

        array_pos_x.append(boton.coordenada_x_position)
        array_rot_x.append(boton.coordenada_x_rotation)

        array_pos_y.append(boton.coordenada_y_position)
        array_rot_y.append(boton.coordenada_y_rotation)

        array_pos_z.append(boton.coordenada_z_position)
        array_rot_z.append(boton.coordenada_z_rotation)

    array_contenedor = list(zip(array_links, array_nombres_botones, array_pos_x, array_pos_y, array_pos_z, array_rot_x, array_rot_y, array_rot_z,
                                array_contadores, array_enlaces, array_nombe_habitaciones))

    return render(request, 'inmobiliariaVR/habitacion_previa.html', {'link': path, 'array_contenedor': array_contenedor, 'hab_actual': habitacion,
                                                                     'num': i})


def set_rotation(request, path, casa, habitacion, x, y, z):
    array_links = []
    array_nombres_botones = []
    array_contadores = []
    i = 0

    array_enlaces = []
    array_nombe_habitaciones = []

    array_pos_x = []
    array_rot_x = []

    array_pos_y = []
    array_rot_y = []

    array_pos_z = []
    array_rot_z = []

    botones = BotonLink.objects.filter(nombre_casa=casa)

    for boton in botones:
        array_nombres_botones.append(boton.nombre_boton.replace(' ', '_'))
        link = boton.get_download_link()
        array_links.append(link[link.index('VR/') + 2:])
        array_contadores.append(i)
        i += 1

        array_nombe_habitaciones.append(boton.nombre_habitacion)
        array_enlaces.append(boton.enlace_habitacion)

        array_pos_x.append(boton.coordenada_x_position)
        array_rot_x.append(boton.coordenada_x_rotation)

        array_pos_y.append(boton.coordenada_y_position)
        array_rot_y.append(boton.coordenada_y_rotation)

        array_pos_z.append(boton.coordenada_z_position)
        array_rot_z.append(boton.coordenada_z_rotation)

    array_contenedor = list(zip(array_links, array_nombres_botones, array_pos_x, array_pos_y, array_pos_z, array_rot_x, array_rot_y, array_rot_z,
                                array_contadores, array_enlaces, array_nombe_habitaciones))

    return render(request, 'inmobiliariaVR/habitacion_previa.html', {'link': path[:19], 'array_contenedor': array_contenedor, 'hab_actual': habitacion,
                                                                     'num': i, 'x': float(x)+5, 'y': float(y), 'z': float(z)})


def testing(request):

    lista_casas = []
    c = Casa.objects.all()
    for a in c:
        lista_casas.append(a.nombre_casa)
    return render(request, 'inmobiliariaVR/testing_habitaciones.html', {'casas': lista_casas})

def edicion_habitaciones(request, casa=None):
    if casa == None:
        lista_casas = []
        c = Casa.objects.all()
        for a in c:
            lista_casas.append(a.nombre_casa)

        return render(request, 'inmobiliariaVR/edicion_habitaciones.html', {'casas': lista_casas, 'seleccion_casa': True})

    else:
        lista_habitaciones = []
        c = ImagenesHabitaciones.objects.filter(nombre_casa=casa)
        for a in c:
            lista_habitaciones.append(a.nombre_habitacion)

        return render(request, 'inmobiliariaVR/edicion_habitaciones.html', {'habitaciones': lista_habitaciones, 'seleccion_casa': False, 'casa': casa})

def generar_zip(request):

    lista_casas = []
    c = Casa.objects.all()
    for a in c:
        lista_casas.append(a.nombre_casa)

    return render(request, 'inmobiliariaVR/generar_zip.html', {'casas': lista_casas})


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
        habitaciones = []
        botones = []

        seleccionada = request.POST.get('habitacion_seleccionada', '')
        data["habitacion_actual"] = request.POST["habitacion_seleccionada"]
        data["casa_actual"] = request.POST["casa_seleccionada_2"]

        if seleccionada == '':
            data["seleccionada"] = False
            data["mensaje"] = "Debe seleccionar una opcion de la lista"
            return JsonResponse(data, safe=False)
        else:
            c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada_2"], nombre_habitacion=request.POST["habitacion_seleccionada"])
            for a in c:
                data["seleccionada"] = True
                data["link"] = a.get_download_link()
            c = ImagenesHabitaciones.objects.filter(nombre_casa=request.POST["casa_seleccionada_2"])
            for a in c:
                habitaciones.append(a.nombre_habitacion)
                data["habitaciones"] = habitaciones
            c = BotonLink.objects.filter(nombre_casa=request.POST["casa_seleccionada_2"], nombre_habitacion=request.POST["habitacion_seleccionada"])
            for a in c:
                botones.append(a.nombre_boton)
                data["botones"] = botones

        return JsonResponse(data, safe=False)

