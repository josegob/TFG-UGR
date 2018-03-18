from django.conf.urls import url
from . import views
from .views import *



app_name = 'appVR'
urlpatterns = [
    url(r'^nueva-casa/$', NuevaCasa.as_view(), name='nueva_casa'),
]
