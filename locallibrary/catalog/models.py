from django.db import models
# catalog/models.py
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Email')
    agreement = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        verbose_name='Группы',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        verbose_name='User permissions',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
