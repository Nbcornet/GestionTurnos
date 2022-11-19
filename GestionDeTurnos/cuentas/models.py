# from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.core.files import File # NEW

# Create your models here.

class User(AbstractUser):
    is_medico = models.BooleanField(default=False)
    is_paciente = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # CASCADE, al eliminar el usuario, elimina el profile
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # def save(self):
    #     super().save()

    #     img = File.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size= (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

# class medico(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE) # CASCADE, al eliminar el usuario, elimina el profile

