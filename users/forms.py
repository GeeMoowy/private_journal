from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя, расширяющая стандартную UserCreationForm.

    Добавляет дополнительные поля:
    - nickname (необязательное поле для отображения имени пользователя)
    - avatar (необязательное поле для загрузки аватара)

    Особенности:
    - Автоматически генерирует nickname из email, если он не указан
    - Включает валидацию на уникальность email и nickname
    - Поддерживает загрузку аватара при регистрации

    Атрибуты:
        password1 (CharField): Поле для ввода пароля
        password2 (CharField): Поле для подтверждения пароля
        nickname (CharField): Необязательное поле для никнейма пользователя

    Meta:
        model (CustomUser): Связь с кастомной моделью пользователя
        fields (tuple): Поля, включаемые в форму (email, nickname, avatar)
        widgets (dict): Кастомизация виджетов для полей формы

    Методы:
        clean_nickname: Проверяет уникальность nickname
        clean_email: Проверяет уникальность email"""

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    nickname = forms.CharField(
        label="Никнейм",
        required=False,  # Делаем необязательным, так как у вас есть логика авто-заполнения
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Если не указать, будет использована часть email до @"
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'avatar')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def clean_nickname(self):
        """Валидация поля nickname. Проверяет, что указанный никнейм еще не занят другим пользователем.
        Если nickname не указан, проверка не выполняется
        (значение будет автоматически сгенерировано из email при сохранении).
            Возвращает:
                str: Валидный никнейм
            Вызывает:
                ValidationError: Если nickname уже существует в системе"""

        nickname = self.cleaned_data.get('nickname')
        if nickname and CustomUser.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("Этот никнейм уже занят")
        return nickname

    def clean_email(self):
        """Валидация поля email. Проверяет, что указанный email еще не зарегистрирован в системе.
            Возвращает:
                str: Валидный email
            Вызывает:
                ValidationError: Если email уже существует в системе"""

        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован")
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'nickname']
