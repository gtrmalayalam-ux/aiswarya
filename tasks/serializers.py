from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_name',
            'created_by', 'created_by_name', 'due_date', 'status',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'completed_at']

class TaskUpdateSerializer(serializers.ModelSerializer):
    completion_report = serializers.CharField(required=False, allow_blank=True)
    worked_hours = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    
    def validate(self, attrs):
        if attrs.get('status') == 'completed':
            if not attrs.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required when marking task as completed.'
                })
            if not attrs.get('worked_hours'):
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours is required when marking task as completed.'
                })
        return attrs

class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'assigned_to_name', 'status',
            'completion_report', 'worked_hours', 'completed_at'
        ]