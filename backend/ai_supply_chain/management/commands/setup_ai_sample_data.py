"""
Management command to set up sample AI Supply Chain data
Usage: python manage.py setup_ai_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from ai_supply_chain.models import (
    SupplyChainConfig, Product, Supplier, DeliveryLocation,
    AIModelPerformance
)


class Command(BaseCommand):
    help = 'Set up sample data for AI Supply Chain demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all AI Supply Chain data before creating sample data',
        )

    def handle(self, *args, **options):
        self.stdout.write('Setting up AI Supply Chain sample data...')

        if options['reset']:
            self.stdout.write('Resetting existing data...')
            # Clear existing data
            Product.objects.filter(enable_demand_forecasting=True).delete()
            Supplier.objects.all().delete()
            DeliveryLocation.objects.all().delete()
            AIModelPerformance.objects.all().delete()
            SupplyChainConfig.objects.all().delete()

        # Create or get AI configuration
        config, created = SupplyChainConfig.objects.get_or_create(
            id=1,
            defaults={
                'demand_forecasting_enabled': True,
                'dynamic_pricing_enabled': True,
                'route_optimization_enabled': True,
                'risk_management_enabled': True,
                'forecasting_horizon_days': 30,
                'seasonal_adjustment_factor': 1.2,
                'demand_sensitivity': 0.8,
                'min_profit_margin': 0.15,
                'max_price_adjustment': 0.25,
                'competitor_weight': 0.3,
                'market_weight': 0.4,
                'inventory_weight': 0.3,
                'fuel_cost_per_km': 1.5,
                'driver_cost_per_hour': 25.0,
                'vehicle_capacity_kg': 1000.0,
                'max_delivery_distance_km': 500.0,
                'risk_threshold_high': 8.0,
                'risk_threshold_medium': 5.0,
                'alert_notification_enabled': True,
                'ai_model_update_frequency_hours': 24,
                'data_retention_days': 365
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Created AI Supply Chain configuration')
            )
        else:
            self.stdout.write(
                self.style.WARNING('! AI Supply Chain configuration already exists')
            )

        # Create sample products with AI features enabled
        sample_products = [
            {
                'name': 'Wireless Bluetooth Headphones',
                'sku': 'WBH001',
                'category': 'electronics',
                'base_cost': Decimal('45.00'),
                'current_price': Decimal('89.99'),
                'current_stock': 150,
                'reorder_level': 25,
                'max_stock_level': 500,
                'weight_kg': 0.3,
                'seasonal_factor': 1.4,  # Higher demand in holidays
                'demand_volatility': 0.7
            },
            {
                'name': 'Smart Fitness Tracker',
                'sku': 'SFT002',
                'category': 'electronics',
                'base_cost': Decimal('65.00'),
                'current_price': Decimal('129.99'),
                'current_stock': 80,
                'reorder_level': 15,
                'max_stock_level': 300,
                'weight_kg': 0.15,
                'seasonal_factor': 1.6,  # High demand in January (fitness resolutions)
                'demand_volatility': 0.9
            },
            {
                'name': 'Ergonomic Office Chair',
                'sku': 'EOC003',
                'category': 'furniture',
                'base_cost': Decimal('120.00'),
                'current_price': Decimal('249.99'),
                'current_stock': 40,
                'reorder_level': 8,
                'max_stock_level': 100,
                'weight_kg': 15.5,
                'seasonal_factor': 1.1,  # Steady demand
                'demand_volatility': 0.4
            },
            {
                'name': 'Premium Coffee Beans (1kg)',
                'sku': 'PCB004',
                'category': 'food',
                'base_cost': Decimal('12.00'),
                'current_price': Decimal('24.99'),
                'current_stock': 200,
                'reorder_level': 50,
                'max_stock_level': 800,
                'weight_kg': 1.0,
                'seasonal_factor': 1.3,  # Higher in winter
                'demand_volatility': 0.5
            },
            {
                'name': 'Organic Cotton T-Shirt',
                'sku': 'OCT005',
                'category': 'clothing',
                'base_cost': Decimal('8.00'),
                'current_price': Decimal('19.99'),
                'current_stock': 120,
                'reorder_level': 30,
                'max_stock_level': 400,
                'weight_kg': 0.2,
                'seasonal_factor': 1.2,  # Higher in summer
                'demand_volatility': 0.8
            }
        ]

        created_products = 0
        for product_data in sample_products:
            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    **product_data,
                    'enable_demand_forecasting': True,
                    'enable_dynamic_pricing': True,
                    'min_price': product_data['current_price'] * Decimal('0.7'),
                    'max_price': product_data['current_price'] * Decimal('1.5'),
                    'dimensions_cm': {'length': 10, 'width': 10, 'height': 10}
                }
            )
            if created:
                created_products += 1

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {created_products} sample products')
        )

        # Create sample suppliers
        sample_suppliers = [
            {
                'name': 'TechSupply Global',
                'code': 'TSG001',
                'contact_person': 'Sarah Johnson',
                'email': 'sarah@techsupply.com',
                'phone': '+1-555-0101',
                'address': '123 Tech Street',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'USA',
                'postal_code': '94102',
                'reliability_score': 9.2,
                'avg_delivery_time_days': 3,
                'on_time_delivery_rate': 96.5,
                'quality_score': 9.1,
                'financial_stability': 8.8,
                'geographic_risk': 2.1,
                'payment_terms_days': 30,
                'minimum_order_value': Decimal('500.00')
            },
            {
                'name': 'EcoFriendly Materials Co.',
                'code': 'EFM002',
                'contact_person': 'Mike Chen',
                'email': 'mike@ecofriendly.com',
                'phone': '+1-555-0202',
                'address': '456 Green Avenue',
                'city': 'Portland',
                'state': 'OR',
                'country': 'USA',
                'postal_code': '97201',
                'reliability_score': 8.7,
                'avg_delivery_time_days': 5,
                'on_time_delivery_rate': 92.3,
                'quality_score': 9.5,
                'financial_stability': 8.2,
                'geographic_risk': 1.8,
                'payment_terms_days': 45,
                'minimum_order_value': Decimal('300.00')
            },
            {
                'name': 'Global Logistics Partners',
                'code': 'GLP003',
                'contact_person': 'Emma Davis',
                'email': 'emma@globallogistics.com',
                'phone': '+1-555-0303',
                'address': '789 Shipping Boulevard',
                'city': 'Miami',
                'state': 'FL',
                'country': 'USA',
                'postal_code': '33101',
                'reliability_score': 8.9,
                'avg_delivery_time_days': 4,
                'on_time_delivery_rate': 94.8,
                'quality_score': 8.6,
                'financial_stability': 9.1,
                'geographic_risk': 2.5,
                'payment_terms_days': 30,
                'minimum_order_value': Decimal('1000.00')
            }
        ]

        created_suppliers = 0
        for supplier_data in sample_suppliers:
            supplier, created = Supplier.objects.get_or_create(
                code=supplier_data['code'],
                defaults=supplier_data
            )
            if created:
                created_suppliers += 1

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {created_suppliers} sample suppliers')
        )

        # Create sample delivery locations
        sample_locations = [
            {
                'name': 'Main Warehouse',
                'address': '100 Industrial Drive, Newark, NJ 07102',
                'latitude': 40.7282,
                'longitude': -74.1776,
                'delivery_time_window_start': '08:00:00',
                'delivery_time_window_end': '18:00:00',
                'access_difficulty_score': 1
            },
            {
                'name': 'Downtown Store',
                'address': '250 Broadway, New York, NY 10007',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'delivery_time_window_start': '10:00:00',
                'delivery_time_window_end': '16:00:00',
                'access_difficulty_score': 8
            },
            {
                'name': 'Suburban Mall Location',
                'address': '500 Mall Drive, Paramus, NJ 07652',
                'latitude': 40.9176,
                'longitude': -74.0685,
                'delivery_time_window_start': '09:00:00',
                'delivery_time_window_end': '17:00:00',
                'access_difficulty_score': 3
            },
            {
                'name': 'Office Complex',
                'address': '1000 Corporate Blvd, Jersey City, NJ 07302',
                'latitude': 40.7178,
                'longitude': -74.0431,
                'delivery_time_window_start': '08:30:00',
                'delivery_time_window_end': '17:30:00',
                'access_difficulty_score': 4
            },
            {
                'name': 'University Campus',
                'address': '300 University Ave, Princeton, NJ 08544',
                'latitude': 40.3573,
                'longitude': -74.6672,
                'delivery_time_window_start': '10:00:00',
                'delivery_time_window_end': '15:00:00',
                'access_difficulty_score': 5
            }
        ]

        created_locations = 0
        for location_data in sample_locations:
            location, created = DeliveryLocation.objects.get_or_create(
                name=location_data['name'],
                defaults=location_data
            )
            if created:
                created_locations += 1

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {created_locations} sample delivery locations')
        )

        # Create AI model performance records
        ai_models = [
            {
                'model_type': 'demand_forecasting',
                'model_version': '1.0',
                'accuracy_score': 0.87,
                'precision_score': 0.84,
                'recall_score': 0.89,
                'f1_score': 0.86,
                'training_data_size': 10000,
                'training_duration_minutes': 45,
                'last_trained': timezone.now() - timedelta(days=2),
                'cost_savings_generated': Decimal('25000.00'),
                'revenue_impact': Decimal('75000.00'),
                'hyperparameters': {
                    'n_estimators': 100,
                    'max_depth': 10,
                    'learning_rate': 0.1
                },
                'feature_importance': {
                    'historical_demand': 0.35,
                    'seasonality': 0.25,
                    'price': 0.15,
                    'promotions': 0.12,
                    'external_factors': 0.13
                }
            },
            {
                'model_type': 'dynamic_pricing',
                'model_version': '1.0',
                'accuracy_score': 0.82,
                'precision_score': 0.80,
                'recall_score': 0.85,
                'f1_score': 0.82,
                'training_data_size': 8500,
                'training_duration_minutes': 30,
                'last_trained': timezone.now() - timedelta(days=1),
                'cost_savings_generated': Decimal('18000.00'),
                'revenue_impact': Decimal('95000.00'),
                'hyperparameters': {
                    'penalty': 'l2',
                    'C': 1.0,
                    'solver': 'liblinear'
                },
                'feature_importance': {
                    'inventory_level': 0.30,
                    'demand_trend': 0.25,
                    'competitor_price': 0.20,
                    'seasonality': 0.15,
                    'cost': 0.10
                }
            },
            {
                'model_type': 'route_optimization',
                'model_version': '1.0',
                'accuracy_score': 0.92,
                'precision_score': 0.91,
                'recall_score': 0.93,
                'f1_score': 0.92,
                'training_data_size': 5000,
                'training_duration_minutes': 20,
                'last_trained': timezone.now() - timedelta(days=3),
                'cost_savings_generated': Decimal('32000.00'),
                'revenue_impact': Decimal('15000.00'),
                'hyperparameters': {
                    'population_size': 100,
                    'generations': 500,
                    'mutation_rate': 0.1
                },
                'feature_importance': {
                    'distance': 0.40,
                    'traffic_conditions': 0.25,
                    'delivery_windows': 0.20,
                    'vehicle_capacity': 0.15
                }
            },
            {
                'model_type': 'risk_management',
                'model_version': '1.0',
                'accuracy_score': 0.79,
                'precision_score': 0.76,
                'recall_score': 0.83,
                'f1_score': 0.79,
                'training_data_size': 3000,
                'training_duration_minutes': 15,
                'last_trained': timezone.now() - timedelta(days=5),
                'cost_savings_generated': Decimal('45000.00'),
                'revenue_impact': Decimal('120000.00'),
                'hyperparameters': {
                    'threshold': 0.5,
                    'weights': 'balanced'
                },
                'feature_importance': {
                    'supplier_reliability': 0.35,
                    'financial_indicators': 0.25,
                    'geographic_factors': 0.20,
                    'market_conditions': 0.20
                }
            }
        ]

        created_models = 0
        for model_data in ai_models:
            model, created = AIModelPerformance.objects.get_or_create(
                model_type=model_data['model_type'],
                model_version=model_data['model_version'],
                defaults=model_data
            )
            if created:
                created_models += 1

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {created_models} AI model performance records')
        )

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 AI Supply Chain sample data setup complete!'))
        self.stdout.write('\nSample data created:')
        self.stdout.write(f'  • Products with AI features: {created_products}')
        self.stdout.write(f'  • Suppliers: {created_suppliers}')
        self.stdout.write(f'  • Delivery locations: {created_locations}')
        self.stdout.write(f'  • AI model records: {created_models}')
        self.stdout.write('\nNext steps:')
        self.stdout.write('  1. Access Django Admin: /admin/')
        self.stdout.write('  2. Navigate to "AI Supply Chain Optimization"')
        self.stdout.write('  3. Try the API endpoints: /api/v1/ai-supply-chain/')
        self.stdout.write('  4. Generate demand forecasts for products')
        self.stdout.write('  5. Calculate dynamic pricing recommendations')
        self.stdout.write('  6. Optimize delivery routes')
        self.stdout.write('  7. Run risk assessments')
        self.stdout.write('='*50)
