from django.db import models

# Create your models here.


class Casa(models.Model):
    nombre_casa = models.CharField(max_length=100)
    numero_habitaciones = models.IntegerField()


class Habitacion(models.Model):
    nombre_casa = models.CharField(max_length=100)
    nombre_habitacion = models.CharField(max_length=100)
    nombre_boton = models.CharField(max_length=100)
    link_habitacion = models.CharField(max_length=100)
    imagen_habitacion = models.FileField()


class BotonLink(models.Model):
    nombre_boton = models.CharField(max_length=100)
    nombre_habitacion = models.CharField(max_length=100)

    coordenada_x_position = models.IntegerField()
    coordenada_y_position = models.IntegerField()
    coordenada_z_position = models.IntegerField()

    coordenada_x_rotation = models.IntegerField()
    coordenada_y_rotation = models.IntegerField()
    coordenada_z_rotation = models.IntegerField()