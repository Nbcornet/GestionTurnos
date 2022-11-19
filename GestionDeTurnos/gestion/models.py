from django.db import models
from cuentas.models import User
# Create your models here.

department = (
    ('Dentistry', "Dentistry"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Astrology', 'Astrology'),
    ('Neuroanatomy', 'Neuroanatomy'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
)

hospitales = (
    ('Hospital de Niños', 'Hospital de Niños'),
    ('Hospital de Niñas', 'Hospital de Niñas'),
    ('Hospital de Niños y Niñas', 'Hospital de Niños y Niñas'),
    ('Hospital de Niñas y Niños', 'Hospital de Niñas y Niños'),
)

class Especialidades(models.Model):
    nombre = models.CharField(max_length=100, choices=department)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=500)

    def __str__(self):
        return self.nombre

class Agenda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    hospital = models.CharField(choices=hospitales, max_length=250)
    especialidad = models.CharField(choices=department, max_length=250)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Turno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    mensaje = models.TextField()
    telefono = models.CharField(max_length=120)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'