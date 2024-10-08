# Generated by Django 5.1.1 on 2024-09-28 12:07

import cars.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_car_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[cars.validators.CarYearValidator(), django.core.validators.MaxValueValidator(3000), django.core.validators.MinValueValidator(1885, 'Год не может быть меньше 1885.')], verbose_name='Год выпуска'),
        ),
    ]
