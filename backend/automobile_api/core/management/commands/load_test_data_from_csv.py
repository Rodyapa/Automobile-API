import csv
import os

from cars.models import Car, Comment
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


def users_import(row):
    if not UserModel.objects.filter(username=row[0]):
        UserModel.objects.create_user(
            username=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            password=row[4]
        )


def cars_import(row):
    owner = UserModel.objects.get(id=row[4])
    Car.objects.get_or_create(
        make=row[0],
        model=row[1],
        year=row[2],
        description=row[3],
        owner=owner
    )


def comments_import(row):
    car = Car.objects.get(id=row[1])
    author = UserModel.objects.get(id=row[2])
    Comment.objects.get_or_create(
        content=row[0],
        author=author,
        car=car
    )


action = {
    'users.csv': users_import,
    'cars.csv': cars_import,  # Must to be after user_import
    'comments.csv': comments_import,  # Must to be after user and cars imports
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'tests/test_data/')
        for key in action.keys():
            with open(path + key, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    action[key](row)
