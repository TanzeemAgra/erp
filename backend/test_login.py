#!/usr/bin/env python
import os
import django
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_core.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

def test_authentication():
    print("Testing authentication...")
    
    # Check if user exists
    try:
        user = User.objects.get(username='admin')
        print(f"User found: {user.username}")
        print(f"Is active: {user.is_active}")
        print(f"Password hash: {user.password[:20]}...")
    except User.DoesNotExist:
        print("Admin user does not exist")
        return
    
    # Test authentication
    auth_user = authenticate(username='admin', password='admin')
    if auth_user:
        print("Authentication successful!")
        print(f"Authenticated user: {auth_user.username}")
    else:
        print("Authentication failed!")
        
        # Try manual password check
        if user.check_password('admin'):
            print("Manual password check passed - issue might be with authentication backend")
        else:
            print("Manual password check failed - password is wrong")

if __name__ == '__main__':
    test_authentication()
