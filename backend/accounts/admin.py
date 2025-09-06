"""
Accounts App Admin Configuration

Admin interface for User, Department, and Designation models
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from .models import User, Department, Designation


@admin.register(User)
class UserAdmin(BaseUserAdmin, SimpleHistoryAdmin):
    """Custom User Admin with additional fields"""
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'middle_name', 'last_name', 'email',
                'phone_number', 'date_of_birth', 'profile_picture', 'bio'
            )
        }),
        (_('Professional info'), {
            'fields': (
                'employee_id', 'department', 'designation', 'joining_date',
                'is_hr_manager', 'is_project_manager', 'is_finance_manager'
            )
        }),
        (_('Address'), {
            'fields': (
                'address_line1', 'address_line2', 'city', 'state',
                'postal_code', 'country'
            ),
            'classes': ('collapse',)
        }),
        (_('Emergency Contact'), {
            'fields': (
                'emergency_contact_name', 'emergency_contact_phone',
                'emergency_contact_relation'
            ),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'employee_id'
            ),
        }),
    )
    
    list_display = (
        'username', 'email', 'get_full_name', 'employee_id',
        'department', 'designation', 'is_active', 'is_staff', 'date_joined'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'department',
        'designation', 'is_hr_manager', 'is_project_manager', 'is_finance_manager',
        'date_joined'
    )
    
    search_fields = (
        'username', 'first_name', 'last_name', 'email',
        'employee_id', 'phone_number'
    )
    
    ordering = ('-date_joined',)
    
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')


@admin.register(Department)
class DepartmentAdmin(SimpleHistoryAdmin):
    """Department Admin"""
    
    list_display = ('name', 'head', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'head', 'is_active')
        }),
        (_('Audit'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Designation)
class DesignationAdmin(SimpleHistoryAdmin):
    """Designation Admin"""
    
    list_display = ('title', 'department', 'level', 'is_active', 'created_at')
    list_filter = ('department', 'level', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('department', 'level', 'title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'department', 'level', 'is_active')
        }),
        (_('Audit'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
