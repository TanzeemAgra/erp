"""
Chatbot API Views
Handles REST API endpoints for the Smart Chatbot functionality
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
import json
import logging

from .services import get_chatbot_service

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message(request):
    """
    Process chatbot messages
    
    Expected payload:
    {
        "message": "User's question",
        "context": "employee" | "customer",
        "user_type": "employee" | "customer"
    }
    """
    try:
        data = request.data
        message = data.get('message', '').strip()
        context = data.get('context', 'employee')
        user_type = data.get('user_type', 'employee')
        
        if not message:
            return Response({
                "error": "Message is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get chatbot service
        chatbot = get_chatbot_service()
        
        # Process based on user type
        if user_type == 'employee':
            result = chatbot.process_employee_query(
                question=message,
                user_id=request.user.id
            )
        elif user_type == 'customer':
            # For customers, we'd need to identify them differently
            # For now, using user_id but in production this would be customer_id
            result = chatbot.process_customer_query(
                question=message,
                customer_id=getattr(request.user, 'customer_id', None)
            )
        else:
            return Response({
                "error": "Invalid user_type. Must be 'employee' or 'customer'"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log the interaction
        logger.info(f"Chatbot interaction - User: {request.user.id}, Type: {user_type}, Message: {message[:100]}")
        
        return Response({
            "response": result.get('response'),
            "type": result.get('type'),
            "escalate": result.get('escalate', False),
            "suggestions": result.get('suggestions', []),
            "timestamp": "2025-09-04T11:33:00Z"  # Current timestamp
        })
        
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        return Response({
            "error": "An error occurred processing your message",
            "response": "I'm sorry, I'm experiencing technical difficulties. Please try again later or contact support.",
            "escalate": True
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auto_fill_form(request):
    """
    Auto-fill form data for employees
    
    Expected payload:
    {
        "form_type": "leave_request" | "expense_report" | "equipment_request"
    }
    """
    try:
        data = request.data
        form_type = data.get('form_type')
        
        if not form_type:
            return Response({
                "error": "form_type is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        chatbot = get_chatbot_service()
        result = chatbot.auto_fill_form_data(form_type, request.user.id)
        
        if 'error' in result:
            return Response({
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"Auto-fill form error: {str(e)}")
        return Response({
            "error": "Could not auto-fill form data"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """
    Get personalized recommendations for customers
    """
    try:
        chatbot = get_chatbot_service()
        
        # For customers, get personalized recommendations
        # For employees, this could return training recommendations, etc.
        if hasattr(request.user, 'customer_id'):
            recommendations = chatbot.get_personalized_recommendations(request.user.customer_id)
        else:
            # Default recommendations for employees
            recommendations = [
                {
                    "type": "training",
                    "title": "Upcoming Security Training",
                    "description": "Mandatory cybersecurity training session",
                    "confidence": 1.0
                },
                {
                    "type": "policy",
                    "title": "Updated Leave Policy",
                    "description": "Review the recently updated leave policy",
                    "confidence": 0.8
                }
            ]
        
        return Response({
            "recommendations": recommendations
        })
        
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        return Response({
            "error": "Could not fetch recommendations"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def chatbot_status(request):
    """
    Check chatbot service status (public endpoint for health checks)
    """
    try:
        # Basic health check
        chatbot = get_chatbot_service()
        
        status_info = {
            "status": "healthy",
            "version": "1.0.0",
            "features": {
                "employee_assistance": True,
                "customer_support": True,
                "auto_fill": True,
                "recommendations": True,
                "rag_enabled": True
            },
            "timestamp": "2025-09-04T11:33:00Z"
        }
        
        return Response(status_info)
        
    except Exception as e:
        return Response({
            "status": "unhealthy",
            "error": str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def escalate_to_human(request):
    """
    Escalate conversation to human agent
    
    Expected payload:
    {
        "conversation_id": "unique_id",
        "reason": "escalation_reason",
        "priority": "low" | "medium" | "high"
    }
    """
    try:
        data = request.data
        conversation_id = data.get('conversation_id')
        reason = data.get('reason', 'User requested escalation')
        priority = data.get('priority', 'medium')
        
        # In a real implementation, this would:
        # 1. Create a support ticket
        # 2. Notify available agents
        # 3. Transfer conversation context
        
        # For now, return a mock response
        return Response({
            "escalated": True,
            "ticket_id": f"TICKET-{conversation_id}-001",
            "estimated_wait_time": "5-10 minutes",
            "message": "Your conversation has been escalated to a human agent. You will be contacted shortly."
        })
        
    except Exception as e:
        logger.error(f"Escalation error: {str(e)}")
        return Response({
            "error": "Could not escalate to human agent"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
