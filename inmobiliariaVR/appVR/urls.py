from django.conf.urls import url
from . import views
from .views import *
from django.views.decorators.csrf import csrf_exempt



app_name = 'appVR'
urlpatterns = [
    url(r'^nueva-casa/$', csrf_exempt(NuevaCasa.as_view()), name='nueva_casa'),
    url(r'^upload/$', csrf_exempt(FileUploadView.as_view()), name='upload'),
    url(r'^guardar-boton/$', csrf_exempt(SaveButton.as_view()), name='save_button'),
    url(r'^eliminar-casa/$', csrf_exempt(DeleteHouse.as_view()), name='delete_house'),
    url(r'^eliminar-boton/$', csrf_exempt(Deletebutton.as_view()), name='delete_button'),
    url(r'^rotar-vista/$', csrf_exempt(RotateView.as_view()), name='rotate_view'),
    url(r'^generar-zip/$', csrf_exempt(GenerateZip.as_view()), name='generate_zip'),
]
