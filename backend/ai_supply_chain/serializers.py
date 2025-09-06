"""
AI Supply Chain Serializers
DRF serializers for AI Supply Chain API endpoints
"""

from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import (
    SupplyChainConfig, Product, Supplier, DemandForecast,
    DynamicPricing, DeliveryLocation, RouteOptimization, RouteStop,
    RiskFactor, RiskAlert, AIModelPerformance
)


class SupplyChainConfigSerializer(serializers.ModelSerializer):
    """Serializer for Supply Chain Configuration"""
    
    class Meta:
        model = SupplyChainConfig
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'updated_by']
    
    def validate(self, data):
        """Validate configuration parameters"""
        if data.get('min_profit_margin', 0) < 0:
            raise serializers.ValidationError("Minimum profit margin cannot be negative")
        
        if data.get('max_price_adjustment', 0) > 1.0:
            raise serializers.ValidationError("Maximum price adjustment cannot exceed 100%")
        
        return data


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Products"""
    
    profit_margin = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()
    demand_forecast_available = serializers.SerializerMethodField()
    latest_pricing_recommendation = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_profit_margin(self, obj):
        """Calculate current profit margin"""
        if obj.base_cost and obj.current_price:
            return ((obj.current_price - obj.base_cost) / obj.current_price) * 100
        return None
    
    def get_stock_status(self, obj):
        """Determine stock status"""
        if obj.current_stock <= obj.reorder_level:
            return "low"
        elif obj.current_stock >= obj.max_stock_level:
            return "high"
        return "normal"
    
    def get_demand_forecast_available(self, obj):
        """Check if recent demand forecast is available"""
        recent_forecast = DemandForecast.objects.filter(
            product=obj,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).exists()
        return recent_forecast
    
    def get_latest_pricing_recommendation(self, obj):
        """Get latest pricing recommendation"""
        latest_pricing = DynamicPricing.objects.filter(
            product=obj,
            is_applied=False,
            valid_until__gt=timezone.now()
        ).order_by('-created_at').first()
        
        if latest_pricing:
            return {
                'recommended_price': latest_pricing.recommended_price,
                'price_change_percentage': latest_pricing.price_change_percentage,
                'pricing_strategy': latest_pricing.pricing_strategy
            }
        return None


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Suppliers"""
    
    risk_level = serializers.SerializerMethodField()
    performance_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_risk_level(self, obj):
        """Calculate overall risk level"""
        risk_score = 0
        factors = 0
        
        if obj.reliability_score is not None:
            risk_score += (10 - obj.reliability_score)
            factors += 1
        
        if obj.financial_stability is not None:
            risk_score += (10 - obj.financial_stability)
            factors += 1
        
        if obj.geographic_risk is not None:
            risk_score += obj.geographic_risk
            factors += 1
        
        if factors > 0:
            avg_risk = risk_score / factors
            if avg_risk <= 3:
                return "low"
            elif avg_risk <= 6:
                return "medium"
            else:
                return "high"
        
        return "unknown"
    
    def get_performance_score(self, obj):
        """Calculate overall performance score"""
        scores = []
        
        if obj.reliability_score is not None:
            scores.append(obj.reliability_score)
        
        if obj.on_time_delivery_rate is not None:
            scores.append(obj.on_time_delivery_rate)
        
        if obj.quality_score is not None:
            scores.append(obj.quality_score)
        
        if scores:
            return sum(scores) / len(scores)
        
        return None


class DemandForecastSerializer(serializers.ModelSerializer):
    """Serializer for Demand Forecasts"""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    forecast_accuracy = serializers.SerializerMethodField()
    
    class Meta:
        model = DemandForecast
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_forecast_accuracy(self, obj):
        """Calculate forecast accuracy if actual demand is available"""
        if obj.actual_demand is not None and obj.predicted_demand > 0:
            error = abs(obj.actual_demand - obj.predicted_demand) / obj.predicted_demand
            return max(0, (1 - error) * 100)
        return None


