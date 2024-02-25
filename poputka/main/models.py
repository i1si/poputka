from django.db import models
from users.models import User


class Ride(models.Model):
    from_place = models.CharField('Откуда', max_length=30)
    to_place = models.CharField('Куда', max_length=30)
    ride_datetime = models.DateTimeField('Дата')
    seats_count = models.PositiveIntegerField('Свободные места', null=True)
    price = models.PositiveIntegerField('Цена за место', null=True)
    text = models.CharField('Описание', null=True)
    driver = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Водитель')

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'

    def __str__(self):
        return f'{self.from_place} - {self.to_place}'
    

class City(models.Model):
    name = models.CharField('Название')
    subject = models.CharField('Субъект')
    latitude = models.CharField('Широта')
    longtitude = models.CharField('Долгота')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.name}, {self.subject}'


class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Не понравилось'),
        (2, 'Ожидания не оправдались'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]
    author = models.ForeignKey(to=User, on_delete=models.SET('Удален'), verbose_name='Автор', related_name='author')
    rated_user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.CharField('Текст', max_length=300)
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)    # TODO выбор из нескольких оценок
    date = models.DateField('Дата')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return f'{self.rated_user} | {self.rating}'
    