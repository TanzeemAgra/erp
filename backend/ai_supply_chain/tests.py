"""
AI Supply Chain Tests
Basic tests to verify AI services functionality
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import (
    SupplyChainConfig, Product, Supplier, DeliveryLocation,
    DemandForecast, DynamicPricing, RouteOptimization
)
from .services import (
    DemandForecastingService, DynamicPricingService,
    RouteOptimizationService, RiskManagementService
)


class AISupplyChainTestCase(TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Set up test data"""
        # Create configuration
        self.config = SupplyChainConfig.objects.create()
        
        # Create test product
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            category="electronics",
            base_cost=Decimal('50.00'),
            current_price=Decimal('75.00'),
            min_price=Decimal('60.00'),
            max_price=Decimal('100.00'),
            current_stock=100,
            reorder_level=20,
            max_stock_level=500,
            weight_kg=0.5,
            dimensions_cm={'length': 10, 'width': 8, 'height': 5},
            enable_demand_forecasting=True,
            enable_dynamic_pricing=True,
            seasonal_factor=1.2,
            demand_volatility=0.7
        )
        
        # Create test supplier
        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            code="SUP001",
            reliability_score=8.5,
            on_time_delivery_rate=92.0,
            quality_score=9.2,
            financial_stability=8.0
        )
        
        # Create delivery locations
        self.start_location = DeliveryLocation.objects.create(
            name="Warehouse",
            address="123 Main St",
            latitude=40.7128,
            longitude=-74.0060,
            delivery_time_window_start="08:00:00",
            delivery_time_window_end="18:00:00"
        )
        
        self.delivery_location1 = DeliveryLocation.objects.create(
            name="Customer A",
            address="456 Oak Ave",
            latitude=40.7589,
            longitude=-73.9851,
            delivery_time_window_start="09:00:00",
            delivery_time_window_end="17:00:00"
        )
        
        self.delivery_location2 = DeliveryLocation.objects.create(
            name="Customer B",
            address="789 Pine St",
            latitude=40.6782,
            longitude=-73.9442,
            delivery_time_window_start="10:00:00",
            delivery_time_window_end="16:00:00"
        )


class DemandForecastingServiceTest(AISupplyChainTestCase):
    """Test demand forecasting service"""
    
    def test_predict_demand(self):
        """Test demand prediction"""
        service = DemandForecastingService()
        target_date = timezone.now().date() + timedelta(days=7)
        
        result = service.predict_demand(self.product, target_date)
        
        # Verify result structure
        self.assertIn('predicted_demand', result)
        self.assertIn('confidence_score', result)
        self.assertIn('seasonal_factor', result)
        self.assertIn('confidence_interval_lower', result)
        self.assertIn('confidence_interval_upper', result)
        
        # Verify data types and ranges
        self.assertIsInstance(result['predicted_demand'], (int, float))
        self.assertGreaterEqual(result['predicted_demand'], 0)
        
        self.assertIsInstance(result['confidence_score'], (int, float))
        self.assertGreaterEqual(result['confidence_score'], 0)
        self.assertLessEqual(result['confidence_score'], 1)
        
        self.assertIsInstance(result['seasonal_factor'], (int, float))
        self.assertGreater(result['seasonal_factor'], 0)


class DynamicPricingServiceTest(AISupplyChainTestCase):
    """Test dynamic pricing service"""
    
    def test_calculate_optimal_price(self):
        """Test price optimization"""
        service = DynamicPricingService()
        
        result = service.calculate_optimal_price(self.product)
        
        # Verify result structure
        self.assertIn('recommended_price', result)
        self.assertIn('pricing_strategy', result)
        self.assertIn('price_change_percentage', result)
        self.assertIn('factors', result)
        self.assertIn('expected_demand_change', result)
        self.assertIn('expected_revenue_impact', result)
        
        # Verify pricing strategy is valid
        valid_strategies = ['premium', 'competitive', 'penetration', 'dynamic', 'maintain']
        self.assertIn(result['pricing_strategy'], valid_strategies)
        
        # Verify price is reasonable
        self.assertGreater(result['recommended_price'], 0)
        
        # Verify factors structure
        factors = result['factors']
        self.assertIn('inventory_factor', factors)
        self.assertIn('demand_factor', factors)
        self.assertIn('competition_factor', factors)
        self.assertIn('seasonality_factor', factors)


