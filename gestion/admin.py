from django.contrib import admin
from .models import Especialidades, Agenda, Hospitales,Turno
# Register your models here.

admin.site.register(Especialidades)
admin.site.register(Hospitales)
admin.site.register(Agenda)
admin.site.register(Turno)