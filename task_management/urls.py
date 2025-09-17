"""
URL configuration for task_management project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api/auth/', include('accounts.urls')),
    path('admin-panel/', include('admin_panel.urls')),
]