from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import CategoryForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import Category


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
            return redirect('home')
    else:
        form = DesignRequestForm()

    return render(request, 'catalog/create_design_request.html', {'form': form})


from django.contrib.auth.decorators import login_required


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
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)

    if design_request.status == 'New':
        design_request.delete()

    return redirect('user_profile')


from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def change_status(request, request_id, new_status):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if design_request.status == 'New' and new_status in ['In Progress', 'Completed']:
        design_request.status = new_status
        design_request.save()
        # Дополнительные действия, например, отправка уведомления

    return redirect('admin_home')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CategoryForm
from .models import Category, DesignRequest


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'catalog/manage_categories.html', {'categories': categories})


@user_passes_test(is_staff)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'catalog/add_category.html', {'form': form})


# catalog/views.py


from django.http import JsonResponse
from .models import Category


@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'DELETE':
        category.delete()
        return JsonResponse({'message': 'Категория успешно удалена'}, status=200)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=400)


@staff_member_required
def change_status(request, request_id, new_status):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if design_request.status == 'New' and new_status in ['In Progress', 'Completed']:
        design_request.status = new_status
        design_request.save()
        # Дополнительные действия, например, отправка уведомления

    return redirect('admin_home')


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


@login_required
def user_profile(request):
    user_requests = DesignRequest.objects.filter(user=request.user)

    return render(request, 'catalog/user_profile.html', {'user_requests': user_requests})


from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request):
    user_requests = DesignRequest.objects.filter(user=request.user).order_by('-timestamp')
    context = {'user_requests': user_requests}
    return render(request, 'catalog/user_profile.html', context)


from django.shortcuts import render, get_object_or_404
from .models import DesignRequest


@login_required
def edit_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)

    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = DesignRequestForm(instance=design_request)

    return render(request, 'catalog/edit_design_request.html', {'form': form, 'design_request': design_request})


from django.shortcuts import render
from .forms import DesignRequestForm


@login_required
def create_design_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            return redirect('home')
    else:
        form = DesignRequestForm()

    return render(request, 'catalog/create_design_request.html', {'form': form})
