from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с аутентификацией по email и поддержкой аватара.
    Наследуется от AbstractUser, но полностью отключает стандартное поле username,
    заменяя его на email в качестве уникального идентификатора пользователя.
    Добавляет возможность загрузки аватара.

    Атрибуты:
        email (EmailField): Уникальный email пользователя, используется для входа вместо username.
            - Параметры: unique=True, verbose_name='Email', help_text
        avatar (ImageField): Необязательное изображение-аватар пользователя.
            - Параметры: upload_to='avatars/', verbose_name='Фото', null=True, blank=True,
            help_text='Загрузите свое фото'
        USERNAME_FIELD = 'email': указывает, что email используется как идентификатор для входа
        REQUIRED_FIELDS = []: список обязательных полей при создании суперпользователя

    Методы:
        __str__(): возвращает строковое представление пользователя в формате "Пользователь email@example.com"

    Meta-класс:
        verbose_name = 'Пользователь', verbose_name_plural = 'Пользователи'

    Менеджер:
        objects = UserManager(): кастомный менеджер пользователей, поддерживающий создание
                                пользователей и суперпользователей по email"""

    # Полностью отключаем стандартное поле username
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Введите свой email'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Фото',
        null=True,
        blank=True,
        help_text='Загрузите свое фото'
    )
    nickname = models.CharField(
        max_length=50,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.nickname:  # Если nickname не указан
            self.nickname = self.email.split('@')[0]  # Берем часть до @
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Пользователь {self.email}'
