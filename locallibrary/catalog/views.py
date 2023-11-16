from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DesignRequest


@login_required
def home(request):
    # Получите последние 4 выполненные заявки
    completed_requests = DesignRequest.objects.filter(status='Completed').order_by('-timestamp')[:4]

    # Получите количество заявок в статусе "Принято в работу"
    in_progress_count = DesignRequest.objects.filter(status='In Progress').count()

    context = {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
        'user': request.user,  # Добавьте текущего пользователя в контекст
    }

    return render(request, 'catalog/home.html', context)


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


from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect('home')  # Измените на ваше имя для главной страницы
            else:
                messages.error(request, "Неправильный логин или пароль.")
        else:
            messages.error(request, "Неправильный логин или пароль.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
