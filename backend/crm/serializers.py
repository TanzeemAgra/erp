from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Client, ContactPerson, ClientInteraction, Opportunity, Task,
    ClientCategory, ClientStatus, IndustryType, InteractionType, OpportunityStage
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class ContactPersonSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = ContactPerson
        fields = '__all__'


class ClientInteractionSerializer(serializers.ModelSerializer):
    handled_by_name = serializers.CharField(source='handled_by.get_full_name', read_only=True)
    contact_person_name = serializers.CharField(source='contact_person.full_name', read_only=True)
    interaction_type_display = serializers.CharField(source='get_interaction_type_display', read_only=True)
    
    class Meta:
        model = ClientInteraction
        fields = '__all__'


class OpportunitySerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    weighted_value = serializers.ReadOnlyField()
    
    class Meta:
        model = Opportunity
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    opportunity_name = serializers.CharField(source='opportunity.title', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'


class ClientListSerializer(serializers.ModelSerializer):
    """Serializer for client list view with minimal fields"""
    account_manager_name = serializers.CharField(source='account_manager.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    industry_display = serializers.CharField(source='get_industry_display', read_only=True)
    
    # Counts
    contacts_count = serializers.SerializerMethodField()
    interactions_count = serializers.SerializerMethodField()
    opportunities_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'company_name', 'contact_person', 'email', 'phone', 'website',
            'industry', 'industry_display', 'category', 'category_display', 
            'status', 'status_display', 'city', 'state', 'country',
            'account_manager', 'account_manager_name', 'assigned_to', 'assigned_to_name',
            'first_contact_date', 'last_contact_date', 'next_follow_up',
            'contacts_count', 'interactions_count', 'opportunities_count', 'tasks_count',
            'created_at', 'updated_at'
        ]
    
    def get_contacts_count(self, obj):
        return obj.contacts.count()
    
    def get_interactions_count(self, obj):
        return obj.interactions.count()
    
    def get_opportunities_count(self, obj):
        return obj.opportunities.count()
    
    def get_tasks_count(self, obj):
        return obj.tasks.filter(status__in=['pending', 'in_progress']).count()


class ClientDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for client detail view"""
    account_manager_name = serializers.CharField(source='account_manager.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    industry_display = serializers.CharField(source='get_industry_display', read_only=True)
    full_address = serializers.ReadOnlyField()
    
    # Related data
    contacts = ContactPersonSerializer(many=True, read_only=True)
    recent_interactions = serializers.SerializerMethodField()
    active_opportunities = serializers.SerializerMethodField()
    pending_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = '__all__'
        extra_fields = [
            'account_manager_name', 'assigned_to_name', 'created_by_name',
            'category_display', 'status_display', 'industry_display', 'full_address',
            'contacts', 'recent_interactions', 'active_opportunities', 'pending_tasks'
        ]
    
    def get_recent_interactions(self, obj):
        interactions = obj.interactions.order_by('-interaction_date')[:5]
        return ClientInteractionSerializer(interactions, many=True).data
    
    def get_active_opportunities(self, obj):
        opportunities = obj.opportunities.exclude(stage__in=['closed_won', 'closed_lost'])
        return OpportunitySerializer(opportunities, many=True).data
    
    def get_pending_tasks(self, obj):
        tasks = obj.tasks.filter(status__in=['pending', 'in_progress'])
        return TaskSerializer(tasks, many=True).data


class ClientCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating clients"""
    
    class Meta:
        model = Client
        exclude = ['created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set created_by to the current user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


# Choice serializers for frontend dropdowns
class ChoicesSerializer(serializers.Serializer):
    client_categories = serializers.SerializerMethodField()
    client_statuses = serializers.SerializerMethodField()
    industries = serializers.SerializerMethodField()
    interaction_types = serializers.SerializerMethodField()
    opportunity_stages = serializers.SerializerMethodField()
    task_priorities = serializers.SerializerMethodField()
    task_statuses = serializers.SerializerMethodField()
    
    def get_client_categories(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in ClientCategory.choices]
    
    def get_client_statuses(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in ClientStatus.choices]
    
    def get_industries(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in IndustryType.choices]
    
    def get_interaction_types(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in InteractionType.choices]
    
    def get_opportunity_stages(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in OpportunityStage.choices]
    
    def get_task_priorities(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in Task.PRIORITY_CHOICES]
    
    def get_task_statuses(self, obj):
        return [{'value': choice[0], 'label': choice[1]} for choice in Task.STATUS_CHOICES]


# Dashboard Statistics Serializer
class CRMDashboardSerializer(serializers.Serializer):
    total_clients = serializers.IntegerField()
    total_leads = serializers.IntegerField()
    total_opportunities = serializers.IntegerField()
    total_opportunity_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending_tasks = serializers.IntegerField()
    recent_interactions = serializers.IntegerField()
    
    # Charts data
    clients_by_status = serializers.ListField()
    clients_by_industry = serializers.ListField()
    opportunities_by_stage = serializers.ListField()
    monthly_interactions = serializers.ListField()
    top_opportunities = OpportunitySerializer(many=True)
    upcoming_tasks = TaskSerializer(many=True)