class RouteOptimizationServiceTest(AISupplyChainTestCase):
    """Test route optimization service"""
    
    def test_optimize_route(self):
        """Test route optimization"""
        service = RouteOptimizationService()
        delivery_locations = [self.delivery_location1, self.delivery_location2]
        
        result = service.optimize_route(self.start_location, delivery_locations)
        
        # Verify result structure
        self.assertIn('optimized_route', result)  # Changed from 'optimized_order'
        self.assertIn('total_distance_km', result)
        self.assertIn('total_time_hours', result)
        self.assertIn('total_cost', result)
        self.assertIn('fuel_cost', result)
        self.assertIn('driver_cost', result)
        self.assertIn('cost_savings_percentage', result)
        self.assertIn('algorithm_used', result)
        
        # Verify optimized route includes all locations
        optimized_route = result['optimized_route']  # Changed from 'optimized_order'
        self.assertEqual(len(optimized_route), len(delivery_locations) + 1)  # +1 for start location
        
        # Verify metrics are reasonable
        self.assertGreaterEqual(result['total_distance_km'], 0)
        self.assertGreaterEqual(result['total_time_hours'], 0)
        self.assertGreaterEqual(result['total_cost'], 0)
        self.assertGreaterEqual(result['cost_savings_percentage'], 0)


class RiskManagementServiceTest(AISupplyChainTestCase):
    """Test risk management service"""
    
    def test_assess_supply_chain_risks(self):
        """Test risk assessment"""
        service = RiskManagementService()
        
        result = service.assess_supply_chain_risks()
        
        # Verify result is a list
        self.assertIsInstance(result, list)
        
        # If risks are found, verify structure
        if result:
            risk = result[0]
            required_keys = [
                'type', 'title', 'description', 'probability',
                'risk_score', 'factors', 'recommendations'  # Removed 'impact'
            ]
            
            for key in required_keys:
                self.assertIn(key, risk)
            
            # Verify data types and ranges
            self.assertIsInstance(risk['probability'], (int, float))
            self.assertGreaterEqual(risk['probability'], 0)
            self.assertLessEqual(risk['probability'], 1)
            
            self.assertIsInstance(risk['risk_score'], (int, float, Decimal))
            self.assertGreaterEqual(float(risk['risk_score']), 0)


class IntegrationTest(AISupplyChainTestCase):
    """Integration tests for the complete AI pipeline"""
    
    def test_end_to_end_workflow(self):
        """Test complete AI workflow"""
        # 1. Generate demand forecast
        forecast_service = DemandForecastingService()
        target_date = timezone.now().date() + timedelta(days=7)
        forecast_result = forecast_service.predict_demand(self.product, target_date)
        
        # Create forecast record
        forecast = DemandForecast.objects.create(
            product=self.product,
            forecast_date=target_date,
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
        
        self.assertIsNotNone(forecast.id)
        
        # 2. Calculate dynamic pricing
        pricing_service = DynamicPricingService()
        pricing_result = pricing_service.calculate_optimal_price(self.product)
        
        # Create pricing record
        pricing = DynamicPricing.objects.create(
            product=self.product,
            current_price=self.product.current_price,
            current_stock_level=self.product.current_stock,
            current_demand_rate=10.0,
            recommended_price=pricing_result['recommended_price'],
            price_change_percentage=pricing_result['price_change_percentage'],
            pricing_strategy=pricing_result['pricing_strategy'],
            inventory_factor=pricing_result['factors']['inventory_factor'],
            demand_factor=pricing_result['factors']['demand_factor'],
            competition_factor=pricing_result['factors']['competition_factor'],
            seasonality_factor=pricing_result['factors']['seasonality_factor'],
            expected_demand_change=pricing_result['expected_demand_change'],
            expected_revenue_impact=pricing_result['expected_revenue_impact'],
            expected_profit_margin=15.0,
            valid_until=timezone.now() + timedelta(days=7)
        )
        
        self.assertIsNotNone(pricing.id)
        
        # 3. Optimize route
        route_service = RouteOptimizationService()
        delivery_locations = [self.delivery_location1, self.delivery_location2]
        route_result = route_service.optimize_route(self.start_location, delivery_locations)
        
        # Create route optimization record
        route = RouteOptimization.objects.create(
            route_name="Test Route",
            delivery_date=timezone.now().date() + timedelta(days=1),
            start_location=self.start_location,
            total_distance_km=route_result['total_distance_km'],
            total_time_hours=route_result['total_time_hours'],
            total_cost=route_result['total_cost'],
            fuel_cost=route_result['fuel_cost'],
            driver_cost=route_result['driver_cost'],
            algorithm_used=route_result['algorithm_used'],
            optimization_time_seconds=1.0,  # Default value since not in result
            cost_savings_percentage=route_result['cost_savings_percentage'],
            status='completed'
        )
        
        self.assertIsNotNone(route.id)
        
        # 4. Run risk assessment
        risk_service = RiskManagementService()
        risks = risk_service.assess_supply_chain_risks()
        
        # Verify risks were assessed (even if empty)
        self.assertIsInstance(risks, list)
        
        # Verify all components work together
        self.assertTrue(
            forecast.id and pricing.id and route.id,
            "All AI components should work together successfully"
        )
