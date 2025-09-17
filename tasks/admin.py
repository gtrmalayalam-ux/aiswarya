from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'created_by', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'assigned_to', 'created_by', 'due_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Completion Details', {
            'fields': ('completion_report', 'worked_hours', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('completed_at',)