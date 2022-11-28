from django.urls import path

from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.index, name='index'),
    path('lista_agenda/', views.AgentaLista.as_view(), name='lista_agenda'),
    path('crear_agenda/', views.AgendaCrear.as_view(), name='crear_agenda'),
    path('editar_agenda/<pk>', views.editar_agenda.as_view(), name='editar_agenda'),
    path('lista_agenda/eliminar/<int:id_agenda>', views.eliminar_agenda, name='eliminar_agenda'),
]