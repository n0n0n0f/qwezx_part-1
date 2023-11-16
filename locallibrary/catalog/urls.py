from . import views
from .views import user_login
from .views import register
from .views import user_logout
from .views import home
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='base_generic'),
    path('home/', home, name='home'),
]
# Ваш проект/приложение/urls.py


