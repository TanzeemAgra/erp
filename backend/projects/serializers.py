from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Task, TimeEntry, ProjectComment, TaskComment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ProjectCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProjectComment
        fields = ['id', 'comment', 'user', 'created_at', 'updated_at']

class TaskCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'comment', 'user', 'created_at', 'updated_at']

class TimeEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TimeEntry
        fields = ['id', 'start_time', 'end_time', 'hours', 'description', 'user', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    time_entries = TimeEntrySerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    # Write fields for assignment
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'start_date', 'due_date', 'completed_date',
            'estimated_hours', 'actual_hours',
            'assigned_to', 'assigned_to_id', 'created_by',
            'comments', 'time_entries', 'is_overdue',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        task = Task.objects.create(**validated_data)
        if assigned_to_id:
            task.assigned_to_id = assigned_to_id
            task.save()
        return task
    
    def update(self, instance, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id is not None:
            instance.assigned_to_id = assigned_to_id
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ProjectListSerializer(serializers.ModelSerializer):
    project_manager = UserSerializer(read_only=True)
    team_members = UserSerializer(many=True, read_only=True)
    budget_utilization = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    task_count = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'priority',
            'start_date', 'end_date', 'progress_percentage',
            'budget', 'spent_amount', 'budget_utilization',
            'client_name', 'client_email',
            'project_manager', 'team_members',
            'is_overdue', 'task_count', 'completed_tasks',
            'created_at', 'updated_at'
        ]
    
    def get_task_count(self, obj):
        return obj.tasks.count()
    
    def get_completed_tasks(self, obj):
        return obj.tasks.filter(status='done').count()

class ProjectDetailSerializer(serializers.ModelSerializer):
    project_manager = UserSerializer(read_only=True)
    team_members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    comments = ProjectCommentSerializer(many=True, read_only=True)
    budget_utilization = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    # Write fields for assignment
    project_manager_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    team_member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'priority',
            'start_date', 'end_date', 'progress_percentage',
            'budget', 'spent_amount', 'budget_utilization',
            'client_name', 'client_email',
            'project_manager', 'project_manager_id',
            'team_members', 'team_member_ids',
            'tasks', 'comments', 'is_overdue',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        team_member_ids = validated_data.pop('team_member_ids', [])
        project_manager_id = validated_data.pop('project_manager_id', None)
        
        project = Project.objects.create(**validated_data)
        
        if project_manager_id:
            project.project_manager_id = project_manager_id
        
        if team_member_ids:
            project.team_members.set(team_member_ids)
        
        project.save()
        return project
    
    def update(self, instance, validated_data):
        team_member_ids = validated_data.pop('team_member_ids', None)
        project_manager_id = validated_data.pop('project_manager_id', None)
        
        if project_manager_id is not None:
            instance.project_manager_id = project_manager_id
        
        if team_member_ids is not None:
            instance.team_members.set(team_member_ids)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class ProjectCreateSerializer(serializers.ModelSerializer):
    project_manager_id = serializers.IntegerField(required=False, allow_null=True)
    team_member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'status', 'priority',
            'start_date', 'end_date', 'budget',
            'client_name', 'client_email',
            'project_manager_id', 'team_member_ids'
        ]
    
    def create(self, validated_data):
        team_member_ids = validated_data.pop('team_member_ids', [])
        project_manager_id = validated_data.pop('project_manager_id', None)
        
        project = Project.objects.create(**validated_data)
        
        if project_manager_id:
            project.project_manager_id = project_manager_id
        
        if team_member_ids:
            project.team_members.set(team_member_ids)
        
        project.save()
        return project
