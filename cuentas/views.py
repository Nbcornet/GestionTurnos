# from email import message
from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
# from django.views.generic.edit import DeleteView, UpdateView
from cuentas.decorators import unauthenticated_user, allowed_users
from .forms import RegistracionMedicoForm, RegistracionPacientesForm,LoginForm, EditarPerfilMedicoForm,EditarPerfilPacienteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.urls import reverse_lazy
# from django.http import Http404
# from django.utils.decorators import method_decorator
# from .decorators import user_is_medico

# Create your views here.


@unauthenticated_user
def RegistracionMedico(request):    
    form = RegistracionMedicoForm()

    if request.method == "POST":
        form = RegistracionMedicoForm(request.POST)    
        if form.is_valid():
            user = form.save()
            # profile = form.save()
            # username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            # messages.success(request, 'Account was created for ' + username)
            messages.success(request, 'Felicitaciones ' + first_name + '. Su cuenta fue creada')

            group = Group.objects.get(name='medico')
            user.groups.add(group)
            # profile.groups.add(group)

            return redirect("/login") # redirect "Login"
        
        else: 
            # form = RegistracionMedicoForm()
            messages.error(request,'Los datos ingresados son incorrectos ')

    context = {"form":form}
    return render(request, 'cuentas/medicos/registracion.html', context)


@login_required
@allowed_users(allowed_roles=['medico'])
def EditarPerfilMedico(request):
    if request.method == 'POST':
        form = EditarPerfilMedicoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Los cambios fueron guardados correctamente')
            return redirect('cuentas:editar_perfil_medico')
    else:
        form = EditarPerfilMedicoForm(instance=request.user)
    context = {
        'form' : form,
    }


    return render(request, 'cuentas/medicos/editar-perfil-medico.html', context)


@unauthenticated_user
def RegistracionPaciente(request):    
    form = RegistracionPacientesForm()

    if request.method == "POST":
        form = RegistracionPacientesForm(request.POST)    
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Felicitaciones ' + first_name + '. Su cuenta fue creada')

            group = Group.objects.get(name='paciente')
            user.groups.add(group)

            return redirect("/login") # redirect "Login"
        else: 
            messages.error(request,'Los datos ingresados son incorrectos ')
    
    context = {"form":form}
    return render(request, 'cuentas/pacientes/registracion.html', context)


@login_required
@allowed_users(allowed_roles=['paciente'])
def EditarPerfilPaciente(request):
    form = RegistracionPacientesForm()
    if request.method == "POST":
        form = RegistracionPacientesForm(request.POST)    
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Felicitaciones ' + first_name + '. Su cuenta fue creada')

            group = Group.objects.get(name='paciente')
            user.groups.add(group)

            return redirect("/login") # redirect "Login"
        else: 
            messages.error(request,'Los datos ingresados son incorrectos ')

    context = {
        'form' : form,
    }

    return render(request, 'cuentas/pacientes/editar-perfil-paciente.html', context)


@unauthenticated_user
def loginPage(request):

    # Autenticación   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/') # index or home
        else:
            messages.info(request, 'El nombre de usuario o la contraseña es incorrecta')
            
    form = LoginForm()
    context = {"form": form}
    return render(request, 'cuentas/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')


