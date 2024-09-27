# Generated by Django 5.1.1 on 2024-09-27 15:10

import cars.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[cars.validators.CarYearValidator()], verbose_name='Год выпуска'),
        ),
    ]
