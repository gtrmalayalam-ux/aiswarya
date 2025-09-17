from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='api_login'),
    path('refresh/', views.refresh_token_view, name='api_refresh'),
]