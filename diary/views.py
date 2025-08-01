from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from diary.models import Diary
from diary.forms import DiaryForm


class HomeView(TemplateView):
    template_name = 'diary/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context


class DiaryListView(LoginRequiredMixin, ListView):
    """  """

    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        # Только записи текущего пользователя + сортировка по дате
        queryset = Diary.objects.filter(owner=self.request.user).order_by('-created_at')

        # Получаем поисковый запрос из параметра 'q' в URL
        search_query = self.request.GET.get('q')

        if search_query:
            # Ищем по заголовку (регистронезависимо)
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем поисковый запрос в контекст для отображения в форме
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DiaryDetailView(LoginRequiredMixin, DetailView):
    """  """

    model = Diary
    template_name = 'diary/diary_detail.html'
    context_object_name = 'diary'

    def get_queryset(self):
        # Защита от просмотра чужих записей
        return Diary.objects.filter(owner=self.request.user)


class DiaryCreateView(LoginRequiredMixin, CreateView):
    """  """

    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        # Автоматическое привязывание к текущему пользователю
        form.instance.owner = self.request.user
        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    context_object_name = 'diary'

    def get_success_url(self):
        messages.success(self.request, 'Запись обновлена!')
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        # Только свои записи можно редактировать
        return Diary.objects.filter(owner=self.request.user)


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Diary
    template_name = 'diary/diary_confirm_delete.html'
    context_object_name = 'diary'

    def get_success_url(self):
        # Определяем, откуда пришел запрос (публичная/личная запись)
        if self.object.is_public and not self.object.owner == self.request.user:
            messages.success(self.request, 'Публичная запись удалена!')
            return reverse_lazy('diary:public_list')
        else:
            messages.success(self.request, 'Ваша запись удалена!')
            return reverse_lazy('diary:diary_list')

    def get_queryset(self):
        queryset = Diary.objects.filter(owner=self.request.user)
        if self.request.user.has_perm('diary.can_delete_public_diaries'):
            queryset |= Diary.objects.filter(is_public=True)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj not in self.get_queryset():
            raise PermissionDenied("У вас нет прав на удаление этой записи.")
        return super().dispatch(request, *args, **kwargs)


class PublicDiaryListView(ListView):
    """  """

    model = Diary
    template_name = 'diary/public_diary_list.html'
    context_object_name = 'public_diaries'
    paginate_by = 10

    def get_queryset(self):
        queryset = Diary.objects.filter(is_public=True)
        return queryset.exclude(owner=self.request.user).order_by('-created_at')


class PublicDiaryDetailView(DetailView):
    model = Diary
    template_name = 'diary/public_diary_detail.html'
    context_object_name = 'diary'

    def get_queryset(self):
        return Diary.objects.filter(is_public=True)
