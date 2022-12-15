from django.db import models
from cuentas.models import User
# Create your models here.

department = (
    ('Dentista', "Dentista"),
    ('Cardiología', "Cardiología"),
    ('Traumatología', "Traumatología"),
    ('Neurología', 'Neurología'),
    ('Dermatología', 'Dermatología'),
    ('Oftalmología', 'Oftalmología'),
    ('Pedicuría', 'Pedicuría'),
)

hospitales = (
    ('Hospital de Niños', 'Hospital de Niños'),
    ('Hospital de Niños de la Maternidad', 'Hospital de Niños de la Maternidad'),
    ('Hospital Pirovano', 'Hospital Pirovano'),
    ('Hospital Vicente López', 'Hospital Vicente López'),
    ('Hospital de Clínicas', 'Hospital de Clínicas'),
    ('Hospital de Clínicas de la Universidad de Buenos Aires', 'Hospital de Clínicas de la Universidad de Buenos Aires'),
)

class Hospitales(models.Model):
    nombre = models.CharField(max_length=100, choices=hospitales, default='Hospital de Niños')
    direccion = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Especialidades(models.Model):
    nombre = models.CharField(max_length=100, choices=department)
    descripcion = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Agenda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default='2021-10-10 10:00:00')
    hospital = models.ForeignKey(Hospitales, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidades, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        unique_together = ("user", "fecha", "hospital")

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
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, null=True)
    mensaje = models.TextField()
    telefono = models.CharField(max_length=120)
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