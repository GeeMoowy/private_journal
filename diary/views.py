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
        return Diary.objects.filter(owner=self.request.user).order_by('-created_at')


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
    success_url = reverse_lazy('diary:diary_list')
    context_object_name = 'diary'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Запись удалена!')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        # Только свои записи можно удалять
        return Diary.objects.filter(owner=self.request.user)
