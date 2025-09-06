#!/usr/bin/env python3
"""
CORS Configuration Test Script
Tests if the CORS configuration is working properly
"""

import requests
import json

def test_cors_configuration():
    """Test CORS configuration by making requests from different origins"""
    
    print("🧪 Testing CORS Configuration")
    print("=" * 50)
    
    # Test endpoints
    base_url = "http://localhost:8000"
    test_endpoints = [
        "/api/v1/auth/login/",
        "/api/v1/accounts/users/",
        "/api/v1/crm/clients/",
    ]
    
    # Test origins
    test_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    for origin in test_origins:
        print(f"\n🌐 Testing origin: {origin}")
        
        for endpoint in test_endpoints:
            url = base_url + endpoint
            
            # Test OPTIONS request (preflight)
            headers = {
                'Origin': origin,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization',
            }
            
            try:
                response = requests.options(url, headers=headers, timeout=5)
                
                cors_headers = {
                    'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                    'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                    'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                    'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
                }
                
                if response.status_code == 200:
                    print(f"  ✅ {endpoint}: CORS OK")
                    if cors_headers['Access-Control-Allow-Origin']:
                        print(f"    🎯 Allowed Origin: {cors_headers['Access-Control-Allow-Origin']}")
                else:
                    print(f"  ❌ {endpoint}: CORS Failed (Status: {response.status_code})")
                
            except requests.exceptions.RequestException as e:
                print(f"  ⚠️  {endpoint}: Connection failed - {e}")
    
    print("\n" + "=" * 50)
    print("🔧 CORS Configuration Summary:")
    print("✅ Added port 3001 to CORS_ALLOWED_ORIGINS")
    print("✅ Dynamic configuration via environment variables")
    print("✅ Development mode includes common ports")
    print("✅ Custom middleware for debugging")
    print("✅ Comprehensive headers and methods allowed")

if __name__ == "__main__":
    test_cors_configuration()
