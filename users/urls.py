from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
#from .views import RegisterView, ProfileEditView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
    #path('register/', RegisterView.as_view(template_name='register.html'), name='register'),
    #path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
]