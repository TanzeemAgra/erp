"""
Django Management Script for ERP System Setup

This script automates the initial setup of the ERP system including:
- Running migrations
- Creating superuser
- Loading initial data
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_core.settings')
    django.setup()

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Migrations completed successfully!")

def create_superuser():
    """Create superuser if it doesn't exist"""
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("👤 Creating superuser...")
        print("Please enter superuser details:")
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully!")
    else:
        print("ℹ️ Superuser already exists")

def load_initial_data():
    """Load initial data for departments and designations"""
    from accounts.models import Department, Designation
    
    # Create default departments
    departments_data = [
        {'name': 'Information Technology', 'description': 'IT Department'},
        {'name': 'Human Resources', 'description': 'HR Department'},
        {'name': 'Finance', 'description': 'Finance Department'},
        {'name': 'Operations', 'description': 'Operations Department'},
        {'name': 'Sales & Marketing', 'description': 'Sales and Marketing Department'},
    ]
    
    print("📊 Loading initial departments...")
    for dept_data in departments_data:
        department, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        if created:
            print(f"✅ Created department: {department.name}")
    
    # Create default designations
    it_dept = Department.objects.get(name='Information Technology')
    hr_dept = Department.objects.get(name='Human Resources')
    finance_dept = Department.objects.get(name='Finance')
    
    designations_data = [
        {'title': 'Software Developer', 'department': it_dept, 'level': 2},
        {'title': 'Senior Software Developer', 'department': it_dept, 'level': 3},
        {'title': 'Tech Lead', 'department': it_dept, 'level': 4},
        {'title': 'Project Manager', 'department': it_dept, 'level': 4},
        {'title': 'DevOps Engineer', 'department': it_dept, 'level': 3},
        {'title': 'HR Manager', 'department': hr_dept, 'level': 4},
        {'title': 'HR Executive', 'department': hr_dept, 'level': 2},
        {'title': 'Finance Manager', 'department': finance_dept, 'level': 4},
        {'title': 'Accountant', 'department': finance_dept, 'level': 2},
    ]
    
    print("👔 Loading initial designations...")
    for desig_data in designations_data:
        designation, created = Designation.objects.get_or_create(
            title=desig_data['title'],
            department=desig_data['department'],
            defaults={'level': desig_data['level']}
        )
        if created:
            print(f"✅ Created designation: {designation.title}")

def main():
    """Main setup function"""
    print("🚀 Starting ERP System Setup...")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Run migrations
    run_migrations()
    
    # Load initial data
    load_initial_data()
    
    # Create superuser
    create_superuser()
    
    print("=" * 50)
    print("✨ ERP System setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your database credentials")
    print("2. Start the development server: python manage.py runserver")
    print("3. Access admin panel: http://localhost:8000/admin/")
    print("4. Access API docs: http://localhost:8000/api/docs/")

if __name__ == '__main__':
    main()
