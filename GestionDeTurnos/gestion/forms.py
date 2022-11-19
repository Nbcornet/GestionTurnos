from django import forms
from .models import Agenda


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = [
            'direccion',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'hospital',
            'especialidad',
        ]

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        # fecha as date
        self.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})

    # add another field call days
    days_choices = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    days = forms.MultipleChoiceField(choices=days_choices, widget=forms.CheckboxSelectMultiple)
    