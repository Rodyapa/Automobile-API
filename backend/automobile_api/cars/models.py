from cars.constants import MAX_CHARFIELD
from cars.validators import CarYearValidator, TextValidator, TitleValidator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

UserModel = get_user_model()


class Car(models.Model):
    '''Database model for the Car entity.'''
    make = models.CharField(
        verbose_name='Марка автомобиля',
        unique=False,  # I assume that users can have the same car.
        null=False,
        blank=False,
        max_length=MAX_CHARFIELD,
        validators=(TitleValidator(), )
    )
    model = models.CharField(
        verbose_name='Модель автомобиля',
        unique=False,
        null=False,
        blank=False,
        max_length=MAX_CHARFIELD,
        validators=(TextValidator(), )
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        null=True,
        blank=True,
        validators=(CarYearValidator(),
                    MaxValueValidator(3000),
                    MinValueValidator(1885,
                                      'Год не может быть меньше 1885.'))
    )
    description = models.TextField(
        verbose_name='Описание автомобиля',
        null=False,
        blank=False,
        validators=(TextValidator(),)
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания записи об автомобиле.',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время последнего обновления записи.',
        auto_now=True
    )
    owner = models.ForeignKey(
        to=UserModel,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        null=False,
        related_name='cars'
    )

    def __str__(self) -> str:
        return f'{self.model}'

    class Meta:
        ordering = ('-created_at', )


class Comment(models.Model):
    '''Database model for the Car Comment entity.'''
    content = models.TextField(
        verbose_name='Cодержание комментария.',
        null=False,
        blank=False,
        validators=(TextValidator(),)
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания комментария об автомобиле.',
        auto_now_add=True
    )
    car = models.ForeignKey(
        to=Car,
        verbose_name='Автомобиль',
        on_delete=models.CASCADE,
        null=False,
        related_name='comments'
    )
    author = models.ForeignKey(
        to=UserModel,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=False,
        related_name='comments'
    )

    class Meta:
        ordering = ('-created_at', )
