from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='admin_login'),
    path('logout/', views.logout_view, name='admin_logout'),
    path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('', views.dashboard_view, name='admin_home'),
]