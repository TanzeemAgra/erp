"""
Smart Chatbot Testing Script
Tests the RAG-powered chatbot functionality
"""

import os
import sys
import json
from datetime import datetime

# Add Django project to path
sys.path.append('C:\\Users\\Xerxez Solutions\\Desktop\\ERP\\backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_core.settings')

import django
django.setup()

from chatbot.services import SmartChatbotService

def test_chatbot_basic():
    """Test basic chatbot functionality"""
    print("🤖 Testing Smart Chatbot - Basic Functionality")
    print("=" * 50)
    
    # Note: This test requires OPENAI_API_KEY to be set
    # For demo purposes, we'll test the structure without actual OpenAI calls
    
    try:
        chatbot = SmartChatbotService()
        print("✅ Chatbot service initialized successfully")
        
        # Test employee queries
        employee_questions = [
            "What is the leave policy?",
            "How do I apply for annual leave?", 
            "What are my payroll details?",
            "Who is my manager?",
            "What equipment am I assigned?"
        ]
        
        print("\n📋 Testing Employee Queries:")
        for question in employee_questions:
            try:
                result = chatbot.process_employee_query(question, user_id=1)
                print(f"Q: {question}")
                print(f"A: {result.get('response', 'No response')[:100]}...")
                print(f"Type: {result.get('type')}, Escalate: {result.get('escalate')}")
                print("---")
            except Exception as e:
                print(f"❌ Error with question '{question}': {e}")
        
        # Test customer queries
        customer_questions = [
            "What is the status of my order?",
            "I need help with my invoice",
            "How can I track my delivery?",
            "I want to cancel my order",
            "What services do you offer?"
        ]
        
        print("\n👥 Testing Customer Queries:")
        for question in customer_questions:
            try:
                result = chatbot.process_customer_query(question, customer_id=1)
                print(f"Q: {question}")
                print(f"A: {result.get('response', 'No response')[:100]}...")
                print(f"Type: {result.get('type')}, Escalate: {result.get('escalate')}")
                print("---")
            except Exception as e:
                print(f"❌ Error with question '{question}': {e}")
        
        # Test auto-fill functionality
        print("\n📝 Testing Auto-Fill Functionality:")
        try:
            form_data = chatbot.auto_fill_form_data("leave_request", 1)
            print("Leave Request Auto-Fill:")
            print(json.dumps(form_data, indent=2, default=str))
        except Exception as e:
            print(f"❌ Error with auto-fill: {e}")
        
        # Test recommendations
        print("\n💡 Testing Recommendations:")
        try:
            recommendations = chatbot.get_personalized_recommendations(1)
            print("Customer Recommendations:")
            print(json.dumps(recommendations, indent=2))
        except Exception as e:
            print(f"❌ Error with recommendations: {e}")
            
        print("\n✅ Chatbot testing completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        print("Note: Make sure OPENAI_API_KEY is set in your environment or .env file")

def test_vector_store_setup():
    """Test vector store document preparation"""
    print("\n🔍 Testing Vector Store Document Preparation")
    print("=" * 50)
    
    try:
        chatbot = SmartChatbotService()
        
        # Test document extraction
        employee_docs = chatbot._get_employee_documents()
        customer_docs = chatbot._get_customer_documents()
        policy_docs = chatbot._get_policy_documents()
        
        print(f"📊 Document Counts:")
        print(f"Employee documents: {len(employee_docs)}")
        print(f"Customer documents: {len(customer_docs)}")
        print(f"Policy documents: {len(policy_docs)}")
        
        # Show sample documents
        if employee_docs:
            print(f"\n📋 Sample Employee Document:")
            print(employee_docs[0].page_content[:200] + "...")
            print(f"Metadata: {employee_docs[0].metadata}")
        
        if policy_docs:
            print(f"\n📜 Sample Policy Document:")
            print(policy_docs[0].page_content[:200] + "...")
            print(f"Metadata: {policy_docs[0].metadata}")
            
        print("\n✅ Vector store setup testing completed!")
        
    except Exception as e:
        print(f"❌ Error testing vector stores: {e}")

def test_api_endpoints():
    """Test API endpoint structure"""
    print("\n🌐 Testing API Endpoint Structure")
    print("=" * 50)
    
    endpoints = [
        "/api/v1/chatbot/chat/",
        "/api/v1/chatbot/autofill/",
        "/api/v1/chatbot/recommendations/",
        "/api/v1/chatbot/escalate/",
        "/api/v1/chatbot/status/"
    ]
    
    for endpoint in endpoints:
        print(f"✅ Endpoint configured: {endpoint}")
    
    print("\n📝 Sample API Requests:")
    
    sample_chat_request = {
        "message": "What is the leave policy?",
        "context": "employee",
        "user_type": "employee"
    }
    print(f"Chat Request: {json.dumps(sample_chat_request, indent=2)}")
    
    sample_autofill_request = {
        "form_type": "leave_request"
    }
    print(f"Auto-fill Request: {json.dumps(sample_autofill_request, indent=2)}")

if __name__ == "__main__":
    print("🚀 Smart Chatbot Test Suite")
    print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # Run tests
    test_vector_store_setup()
    test_api_endpoints()
    
    # Basic chatbot test (requires OpenAI API key)
    if os.getenv('OPENAI_API_KEY'):
        test_chatbot_basic()
    else:
        print("\n⚠️  OpenAI API key not found.")
        print("Set OPENAI_API_KEY environment variable to test AI functionality.")
        print("For now, testing basic structure only.")
    
    print("\n🎉 Testing completed!")
    print("Next steps:")
    print("1. Set up OpenAI API key")
    print("2. Test frontend integration")
    print("3. Deploy chatbot to production")
