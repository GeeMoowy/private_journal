from django.contrib import admin

from diary.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_filter = ('mood', 'created_at')
