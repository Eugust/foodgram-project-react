from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        help_text='email address',
        max_length=254,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self) -> str:
        return self.username