class DynamicPricingSerializer(serializers.ModelSerializer):
    """Serializer for Dynamic Pricing"""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    potential_revenue_increase = serializers.SerializerMethodField()
    
    class Meta:
        model = DynamicPricing
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_potential_revenue_increase(self, obj):
        """Calculate potential revenue increase"""
        if obj.expected_revenue_impact:
            return obj.expected_revenue_impact
        
        # Simplified calculation
        price_diff = obj.recommended_price - obj.current_price
        if price_diff > 0:
            return (price_diff / obj.current_price) * 100
        return 0


class DeliveryLocationSerializer(serializers.ModelSerializer):
    """Serializer for Delivery Locations"""
    
    estimated_delivery_time = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryLocation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_estimated_delivery_time(self, obj):
        """Calculate estimated delivery time based on distance and access difficulty"""
        # Simplified calculation - in production, use real distance calculation
        base_time = 60  # minutes
        difficulty_multiplier = 1 + (obj.access_difficulty_score * 0.1)
        return base_time * difficulty_multiplier


class RouteStopSerializer(serializers.ModelSerializer):
    """Serializer for Route Stops"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    location_address = serializers.CharField(source='location.address', read_only=True)
    
    class Meta:
        model = RouteStop
        fields = '__all__'


class RouteOptimizationSerializer(serializers.ModelSerializer):
    """Serializer for Route Optimization"""
    
    stops = RouteStopSerializer(source='routestop_set', many=True, read_only=True)
    cost_efficiency = serializers.SerializerMethodField()
    environmental_impact = serializers.SerializerMethodField()
    
    class Meta:
        model = RouteOptimization
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_cost_efficiency(self, obj):
        """Calculate cost efficiency metrics"""
        if obj.total_distance_km and obj.total_cost:
            return {
                'cost_per_km': obj.total_cost / obj.total_distance_km,
                'cost_savings_percentage': obj.cost_savings_percentage
            }
        return None
    
    def get_environmental_impact(self, obj):
        """Calculate environmental impact"""
        if obj.total_distance_km:
            # Simplified calculation - 0.2 kg CO2 per km
            co2_emissions = obj.total_distance_km * 0.2
            return {
                'co2_emissions_kg': round(co2_emissions, 2),
                'fuel_consumption_liters': round(obj.total_distance_km * 0.08, 2)
            }
        return None


class RiskFactorSerializer(serializers.ModelSerializer):
    """Serializer for Risk Factors"""
    
    risk_level = serializers.SerializerMethodField()
    affected_suppliers_count = serializers.SerializerMethodField()
    affected_products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RiskFactor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'last_assessed']
    
    def get_risk_level(self, obj):
        """Determine risk level based on probability and impact"""
        risk_score = (obj.probability * obj.impact_score) / 10
        
        if risk_score >= 8:
            return "critical"
        elif risk_score >= 6:
            return "high"
        elif risk_score >= 4:
            return "medium"
        else:
            return "low"
    
    def get_affected_suppliers_count(self, obj):
        """Count affected suppliers"""
        return obj.affected_suppliers.count()
    
    def get_affected_products_count(self, obj):
        """Count affected products"""
        return obj.affected_products.count()


class RiskAlertSerializer(serializers.ModelSerializer):
    """Serializer for Risk Alerts"""
    
    risk_factor_names = serializers.SerializerMethodField()
    affected_suppliers_count = serializers.SerializerMethodField()
    affected_products_count = serializers.SerializerMethodField()
    time_since_created = serializers.SerializerMethodField()
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = RiskAlert
        fields = '__all__'
        read_only_fields = ['created_at', 'email_sent', 'sms_sent']
    
    def get_risk_factor_names(self, obj):
        """Get names of associated risk factors"""
        return [rf.name for rf in obj.risk_factors.all()]
    
    def get_affected_suppliers_count(self, obj):
        """Count affected suppliers"""
        return obj.affected_suppliers.count()
    
    def get_affected_products_count(self, obj):
        """Count affected products"""
        return obj.affected_products.count()
    
    def get_time_since_created(self, obj):
        """Calculate time since alert was created"""
        time_diff = timezone.now() - obj.created_at
        
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif time_diff.seconds > 3600:
            hours = time_diff.seconds // 3600
            return f"{hours} hours ago"
        elif time_diff.seconds > 60:
            minutes = time_diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"


class AIModelPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for AI Model Performance"""
    
    overall_score = serializers.SerializerMethodField()
    training_status = serializers.SerializerMethodField()
    
    class Meta:
        model = AIModelPerformance
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_overall_score(self, obj):
        """Calculate overall model performance score"""
        scores = []
        
        if obj.accuracy_score is not None:
            scores.append(obj.accuracy_score)
        
        if obj.precision_score is not None:
            scores.append(obj.precision_score)
        
        if obj.recall_score is not None:
            scores.append(obj.recall_score)
        
        if obj.f1_score is not None:
            scores.append(obj.f1_score)
        
        if scores:
            return sum(scores) / len(scores)
        
        return None
    
    def get_training_status(self, obj):
        """Determine training status"""
        if not obj.last_trained:
            return "never_trained"
        
        time_since_training = timezone.now() - obj.last_trained
        
        if time_since_training.days > 30:
            return "needs_retraining"
        elif time_since_training.days > 7:
            return "should_retrain"
        else:
            return "up_to_date"


