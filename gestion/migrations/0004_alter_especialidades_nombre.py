# Generated by Django 3.2.14 on 2022-11-16 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0003_auto_20221115_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialidades',
            name='nombre',
            field=models.CharField(choices=[('Dentistry', 'Dentistry'), ('Cardiology', 'Cardiology'), ('ENT Specialists', 'ENT Specialists'), ('Astrology', 'Astrology'), ('Neuroanatomy', 'Neuroanatomy'), ('Blood Screening', 'Blood Screening'), ('Eye Care', 'Eye Care'), ('Physical Therapy', 'Physical Therapy')], max_length=100),
        ),
    ]
