"""
ERP Core URL Configuration

Enterprise Resource Planning System for IT Companies
Main URL router for all API endpoints and admin interface
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Admin customization
admin.site.site_header = "ERP System Administration"
admin.site.site_title = "ERP Admin"
admin.site.index_title = "Welcome to ERP System Administration"

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 endpoints
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/hr/', include('hr.urls')),
    path('api/v1/crm/', include('crm.urls')),
    path('api/v1/projects/', include('projects.urls')),
    path('api/v1/finance/', include('finance.urls')),
    path('api/v1/assets/', include('assets.urls')),
    path('api/v1/chatbot/', include('chatbot.urls')),
    path('', include('ai_supply_chain.urls')),  # AI Supply Chain Optimization
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
