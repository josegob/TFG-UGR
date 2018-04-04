"""inmobiliariaVR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^appVR/', include('appVR.urls')),
    url(r'^$', views.main_page, name='index'),
    url(r'^sample/(?P<path>.*)/$', views.sample, name='sample'),
    url(r'^edicion-habitaciones/$', views.edicion_habitaciones, name='creacion_habitaciones'),
    url(r'^edicion-habitaciones/(?P<casa>.*)/$', views.edicion_habitaciones, name='creacion_habitaciones'),
    url(r'^get-habitaciones/$', GetHabitaciones.as_view(), name='get_habitaciones'),
    url(r'^get-links/$', GetLinkHabitacion.as_view(), name='get_links'),
    url(r'^previa-habitaciones/$', views.previa, name='previa'),
    url(r'^sample-buttons/(?P<path>.*)/(?P<casa>.*)/(?P<habitacion>.*)/$', views.sample_butons, name='sample_buttons'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.TMP_URL, document_root=settings.TMP_ROOT)