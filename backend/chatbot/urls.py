"""
Chatbot URL Configuration
"""

from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Main chat endpoint
    path('chat/', views.chat_message, name='chat_message'),
    
    # Form auto-fill
    path('autofill/', views.auto_fill_form, name='auto_fill_form'),
    
    # Personalized recommendations
    path('recommendations/', views.get_recommendations, name='recommendations'),
    
    # Escalation to human
    path('escalate/', views.escalate_to_human, name='escalate_to_human'),
    
    # Health check
    path('status/', views.chatbot_status, name='status'),
]
