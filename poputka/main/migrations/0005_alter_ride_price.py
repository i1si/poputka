# Generated by Django 5.0 on 2024-01-21 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_ride_price_alter_ride_seats_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='price',
            field=models.PositiveIntegerField(null=True, verbose_name='Цена за место'),
        ),
    ]
