from django.contrib import admin
from appVR.models import Casa
from appVR.models import BotonLink
from appVR.models import ImagenesHabitaciones
from appVR.models import CasasAdmin
from appVR.models import ImagenesHabitacionesAdmin

# Register your models here.

admin.site.register(Casa, CasasAdmin)
admin.site.register(BotonLink)
admin.site.register(ImagenesHabitaciones, ImagenesHabitacionesAdmin)

