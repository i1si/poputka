# Generated by Django 5.0 on 2024-02-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_ride_seats_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('subject', models.CharField(verbose_name='Субъект')),
                ('latitude', models.CharField(verbose_name='Широта')),
                ('longtitude', models.CharField(verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Города',
            },
        ),
    ]
