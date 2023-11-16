from django.urls import path
from . import views

urlpatterns = [
    path('', views.home)
]

from django.urls import path
from .views import register

urlpatterns = [
    # Другие маршруты...
    path('register/', register, name='register'),
]
