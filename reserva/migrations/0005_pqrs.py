# Generated by Django 5.1.3 on 2024-11-26 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0004_alter_carrito_tipodepago'),
    ]

    operations = [
        migrations.CreateModel(
            name='PQRS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('celular', models.IntegerField()),
                ('correo', models.EmailField(max_length=50)),
                ('numero_reserva', models.IntegerField()),
                ('detalles', models.TextField()),
            ],
        ),
    ]