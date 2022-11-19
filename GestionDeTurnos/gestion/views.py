from contextvars import Context
from pipes import Template
from django.shortcuts import render
from django.http import HttpResponse
from .models import Especialidades
#
from django.views import generic
from .forms import AgendaForm
# Create your views here.
def index(request):
    titulo = "Busca profesionales en tu ciudad"
    descripcion = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Earum perspiciatis excepturi optio libero quasi beatae itaque, officiis numquam iste tempore dolor! Odio tempora sit rem tenetur consectetur eum atque iste?"
    
    especialidades = Especialidades.objects.all()
    # especialidades =  [
    #         'Clínica médica',
    #         'Dermatología',
    #         'Gastroenterología'
    #         'Ginecología',
    #         'Nefrología',
    #         'Nutrición',
    #         'Traumatología'
    #         ]
    contexto = {
        "titulo": titulo, 
        "especialidades": especialidades,  
        "descripcion": descripcion,        
        }
    return render(request,'./index.html', contexto)

class TakeAppointment(generic.View):

    def get(self, request):
        form = AgendaForm()
        return render(request, 'gestion/take_appointment.html', {'form': form})


def create(request):
    pass

def detail(request, id):
    return HttpResponse("Estás viendo el detalle del turno %s." % id)

def update(request, id):
    return HttpResponse("Estás actualizando el turno %s." % id)