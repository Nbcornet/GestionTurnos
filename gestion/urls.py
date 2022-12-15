from django.urls import path

from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('lista_agenda/', views.AgendaLista.as_view(), name='lista_agenda'),
    path('crear_agenda/', views.AgendaCrear.as_view(), name='crear_agenda'),
    path('editar_agenda/<pk>', views.editar_agenda.as_view(), name='editar_agenda'),
    path('lista_agenda/eliminar/<int:id_agenda>', views.eliminar_agenda, name='eliminar_agenda'),
    path('turno_paciente/<int:id>', views.TurnoPaciente, name='turno_paciente'),
    path('mis_turnos/', views.MisTurnosLista.as_view(), name='mis_turnos'),
    path('mis_turnos/eliminar/<int:id_turno>', views.eliminar_turno, name='eliminar_turno'),
    path('mis_pacientes/', views.MisPacientesLista.as_view(), name='mis_pacientes'),
]
