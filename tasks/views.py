from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    """
    GET /tasks: Fetch all tasks assigned to the logged-in user
    """
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def task_update(request, pk):
    """
    PUT /tasks/{id}: Update task status (mark as completed with report and hours)
    """
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    
    serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        # If marking as completed, set completion timestamp
        if serializer.validated_data.get('status') == 'completed':
            serializer.validated_data['completed_at'] = timezone.now()
        
        serializer.save()
        
        # Return updated task data
        task_serializer = TaskSerializer(task)
        return Response(task_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_report(request, pk):
    """
    GET /tasks/{id}/report: View completion report (Admin/SuperAdmin only)
    """
    task = get_object_or_404(Task, pk=pk)
    
    # Check if user has permission to view the report
    if not task.can_view_report(request.user):
        return Response(
            {'error': 'You do not have permission to view this task report.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Check if task is completed
    if task.status != 'completed':
        return Response(
            {'error': 'Task is not completed yet.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = TaskReportSerializer(task)
    return Response(serializer.data)