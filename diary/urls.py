from django.urls import path

from diary.apps import DiaryConfig
from diary.views import DiaryView, DiaryListView, DiaryDetailView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView

app_name = DiaryConfig.name


urlpatterns = [
    path('', DiaryView.as_view(), name='home'),
    path('list/', DiaryListView.as_view(), name='diary_list'),
    path('<int:pk>/', DiaryDeleteView.as_view(), name='diary_detail'),
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
]
