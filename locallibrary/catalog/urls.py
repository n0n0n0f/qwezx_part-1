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

# catalog/urls.py
from django.urls import path
from .views import user_login

urlpatterns = [
    # Другие маршруты...
    path('login/', user_login, name='login'),
]

# catalog/urls.py
from django.urls import path
from .views import user_logout

urlpatterns = [
    # Другие маршруты...
    path('logout/', user_logout, name='logout'),
]
