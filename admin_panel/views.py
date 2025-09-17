from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from accounts.models import CustomUser
from tasks.models import Task

def login_view(request):
    """Admin panel login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user and (user.is_admin() or user.is_superadmin()):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'admin_panel/login.html')

@login_required
def logout_view(request):
    """Admin panel logout"""
    logout(request)
    return redirect('admin_login')

@login_required
def dashboard_view(request):
    """Admin panel dashboard"""
    if not (request.user.is_admin() or request.user.is_superadmin()):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')
    
    # Dashboard statistics
    stats = {}
    
    if request.user.is_superadmin():
        stats['total_users'] = CustomUser.objects.filter(role='user').count()
        stats['total_admins'] = CustomUser.objects.filter(role='admin').count()
        stats['total_tasks'] = Task.objects.count()
        stats['completed_tasks'] = Task.objects.filter(status='completed').count()
        recent_tasks = Task.objects.all()[:5]
    else:  # Admin
        assigned_users = request.user.assigned_users.all()
        stats['assigned_users'] = assigned_users.count()
        stats['total_tasks'] = Task.objects.filter(assigned_to__in=assigned_users).count()
        stats['completed_tasks'] = Task.objects.filter(
            assigned_to__in=assigned_users, 
            status='completed'
        ).count()
        recent_tasks = Task.objects.filter(assigned_to__in=assigned_users)[:5]
    
    context = {
        'stats': stats,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
def users_list(request):
    """Users management (SuperAdmin only)"""
    if not request.user.is_superadmin():
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')
    
    users = CustomUser.objects.filter(role='user').order_by('-created_at')
    admins = CustomUser.objects.filter(role='admin').order_by('-created_at')
    
    context = {
        'users': users,
        'admins': admins,
    }
    return render(request, 'admin_panel/users.html', context)

@login_required
def create_user(request):
    """Create new user (SuperAdmin only)"""
    if not request.user.is_superadmin():
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role', 'user')
        assigned_admin_id = request.POST.get('assigned_admin')
        
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=role
            )
            
            if role == 'user' and assigned_admin_id:
                user.assigned_admin_id = assigned_admin_id
                user.save()
            
            messages.success(request, f'{role.title()} created successfully.')
            return redirect('users_list')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    admins = CustomUser.objects.filter(role='admin')
    context = {'admins': admins}
    return render(request, 'admin_panel/create_user.html', context)

@login_required
def tasks_list(request):
    """Tasks management"""
    if not (request.user.is_admin() or request.user.is_superadmin()):
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')
    
    if request.user.is_superadmin():
        tasks = Task.objects.all().order_by('-created_at')
    else:  # Admin
        assigned_users = request.user.assigned_users.all()
        tasks = Task.objects.filter(assigned_to__in=assigned_users).order_by('-created_at')
    
    context = {'tasks': tasks}
    return render(request, 'admin_panel/tasks.html', context)

@login_required
def create_task(request):
    """Create new task"""
    if not (request.user.is_admin() or request.user.is_superadmin()):
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        
        try:
            task = Task.objects.create(
                title=title,
                description=description,
                assigned_to_id=assigned_to_id,
                created_by=request.user,
                due_date=due_date
            )
            
            messages.success(request, 'Task created successfully.')
            return redirect('tasks_list')
            
        except Exception as e:
            messages.error(request, f'Error creating task: {str(e)}')
    
    # Get users that can be assigned tasks
    if request.user.is_superadmin():
        users = CustomUser.objects.filter(role='user')
    else:  # Admin
        users = request.user.assigned_users.all()
    
    context = {'users': users}
    return render(request, 'admin_panel/create_task.html', context)

@login_required
def task_detail(request, pk):
    """Task detail and completion report"""
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions
    if not task.can_view_report(request.user):
        messages.error(request, 'Access denied.')
        return redirect('tasks_list')
    
    context = {'task': task}
    return render(request, 'admin_panel/task_detail.html', context)

@login_required
def delete_user(request, pk):
    """Delete user (SuperAdmin only)"""
    if not request.user.is_superadmin():
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')
    
    user = get_object_or_404(CustomUser, pk=pk)
    if user != request.user:  # Can't delete self
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'You cannot delete yourself.')
    
    return redirect('users_list')