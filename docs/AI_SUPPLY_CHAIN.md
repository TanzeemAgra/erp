# AI Supply Chain Optimization System

## Overview

The AI Supply Chain Optimization system is a comprehensive machine learning-powered module that enhances your ERP system with intelligent supply chain management capabilities. It provides four core AI features: demand forecasting, dynamic pricing, route optimization, and risk management.

## Features

### 1. Demand Forecasting 🔮
- **AI-Powered Predictions**: Uses ensemble machine learning models (Random Forest + Gradient Boosting)
- **Multiple Time Horizons**: Daily, weekly, and monthly forecasts
- **Seasonal Adjustments**: Automatically detects and adjusts for seasonal patterns
- **Confidence Intervals**: Provides prediction confidence ranges
- **Accuracy Tracking**: Monitors and improves forecast accuracy over time

### 2. Dynamic Pricing 💰
- **Real-Time Price Optimization**: Adjusts prices based on multiple factors
- **Market Analysis**: Considers competitor prices and market conditions
- **Inventory-Based Pricing**: Adjusts based on stock levels and demand
- **Strategy Selection**: Supports premium, competitive, penetration, and dynamic strategies
- **Revenue Impact Prediction**: Estimates financial impact of price changes

### 3. Route Optimization 🚚
- **AI-Powered Routing**: Uses genetic algorithms for optimal delivery routes
- **Cost Minimization**: Optimizes for fuel costs, time, and operational efficiency
- **Multi-Stop Planning**: Handles complex multi-destination deliveries
- **Real-Time Adjustments**: Adapts to traffic and delivery constraints
- **Environmental Impact**: Tracks and minimizes carbon footprint

### 4. Risk Management ⚠️
- **Predictive Risk Assessment**: Identifies potential supply chain disruptions
- **Multi-Factor Analysis**: Considers supplier reliability, market conditions, and external factors
- **Automated Alerts**: Real-time notifications for high-risk situations
- **Mitigation Strategies**: AI-recommended actions for risk reduction
- **Continuous Monitoring**: 24/7 risk assessment and alerting

## Architecture

### Database Models

#### Core Configuration
- **SupplyChainConfig**: Central configuration for all AI features
- **AIModelPerformance**: Tracks ML model performance and metrics

#### Master Data
- **Product**: Enhanced product data with AI optimization flags
- **Supplier**: Supplier information with performance and risk metrics
- **DeliveryLocation**: Geographic locations for route optimization

#### AI-Generated Data
- **DemandForecast**: AI-generated demand predictions
- **DynamicPricing**: Price optimization recommendations
- **RouteOptimization**: Optimized delivery routes
- **RiskAlert**: AI-identified risk scenarios

### AI Services

#### DemandForecastingService
```python
# Generate demand forecasts
forecast_service = DemandForecastingService()
result = forecast_service.predict_demand(product, target_date)
```

#### DynamicPricingService
```python
# Calculate optimal pricing
pricing_service = DynamicPricingService()
result = pricing_service.calculate_optimal_price(product)
```

#### RouteOptimizationService
```python
# Optimize delivery routes
route_service = RouteOptimizationService()
result = route_service.optimize_route(start_location, delivery_locations)
```

#### RiskManagementService
```python
# Assess supply chain risks
risk_service = RiskManagementService()
risks = risk_service.assess_supply_chain_risks()
```

## API Endpoints

### Configuration
```
GET/PUT/PATCH /api/v1/ai-supply-chain/config/
GET /api/v1/ai-supply-chain/config/active_config/
```

### Products & Demand Forecasting
```
GET/POST /api/v1/ai-supply-chain/products/
POST /api/v1/ai-supply-chain/products/{id}/generate_demand_forecast/
GET /api/v1/ai-supply-chain/products/analytics/
GET /api/v1/ai-supply-chain/demand-forecasts/
GET /api/v1/ai-supply-chain/demand-forecasts/accuracy_report/
```

### Dynamic Pricing
```
POST /api/v1/ai-supply-chain/products/{id}/calculate_dynamic_pricing/
GET /api/v1/ai-supply-chain/dynamic-pricing/
POST /api/v1/ai-supply-chain/dynamic-pricing/{id}/apply_pricing/
GET /api/v1/ai-supply-chain/dynamic-pricing/revenue_impact_report/
```

### Route Optimization
```
GET/POST /api/v1/ai-supply-chain/route-optimization/
POST /api/v1/ai-supply-chain/route-optimization/optimize_route/
POST /api/v1/ai-supply-chain/route-optimization/{id}/implement_route/
GET /api/v1/ai-supply-chain/route-optimization/savings_report/
```

### Risk Management
```
GET/POST /api/v1/ai-supply-chain/risk-alerts/
POST /api/v1/ai-supply-chain/risk-alerts/run_risk_assessment/
POST /api/v1/ai-supply-chain/risk-alerts/{id}/resolve_alert/
```

### AI Model Performance
```
GET /api/v1/ai-supply-chain/ai-models/
GET /api/v1/ai-supply-chain/ai-models/dashboard_summary/
```

## Installation & Setup

### 1. Install Dependencies
```bash
# Core ML dependencies
pip install -r requirements_ai.txt

# Or install individually:
pip install scikit-learn numpy pandas scipy matplotlib seaborn
pip install networkx geopy requests statsmodels
```

### 2. Database Migration
```bash
python manage.py makemigrations ai_supply_chain
python manage.py migrate
```

