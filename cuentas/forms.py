from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms
from django.forms import ValidationError
from django.db import transaction


class RegistracionMedicoForm(UserCreationForm):
    class Meta:
        # model = get_user_model
        model = User
        fields = ["first_name", "last_name","username", "email", "password1", "password2",'image',]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de Usuario',
            'email': 'Correo Electronico',
            'image': 'Foto de Perfil',
        }



    def solo_caracteres(value):
        if any(char.isdigit() for char in value ):
            raise ValidationError('El nombre no puede contener números',
                                code='Error1',
                                params={'valor':value})
    

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_count = User.objects.filter(username=username).count()
        if user_count > 0:
            raise forms.ValidationError("Ya existe una cuenta con ese nombre de usuario")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("Ya existe una cuenta con esa dirección de correo electrónico")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('La contraseña no coincide')
        return password2

    # CHECK
    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name') # NEW 
        user.last_name = self.cleaned_data.get('last_name') # NEW
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data['password1'])
        user.is_medico =  True
        user.save()
        # if commit:
        #     user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegistracionMedicoForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'placeholder':'Ingrese su nombre '
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder':'Ingrese su apellido '
        })
        self.fields['username'].widget.attrs.update({
            'placeholder':'Ingrese su nombre de usuario '
        })
        self.fields['email'].widget.attrs.update({
            'placeholder':'Ingrese su email'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder':'Ingrese su contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder':'Confirme su contraseña'
        })



class RegistracionPacientesForm(UserCreationForm):
    class Meta:
        # model = get_user_model
        model = User
        fields = ["first_name", "last_name","username", "email", "password1", "password2",'image',]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de Usuario',
            'email': 'Correo Electronico',
            'image': 'Foto de Perfil',
        }

    def solo_caracteres(value):
        if any(char.isdigit() for char in value ):
            raise ValidationError('El nombre no puede contener números',
                                code='Error1',
                                params={'valor':value})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_count = User.objects.filter(username=username).count()
        if user_count > 0:
            raise forms.ValidationError("Ya existe una cuenta con ese nombre de usuario")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("Ya existe una cuenta con esa dirección de correo electrónico")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('La contraseña no coincide')
        return password2

    # CHECK
    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name') # NEW 
        user.last_name = self.cleaned_data.get('last_name') # NEW
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data['password1'])
        user.is_paciente =  True
        user.save()
        # if commit:
        #     user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegistracionPacientesForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'placeholder':'Ingrese su nombre '
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder':'Ingrese su apellido '
        })
        self.fields['username'].widget.attrs.update({
            'placeholder':'Ingrese su nombre de usuario'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder':'Ingrese su email'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder':'Ingrese su contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder':'Confirme su contraseña'
        })


class LoginForm(forms.Form):

    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'floatingInput',
            'placeholder':'Ingrese su nombre de usuario',
            'type': 'text'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 
            'type': 'password',
            'placeholder':'Ingrese su contraseña',
            'id': 'floatingPassword'
        })

        # change label
        self.fields['username'].label = 'Usuario'
        self.fields['password'].label = 'Contraseña'


class EditarPerfilMedicoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name",'image',]

    def __init__(self, *args, **kwargs):
        super(EditarPerfilMedicoForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
        })
    

class EditarPerfilPacienteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email",'first_name','last_name','image',]

    def __init__(self, *args, **kwargs):
        super(EditarPerfilPacienteForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
        })





    