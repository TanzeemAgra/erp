from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Client, ContactPerson, ClientInteraction, Opportunity, Task
from .serializers import (
    ClientListSerializer, ClientDetailSerializer, ClientCreateUpdateSerializer,
    ContactPersonSerializer, ClientInteractionSerializer, OpportunitySerializer,
    TaskSerializer, UserSerializer, ChoicesSerializer, CRMDashboardSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'industry', 'account_manager', 'assigned_to']
    search_fields = ['company_name', 'contact_person', 'email', 'phone', 'city', 'state']
    ordering_fields = ['company_name', 'created_at', 'last_contact_date', 'next_follow_up']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClientListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClientCreateUpdateSerializer
        else:
            return ClientDetailSerializer
    
    def get_queryset(self):
        queryset = Client.objects.select_related(
            'account_manager', 'assigned_to', 'created_by'
        ).prefetch_related(
            'contacts', 'interactions', 'opportunities', 'tasks'
        )
        return queryset
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get CRM dashboard statistics"""
        # Basic counts
        total_clients = Client.objects.count()
        total_leads = Client.objects.filter(category='lead').count()
        total_opportunities = Opportunity.objects.count()
        total_opportunity_value = Opportunity.objects.aggregate(
            total=Sum('estimated_value')
        )['total'] or 0
        pending_tasks = Task.objects.filter(status__in=['pending', 'in_progress']).count()
        
        # Recent interactions (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_interactions = ClientInteraction.objects.filter(
            interaction_date__gte=thirty_days_ago
        ).count()
        
        # Charts data
        clients_by_status = list(
            Client.objects.values('status').annotate(count=Count('id'))
        )
        
        clients_by_industry = list(
            Client.objects.values('industry').annotate(count=Count('id'))
        )
        
        opportunities_by_stage = list(
            Opportunity.objects.values('stage').annotate(count=Count('id'))
        )
        
        # Monthly interactions for the last 6 months
        monthly_interactions = []
        for i in range(6):
            month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=31)
            count = ClientInteraction.objects.filter(
                interaction_date__gte=month_start,
                interaction_date__lt=month_end
            ).count()
            monthly_interactions.append({
                'month': month_start.strftime('%b %Y'),
                'count': count
            })
        
        # Top opportunities
        top_opportunities = Opportunity.objects.exclude(
            stage__in=['closed_won', 'closed_lost']
        ).order_by('-estimated_value')[:5]
        
        # Upcoming tasks
        upcoming_tasks = Task.objects.filter(
            status__in=['pending', 'in_progress'],
            due_date__gte=timezone.now()
        ).order_by('due_date')[:10]
        
        dashboard_data = {
            'total_clients': total_clients,
            'total_leads': total_leads,
            'total_opportunities': total_opportunities,
            'total_opportunity_value': total_opportunity_value,
            'pending_tasks': pending_tasks,
            'recent_interactions': recent_interactions,
            'clients_by_status': clients_by_status,
            'clients_by_industry': clients_by_industry,
            'opportunities_by_stage': opportunities_by_stage,
            'monthly_interactions': monthly_interactions,
            'top_opportunities': OpportunitySerializer(top_opportunities, many=True).data,
            'upcoming_tasks': TaskSerializer(upcoming_tasks, many=True).data,
        }
        
        return Response(dashboard_data)
    
    @action(detail=True, methods=['post'])
    def add_interaction(self, request, pk=None):
        """Add an interaction to a client"""
        client = self.get_object()
        serializer = ClientInteractionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
            serializer.save(client=client, handled_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_opportunity(self, request, pk=None):
        """Add an opportunity to a client"""
        client = self.get_object()
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
            serializer.save(client=client, owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        """Add a task to a client"""
        client = self.get_object()
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
            serializer.save(client=client, created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactPersonViewSet(viewsets.ModelViewSet):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['client', 'is_primary', 'is_decision_maker']
    search_fields = ['first_name', 'last_name', 'email', 'job_title']


class ClientInteractionViewSet(viewsets.ModelViewSet):
    queryset = ClientInteraction.objects.all()
    serializer_class = ClientInteractionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'interaction_type', 'handled_by']
    search_fields = ['subject', 'description']
    ordering_fields = ['interaction_date']
    ordering = ['-interaction_date']
    
    def perform_create(self, serializer):
        # Use admin user if no user is authenticated
        user = self.request.user if self.request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
        serializer.save(handled_by=user)


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'stage', 'owner']
    search_fields = ['title', 'description']
    ordering_fields = ['estimated_value', 'expected_close_date', 'probability']
    ordering = ['-estimated_value']
    
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
        serializer.save(owner=user)
    
    @action(detail=False, methods=['get'])
    def pipeline(self, request):
        """Get opportunities pipeline data"""
        pipeline_data = []
        stages = ['qualification', 'needs_analysis', 'proposal', 'negotiation']
        
        for stage in stages:
            opportunities = Opportunity.objects.filter(stage=stage)
            total_value = opportunities.aggregate(total=Sum('estimated_value'))['total'] or 0
            weighted_value = sum(opp.weighted_value for opp in opportunities)
            
            pipeline_data.append({
                'stage': stage,
                'stage_display': dict(Opportunity._meta.get_field('stage').choices)[stage],
                'count': opportunities.count(),
                'total_value': total_value,
                'weighted_value': weighted_value,
                'opportunities': OpportunitySerializer(opportunities, many=True).data
            })
        
        return Response(pipeline_data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'status', 'priority', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    ordering = ['due_date']
    
    def perform_create(self, serializer):
        # Use admin user if no user is authenticated
        user = self.request.user if self.request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
        serializer.save(created_by=user)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get tasks assigned to current user"""
        if request.user.is_authenticated:
            tasks = Task.objects.filter(assigned_to=request.user, status__in=['pending', 'in_progress'])
        else:
            tasks = Task.objects.filter(status__in=['pending', 'in_progress'])[:10]
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    search_fields = ['username', 'first_name', 'last_name', 'email']


class ChoicesViewSet(viewsets.ViewSet):
    """API endpoint for getting choice options"""
    permission_classes = [AllowAny]
    
    def list(self, request):
        serializer = ChoicesSerializer({})
        return Response(serializer.data)
