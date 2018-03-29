from django.db import models
from django.contrib import admin
# Create your models here.


class Casa(models.Model):
    nombre_casa = models.CharField(max_length=100)
    numero_habitaciones = models.IntegerField()

class CasasAdmin(admin.ModelAdmin):
    list_display = ('nombre_casa', )


class BotonLink(models.Model):
    imagen_boton = models.FileField()
    nombre_boton = models.CharField(max_length=100)
    nombre_habitacion = models.CharField(max_length=100)
    nombre_casa = models.CharField(max_length=100)
    enlace_habitacion = models.CharField(max_length=100)

    coordenada_x_position = models.FloatField()
    coordenada_y_position = models.FloatField()
    coordenada_z_position = models.FloatField()

    coordenada_x_rotation = models.FloatField()
    coordenada_y_rotation = models.FloatField()
    coordenada_z_rotation = models.FloatField()

    def get_download_link(self):
        return self.imagen_boton.url


class ImagenesHabitaciones(models.Model):
    imagen_habitacion = models.FileField()
    nombre_habitacion = models.CharField(max_length=100)
    nombre_casa = models.CharField(max_length=100)

    def get_download_link(self):
        return self.imagen_habitacion.url

class ImagenesHabitacionesAdmin(admin.ModelAdmin):
    list_display = ('nombre_casa', )
