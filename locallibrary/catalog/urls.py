from django.contrib.auth.views import LogoutView
from . import views
from .views import user_login, create_design_request, view_own_requests, delete_design_request, change_status, \
    add_category, manage_categories, user_profile, edit_design_request, delete_category
from .views import register
from .views import user_logout
from .views import home
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_design_request/', create_design_request, name='create_design_request'),
    path('delete_design_request/<int:request_id>/', delete_design_request, name='delete_design_request'),
    path('change_status/<int:request_id>/<str:new_status>/', change_status, name='change_status'),
    path('manage_categories/', manage_categories, name='manage_categories'),
    path('add_category/', add_category, name='add_category'),
    path('view_own_requests/', view_own_requests, name='view_own_requests'),
    path('user-profile/', user_profile, name='user_profile'),
    path('', home, name='home'),
    path('user-profile/', user_profile, name='user_profile'),
    path('edit-design-request/<int:request_id>/',
         edit_design_request, name='edit_design_request'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


