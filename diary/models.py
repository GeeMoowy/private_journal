from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Diary(models.Model):
    """ """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diaries',
        verbose_name='Пользователь - создатель дневника'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок записи',
        help_text='Введите заголовок записи'
    )
    content = models.TextField(
        verbose_name='Содержание записи',
        help_text='Поделитесь своей записью (текст записи)'
    )
    MOOD_CHOICES = [
        ('😊', 'Счастье'),
        ('😟', 'Грусть'),
        ('😡', 'Злость'),
        ('😫', 'Усталость'),
        ('🤩', 'Воодушевление'),
        ('😮', 'Удивление'),
        ('😍', 'Влюбленность')
    ]
    mood = models.CharField(
        max_length=2,
        choices=MOOD_CHOICES,
        blank=True,
        verbose_name='Настроение',
        help_text='Выберите ваше настроение'
    )
    image = models.ImageField(
        upload_to='diary_images/',
        blank=True,
        verbose_name='Картинка',
        help_text='Загрузите картинку'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная запись',
        help_text='Является ли запись публичной?'
    )
    read_time = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Время чтения (мин)'
    )

    def __str__(self):
        return self.title
