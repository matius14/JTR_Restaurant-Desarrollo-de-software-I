# Generated by Django 5.1.3 on 2024-11-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('cargoLaboral', models.CharField(max_length=100)),
                ('fechaInicio', models.DateField()),
                ('sueldo', models.IntegerField()),
                ('telefono', models.IntegerField()),
                ('correo', models.EmailField(max_length=50, unique=True)),
                ('direccion', models.CharField(max_length=70)),
                ('contracenia', models.CharField(max_length=255)),
            ],
        ),
    ]
