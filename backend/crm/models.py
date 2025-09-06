from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords

User = get_user_model()

class ClientCategory(models.TextChoices):
    LEAD = 'lead', 'Lead'
    PROSPECT = 'prospect', 'Prospect'
    CUSTOMER = 'customer', 'Customer'
    PARTNER = 'partner', 'Partner'

class ClientStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    POTENTIAL = 'potential', 'Potential'
    LOST = 'lost', 'Lost'

class IndustryType(models.TextChoices):
    TECHNOLOGY = 'technology', 'Technology'
    HEALTHCARE = 'healthcare', 'Healthcare'
    FINANCE = 'finance', 'Finance'
    EDUCATION = 'education', 'Education'
    RETAIL = 'retail', 'Retail'
    MANUFACTURING = 'manufacturing', 'Manufacturing'
    CONSULTING = 'consulting', 'Consulting'
    OTHER = 'other', 'Other'

class Client(models.Model):
    # Basic Information
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    
    # Business Details
    industry = models.CharField(max_length=20, choices=IndustryType.choices, default=IndustryType.OTHER)
    company_size = models.PositiveIntegerField(help_text="Number of employees", blank=True, null=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    
    # CRM Status
    category = models.CharField(max_length=20, choices=ClientCategory.choices, default=ClientCategory.LEAD)
    status = models.CharField(max_length=20, choices=ClientStatus.choices, default=ClientStatus.POTENTIAL)
    source = models.CharField(max_length=100, help_text="How did they find us?", blank=True, null=True)
    
    # Relationship Management
    account_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_clients')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_clients')
    
    # Financial Information
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    payment_terms = models.CharField(max_length=50, blank=True, null=True)
    
    # Important Dates
    first_contact_date = models.DateField(auto_now_add=True)
    last_contact_date = models.DateTimeField(blank=True, null=True)
    next_follow_up = models.DateTimeField(blank=True, null=True)
    
    # Notes and Additional Info
    notes = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=500, help_text="Comma-separated tags", blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_clients')
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"
    
    @property
    def full_address(self):
        address_parts = [self.address_line1]
        if self.address_line2:
            address_parts.append(self.address_line2)
        address_parts.extend([self.city, self.state, self.postal_code, self.country])
        return ", ".join(address_parts)


class ContactPerson(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    is_decision_maker = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.client.company_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class InteractionType(models.TextChoices):
    CALL = 'call', 'Phone Call'
    EMAIL = 'email', 'Email'
    MEETING = 'meeting', 'Meeting'
    DEMO = 'demo', 'Demo'
    PROPOSAL = 'proposal', 'Proposal'
    FOLLOWUP = 'followup', 'Follow-up'
    SUPPORT = 'support', 'Support'
    OTHER = 'other', 'Other'


class ClientInteraction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interactions')
    contact_person = models.ForeignKey(ContactPerson, on_delete=models.SET_NULL, null=True, blank=True)
    interaction_type = models.CharField(max_length=20, choices=InteractionType.choices)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    interaction_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_date = models.DateTimeField(blank=True, null=True)
    
    # Who handled this interaction
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-interaction_date']
    
    def __str__(self):
        return f"{self.interaction_type.title()} with {self.client.company_name} - {self.subject}"


class OpportunityStage(models.TextChoices):
    QUALIFICATION = 'qualification', 'Qualification'
    NEEDS_ANALYSIS = 'needs_analysis', 'Needs Analysis'
    PROPOSAL = 'proposal', 'Proposal'
    NEGOTIATION = 'negotiation', 'Negotiation'
    CLOSED_WON = 'closed_won', 'Closed Won'
    CLOSED_LOST = 'closed_lost', 'Closed Lost'


class Opportunity(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2)
    probability = models.PositiveIntegerField(default=50, help_text="Probability of closing (0-100%)")
    stage = models.CharField(max_length=20, choices=OpportunityStage.choices, default=OpportunityStage.QUALIFICATION)
    
    # Important Dates
    expected_close_date = models.DateField()
    actual_close_date = models.DateField(blank=True, null=True)
    
    # Assignment
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='opportunities')
    
    # Competition and Notes
    competitors = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-expected_close_date']
        verbose_name_plural = "Opportunities"
    
    def __str__(self):
        return f"{self.title} - {self.client.company_name}"
    
    @property
    def weighted_value(self):
        return (self.estimated_value * self.probability) / 100


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='crm_tasks')
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_crm_tasks')
    
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.title} - {self.client.company_name}"
