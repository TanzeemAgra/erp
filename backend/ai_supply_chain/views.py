"""
AI Supply Chain Views
Django REST Framework views for AI Supply Chain API endpoints
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from datetime import timedelta, datetime
from django.db.models import Q, Avg, Count, Sum, F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    SupplyChainConfig, Product, Supplier, DemandForecast,
    DynamicPricing, DeliveryLocation, RouteOptimization, RouteStop,
    RiskFactor, RiskAlert, AIModelPerformance
)
from .serializers import (
    SupplyChainConfigSerializer, ProductSerializer, SupplierSerializer,
    DemandForecastSerializer, DynamicPricingSerializer, DeliveryLocationSerializer,
    RouteOptimizationSerializer, RiskFactorSerializer, RiskAlertSerializer,
    AIModelPerformanceSerializer, DemandForecastCreateSerializer,
    DynamicPricingCreateSerializer, RouteOptimizationCreateSerializer,
    RiskAssessmentCreateSerializer, RouteStopSerializer
)
from .services import (
    DemandForecastingService, DynamicPricingService,
    RouteOptimizationService, RiskManagementService
)


class SupplyChainConfigViewSet(viewsets.ModelViewSet):
    """ViewSet for Supply Chain Configuration"""
    
    queryset = SupplyChainConfig.objects.all()
    serializer_class = SupplyChainConfigSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        """Set updated_by when saving configuration"""
        serializer.save(updated_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active_config(self, request):
        """Get the active configuration"""
        config, created = SupplyChainConfig.objects.get_or_create(
            id=1,
            defaults={
                'updated_by': request.user
            }
        )
        serializer = self.get_serializer(config)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Products"""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = [
        'category', 'enable_demand_forecasting', 'enable_dynamic_pricing'
    ]
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'current_price', 'current_stock', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['post'])
    def generate_demand_forecast(self, request, pk=None):
        """Generate demand forecast for a specific product"""
        product = self.get_object()
        
        if not product.enable_demand_forecasting:
            return Response(
                {'error': 'Demand forecasting is not enabled for this product'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DemandForecastCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                forecast_service = DemandForecastingService()
                
                # Calculate forecast date
                horizon_days = serializer.validated_data.get('forecast_horizon_days', 30)
                forecast_date = timezone.now().date() + timedelta(days=horizon_days)
                
                # Generate forecast
                forecast_result = forecast_service.predict_demand(product, forecast_date)
                
                # Create forecast record
                forecast = DemandForecast.objects.create(
                    product=product,
                    forecast_date=forecast_date,
                    forecast_type=serializer.validated_data.get('forecast_type', 'weekly'),
                    predicted_demand=forecast_result['predicted_demand'],
                    confidence_interval_lower=forecast_result['confidence_interval_lower'],
                    confidence_interval_upper=forecast_result['confidence_interval_upper'],
                    confidence_score=forecast_result['confidence_score'],
                    seasonal_factor=forecast_result['seasonal_factor'],
                    trend_factor=forecast_result.get('trend_factor', 1.0),
                    market_factor=forecast_result.get('market_factor', 1.0),
                    model_version='1.0',
                    algorithm_used='ensemble',
                    training_data_points=100
                )
                
                forecast_serializer = DemandForecastSerializer(forecast)
                return Response(forecast_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to generate forecast: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def calculate_dynamic_pricing(self, request, pk=None):
        """Calculate dynamic pricing for a specific product"""
        product = self.get_object()
        
        if not product.enable_dynamic_pricing:
            return Response(
                {'error': 'Dynamic pricing is not enabled for this product'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DynamicPricingCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pricing_service = DynamicPricingService()
                
                # Calculate optimal price
                pricing_result = pricing_service.calculate_optimal_price(product)
                
                # Create pricing recommendation
                pricing = DynamicPricing.objects.create(
                    product=product,
                    current_price=product.current_price,
                    current_stock_level=product.current_stock,
                    current_demand_rate=10.0,  # This should come from actual data
                    recommended_price=pricing_result['recommended_price'],
                    price_change_percentage=pricing_result['price_change_percentage'],
                    pricing_strategy=pricing_result['pricing_strategy'],
                    inventory_factor=pricing_result['factors']['inventory_factor'],
                    demand_factor=pricing_result['factors']['demand_factor'],
                    competition_factor=pricing_result['factors']['competition_factor'],
                    seasonality_factor=pricing_result['factors']['seasonality_factor'],
                    expected_demand_change=pricing_result['expected_demand_change'],
                    expected_revenue_impact=pricing_result['expected_revenue_impact'],
                    expected_profit_margin=15.0,  # Calculate from actual data
                    valid_until=timezone.now() + timedelta(days=7)
                )
                
                pricing_serializer = DynamicPricingSerializer(pricing)
                return Response(pricing_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to calculate pricing: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get product analytics summary"""
        total_products = Product.objects.count()
        forecasting_enabled = Product.objects.filter(enable_demand_forecasting=True).count()
        pricing_enabled = Product.objects.filter(enable_dynamic_pricing=True).count()
        low_stock_products = Product.objects.filter(
            current_stock__lte=F('reorder_level')
        ).count()
        
        # Recent forecasts
        recent_forecasts = DemandForecast.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Recent pricing recommendations
        recent_pricing = DynamicPricing.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return Response({
            'total_products': total_products,
            'forecasting_enabled': forecasting_enabled,
            'pricing_enabled': pricing_enabled,
            'low_stock_products': low_stock_products,
            'recent_forecasts': recent_forecasts,
            'recent_pricing_recommendations': recent_pricing,
            'forecasting_adoption_rate': (forecasting_enabled / total_products * 100) if total_products > 0 else 0,
            'pricing_adoption_rate': (pricing_enabled / total_products * 100) if total_products > 0 else 0
        })


class SupplierViewSet(viewsets.ModelViewSet):
    """ViewSet for Suppliers"""
    
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['is_active', 'country', 'reliability_score']
    search_fields = ['name', 'code', 'contact_person', 'email']
    ordering_fields = ['name', 'reliability_score', 'on_time_delivery_rate', 'quality_score']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def performance_analytics(self, request):
        """Get supplier performance analytics"""
        suppliers = Supplier.objects.filter(is_active=True)
        
        avg_reliability = suppliers.aggregate(
            avg_reliability=Avg('reliability_score')
        )['avg_reliability'] or 0
        
        avg_delivery_rate = suppliers.aggregate(
            avg_delivery=Avg('on_time_delivery_rate')
        )['avg_delivery'] or 0
        
        avg_quality = suppliers.aggregate(
            avg_quality=Avg('quality_score')
        )['avg_quality'] or 0
        
        # Risk distribution
        high_risk = suppliers.filter(reliability_score__lt=6).count()
        medium_risk = suppliers.filter(
            reliability_score__gte=6,
            reliability_score__lt=8
        ).count()
        low_risk = suppliers.filter(reliability_score__gte=8).count()
        
        return Response({
            'total_suppliers': suppliers.count(),
            'average_reliability_score': round(avg_reliability, 2),
            'average_on_time_delivery_rate': round(avg_delivery_rate, 2),
            'average_quality_score': round(avg_quality, 2),
            'risk_distribution': {
                'high_risk': high_risk,
                'medium_risk': medium_risk,
                'low_risk': low_risk
            }
        })


class DemandForecastViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Demand Forecasts (read-only)"""
    
    queryset = DemandForecast.objects.all()
    serializer_class = DemandForecastSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    filterset_fields = ['forecast_type', 'product']
    ordering_fields = ['forecast_date', 'created_at', 'confidence_score']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def accuracy_report(self, request):
        """Get forecast accuracy report"""
        forecasts_with_actuals = DemandForecast.objects.filter(
            actual_demand__isnull=False,
            accuracy_score__isnull=False
        )
        
        if not forecasts_with_actuals.exists():
            return Response({
                'message': 'No forecast accuracy data available',
                'total_forecasts': 0,
                'average_accuracy': 0
            })
        
        avg_accuracy = forecasts_with_actuals.aggregate(
            avg_accuracy=Avg('accuracy_score')
        )['avg_accuracy']
        
        # Accuracy by forecast type
        accuracy_by_type = {}
        for forecast_type in ['daily', 'weekly', 'monthly']:
            type_accuracy = forecasts_with_actuals.filter(
                forecast_type=forecast_type
            ).aggregate(avg_accuracy=Avg('accuracy_score'))['avg_accuracy']
            
            if type_accuracy:
                accuracy_by_type[forecast_type] = round(type_accuracy, 2)
        
        return Response({
            'total_forecasts_validated': forecasts_with_actuals.count(),
            'average_accuracy_percentage': round(avg_accuracy, 2) if avg_accuracy else 0,
            'accuracy_by_forecast_type': accuracy_by_type
        })


class DynamicPricingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Dynamic Pricing (read-only)"""
    
    queryset = DynamicPricing.objects.all()
    serializer_class = DynamicPricingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    filterset_fields = ['pricing_strategy', 'is_applied', 'product']
    ordering_fields = ['created_at', 'price_change_percentage', 'expected_revenue_impact']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def apply_pricing(self, request, pk=None):
        """Apply a pricing recommendation"""
        pricing = self.get_object()
        
        if pricing.is_applied:
            return Response(
                {'error': 'This pricing recommendation has already been applied'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if pricing.valid_until < timezone.now():
            return Response(
                {'error': 'This pricing recommendation has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Update product price
            pricing.product.current_price = pricing.recommended_price
            pricing.product.save()
            
            # Mark pricing as applied
            pricing.is_applied = True
            pricing.applied_at = timezone.now()
            pricing.save()
            
            return Response({
                'message': 'Pricing recommendation applied successfully',
                'new_price': pricing.recommended_price
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to apply pricing: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def revenue_impact_report(self, request):
        """Get revenue impact report from applied pricing"""
        applied_pricing = DynamicPricing.objects.filter(is_applied=True)
        
        total_revenue_impact = applied_pricing.aggregate(
            total_impact=Sum('expected_revenue_impact')
        )['total_impact'] or 0
        
        # Group by pricing strategy
        strategy_impact = {}
        for strategy in ['premium', 'competitive', 'penetration', 'dynamic']:
            strategy_revenue = applied_pricing.filter(
                pricing_strategy=strategy
            ).aggregate(
                revenue=Sum('expected_revenue_impact')
            )['revenue'] or 0
            
            strategy_impact[strategy] = strategy_revenue
        
        return Response({
            'total_applied_recommendations': applied_pricing.count(),
            'total_revenue_impact': round(total_revenue_impact, 2),
            'revenue_impact_by_strategy': {
                k: round(v, 2) for k, v in strategy_impact.items()
            }
        })


class DeliveryLocationViewSet(viewsets.ModelViewSet):
    """ViewSet for Delivery Locations"""
    
    queryset = DeliveryLocation.objects.all()
    serializer_class = DeliveryLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['is_active', 'access_difficulty_score']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'access_difficulty_score']
    ordering = ['name']


class RouteOptimizationViewSet(viewsets.ModelViewSet):
    """ViewSet for Route Optimization"""
    
    queryset = RouteOptimization.objects.all()
    serializer_class = RouteOptimizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    filterset_fields = ['status', 'is_implemented', 'delivery_date']
    ordering_fields = ['delivery_date', 'total_cost', 'cost_savings_percentage']
    ordering = ['-delivery_date']
    
    @action(detail=False, methods=['post'])
    def optimize_route(self, request):
        """Create and optimize a new route"""
        serializer = RouteOptimizationCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                optimization_service = RouteOptimizationService()
                
                # Get locations
                start_location = get_object_or_404(
                    DeliveryLocation,
                    id=serializer.validated_data['start_location_id']
                )
                
                delivery_locations = DeliveryLocation.objects.filter(
                    id__in=serializer.validated_data['delivery_locations']
                )
                
                # Optimize route
                optimization_result = optimization_service.optimize_route(
                    start_location, list(delivery_locations)
                )
                
                if 'error' in optimization_result:
                    return Response(
                        {'error': optimization_result['error']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create route optimization record
                route = RouteOptimization.objects.create(
                    route_name=f"Route {timezone.now().strftime('%Y%m%d_%H%M%S')}",
                    delivery_date=serializer.validated_data['delivery_date'],
                    start_location=start_location,
                    total_distance_km=optimization_result['total_distance_km'],
                    total_time_hours=optimization_result['total_time_hours'],
                    total_cost=optimization_result['total_cost'],
                    fuel_cost=optimization_result['fuel_cost'],
                    driver_cost=optimization_result['driver_cost'],
                    algorithm_used=optimization_result['algorithm_used'],
                    optimization_time_seconds=optimization_result['optimization_time_seconds'],
                    cost_savings_percentage=optimization_result['cost_savings_percentage'],
                    status='completed'
                )
                
                # Create route stops
                for i, location in enumerate(optimization_result['optimized_order']):
                    RouteStop.objects.create(
                        route=route,
                        location=location,
                        stop_order=i + 1,
                        estimated_arrival_time=timezone.now() + timedelta(
                            hours=i * 0.5  # Simplified calculation
                        ),
                        delivery_weight_kg=100.0  # This should come from actual order data
                    )
                
                route_serializer = RouteOptimizationSerializer(route)
                return Response(route_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to optimize route: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def implement_route(self, request, pk=None):
        """Mark a route as implemented"""
        route = self.get_object()
        
        if route.is_implemented:
            return Response(
                {'error': 'Route has already been implemented'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        route.is_implemented = True
        route.status = 'implemented'
        route.save()
        
        return Response({'message': 'Route marked as implemented'})
    
    @action(detail=False, methods=['get'])
    def savings_report(self, request):
        """Get route optimization savings report"""
        implemented_routes = RouteOptimization.objects.filter(is_implemented=True)
        
        total_savings = implemented_routes.aggregate(
            total_cost=Sum('total_cost'),
            total_distance=Sum('total_distance_km')
        )
        
        avg_savings_percentage = implemented_routes.aggregate(
            avg_savings=Avg('cost_savings_percentage')
        )['avg_savings'] or 0
        
        return Response({
            'total_implemented_routes': implemented_routes.count(),
            'total_cost_savings': round(total_savings['total_cost'] or 0, 2),
            'total_distance_optimized': round(total_savings['total_distance'] or 0, 2),
            'average_savings_percentage': round(avg_savings_percentage, 2)
        })


class RiskFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for Risk Factors"""
    
    queryset = RiskFactor.objects.all()
    serializer_class = RiskFactorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['risk_type', 'severity', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'severity', 'impact_score', 'last_assessed']
    ordering = ['-impact_score']


class RiskAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for Risk Alerts"""
    
    queryset = RiskAlert.objects.all()
    serializer_class = RiskAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['alert_type', 'status', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'risk_score', 'confidence_score']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['post'])
    def run_risk_assessment(self, request):
        """Run AI-powered risk assessment"""
        serializer = RiskAssessmentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                risk_service = RiskManagementService()
                
                # Run risk assessment
                risks = risk_service.assess_supply_chain_risks()
                
                risk_threshold = serializer.validated_data.get('risk_threshold', 5.0)
                new_alerts = []
                
                # Create alerts for high-risk items
                for risk in risks:
                    if risk['risk_score'] >= risk_threshold:
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
                            new_alerts.append(alert)
                
                # Serialize new alerts
                alert_serializer = RiskAlertSerializer(new_alerts, many=True)
                
                return Response({
                    'message': f'Risk assessment completed. Created {len(new_alerts)} new alerts.',
                    'total_risks_identified': len(risks),
                    'new_alerts': alert_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to run risk assessment: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def resolve_alert(self, request, pk=None):
        """Resolve a risk alert"""
        alert = self.get_object()
        
        if alert.status == 'resolved':
            return Response(
                {'error': 'Alert is already resolved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resolution_notes = request.data.get('resolution_notes', '')
        
        alert.status = 'resolved'
        alert.resolved_at = timezone.now()
        alert.resolution_notes = resolution_notes
        alert.save()
        
        return Response({'message': 'Alert resolved successfully'})


class AIModelPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AI Model Performance (read-only)"""
    
    queryset = AIModelPerformance.objects.all()
    serializer_class = AIModelPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    filterset_fields = ['model_type', 'is_active']
    ordering_fields = ['model_type', 'accuracy_score', 'last_trained']
    ordering = ['-last_trained']
    
    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        """Get AI models dashboard summary"""
        models = AIModelPerformance.objects.filter(is_active=True)
        
        summary = {
            'total_active_models': models.count(),
            'models_by_type': {},
            'average_accuracy': 0,
            'models_needing_retraining': 0,
            'total_cost_savings': 0
        }
        
        # Models by type
        for model_type in ['demand_forecasting', 'dynamic_pricing', 'route_optimization', 'risk_management']:
            type_models = models.filter(model_type=model_type)
            summary['models_by_type'][model_type] = {
                'count': type_models.count(),
                'avg_accuracy': type_models.aggregate(
                    avg_acc=Avg('accuracy_score')
                )['avg_acc'] or 0
            }
        
        # Overall average accuracy
        summary['average_accuracy'] = models.aggregate(
            avg_acc=Avg('accuracy_score')
        )['avg_acc'] or 0
        
        # Models needing retraining (older than 30 days)
        cutoff_date = timezone.now() - timedelta(days=30)
        summary['models_needing_retraining'] = models.filter(
            Q(last_trained__lt=cutoff_date) | Q(last_trained__isnull=True)
        ).count()
        
        # Total cost savings
        summary['total_cost_savings'] = models.aggregate(
            total_savings=Sum('cost_savings_generated')
        )['total_savings'] or 0
        
        return Response(summary)
