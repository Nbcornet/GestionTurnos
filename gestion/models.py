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
    ('Hospital de Niños de la Maternidad', 'Hospital de Niños de la Maternidad'),
    ('Hospital Pirovano', 'Hospital Pirovano'),
    ('Hospital Vicente López', 'Hospital Vicente López'),
    ('Hospital de Clínicas', 'Hospital de Clínicas'),
    ('Hospital de Clínicas de la Universidad de Buenos Aires', 'Hospital de Clínicas de la Universidad de Buenos Aires'),
)

class Especialidades(models.Model):
    nombre = models.CharField(max_length=100, choices=department)
    codigo = models.IntegerField(unique=True)
    descripcion = models.TextField(max_length=500)

    def __str__(self):
        return self.nombre

class Agenda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default='2021-10-10 10:00:00')
    hospital = models.CharField(choices=hospitales, max_length=250)
    especialidad = models.CharField(choices=department, max_length=250)
    creado = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def soft_delete(self):
        self.is_deleted=True
        super().save()
    
    def restore(self):
        self.is_deleted=False
        super().save()


class Turno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    mensaje = models.TextField()
    telefono = models.CharField(max_length=120)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'