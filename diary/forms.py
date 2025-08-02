from django import forms

from diary.models import Diary


class DiaryForm(forms.ModelForm):
    """Форма для создания и редактирования записей дневника.
    Поля:
        title (CharField): Заголовок записи (обязательное поле)
        content (TextField): Содержание записи
        mood (ChoiceField): Настроение во время записи
        image (ImageField): Изображение к записи (опционально)
        is_public (BooleanField): Флаг публичности записи"""

    class Meta:
        model = Diary
        fields = ['title', 'content', 'mood', 'image', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите ваши мысли и события...'
            }),
            'mood': forms.Select(choices=Diary.MOOD_CHOICES),
        }
        labels = {
            'is_public': 'Сделать запись публичной',
            'mood': 'Настроение',
            'image': 'Изображение'
        }
        help_texts = {
            'is_public': 'Если отмечено, запись смогут увидеть другие пользователи',
            'mood': 'Выберите ваше текущее настроение'
        }
