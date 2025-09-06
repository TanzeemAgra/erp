"""
Custom User Model for ERP System

Extends Django's AbstractUser to include additional fields
for employee profile and company association
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    """
    Custom User Model with additional ERP-specific fields
    """
    
    # Personal Information
    middle_name = models.CharField(_('Middle Name'), max_length=150, blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    
    # Professional Information
    employee_id = models.CharField(_('Employee ID'), max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(_('Department'), max_length=100, blank=True)
    designation = models.CharField(_('Designation'), max_length=100, blank=True)
    joining_date = models.DateField(_('Joining Date'), null=True, blank=True)
    
    # Profile Information
    profile_picture = models.ImageField(_('Profile Picture'), upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    
    # Status and Permissions
    is_hr_manager = models.BooleanField(_('HR Manager'), default=False)
    is_project_manager = models.BooleanField(_('Project Manager'), default=False)
    is_finance_manager = models.BooleanField(_('Finance Manager'), default=False)
    
    # Address Information
    address_line1 = models.CharField(_('Address Line 1'), max_length=255, blank=True)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    state = models.CharField(_('State'), max_length=100, blank=True)
    postal_code = models.CharField(_('Postal Code'), max_length=20, blank=True)
    country = models.CharField(_('Country'), max_length=100, blank=True, default='India')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(_('Emergency Contact Name'), max_length=200, blank=True)
    emergency_contact_phone = models.CharField(_('Emergency Contact Phone'), max_length=20, blank=True)
    emergency_contact_relation = models.CharField(_('Emergency Contact Relation'), max_length=50, blank=True)
    
    # Audit
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def get_full_name(self):
        """
        Return the first_name plus the middle_name plus the last_name, with spaces in between.
        """
        full_name = f"{self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        if self.last_name:
            full_name += f" {self.last_name}"
        return full_name.strip()
    
    @property
    def display_name(self):
        """Return full name if available, otherwise username"""
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class Department(models.Model):
    """
    Department model for organizing employees
    """
    name = models.CharField(_('Department Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    head = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='heading_departments',
        verbose_name=_('Department Head')
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    
    # Audit
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Designation(models.Model):
    """
    Designation/Job Title model
    """
    title = models.CharField(_('Designation Title'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='designations',
        verbose_name=_('Department')
    )
    level = models.PositiveIntegerField(_('Level'), default=1, help_text=_('Hierarchy level (1=Junior, 5=Senior)'))
    is_active = models.BooleanField(_('Is Active'), default=True)
    
    # Audit
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ['department', 'level', 'title']
        unique_together = ['title', 'department']
    
    def __str__(self):
        return f"{self.title} - {self.department.name}"
