# Generated by Django 3.2.16 on 2022-12-15 03:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='agenda',
            unique_together={('user', 'fecha', 'hospital')},
        ),
    ]
