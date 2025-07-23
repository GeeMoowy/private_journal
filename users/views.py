from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

from .forms import RegisterForm


class RegisterView(View):
    """Представление для регистрации пользователя. Обрабатывает GET и POST запросы для регистрации:
        - GET: Отображает пустую форму регистрации.
        - POST: Проверяет данные формы, создает пользователя, выполняет вход и перенаправляет на главную страницу.
    Атрибуты:
        template_name (str): Путь к шаблону страницы регистрации
        form_class (Form): Класс формы для регистрации"""

    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request):
        """Обработка GET-запроса.
            Args:
                request: Объект HttpRequest.
            Returns:
                HttpResponse с формой регистрации"""

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Обработка POST-запроса.
            Args:
                request: Объект HttpRequest с данными формы.
            Returns:
                HttpResponse с формой (если данные невалидны) или редирект на главную страницу (если успешно)"""

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('diary:home')
        return render(request, self.template_name, {'form': form})
