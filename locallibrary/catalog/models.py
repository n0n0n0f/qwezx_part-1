from django.contrib.auth.models import BaseUserManager, User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Введите новую категорию заявки')

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Этот email уже занят')
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
        help_text='Группы, к которым принадлежит этот пользователь. Пользователь получит все разрешения, '
                  'предоставленные каждой из его групп..'
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


class DesignRequest(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='design_request_photos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    STATUS_CHOICES = [
        ('New', 'Новая'),
        ('In Progress', 'Принято в работу'),
        ('Completed', 'Выполнено'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image_admin = models.ImageField(verbose_name="Фотография дизайна", upload_to='images_admin/',
                                    validators=[
                                        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])],
                                    help_text="Указать фото дизайна при смене статуса на 'Выполнено'", blank=True)
    comment_admin = models.TextField(verbose_name="Комментарий",
                                     help_text="Указать комментарий при смене статуса на 'Принята в работу'",
                                     blank=True)

    def save(self, *args, **kwargs):
        # Проверяем, изменился ли статус на "Выполнено" и есть ли изображение
        if self.status == 'Выполнено' and not self.design_image:
            raise ValidationError("При смене статуса на 'Выполнено' необходимо добавить изображение дизайна.")
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Проверяем, изменился ли статус на "Принято в работу" и есть ли комментарий
        if self.status == 'Принято в работу' and not self.comments:
            raise ValidationError("При смене статуса на 'Принято в работу' необходимо указать комментарий.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
