# from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.core.files import File # NEW

# Create your models here.

class User(AbstractUser):
    is_medico = models.BooleanField(default=False)
    is_paciente = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.username

