from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Project, Task, TimeEntry, ProjectComment, TaskComment
from .serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectCreateSerializer,
    TaskSerializer, TimeEntrySerializer, ProjectCommentSerializer, TaskCommentSerializer,
    UserSerializer
)

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'project_manager']
    search_fields = ['name', 'description', 'client_name']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        elif self.action in ['retrieve']:
            return ProjectDetailSerializer
        return ProjectListSerializer
    
    def get_queryset(self):
        queryset = Project.objects.select_related('project_manager').prefetch_related('team_members', 'tasks')
        
        # Filter by team member
        team_member = self.request.query_params.get('team_member', None)
        if team_member:
            queryset = queryset.filter(team_members__id=team_member)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for projects"""
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status__in=['planning', 'in_progress']).count()
        completed_projects = Project.objects.filter(status='completed').count()
        overdue_projects = Project.objects.filter(
            end_date__lt=timezone.now().date(),
            status__in=['planning', 'in_progress']
        ).count()
        
        # Budget analysis
        budget_stats = Project.objects.aggregate(
            total_budget=Sum('budget'),
            total_spent=Sum('spent_amount')
        )
        
        # Recent projects
        recent_projects = Project.objects.order_by('-created_at')[:5]
        recent_serializer = ProjectListSerializer(recent_projects, many=True)
        
        return Response({
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'overdue_projects': overdue_projects,
            'budget_stats': budget_stats,
            'recent_projects': recent_serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a project"""
        project = self.get_object()
        comment_text = request.data.get('comment', '')
        
        if not comment_text:
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = ProjectComment.objects.create(
            project=project,
            user=request.user,
            comment=comment_text
        )
        
        serializer = ProjectCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update project progress"""
        project = self.get_object()
        progress = request.data.get('progress', None)
        
        if progress is None or not (0 <= progress <= 100):
            return Response({'error': 'Progress must be between 0 and 100'}, status=status.HTTP_400_BAD_REQUEST)
        
        project.progress_percentage = progress
        project.save()
        
        serializer = self.get_serializer(project)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def time_tracking(self, request, pk=None):
        """Get time tracking data for a project"""
        project = self.get_object()
        time_entries = TimeEntry.objects.filter(task__project=project).select_related('user', 'task')
        
        # Group by user
        user_stats = {}
        for entry in time_entries:
            user_id = entry.user.id
            if user_id not in user_stats:
                user_stats[user_id] = {
                    'user': UserSerializer(entry.user).data,
                    'total_hours': 0,
                    'entries': []
                }
            user_stats[user_id]['total_hours'] += entry.hours or 0
            user_stats[user_id]['entries'].append(TimeEntrySerializer(entry).data)
        
        return Response({
            'total_hours': sum(entry.hours or 0 for entry in time_entries),
            'user_stats': list(user_stats.values())
        })

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Task.objects.select_related('project', 'assigned_to', 'created_by').prefetch_related('comments', 'time_entries')
        
        # Filter by project
        project_id = self.request.query_params.get('project_id', None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        # Filter by assigned user
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        # Filter by due date
        due_date = self.request.query_params.get('due_date', None)
        if due_date:
            queryset = queryset.filter(due_date=due_date)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a task"""
        task = self.get_object()
        comment_text = request.data.get('comment', '')
        
        if not comment_text:
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = TaskComment.objects.create(
            task=task,
            user=request.user,
            comment=comment_text
        )
        
        serializer = TaskCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def start_timer(self, request, pk=None):
        """Start time tracking for a task"""
        task = self.get_object()
        
        # Check if there's already an active timer
        active_timer = TimeEntry.objects.filter(
            task=task,
            user=request.user,
            end_time__isnull=True
        ).first()
        
        if active_timer:
            return Response({'error': 'Timer already running for this task'}, status=status.HTTP_400_BAD_REQUEST)
        
        time_entry = TimeEntry.objects.create(
            task=task,
            user=request.user,
            start_time=timezone.now()
        )
        
        serializer = TimeEntrySerializer(time_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def stop_timer(self, request, pk=None):
        """Stop time tracking for a task"""
        task = self.get_object()
        
        active_timer = TimeEntry.objects.filter(
            task=task,
            user=request.user,
            end_time__isnull=True
        ).first()
        
        if not active_timer:
            return Response({'error': 'No active timer found for this task'}, status=status.HTTP_400_BAD_REQUEST)
        
        active_timer.end_time = timezone.now()
        active_timer.save()  # This will automatically calculate hours
        
        # Update task actual hours
        task.actual_hours += active_timer.hours or 0
        task.save()
        
        serializer = TimeEntrySerializer(active_timer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get tasks assigned to the current user"""
        tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue_tasks(self, request):
        """Get overdue tasks"""
        overdue_tasks = Task.objects.filter(
            due_date__lt=timezone.now().date(),
            status__in=['todo', 'in_progress', 'review']
        ).order_by('due_date')
        
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)

class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['task', 'user']
    ordering = ['-start_time']
    
    def get_queryset(self):
        queryset = TimeEntry.objects.select_related('task', 'user')
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_time__date__lte=end_date)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def user_report(self, request):
        """Get time tracking report for current user"""
        user_entries = TimeEntry.objects.filter(user=request.user)
        
        # Get date range from query params
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if start_date:
            user_entries = user_entries.filter(start_time__date__gte=start_date)
        if end_date:
            user_entries = user_entries.filter(start_time__date__lte=end_date)
        
        total_hours = sum(entry.hours or 0 for entry in user_entries)
        
        # Group by project
        project_stats = {}
        for entry in user_entries:
            project_name = entry.task.project.name
            if project_name not in project_stats:
                project_stats[project_name] = {
                    'project': entry.task.project.name,
                    'total_hours': 0,
                    'tasks': set()
                }
            project_stats[project_name]['total_hours'] += entry.hours or 0
            project_stats[project_name]['tasks'].add(entry.task.title)
        
        # Convert sets to lists for JSON serialization
        for project in project_stats.values():
            project['tasks'] = list(project['tasks'])
            project['task_count'] = len(project['tasks'])
        
        return Response({
            'total_hours': total_hours,
            'project_breakdown': list(project_stats.values()),
            'entries': TimeEntrySerializer(user_entries, many=True).data
        })
