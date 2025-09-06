"""
AI Supply Chain URL Configuration
URL patterns for AI Supply Chain API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()

# Register all viewsets
router.register(r'config', views.SupplyChainConfigViewSet, basename='supplychain-config')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'suppliers', views.SupplierViewSet, basename='suppliers')
router.register(r'demand-forecasts', views.DemandForecastViewSet, basename='demand-forecasts')
router.register(r'dynamic-pricing', views.DynamicPricingViewSet, basename='dynamic-pricing')
router.register(r'delivery-locations', views.DeliveryLocationViewSet, basename='delivery-locations')
router.register(r'route-optimization', views.RouteOptimizationViewSet, basename='route-optimization')
router.register(r'risk-factors', views.RiskFactorViewSet, basename='risk-factors')
router.register(r'risk-alerts', views.RiskAlertViewSet, basename='risk-alerts')
router.register(r'ai-models', views.AIModelPerformanceViewSet, basename='ai-models')

app_name = 'ai_supply_chain'

urlpatterns = [
    # Include all router URLs
    path('api/v1/ai-supply-chain/', include(router.urls)),
    
    # Additional custom endpoints can be added here if needed
    # Example:
    # path('api/v1/ai-supply-chain/custom-endpoint/', views.custom_view, name='custom-endpoint'),
]

# URL patterns summary for documentation:
"""
Available API Endpoints:

Supply Chain Configuration:
- GET/PUT/PATCH /api/v1/ai-supply-chain/config/ - Configuration management
- GET /api/v1/ai-supply-chain/config/active_config/ - Get active configuration

Products:
- GET/POST/PUT/PATCH/DELETE /api/v1/ai-supply-chain/products/ - Product CRUD
- POST /api/v1/ai-supply-chain/products/{id}/generate_demand_forecast/ - Generate forecast
- POST /api/v1/ai-supply-chain/products/{id}/calculate_dynamic_pricing/ - Calculate pricing
- GET /api/v1/ai-supply-chain/products/analytics/ - Product analytics

Suppliers:
- GET/POST/PUT/PATCH/DELETE /api/v1/ai-supply-chain/suppliers/ - Supplier CRUD
- GET /api/v1/ai-supply-chain/suppliers/performance_analytics/ - Performance analytics

Demand Forecasts:
- GET /api/v1/ai-supply-chain/demand-forecasts/ - View forecasts (read-only)
- GET /api/v1/ai-supply-chain/demand-forecasts/accuracy_report/ - Accuracy report

Dynamic Pricing:
- GET /api/v1/ai-supply-chain/dynamic-pricing/ - View pricing (read-only)
- POST /api/v1/ai-supply-chain/dynamic-pricing/{id}/apply_pricing/ - Apply pricing
- GET /api/v1/ai-supply-chain/dynamic-pricing/revenue_impact_report/ - Revenue impact

Delivery Locations:
- GET/POST/PUT/PATCH/DELETE /api/v1/ai-supply-chain/delivery-locations/ - Location CRUD

Route Optimization:
- GET/POST/PUT/PATCH/DELETE /api/v1/ai-supply-chain/route-optimization/ - Route CRUD
- POST /api/v1/ai-supply-chain/route-optimization/optimize_route/ - Optimize new route
- POST /api/v1/ai-supply-chain/route-optimization/{id}/implement_route/ - Implement route
- GET /api/v1/ai-supply-chain/route-optimization/savings_report/ - Savings report

Risk Factors:
- GET/POST/PUT/PATCH/DELETE /api/v1/ai-supply-chain/risk-factors/ - Risk factor CRUD

Risk Alerts:
- GET/POST/PUT/PATCH/DELETE /api/v1/ai-supply-chain/risk-alerts/ - Risk alert CRUD
- POST /api/v1/ai-supply-chain/risk-alerts/run_risk_assessment/ - Run risk assessment
- POST /api/v1/ai-supply-chain/risk-alerts/{id}/resolve_alert/ - Resolve alert

AI Model Performance:
- GET /api/v1/ai-supply-chain/ai-models/ - View model performance (read-only)
- GET /api/v1/ai-supply-chain/ai-models/dashboard_summary/ - AI dashboard summary

All endpoints support:
- Filtering: ?field=value
- Search: ?search=query
- Ordering: ?ordering=field_name
- Pagination: ?page=1&page_size=20
"""
