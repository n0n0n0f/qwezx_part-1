from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm


def home(request):
    return HttpResponse("Hello Group")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')  # Измените на ваше имя для главной страницы
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


# catalog/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect


def user_logout(request):
    logout(request)
    return redirect('home')  # Измените на ваше имя для главной страницы