### 3. Configuration
1. Access Django Admin: `/admin/`
2. Navigate to "AI Supply Chain Optimization"
3. Configure "Supply Chain Configs" with your parameters
4. Set up Products and Suppliers with AI optimization enabled

### 4. Start Using AI Features
1. Enable AI features for products in the admin interface
2. Use the API endpoints to generate forecasts, optimize pricing, etc.
3. Monitor performance through the AI Models dashboard

## Usage Examples

### Enable Demand Forecasting for a Product
```python
# Via Django Admin or API
product = Product.objects.get(sku='PROD001')
product.enable_demand_forecasting = True
product.save()

# Generate forecast
forecast_service = DemandForecastingService()
result = forecast_service.predict_demand(product, target_date)
```

### Generate Dynamic Pricing Recommendation
```python
# Via API
POST /api/v1/ai-supply-chain/products/1/calculate_dynamic_pricing/
{
    "market_conditions": {"demand_trend": "increasing"},
    "competitor_prices": [{"competitor": "A", "price": 99.99}]
}
```

### Optimize Delivery Route
```python
# Via API
POST /api/v1/ai-supply-chain/route-optimization/optimize_route/
{
    "delivery_locations": [1, 2, 3, 4],
    "start_location_id": 1,
    "delivery_date": "2024-01-15",
    "vehicle_capacity_kg": 1000
}
```

### Run Risk Assessment
```python
# Via API
POST /api/v1/ai-supply-chain/risk-alerts/run_risk_assessment/
{
    "assessment_type": "comprehensive",
    "risk_threshold": 6.0
}
```

## Configuration Options

### AI Features Toggle
- `demand_forecasting_enabled`: Enable/disable demand forecasting
- `dynamic_pricing_enabled`: Enable/disable dynamic pricing
- `route_optimization_enabled`: Enable/disable route optimization
- `risk_management_enabled`: Enable/disable risk management

### Forecasting Parameters
- `forecasting_horizon_days`: Default forecast horizon (30 days)
- `seasonal_adjustment_factor`: Seasonal adjustment strength (1.2)
- `demand_sensitivity`: Demand sensitivity factor (0.8)

### Pricing Parameters
- `min_profit_margin`: Minimum allowed profit margin (0.15)
- `max_price_adjustment`: Maximum price change percentage (0.25)
- `competitor_weight`: Weight for competitor analysis (0.3)
- `market_weight`: Weight for market conditions (0.4)
- `inventory_weight`: Weight for inventory levels (0.3)

### Route Optimization Parameters
- `fuel_cost_per_km`: Fuel cost calculation (1.5)
- `driver_cost_per_hour`: Driver cost calculation (25.0)
- `vehicle_capacity_kg`: Default vehicle capacity (1000)
- `max_delivery_distance_km`: Maximum delivery distance (500)

### Risk Management Parameters
- `risk_threshold_high`: High risk threshold (8.0)
- `risk_threshold_medium`: Medium risk threshold (5.0)
- `alert_notification_enabled`: Enable risk notifications (True)

## Monitoring & Analytics

### Key Metrics Tracked
- **Forecast Accuracy**: MAPE, RMSE, confidence intervals
- **Pricing Performance**: Revenue impact, adoption rates
- **Route Efficiency**: Cost savings, time optimization
- **Risk Detection**: Alert accuracy, false positive rates

### Dashboard Features
- Real-time AI model performance
- Cost savings and revenue impact
- Operational efficiency metrics
- Risk assessment summaries

### Performance Optimization
- Model retraining recommendations
- Data quality assessments
- Algorithm performance comparisons
- Resource utilization tracking

## Security & Compliance

### Data Protection
- All sensitive data is encrypted at rest
- API endpoints require authentication
- Audit trails for all AI decisions
- GDPR-compliant data handling

### Model Governance
- Version control for all AI models
- Explainable AI for transparency
- Regular model validation
- Bias detection and mitigation

## Troubleshooting

### Common Issues

#### 1. Low Forecast Accuracy
- **Cause**: Insufficient historical data
- **Solution**: Accumulate more data or adjust model parameters

#### 2. Pricing Recommendations Not Applied
- **Cause**: Price change exceeds maximum allowed adjustment
- **Solution**: Adjust `max_price_adjustment` in configuration

#### 3. Route Optimization Fails
- **Cause**: Invalid delivery locations or constraints
- **Solution**: Verify location data and capacity constraints

#### 4. Risk Alerts Not Generated
- **Cause**: Risk threshold too high
- **Solution**: Lower `risk_threshold` in configuration

### Getting Help
- Check Django logs for detailed error messages
- Review AI model performance metrics
- Contact support with specific error codes

## Roadmap

### Upcoming Features
- **Deep Learning Models**: Advanced neural networks for complex patterns
- **Real-Time Integration**: Live market data and traffic conditions
- **Multi-Language Support**: Internationalization for global operations
- **Advanced Reporting**: Comprehensive business intelligence dashboards
- **Mobile App Integration**: Native mobile app support
- **External API Integrations**: Third-party logistics and market data

### Performance Improvements
- Model serving optimization
- Distributed computing support
- Real-time streaming analytics
- Edge computing capabilities

---

**Note**: This AI Supply Chain Optimization system is designed to be production-ready while maintaining the flexibility to adapt to your specific business needs. All algorithms are optimized for performance and scalability.
