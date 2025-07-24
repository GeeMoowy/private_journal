from django import forms

from diary.models import Diary


class DiaryForm(forms.ModelForm):
    """  """

    class Meta:
        model = Diary
        fields = ['title', 'content', 'mood', 'image', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'mood': forms.Select(choices=Diary.MOOD_CHOICES),
        }
        labels = {
            'is_public': 'Сделать запись публичной'
        }
