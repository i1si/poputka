# Generated by Django 5.0 on 2024-01-21 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_ride_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='price',
            field=models.IntegerField(null=True, verbose_name='Цена за место'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='seats_count',
            field=models.PositiveIntegerField(verbose_name='Свободные места'),
        ),
    ]
