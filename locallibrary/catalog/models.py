from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    fio_validator = RegexValidator(
        regex=r'^[А-Яа-яЁё\s-]+$',
        message='ФИО может содержать только кириллические буквы, дефис и пробелы.',
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[ASCIIUsernameValidator()],
        verbose_name='Username'
    )

    fio = models.CharField(
        max_length=255,
        validators=[fio_validator],
        verbose_name='ФИО'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Изменен related_name
        related_query_name='custom_user',
        blank=True,
        verbose_name='Группы',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Изменен related_name
        related_query_name='custom_user',
        blank=True,
        verbose_name='User permissions',
        help_text='Specific permissions for this user.'
    )

    email = models.EmailField(unique=True, verbose_name='Email')
    agreement = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# catalog/models.py
from django.db import models
from django.contrib.auth import get_user_model

# catalog/models.py
from django.db import models
from django.contrib.auth.models import User


class DesignRequest(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='design_photos/')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
