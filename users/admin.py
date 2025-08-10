from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления пользователями системы. Предоставляет администратору следующие
    возможности:
        - Просмотр списка пользователей с ключевой информацией
        - Поиск пользователей по email
        - Фильтрация по статусу персонала, активности и дате регистрации

            list_display (tuple): Поля для отображения в списке:
                - email: Уникальный идентификатор пользователя
                - date_joined: Дата и время регистрации
                - is_staff: Статус доступа к административной панели
            search_fields (tuple): Поля для поиска:
                - email: Поиск по полному или частичному совпадению email
            list_filter (tuple): Фильтры для правой боковой панели:
                - is_staff: Фильтр по наличию прав персонала
                - is_active: Фильтр по активности аккаунта
                - date_joined: Фильтр по дате регистрации"""

    list_display = ('email', 'date_joined', 'is_staff')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active', 'date_joined')
