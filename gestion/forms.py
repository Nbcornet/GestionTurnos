from django import forms
from .models import Agenda, Especialidades, Hospitales, Turno
from datetime import datetime

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = [
            'hospital',
            'especialidad',
            'fecha_inicio',
            'fecha_fin',
        ]

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        # fecha_inicio minimo es la fecha actual
        self.fields['fecha_inicio'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%d')
        self.fields['fecha_fin'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%d')

    # add another field call day
    hospital = forms.ModelChoiceField(queryset=Hospitales.objects.all())
    especialidad = forms.ModelChoiceField(queryset=Especialidades.objects.all())

    days_choices = (
        ('Monday', 'Lunes'),
        ('Tuesday', 'Martes'),
        ('Wednesday', 'Miercoles'),
        ('Thursday', 'Jueves'),
        ('Friday', 'Viernes'),
        ('Saturday', 'Sabado'),
        ('Sunday', 'Domingo'),
    )

    dias = forms.MultipleChoiceField(
        choices=days_choices,
        widget=forms.CheckboxSelectMultiple,
        # required=True,
    )

    fecha_inicio = forms.DateField(
        # fecha mayor a la actual
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
    )
    hora_fin = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
    )

    intervalo_choices = (
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),
        ('60', '60'),
    )
    
    intervalo = forms.ChoiceField(
        choices=intervalo_choices,
        widget=forms.Select(),
        # required=True,
    )

    def clean(self):
        cleaned_data = super(AgendaForm, self).clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                'La fecha de inicio debe ser menor a la fecha de fin'
            )
        if hora_inicio > hora_fin:
            raise forms.ValidationError(
                'La hora de inicio debe ser menor a la hora de fin'
            )

    def save(self, commit=True):
        agenda = super(AgendaForm, self).save(commit=False)
        agenda.user = self.user
        
        if commit:
            agenda.save()
        return agenda

class EspecialidadesForm(forms.ModelForm):

    class Meta:
        model = Especialidades
        fields = ["nombre"]


    nombre = forms.ModelChoiceField(queryset=Especialidades.objects.values_list('nombre', flat=True), 
                                    widget=forms.Select(attrs={'class': 'form-select form-select'}),
                                    label='Especialidad',
                                    initial={'nombre':'Dentistry'})


class TurnoPacienteForm(forms.ModelForm):
    
    class Meta:
        model = Turno
        fields = ['mensaje', 'telefono']

    def __init__(self, *args, **kwargs):
        super(TurnoPacienteForm, self).__init__(*args, **kwargs)

        self.fields['mensaje'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'describa su síntoma',
        })
        self.fields['telefono'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Ingrese su número', 
        })

    def save(self, commit=True):
        turno = super(TurnoPacienteForm, self).save(commit=False)
        turno.user = self.user
    #     turno.agenda = self.agenda
         
        if commit:
            turno.save()
        return turno
