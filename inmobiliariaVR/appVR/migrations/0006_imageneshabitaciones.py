# Generated by Django 2.0.2 on 2018-03-24 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appVR', '0005_auto_20180324_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenesHabitaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_habitacion', models.FileField(upload_to='')),
                ('nombre_habitacion', models.CharField(max_length=100)),
                ('nombre_casa', models.CharField(max_length=100)),
            ],
        ),
    ]
