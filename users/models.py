from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.conf import settings


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = models.CharField(max_length=3)  # ISO 4217

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
