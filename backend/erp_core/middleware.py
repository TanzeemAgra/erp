"""
Custom middleware for ERP system
Includes CORS debugging and additional security headers
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class CORSDebugMiddleware:
    """
    Middleware to debug CORS issues and provide additional CORS headers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log CORS requests for debugging
        if settings.DEBUG:
            origin = request.META.get('HTTP_ORIGIN')
            if origin:
                logger.info(f"CORS Request from origin: {origin}")
                if origin not in settings.CORS_ALLOWED_ORIGINS:
                    logger.warning(f"Origin {origin} not in CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")

        response = self.get_response(request)
        
        # Add additional CORS headers for debugging in development
        if settings.DEBUG:
            origin = request.META.get('HTTP_ORIGIN')
            if origin and origin in settings.CORS_ALLOWED_ORIGINS:
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization, X-Requested-With, X-CSRFToken'
                response['Access-Control-Max-Age'] = '86400'
        
        return response


class SecurityHeadersMiddleware:
    """
    Add security headers to responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        if not settings.DEBUG:
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
