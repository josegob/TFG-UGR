from django.contrib import admin
from appVR.models import Casa
from appVR.models import Habitacion
from appVR.models import BotonLink

# Register your models here.

admin.site.register(Casa)
admin.site.register(Habitacion)
admin.site.register(BotonLink)