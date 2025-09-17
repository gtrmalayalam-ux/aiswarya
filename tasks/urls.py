from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/report/', views.task_report, name='task_report'),
]