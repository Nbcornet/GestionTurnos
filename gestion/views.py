from contextvars import Context
from pipes import Template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
#
from django.urls import reverse_lazy
from django.views import generic
from .forms import AgendaForm, EspecialidadesForm, TurnoPacienteForm
from datetime import datetime, timedelta
from .mixins import MedicoMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from itertools import chain
from django.db.models import Q
# Create your views here.



class Index(generic.View):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        context = {
            'especialidades': Especialidades.objects.all(),
            'hospitales': Hospitales.objects.all(),
            'table' : False,
            'especialidad_value' : '',
            'hospital_value' : '',
            'date_start_before' : '',
            'date_end_before' : '',
        }

        return render(request, self.template_name,context)

    def post(self, request,*args, **kwargs): # NEW

        if request.user.is_authenticated and request.user.is_medico:
            # return messages with error
            messages.error(request,'El personal médico no está autorizado a solicitar turnos')
            return redirect('gestion:index')

        elif not request.user.is_authenticated: 
            messages.error(request,'Por favor ingrese a su cuenta')
            return redirect('cuentas:login')

        else: #NEW
            search = Agenda.objects.all().values('id','user__first_name','user__last_name','especialidad__nombre','hospital__nombre','fecha')

            especialidad = self.request.POST.get('especialidad') if self.request.POST.get('especialidad') != None else ''
            hospital = self.request.POST.get('hospital')    if self.request.POST.get('hospital') != None else ''
            date_start = self.request.POST.get('date-start') if self.request.POST.get('date-start') != None else ''
            date_end = self.request.POST.get('date-end')    if self.request.POST.get('date-end') != None else ''

            # print(especialidad)
            # print(hospital)
            # print(date_start)
            # print(date_end)


            if date_end == '':
                date_end = datetime.now().date() + timedelta(days=30)


            if date_start != '' and date_end != '':
                date_end_search = datetime.strptime(date_end, '%Y-%m-%d').date()
                date_end_search = date_end_search + timedelta(days=1)
                date_end_search = date_end_search.strftime('%Y-%m-%d')
                search = search.filter(fecha__range=[date_start, date_end_search])

            if date_start != '' :
                search = search.filter(fecha__gte=date_start)
            if date_end != '' :
                date_end_search = datetime.strptime(date_end, '%Y-%m-%d').date()
                date_end_search = date_end_search + timedelta(days=1)
                date_end_search = date_end_search.strftime('%Y-%m-%d')
                search = search.filter(fecha__lte=date_end_search)

            if especialidad != '':    
                search = search.filter(especialidad=especialidad)

            if hospital != '':
                search = search.filter(hospital=hospital)
                
            
            # for agenda in agendas:
            #     agenda['image'] = User.objects.get(first_name=agenda['user__first_name'], last_name=agenda['user__last_name']).image
            # print(search)
            try:
                nombre_especialidad = Especialidades.objects.get(id=especialidad).nombre
            except:
                nombre_especialidad = ''
                especialidad = ''

            try:
                nombre_hospital = Hospitales.objects.get(id=hospital).nombre
            except:
                nombre_hospital = ''
                hospital = ''

            print(date_end)
            print(date_start)
            context = {
                'agendas': search,
                'especialidades': Especialidades.objects.all(),
                'hospitales': Hospitales.objects.all(),
                'table' : True,
                'date_start_before': date_start,
                'date_end_before': date_end,
                'especialidad_value': especialidad,
                'nombre_especialidad': nombre_especialidad,
                'hospital_value': hospital,
                'nombre_hospital': nombre_hospital,
                # 'id': Agenda.objects.get(pk=id), # NEW
            }
            return render(request, self.template_name, context)


def index(request):
    # especialidades = Especialidades.objects.all()
    # hospitales = Agenda.objects.all()
    # contexto = {
    #     "especialidades": especialidades, "hospitales": hospitales    
    #     }
    # return render(request,'index.html', contexto)


    print(request.method, request.POST.get('nombre'))
    form = EspecialidadesForm
    if request.POST.get('nombre') != None and request.user.is_authenticated and request.user.is_paciente:
        
        especialidad = Especialidades.objects.values_list('nombre', flat=True).filter(nombre=request.POST.get('nombre'))
        print(especialidad[0])

        agendas = Agenda.objects.filter(especialidad=especialidad[0])
        print(agendas)

        form = EspecialidadesForm(initial={'nombre':request.POST.get('nombre')})
        
        return render(request,'index.html', {"agendas": agendas,'form':form})

    elif request.POST.get('nombre') != None and request.user.is_authenticated and request.user.is_medico:
        messages.error(request,'El personal médico no está autorizado a solicitar turnos')

    elif request.POST.get('nombre') != None and not request.user.is_authenticated: 
        messages.error(request,'Por favor ingrese a su cuenta')
        return redirect('cuentas:login')
        
    return render(request,'index.html', {"form": form})

