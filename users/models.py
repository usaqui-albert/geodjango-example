from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.conf import settings
from django.db.models.signals import post_save

from .signals import create_auth_token


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


# Func to connect the signal on post save.
post_save.connect(
    create_auth_token,
    sender=User,
    dispatch_uid="users.models.user_post_save"
)
