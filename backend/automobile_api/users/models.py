from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    '''Inherited model for the purposes of the Django advisory document.'''
