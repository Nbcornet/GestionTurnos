# from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_medico = models.BooleanField(default=False)
    is_paciente = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

  


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # CASCADE, al eliminar el usuario, elimina el profile
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.first_name} Profile'
