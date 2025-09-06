"""
AI Supply Chain Optimization Models
Implements AI-driven supply chain management features
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from decimal import Decimal
import json

User = get_user_model()


class SupplyChainConfig(models.Model):
    """Configuration for AI Supply Chain parameters"""
    
    # AI Model Configuration
    demand_forecasting_enabled = models.BooleanField(default=True)
    dynamic_pricing_enabled = models.BooleanField(default=True)
    route_optimization_enabled = models.BooleanField(default=True)
    risk_management_enabled = models.BooleanField(default=True)
    
    # Forecasting Parameters
    forecasting_horizon_days = models.IntegerField(default=90, validators=[MinValueValidator(1), MaxValueValidator(365)])
    seasonal_adjustment_factor = models.DecimalField(max_digits=5, decimal_places=3, default=1.0)
    demand_sensitivity = models.DecimalField(max_digits=5, decimal_places=3, default=0.8)
    
    # Pricing Parameters
    min_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=15.0)  # %
    max_price_adjustment = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)  # %
    competitor_weight = models.DecimalField(max_digits=3, decimal_places=2, default=0.3)
    market_weight = models.DecimalField(max_digits=3, decimal_places=2, default=0.4)
    inventory_weight = models.DecimalField(max_digits=3, decimal_places=2, default=0.3)
    
    # Route Optimization Parameters
    fuel_cost_per_km = models.DecimalField(max_digits=10, decimal_places=2, default=1.5)
    driver_cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=25.0)
    vehicle_capacity_kg = models.IntegerField(default=1000)
    max_delivery_distance_km = models.IntegerField(default=500)
    
    # Risk Management Parameters
    risk_threshold_high = models.DecimalField(max_digits=3, decimal_places=2, default=0.8)
    risk_threshold_medium = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)
    alert_notification_enabled = models.BooleanField(default=True)
    
    # System Configuration
    ai_model_update_frequency_hours = models.IntegerField(default=24)
    data_retention_days = models.IntegerField(default=365)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Supply Chain Configuration"
        verbose_name_plural = "Supply Chain Configurations"
    
    def __str__(self):
        return f"Supply Chain Config - Updated {self.updated_at.strftime('%Y-%m-%d')}"


class Product(models.Model):
    """Product master for supply chain optimization"""
    
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('software', 'Software'),
        ('hardware', 'Hardware'),
        ('services', 'Services'),
        ('consumables', 'Consumables'),
    ]
    
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    # Pricing Information
    base_cost = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    min_price = models.DecimalField(max_digits=12, decimal_places=2)
    max_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Inventory Information
    current_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    max_stock_level = models.IntegerField(default=1000)
    
    # Physical Properties
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    dimensions_cm = models.CharField(max_length=50, blank=True)  # LxWxH
    
    # AI Optimization Flags
    enable_demand_forecasting = models.BooleanField(default=True)
    enable_dynamic_pricing = models.BooleanField(default=True)
    
    # Seasonality and Demand Patterns
    seasonal_factor = models.JSONField(default=dict, blank=True)  # Monthly factors
    demand_volatility = models.DecimalField(max_digits=5, decimal_places=3, default=0.2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.sku})"


class Supplier(models.Model):
    """Supplier information for supply chain management"""
    
    RELIABILITY_CHOICES = [
        ('excellent', 'Excellent (95-100%)'),
        ('good', 'Good (85-94%)'),
        ('average', 'Average (70-84%)'),
        ('poor', 'Poor (<70%)'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # AI Analytics
    reliability_score = models.CharField(max_length=20, choices=RELIABILITY_CHOICES, default='average')
    avg_delivery_time_days = models.IntegerField(default=7)
    on_time_delivery_rate = models.DecimalField(max_digits=5, decimal_places=2, default=85.0)  # %
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, default=8.0)  # out of 10
    
    # Risk Factors
    financial_stability = models.DecimalField(max_digits=3, decimal_places=2, default=0.8)  # 0-1 scale
    geographic_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0.2)  # 0-1 scale
    
    # Business Terms
    payment_terms_days = models.IntegerField(default=30)
    minimum_order_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class DemandForecast(models.Model):
    """AI-generated demand forecasts for products"""
    
    FORECAST_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='demand_forecasts')
    forecast_date = models.DateField()
    forecast_type = models.CharField(max_length=20, choices=FORECAST_TYPE_CHOICES)
    
    # Forecast Values
    predicted_demand = models.IntegerField()
    confidence_interval_lower = models.IntegerField()
    confidence_interval_upper = models.IntegerField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=3)  # 0-1 scale
    
    # Contributing Factors
    seasonal_factor = models.DecimalField(max_digits=5, decimal_places=3, default=1.0)
    trend_factor = models.DecimalField(max_digits=5, decimal_places=3, default=1.0)
    market_factor = models.DecimalField(max_digits=5, decimal_places=3, default=1.0)
    
    # AI Model Information
    model_version = models.CharField(max_length=20)
    algorithm_used = models.CharField(max_length=50)
    training_data_points = models.IntegerField()
    
    # Actual vs Predicted (for model improvement)
    actual_demand = models.IntegerField(null=True, blank=True)
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Demand Forecast"
        verbose_name_plural = "Demand Forecasts"
        unique_together = ['product', 'forecast_date', 'forecast_type']
        ordering = ['-forecast_date']
    
    def __str__(self):
        return f"{self.product.name} - {self.forecast_date} ({self.forecast_type})"


class DynamicPricing(models.Model):
    """AI-driven dynamic pricing recommendations"""
    
    PRICING_STRATEGY_CHOICES = [
        ('competitive', 'Competitive Pricing'),
        ('premium', 'Premium Pricing'),
        ('penetration', 'Market Penetration'),
        ('inventory_based', 'Inventory-Based'),
        ('demand_based', 'Demand-Based'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pricing_recommendations')
    
    # Current State
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_stock_level = models.IntegerField()
    current_demand_rate = models.DecimalField(max_digits=8, decimal_places=2)
    
    # AI Recommendations
    recommended_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pricing_strategy = models.CharField(max_length=20, choices=PRICING_STRATEGY_CHOICES)
    
    # Market Analysis
    competitor_avg_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    market_price_trend = models.CharField(max_length=20)  # 'increasing', 'decreasing', 'stable'
    
    # Factors Influencing Price
    inventory_factor = models.DecimalField(max_digits=5, decimal_places=3)
    demand_factor = models.DecimalField(max_digits=5, decimal_places=3)
    competition_factor = models.DecimalField(max_digits=5, decimal_places=3)
    seasonality_factor = models.DecimalField(max_digits=5, decimal_places=3)
    
    # Expected Impact
    expected_demand_change = models.DecimalField(max_digits=5, decimal_places=2)  # %
    expected_revenue_impact = models.DecimalField(max_digits=12, decimal_places=2)
    expected_profit_margin = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Implementation
    is_applied = models.BooleanField(default=False)
    applied_at = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Dynamic Pricing"
        verbose_name_plural = "Dynamic Pricing Recommendations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - ${self.current_price} → ${self.recommended_price}"


class DeliveryLocation(models.Model):
    """Customer delivery locations for route optimization"""
    
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    # Delivery Constraints
    delivery_time_window_start = models.TimeField()
    delivery_time_window_end = models.TimeField()
    max_delivery_weight_kg = models.IntegerField(default=1000)
    
    # Historical Data
    avg_delivery_time_minutes = models.IntegerField(default=30)
    access_difficulty_score = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Delivery Location"
        verbose_name_plural = "Delivery Locations"
    
    def __str__(self):
        return self.name


class RouteOptimization(models.Model):
    """AI-optimized delivery routes"""
    
    OPTIMIZATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('optimizing', 'Optimizing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    route_name = models.CharField(max_length=100)
    delivery_date = models.DateField()
    
    # Route Details
    start_location = models.ForeignKey(DeliveryLocation, on_delete=models.CASCADE, related_name='routes_starting')
    delivery_locations = models.ManyToManyField(DeliveryLocation, through='RouteStop')
    
    # Optimization Results
    total_distance_km = models.DecimalField(max_digits=8, decimal_places=2)
    total_time_hours = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # AI Optimization Details
    algorithm_used = models.CharField(max_length=50)
    optimization_time_seconds = models.DecimalField(max_digits=8, decimal_places=2)
    cost_savings_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Status and Implementation
    status = models.CharField(max_length=20, choices=OPTIMIZATION_STATUS_CHOICES, default='pending')
    is_implemented = models.BooleanField(default=False)
    implementation_feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Route Optimization"
        verbose_name_plural = "Route Optimizations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.route_name} - {self.delivery_date}"


class RouteStop(models.Model):
    """Individual stops in an optimized route"""
    
    route = models.ForeignKey(RouteOptimization, on_delete=models.CASCADE)
    location = models.ForeignKey(DeliveryLocation, on_delete=models.CASCADE)
    stop_order = models.IntegerField()
    
    # Stop Details
    estimated_arrival_time = models.TimeField()
    estimated_service_time_minutes = models.IntegerField()
    delivery_weight_kg = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Distance and Time from Previous Stop
    distance_from_previous_km = models.DecimalField(max_digits=8, decimal_places=2)
    travel_time_from_previous_minutes = models.IntegerField()
    
    class Meta:
        verbose_name = "Route Stop"
        verbose_name_plural = "Route Stops"
        ordering = ['route', 'stop_order']
    
    def __str__(self):
        return f"{self.route.route_name} - Stop {self.stop_order}: {self.location.name}"


class RiskFactor(models.Model):
    """Supply chain risk factors for monitoring"""
    
    RISK_TYPE_CHOICES = [
        ('supplier', 'Supplier Risk'),
        ('logistics', 'Logistics Risk'),
        ('market', 'Market Risk'),
        ('financial', 'Financial Risk'),
        ('operational', 'Operational Risk'),
        ('external', 'External Risk'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    name = models.CharField(max_length=200)
    risk_type = models.CharField(max_length=20, choices=RISK_TYPE_CHOICES)
    description = models.TextField()
    
    # Risk Assessment
    probability = models.DecimalField(max_digits=5, decimal_places=3)  # 0-1 scale
    impact_score = models.DecimalField(max_digits=5, decimal_places=2)  # 1-10 scale
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    
    # Associated Entities
    affected_suppliers = models.ManyToManyField(Supplier, blank=True)
    affected_products = models.ManyToManyField(Product, blank=True)
    
    # Monitoring and Mitigation
    monitoring_frequency_hours = models.IntegerField(default=24)
    mitigation_strategy = models.TextField()
    contingency_plan = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_assessed = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Risk Factor"
        verbose_name_plural = "Risk Factors"
        ordering = ['-impact_score', '-probability']
    
    def __str__(self):
        return f"{self.name} ({self.severity})"


class RiskAlert(models.Model):
    """AI-generated risk alerts and notifications"""
    
    ALERT_TYPE_CHOICES = [
        ('demand_spike', 'Demand Spike'),
        ('supplier_delay', 'Supplier Delay'),
        ('stock_shortage', 'Stock Shortage'),
        ('price_volatility', 'Price Volatility'),
        ('route_disruption', 'Route Disruption'),
        ('quality_issue', 'Quality Issue'),
        ('external_event', 'External Event'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # AI Analysis
    confidence_score = models.DecimalField(max_digits=5, decimal_places=3)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)  # 1-10 scale
    predicted_impact = models.TextField()
    
    # Associated Data
    risk_factors = models.ManyToManyField(RiskFactor, blank=True)
    affected_products = models.ManyToManyField(Product, blank=True)
    affected_suppliers = models.ManyToManyField(Supplier, blank=True)
    
    # Recommendations
    recommended_actions = models.JSONField(default=list)
    estimated_cost_impact = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Status and Resolution
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Notifications
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Risk Alert"
        verbose_name_plural = "Risk Alerts"
        ordering = ['-created_at', '-risk_score']
    
    def __str__(self):
        return f"{self.title} ({self.status})"


class AIModelPerformance(models.Model):
    """Track AI model performance metrics"""
    
    MODEL_TYPE_CHOICES = [
        ('demand_forecasting', 'Demand Forecasting'),
        ('dynamic_pricing', 'Dynamic Pricing'),
        ('route_optimization', 'Route Optimization'),
        ('risk_prediction', 'Risk Prediction'),
    ]
    
    model_type = models.CharField(max_length=30, choices=MODEL_TYPE_CHOICES)
    model_version = models.CharField(max_length=20)
    
    # Performance Metrics
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=3)
    precision_score = models.DecimalField(max_digits=5, decimal_places=3)
    recall_score = models.DecimalField(max_digits=5, decimal_places=3)
    f1_score = models.DecimalField(max_digits=5, decimal_places=3)
    
    # Training Information
    training_data_size = models.IntegerField()
    training_duration_minutes = models.DecimalField(max_digits=8, decimal_places=2)
    last_trained = models.DateTimeField()
    
    # Business Impact
    cost_savings_generated = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    revenue_impact = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    # Model Configuration
    hyperparameters = models.JSONField(default=dict)
    feature_importance = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "AI Model Performance"
        verbose_name_plural = "AI Model Performance"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.model_type} v{self.model_version} - Accuracy: {self.accuracy_score}"
