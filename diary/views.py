from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from diary.models import Diary
from diary.forms import DiaryForm


class HomeView(TemplateView):
    """Главная страница дневника. Отображает различный контент для аутентифицированных
    и неаутентифицированных пользователей."""

    template_name = 'diary/home.html'

    def get_context_data(self, **kwargs):
        """Добавляет текущего пользователя в контекст шаблона если он аутентифицирован"""

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context


class DiaryListView(LoginRequiredMixin, ListView):
    """Список личных записей дневника текущего пользователя.
        Поддерживает:
            - Пагинацию (по 10 записей на страницу)
            - Поиск по заголовку и содержанию через параметр GET 'q'
            - Сортировку по дате создания (новые сначала)"""

    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        """Возвращает только записи текущего пользователя с возможностью поиска"""

        queryset = Diary.objects.filter(owner=self.request.user).order_by('-created_at')

        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет поисковый запрос в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DiaryDetailView(LoginRequiredMixin, DetailView):
    """Детальное отображение одной записи дневника. Гарантирует что пользователь может просматривать
    только свои записи"""

    model = Diary
    template_name = 'diary/diary_detail.html'
    context_object_name = 'diary'

    def get_queryset(self):
        """Фильтрует записи - только принадлежащие текущему пользователю."""

        return Diary.objects.filter(owner=self.request.user)


class DiaryCreateView(LoginRequiredMixin, CreateView):
    """Создание новой записи дневника. Автоматически привязывает созданную запись к текущему пользователю.
    При успешном создании показывает сообщение об успехе"""

    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        """Устанавливает владельца записи и добавляет сообщение об успехе"""

        form.instance.owner = self.request.user
        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование существующей записи дневника. Позволяет изменять только свои записи. При успешном обновлении
    перенаправляет на детальную страницу записи"""

    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    context_object_name = 'diary'

    def get_success_url(self):
        """Добавляет сообщение об успехе и возвращает URL для перенаправления"""

        messages.success(self.request, 'Запись обновлена!')
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        """Фильтрует записи - только принадлежащие текущему пользователю"""

        return Diary.objects.filter(owner=self.request.user)


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление записи дневника.
        Особенности:
        - Пользователь может удалять только свои записи
        - Модераторы, с разрешением 'diary.can_delete_public_diaries', могут удалять любые публичные записи
        - Разные сообщения и URL перенаправления для личных/публичных записей"""

    model = Diary
    template_name = 'diary/diary_confirm_delete.html'
    context_object_name = 'diary'

    def get_success_url(self):
        """Определяет URL перенаправления в зависимости от типа записи"""

        if self.object.is_public and not self.object.owner == self.request.user:
            messages.success(self.request, 'Публичная запись удалена!')
            return reverse_lazy('diary:public_list')
        else:
            messages.success(self.request, 'Ваша запись удалена!')
            return reverse_lazy('diary:diary_list')

    def get_queryset(self):
        """Возвращает:
            - Все записи пользователя
            - Все публичные записи (если у пользователя есть права)"""

        queryset = Diary.objects.filter(owner=self.request.user)
        if self.request.user.has_perm('diary.can_delete_public_diaries'):
            queryset |= Diary.objects.filter(is_public=True)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        """Проверяет права доступа перед выполнением действия"""

        obj = self.get_object()
        if obj not in self.get_queryset():
            raise PermissionDenied("У вас нет прав на удаление этой записи.")
        return super().dispatch(request, *args, **kwargs)


class PublicDiaryListView(ListView):
    """Список публичных записей всех пользователей. Исключает записи текущего пользователя (чтобы не дублировать
    личный дневник). Сортирует записи по дате создания (новые сначала)"""

    model = Diary
    template_name = 'diary/public_diary_list.html'
    context_object_name = 'public_diaries'
    paginate_by = 10

    def get_queryset(self):
        """Возвращает только публичные записи других пользователей"""

        queryset = Diary.objects.filter(is_public=True)
        return queryset.exclude(owner=self.request.user).order_by('-created_at')


class PublicDiaryDetailView(DetailView):
    """Детальное отображение публичной записи. Доступно всем пользователям (включая неаутентифицированных)"""

    model = Diary
    template_name = 'diary/public_diary_detail.html'
    context_object_name = 'diary'

    def get_queryset(self):
        """Возвращает только публичные записи"""

        return Diary.objects.filter(is_public=True)
