# Generated by Django 3.2.16 on 2022-11-27 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0009_auto_20221121_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
    ]