class AgendaCrear(MedicoMixin,generic.View):
    template_name = 'gestion/crear_agenda.html'
    form_class = AgendaForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            hospital = form.cleaned_data['hospital']
            especialidad = form.cleaned_data['especialidad']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']
            is_deleted =  False

            fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
            fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")
            hora_inicio_str = hora_inicio.strftime("%H:%M:%S")
            hora_fin_str = hora_fin.strftime("%H:%M:%S")
            fecha_inicio = datetime.strptime(fecha_inicio_str + " " + hora_inicio_str, "%Y-%m-%d %H:%M:%S")
            fecha_fin = datetime.strptime(fecha_fin_str + " " + hora_fin_str, "%Y-%m-%d %H:%M:%S")
            intervalo = form.cleaned_data['intervalo']
            intervalo = int(intervalo)
            # dias de la semana 
            dias = form.cleaned_data['dias']
            print(dias)
            print(fecha_inicio.strftime("%A"))
            #dias entre fecha inicio y fecha fin
            print(hora_fin)
            print(hora_inicio)
            horas = timedelta(hours=hora_fin.hour, minutes=hora_fin.minute, seconds=hora_fin.second) - timedelta(hours=hora_inicio.hour, minutes=hora_inicio.minute, seconds=hora_inicio.second)
            minutos = horas.total_seconds() / 60
            cantidad_turnos = int(minutos / intervalo)

            hospital = Hospitales.objects.get(nombre=hospital)
            especialidad = Especialidades.objects.get(nombre=especialidad)

            try:
            
                while fecha_inicio <= fecha_fin:
                    print("Cree una agenda")
                    if fecha_inicio.strftime("%A") in dias:
                        print("Cree una agenda")
                        for i in range(cantidad_turnos):
                            fecha_turno = fecha_inicio + timedelta(minutes=intervalo * i)
                            turno = Agenda.objects.create(
                                user=user,
                                hospital=hospital,
                                especialidad=especialidad,
                                fecha = fecha_turno,
                                is_deleted = is_deleted
                            )
                        turno.save()
                        print("Cree una agenda")
                    fecha_inicio = fecha_inicio + timedelta(days=1)
                return redirect('gestion:lista_agenda')

            except:
                messages.error(request,'Existen turnos para el mismo día, horario y/o hospital')
                redirect('gestion:crear_agenda')

        return render(request, self.template_name, {'form': form})


class AgendaLista(MedicoMixin,generic.ListView):
    template_name = 'gestion/lista_agenda.html'
    context_object_name = 'agendas'

    def get_queryset(self):
        user = self.request.user
        # para filtrar por fecha actual 
        # fecha__gte=datetime.now(),
        query_agenda = Agenda.objects.filter(user=user, is_deleted=False).order_by('fecha')
        print(query_agenda)
        return query_agenda
    

class editar_agenda(MedicoMixin, generic.UpdateView):
    template_name = 'gestion/editar_agenda.html'
    model = Agenda
    fields = ['hospital', 'especialidad', 'fecha']   
    success_url = reverse_lazy('gestion:lista_agenda')


def eliminar_agenda(request,id_agenda):
    turno = Agenda.objects.get(pk=id_agenda)
    turno.soft_delete()
    return redirect('gestion:lista_agenda')


def TurnoPaciente(request, id): # NEW
    
    agenda = Agenda.objects.get(id = id) 
   
    # agenda.id = {'id': agenda }
    # return render(request, 'gestion/turno_paciente.html', agenda.id)
    
    form = TurnoPacienteForm(request.POST, instance=agenda)
    if form.is_valid():
        
        user = request.user
        mensaje = form.cleaned_data['mensaje']
        telefono = form.cleaned_data['telefono']
        turno = Turno.objects.create(
                        user=user,
                        agenda=agenda,
                        mensaje=mensaje,
                        telefono=telefono,
                    )
        turno.save()


        messages.success(request, f'El turno fue reservado correctamente')
        return redirect('/') # redirect 'Home' pero tiene que ir a 'Mis Turnos'
    
    else:
        form = TurnoPacienteForm()
    context = {
        'form' : form,
    }

    return render(request, 'gestion/turno_paciente.html', context)


class MisTurnosLista(generic.View):
    template_name = 'gestion/mis_turnos.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        turno = Turno.objects.filter(user=user, is_deleted=False).values('agenda__user__first_name', 'agenda__user__last_name','agenda__hospital__nombre','agenda__especialidad__nombre', 'agenda__fecha', 'id')
        context = {'turnos' : turno}
        return render(request, self.template_name, context)


def eliminar_turno(request,id_turno):
    turno = Turno.objects.get(pk=id_turno)
    turno.soft_delete()
    return redirect('gestion:mis_turnos')

class MisPacientesLista(generic.View):
    template_name = 'gestion/mis_pacientes.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        turno = Turno.objects.filter(agenda__user=user, is_deleted=False).values('user__first_name', 'user__last_name','agenda__hospital__nombre','agenda__especialidad__nombre', 'agenda__fecha', 'id','mensaje')
        # print(turno)
        context = {'turnos' : turno}
        return render(request, self.template_name, context)






    