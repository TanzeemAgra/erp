from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Client, ContactPerson, ClientInteraction, Opportunity, Task

@admin.register(Client)
class ClientAdmin(SimpleHistoryAdmin):
    list_display = ['company_name', 'contact_person', 'email', 'category', 'status', 'industry', 'created_at']
    list_filter = ['category', 'status', 'industry', 'created_at']
    search_fields = ['company_name', 'contact_person', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'contact_person', 'email', 'phone', 'website')
        }),
        ('Business Details', {
            'fields': ('industry', 'company_size', 'annual_revenue')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('CRM Information', {
            'fields': ('category', 'status', 'source', 'account_manager', 'assigned_to')
        }),
        ('Financial', {
            'fields': ('credit_limit', 'payment_terms')
        }),
        ('Dates & Follow-up', {
            'fields': ('last_contact_date', 'next_follow_up')
        }),
        ('Additional Information', {
            'fields': ('notes', 'tags')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'client', 'job_title', 'email', 'is_primary', 'is_decision_maker']
    list_filter = ['is_primary', 'is_decision_maker', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'client__company_name']

@admin.register(ClientInteraction)
class ClientInteractionAdmin(admin.ModelAdmin):
    list_display = ['client', 'interaction_type', 'subject', 'interaction_date', 'handled_by']
    list_filter = ['interaction_type', 'interaction_date', 'handled_by']
    search_fields = ['client__company_name', 'subject', 'description']
    date_hierarchy = 'interaction_date'

@admin.register(Opportunity)
class OpportunityAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'client', 'estimated_value', 'probability', 'stage', 'expected_close_date', 'owner']
    list_filter = ['stage', 'probability', 'expected_close_date', 'owner']
    search_fields = ['title', 'client__company_name', 'description']
    date_hierarchy = 'expected_close_date'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'priority', 'status', 'assigned_to', 'due_date']
    list_filter = ['priority', 'status', 'assigned_to', 'due_date']
    search_fields = ['title', 'client__company_name', 'description']
    date_hierarchy = 'due_date'
