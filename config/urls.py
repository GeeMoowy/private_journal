from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Подключаем пути приложений
   path('', include('diary.urls', namespace='diary')),
    # path('users/', include('users.urls', namespace='users'))
]