# Specialized serializers for API endpoints

class DemandForecastCreateSerializer(serializers.Serializer):
    """Serializer for creating demand forecasts"""
    
    product_id = serializers.IntegerField()
    forecast_horizon_days = serializers.IntegerField(min_value=1, max_value=365, default=30)
    forecast_type = serializers.ChoiceField(choices=['daily', 'weekly', 'monthly'], default='weekly')
    
    def validate_product_id(self, value):
        """Validate that product exists and has forecasting enabled"""
        try:
            product = Product.objects.get(id=value)
            if not product.enable_demand_forecasting:
                raise serializers.ValidationError("Demand forecasting is not enabled for this product")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")


class DynamicPricingCreateSerializer(serializers.Serializer):
    """Serializer for creating dynamic pricing recommendations"""
    
    product_id = serializers.IntegerField()
    market_conditions = serializers.JSONField(required=False)
    competitor_prices = serializers.JSONField(required=False)
    
    def validate_product_id(self, value):
        """Validate that product exists and has dynamic pricing enabled"""
        try:
            product = Product.objects.get(id=value)
            if not product.enable_dynamic_pricing:
                raise serializers.ValidationError("Dynamic pricing is not enabled for this product")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")


class RouteOptimizationCreateSerializer(serializers.Serializer):
    """Serializer for creating route optimizations"""
    
    delivery_locations = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=2,
        help_text="List of delivery location IDs"
    )
    start_location_id = serializers.IntegerField()
    delivery_date = serializers.DateField()
    vehicle_capacity_kg = serializers.FloatField(min_value=0, required=False)
    
    def validate_delivery_locations(self, value):
        """Validate that all delivery locations exist"""
        existing_locations = DeliveryLocation.objects.filter(
            id__in=value,
            is_active=True
        ).count()
        
        if existing_locations != len(value):
            raise serializers.ValidationError("One or more delivery locations not found or inactive")
        
        return value
    
    def validate_start_location_id(self, value):
        """Validate that start location exists"""
        if not DeliveryLocation.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Start location not found or inactive")
        return value


class RiskAssessmentCreateSerializer(serializers.Serializer):
    """Serializer for creating risk assessments"""
    
    assessment_type = serializers.ChoiceField(
        choices=['comprehensive', 'supplier', 'product', 'financial'],
        default='comprehensive'
    )
    target_entities = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="IDs of specific entities to assess (suppliers/products)"
    )
    risk_threshold = serializers.FloatField(
        min_value=0,
        max_value=10,
        default=5.0,
        help_text="Minimum risk score to generate alerts"
    )
