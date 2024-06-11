from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    tg_chat_id = models.BigIntegerField()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
