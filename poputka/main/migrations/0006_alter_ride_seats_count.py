# Generated by Django 5.0 on 2024-01-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_ride_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='seats_count',
            field=models.PositiveIntegerField(null=True, verbose_name='Свободные места'),
        ),
    ]