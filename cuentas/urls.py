from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('registracion/medico', views.RegistracionMedico, name='registracion_medico'),
    path('editar/perfil/medico', views.EditarPerfilMedico, name='editar_perfil_medico'),
    path('registracion/paciente', views.RegistracionPaciente ,name='registracion_paciente'),
    path('editar/perfil/paciente', views.EditarPerfilPaciente ,name='editar_perfil_paciente'),
    path('login', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="cuentas/password_reset.html"), 
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="cuentas/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="cuentas/password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="cuentas/password_reset_done.html"), 
        name="password_reset_complete"),
]
