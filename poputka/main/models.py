from django.db import models
from users.models import User


class Ride(models.Model):
    from_place = models.CharField('Откуда', max_length=30)
    to_place = models.CharField('Куда', max_length=30)
    ride_datetime = models.DateTimeField('Дата')
    seats_count = models.PositiveIntegerField('Свободные места', null=True)
    price = models.PositiveIntegerField('Цена за место', null=True)
    driver = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Водитель')

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'

    def __str__(self):
        return f'{self.from_place} - {self.to_place}'
