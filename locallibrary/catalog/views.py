from .forms import RegistrationForm, DesignRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CategoryForm
from .models import Category
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


@login_required
def home(request):
    completed_requests = DesignRequest.objects.filter(status='Completed').order_by('-timestamp')[:4]
    user_requests = DesignRequest.objects.filter(user=request.user)
    in_progress_count = DesignRequest.objects.filter(status='In Progress').count()

    context = {
        'completed_requests': completed_requests,
        'user_requests': user_requests,
        'in_progress_count': in_progress_count,
        'user': request.user,  # Убедитесь, что в контексте есть ключ 'user'
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
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


from django.shortcuts import redirect


def user_logout(request):
    logout(request)
    return redirect(request.GET.get('next', 'home'))


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
                return redirect('home')  # Перенаправление на главную страницу
            else:
                messages.error(request, "Неправильный логин или пароль.")
        else:
            messages.error(request, "Неправильный логин или пароль.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def create_design_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            return redirect('home')  # Измените на ваше имя для главной страницы
    else:
        form = DesignRequestForm()

    return render(request, 'catalog/create_design_request.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DesignRequest


@login_required
def view_own_requests(request):
    status_filter = request.GET.get('status', 'all')

    if status_filter == 'all':
        user_requests = DesignRequest.objects.filter(user=request.user).order_by('-timestamp')
    else:
        user_requests = DesignRequest.objects.filter(user=request.user, status=status_filter).order_by('-timestamp')

    return render(request, 'catalog/view_own_requests.html',
                  {'user_requests': user_requests, 'status_filter': status_filter})


@login_required
def delete_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if design_request.user == request.user:
        design_request.delete()

    return redirect('view_own_requests')


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404


@staff_member_required
def change_status(request, request_id, new_status):
    design_request = get_object_or_404(DesignRequest, id=request_id)
    design_request.status = new_status
    design_request.save()
    return redirect('admin_home')


@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'catalog/manage_categories.html', {'categories': categories})


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'catalog/add_category.html', {'form': form})
