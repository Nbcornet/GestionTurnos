# Generated by Django 3.2.14 on 2022-11-19 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0005_auto_20221119_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='fecha_fin',
            field=models.DateField(default='2021-10-01'),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='fecha_inicio',
            field=models.DateField(default='2021-10-01'),
        ),
    ]
