from django.conf import settings
from django.db import models


class Diary(models.Model):
    """ """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diaries',
        verbose_name='Владелец',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
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
        ('😂', 'Юмор'),
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

    class Meta:
        verbose_name = 'Дневник'
        verbose_name_plural = 'Дневники'
        permissions = [
            ("can_delete_public_diaries", "Может удалять любые публичные записи"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Всегда пересчитываем время чтения, если есть содержимое
        if self.content:
            word_count = len(self.content.split())
            self.read_time = max(1, round(word_count / 200))
        super().save(*args, **kwargs)
