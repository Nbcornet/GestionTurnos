# Generated by Django 3.2.16 on 2022-11-16 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialidades',
            name='codigo',
            field=models.IntegerField(unique=True),
        ),
    ]
