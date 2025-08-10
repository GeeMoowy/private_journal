from django.contrib import admin

from diary.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Diary. Настройки отображения и функциональности в Django Admin:
        - Список записей с основными полями
        - Поиск по ключевым полям
            list_display (tuple): Поля для отображения в списке записей:
                - title: Заголовок записи
                - owner: Владелец записи
                - created_at: Дата создания
            search_fields (tuple): Поля по которым доступен поиск:
                - title: Поиск по заголовку
                - mood: Поиск по настроению"""

    list_display = ('title', 'owner', 'created_at')
    search_fields = ('title', 'mood')
