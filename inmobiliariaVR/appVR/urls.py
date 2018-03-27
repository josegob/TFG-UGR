from django.conf.urls import url
from . import views
from .views import *
from django.views.decorators.csrf import csrf_exempt



app_name = 'appVR'
urlpatterns = [
    url(r'^nueva-casa/$', csrf_exempt(NuevaCasa.as_view()), name='nueva_casa'),
    url(r'^upload/$', csrf_exempt(FileUploadView.as_view()), name='upload'),
]
