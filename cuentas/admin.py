from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import RegistracionMedicoForm, RegistracionPacientesForm

# Register your models here.

# admin.site.register(User, UserAdmin)

class CustomerUserAdmin(UserAdmin):
    model = User
    add_form = RegistracionMedicoForm, RegistracionPacientesForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields':(
                    'is_medico',
                    'is_paciente',
                    'is_admin',
                )
            }
        )
    )

admin.site.register(User, CustomerUserAdmin)
