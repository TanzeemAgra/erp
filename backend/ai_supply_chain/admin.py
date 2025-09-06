"""
AI Supply Chain Admin Interface
Django admin configuration for AI Supply Chain models
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    SupplyChainConfig, Product, Supplier, DemandForecast,
    DynamicPricing, DeliveryLocation, RouteOptimization, RouteStop,
    RiskFactor, RiskAlert, AIModelPerformance
)
from .services import (
    DemandForecastingService, DynamicPricingService,
    RouteOptimizationService, RiskManagementService
)


@admin.register(SupplyChainConfig)
class SupplyChainConfigAdmin(SimpleHistoryAdmin):
    """Admin interface for Supply Chain Configuration"""
    
    list_display = [
        'id', 'demand_forecasting_enabled', 'dynamic_pricing_enabled',
        'route_optimization_enabled', 'risk_management_enabled',
        'updated_at', 'updated_by'
    ]
    
    fieldsets = (
        ('AI Features', {
            'fields': (
                'demand_forecasting_enabled', 'dynamic_pricing_enabled',
                'route_optimization_enabled', 'risk_management_enabled'
            )
        }),
        ('Forecasting Parameters', {
            'fields': (
                'forecasting_horizon_days', 'seasonal_adjustment_factor',
                'demand_sensitivity'
            ),
            'classes': ('collapse',)
        }),
        ('Pricing Parameters', {
            'fields': (
                'min_profit_margin', 'max_price_adjustment',
                'competitor_weight', 'market_weight', 'inventory_weight'
            ),
            'classes': ('collapse',)
        }),
        ('Route Optimization Parameters', {
            'fields': (
                'fuel_cost_per_km', 'driver_cost_per_hour',
                'vehicle_capacity_kg', 'max_delivery_distance_km'
            ),
            'classes': ('collapse',)
        }),
        ('Risk Management Parameters', {
            'fields': (
                'risk_threshold_high', 'risk_threshold_medium',
                'alert_notification_enabled'
            ),
            'classes': ('collapse',)
        }),
        ('System Configuration', {
            'fields': (
                'ai_model_update_frequency_hours', 'data_retention_days'
            ),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    """Admin interface for Products"""
    
    list_display = [
        'name', 'sku', 'category', 'current_price', 'current_stock',
        'demand_forecasting_status', 'dynamic_pricing_status', 'updated_at'
    ]
    
    list_filter = [
        'category', 'enable_demand_forecasting', 'enable_dynamic_pricing'
    ]
    
    search_fields = ['name', 'sku', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'category', 'description')
        }),
        ('Pricing Information', {
            'fields': (
                'base_cost', 'current_price', 'min_price', 'max_price'
            )
        }),
        ('Inventory Information', {
            'fields': (
                'current_stock', 'reorder_level', 'max_stock_level'
            )
        }),
        ('Physical Properties', {
            'fields': ('weight_kg', 'dimensions_cm'),
            'classes': ('collapse',)
        }),
        ('AI Optimization', {
            'fields': (
                'enable_demand_forecasting', 'enable_dynamic_pricing',
                'seasonal_factor', 'demand_volatility'
            )
        })
    )
    
    actions = ['generate_demand_forecast', 'calculate_dynamic_pricing']
    
    def demand_forecasting_status(self, obj):
        if obj.enable_demand_forecasting:
            return format_html('<span style="color: green;">Enabled</span>')
        return format_html('<span style="color: red;">Disabled</span>')
    demand_forecasting_status.short_description = 'Demand Forecasting'
    
    def dynamic_pricing_status(self, obj):
        if obj.enable_dynamic_pricing:
            return format_html('<span style="color: green;">Enabled</span>')
        return format_html('<span style="color: red;">Disabled</span>')
    dynamic_pricing_status.short_description = 'Dynamic Pricing'
    
    def generate_demand_forecast(self, request, queryset):
        """Generate demand forecasts for selected products"""
        forecast_service = DemandForecastingService()
        count = 0
        
        for product in queryset:
            if product.enable_demand_forecasting:
                # Generate forecast (simplified - in production, use real data)
                forecast_result = forecast_service.predict_demand(product, timezone.now() + timedelta(days=7))
                
                # Create forecast record
                DemandForecast.objects.create(
                    product=product,
                    forecast_date=timezone.now().date() + timedelta(days=7),
                    forecast_type='weekly',
                    predicted_demand=forecast_result['predicted_demand'],
                    confidence_interval_lower=forecast_result['confidence_interval_lower'],
                    confidence_interval_upper=forecast_result['confidence_interval_upper'],
                    confidence_score=forecast_result['confidence_score'],
                    seasonal_factor=forecast_result['seasonal_factor'],
                    model_version='1.0',
                    algorithm_used='ensemble',
                    training_data_points=100
                )
                count += 1
        
        messages.success(request, f'Generated demand forecasts for {count} products.')
    generate_demand_forecast.short_description = 'Generate demand forecasts'
    
    def calculate_dynamic_pricing(self, request, queryset):
        """Calculate dynamic pricing for selected products"""
        pricing_service = DynamicPricingService()
        count = 0
        
        for product in queryset:
            if product.enable_dynamic_pricing:
                # Calculate optimal price
                pricing_result = pricing_service.calculate_optimal_price(product)
                
                # Create pricing recommendation
                DynamicPricing.objects.create(
                    product=product,
                    current_price=product.current_price,
                    current_stock_level=product.current_stock,
                    current_demand_rate=10.0,  # Simplified
                    recommended_price=pricing_result['recommended_price'],
                    price_change_percentage=pricing_result['price_change_percentage'],
                    pricing_strategy=pricing_result['pricing_strategy'],
                    inventory_factor=pricing_result['factors']['inventory_factor'],
                    demand_factor=pricing_result['factors']['demand_factor'],
                    competition_factor=pricing_result['factors']['competition_factor'],
                    seasonality_factor=pricing_result['factors']['seasonality_factor'],
                    expected_demand_change=pricing_result['expected_demand_change'],
                    expected_revenue_impact=pricing_result['expected_revenue_impact'],
                    expected_profit_margin=15.0,  # Simplified
                    valid_until=timezone.now() + timedelta(days=7)
                )
                count += 1
        
        messages.success(request, f'Generated pricing recommendations for {count} products.')
    calculate_dynamic_pricing.short_description = 'Calculate dynamic pricing'


@admin.register(Supplier)
class SupplierAdmin(SimpleHistoryAdmin):
    """Admin interface for Suppliers"""
    
    list_display = [
        'name', 'code', 'reliability_score', 'on_time_delivery_rate',
        'quality_score', 'financial_stability', 'is_active'
    ]
    
    list_filter = ['reliability_score', 'is_active', 'country']
    search_fields = ['name', 'code', 'contact_person', 'email']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'contact_person', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Performance Analytics', {
            'fields': (
                'reliability_score', 'avg_delivery_time_days',
                'on_time_delivery_rate', 'quality_score'
            )
        }),
        ('Risk Assessment', {
            'fields': ('financial_stability', 'geographic_risk')
        }),
        ('Business Terms', {
            'fields': ('payment_terms_days', 'minimum_order_value')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )


@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    """Admin interface for Demand Forecasts"""
    
    list_display = [
        'product', 'forecast_date', 'forecast_type', 'predicted_demand',
        'confidence_score', 'accuracy_score', 'created_at'
    ]
    
    list_filter = ['forecast_type', 'forecast_date', 'created_at']
    search_fields = ['product__name', 'product__sku']
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Forecast Details', {
            'fields': ('product', 'forecast_date', 'forecast_type')
        }),
        ('Predictions', {
            'fields': (
                'predicted_demand', 'confidence_interval_lower',
                'confidence_interval_upper', 'confidence_score'
            )
        }),
        ('Contributing Factors', {
            'fields': ('seasonal_factor', 'trend_factor', 'market_factor')
        }),
        ('Model Information', {
            'fields': (
                'model_version', 'algorithm_used', 'training_data_points'
            ),
            'classes': ('collapse',)
        }),
        ('Validation', {
            'fields': ('actual_demand', 'accuracy_score'),
            'classes': ('collapse',)
        })
    )


@admin.register(DynamicPricing)
class DynamicPricingAdmin(admin.ModelAdmin):
    """Admin interface for Dynamic Pricing"""
    
    list_display = [
        'product', 'current_price', 'recommended_price', 'price_change_percentage',
        'pricing_strategy', 'is_applied', 'created_at'
    ]
    
    list_filter = ['pricing_strategy', 'is_applied', 'created_at']
    search_fields = ['product__name', 'product__sku']
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Current State', {
            'fields': (
                'product', 'current_price', 'current_stock_level',
                'current_demand_rate'
            )
        }),
        ('AI Recommendations', {
            'fields': (
                'recommended_price', 'price_change_percentage',
                'pricing_strategy'
            )
        }),
        ('Market Analysis', {
            'fields': ('competitor_avg_price', 'market_price_trend')
        }),
        ('Influencing Factors', {
            'fields': (
                'inventory_factor', 'demand_factor',
                'competition_factor', 'seasonality_factor'
            )
        }),
        ('Expected Impact', {
            'fields': (
                'expected_demand_change', 'expected_revenue_impact',
                'expected_profit_margin'
            )
        }),
        ('Implementation', {
            'fields': ('is_applied', 'applied_at', 'valid_until')
        })
    )
    
    actions = ['apply_pricing_recommendations']
    
    def apply_pricing_recommendations(self, request, queryset):
        """Apply selected pricing recommendations"""
        count = 0
        for pricing in queryset.filter(is_applied=False):
            # Update product price
            pricing.product.current_price = pricing.recommended_price
            pricing.product.save()
            
            # Mark as applied
            pricing.is_applied = True
            pricing.applied_at = timezone.now()
            pricing.save()
            
            count += 1
        
        messages.success(request, f'Applied {count} pricing recommendations.')
    apply_pricing_recommendations.short_description = 'Apply pricing recommendations'


@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    """Admin interface for Delivery Locations"""
    
    list_display = [
        'name', 'latitude', 'longitude', 'delivery_time_window',
        'access_difficulty_score', 'is_active'
    ]
    
    list_filter = ['access_difficulty_score', 'is_active']
    search_fields = ['name', 'address']
    
    def delivery_time_window(self, obj):
        return f"{obj.delivery_time_window_start} - {obj.delivery_time_window_end}"
    delivery_time_window.short_description = 'Delivery Window'


@admin.register(RouteOptimization)
class RouteOptimizationAdmin(SimpleHistoryAdmin):
    """Admin interface for Route Optimization"""
    
    list_display = [
        'route_name', 'delivery_date', 'total_distance_km', 'total_cost',
        'cost_savings_percentage', 'status', 'is_implemented'
    ]
    
    list_filter = ['status', 'is_implemented', 'delivery_date']
    search_fields = ['route_name']
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Route Details', {
            'fields': ('route_name', 'delivery_date', 'start_location')
        }),
        ('Optimization Results', {
            'fields': (
                'total_distance_km', 'total_time_hours', 'total_cost',
                'fuel_cost', 'driver_cost'
            )
        }),
        ('AI Optimization', {
            'fields': (
                'algorithm_used', 'optimization_time_seconds',
                'cost_savings_percentage'
            )
        }),
        ('Implementation', {
            'fields': (
                'status', 'is_implemented', 'implementation_feedback'
            )
        })
    )
    
    actions = ['optimize_routes']
    
    def optimize_routes(self, request, queryset):
        """Optimize selected routes"""
        optimization_service = RouteOptimizationService()
        count = 0
        
        for route in queryset.filter(status='pending'):
            try:
                # Get delivery locations for the route
                delivery_locations = [stop.location for stop in route.routestop_set.all()]
                
                if delivery_locations:
                    # Optimize route
                    result = optimization_service.optimize_route(
                        route.start_location, delivery_locations
                    )
                    
                    if 'error' not in result:
                        # Update route with optimization results
                        route.total_distance_km = result['total_distance_km']
                        route.total_time_hours = result['total_time_hours']
                        route.total_cost = result['total_cost']
                        route.fuel_cost = result['fuel_cost']
                        route.driver_cost = result['driver_cost']
                        route.cost_savings_percentage = result['cost_savings_percentage']
                        route.algorithm_used = result['algorithm_used']
                        route.status = 'completed'
                        route.save()
                        
                        count += 1
            
            except Exception as e:
                messages.error(request, f'Error optimizing route {route.route_name}: {e}')
        
        messages.success(request, f'Optimized {count} routes.')
    optimize_routes.short_description = 'Optimize selected routes'


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    """Admin interface for Route Stops"""
    
    list_display = [
        'route', 'stop_order', 'location', 'estimated_arrival_time',
        'delivery_weight_kg'
    ]
    
    list_filter = ['route__delivery_date']
    ordering = ['route', 'stop_order']


@admin.register(RiskFactor)
class RiskFactorAdmin(SimpleHistoryAdmin):
    """Admin interface for Risk Factors"""
    
    list_display = [
        'name', 'risk_type', 'severity', 'probability', 'impact_score',
        'is_active', 'last_assessed'
    ]
    
    list_filter = ['risk_type', 'severity', 'is_active']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Risk Information', {
            'fields': ('name', 'risk_type', 'description')
        }),
        ('Risk Assessment', {
            'fields': ('probability', 'impact_score', 'severity')
        }),
        ('Affected Entities', {
            'fields': ('affected_suppliers', 'affected_products')
        }),
        ('Monitoring & Mitigation', {
            'fields': (
                'monitoring_frequency_hours', 'mitigation_strategy',
                'contingency_plan'
            )
        }),
        ('Status', {
            'fields': ('is_active', 'last_assessed')
        })
    )


@admin.register(RiskAlert)
class RiskAlertAdmin(SimpleHistoryAdmin):
    """Admin interface for Risk Alerts"""
    
    list_display = [
        'title', 'alert_type', 'risk_score', 'confidence_score',
        'status', 'assigned_to', 'created_at'
    ]
    
    list_filter = ['alert_type', 'status', 'created_at']
    search_fields = ['title', 'description']
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('alert_type', 'title', 'description')
        }),
        ('AI Analysis', {
            'fields': (
                'confidence_score', 'risk_score', 'predicted_impact'
            )
        }),
        ('Associated Data', {
            'fields': (
                'risk_factors', 'affected_products', 'affected_suppliers'
            )
        }),
        ('Recommendations', {
            'fields': ('recommended_actions', 'estimated_cost_impact')
        }),
        ('Status & Resolution', {
            'fields': (
                'status', 'assigned_to', 'resolution_notes', 'resolved_at'
            )
        }),
        ('Notifications', {
            'fields': ('email_sent', 'sms_sent')
        })
    )
    
    actions = ['run_risk_assessment']
    
    def run_risk_assessment(self, request, queryset):
        """Run AI risk assessment"""
        risk_service = RiskManagementService()
        
        try:
            risks = risk_service.assess_supply_chain_risks()
            
            # Create new alerts for high-risk items
            new_alerts = 0
            for risk in risks:
                if risk['risk_score'] > 7.0:  # High risk threshold
                    alert, created = RiskAlert.objects.get_or_create(
                        alert_type=risk['type'],
                        title=risk['title'],
                        defaults={
                            'description': risk['description'],
                            'confidence_score': risk['probability'],
                            'risk_score': risk['risk_score'],
                            'predicted_impact': str(risk['factors']),
                            'recommended_actions': risk['recommendations']
                        }
                    )
                    if created:
                        new_alerts += 1
            
            messages.success(request, f'Risk assessment completed. Created {new_alerts} new alerts.')
        
        except Exception as e:
            messages.error(request, f'Error running risk assessment: {e}')
    
    run_risk_assessment.short_description = 'Run AI risk assessment'


@admin.register(AIModelPerformance)
class AIModelPerformanceAdmin(admin.ModelAdmin):
    """Admin interface for AI Model Performance"""
    
    list_display = [
        'model_type', 'model_version', 'accuracy_score', 'f1_score',
        'cost_savings_generated', 'is_active', 'last_trained'
    ]
    
    list_filter = ['model_type', 'is_active', 'last_trained']
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Model Information', {
            'fields': ('model_type', 'model_version', 'is_active')
        }),
        ('Performance Metrics', {
            'fields': (
                'accuracy_score', 'precision_score', 'recall_score', 'f1_score'
            )
        }),
        ('Training Information', {
            'fields': (
                'training_data_size', 'training_duration_minutes', 'last_trained'
            )
        }),
        ('Business Impact', {
            'fields': ('cost_savings_generated', 'revenue_impact')
        }),
        ('Configuration', {
            'fields': ('hyperparameters', 'feature_importance'),
            'classes': ('collapse',)
        })
    )
