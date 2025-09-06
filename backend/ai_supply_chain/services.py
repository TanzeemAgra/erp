"""
AI Supply Chain Services
Core AI algorithms for supply chain optimization
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Tuple, Optional
from django.conf import settings
from django.utils import timezone
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import logging
import requests
from decouple import config

logger = logging.getLogger(__name__)


def get_seasonal_factor(product, month=None):
    """
    Helper function to safely get seasonal factor from product
    """
    if month is None:
        month = timezone.now().month
    
    if hasattr(product, 'seasonal_factor') and product.seasonal_factor:
        if isinstance(product.seasonal_factor, dict):
            return float(product.seasonal_factor.get(str(month), 1.0))
        else:
            # If seasonal_factor is a simple float, use it directly
            return float(product.seasonal_factor)
    return 1.0

class DemandForecastingService:
    """AI-powered demand forecasting using multiple algorithms"""
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear_regression': LinearRegression()
        }
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, product, historical_data: List[Dict]) -> np.ndarray:
        """Prepare features for demand forecasting"""
        try:
            features = []
            
            for data_point in historical_data:
                feature_vector = [
                    data_point.get('month', 1),  # Seasonality
                    data_point.get('week_of_year', 1),
                    data_point.get('day_of_week', 1),
                    data_point.get('price', product.current_price),
                    data_point.get('stock_level', product.current_stock),
                    data_point.get('promotion_active', 0),  # 1 if promotion, 0 otherwise
                    data_point.get('competitor_price', product.current_price * 1.1),
                    data_point.get('economic_indicator', 1.0),  # Economic index
                    data_point.get('weather_factor', 1.0),  # Weather impact if applicable
                    float(product.seasonal_factor.get(str(data_point.get('month', 1)), 1.0))
                ]
                features.append(feature_vector)
            
            return np.array(features)
        
        except Exception as e:
            logger.error(f"Error preparing features for demand forecasting: {e}")
            return np.array([])
    
    def train_models(self, product, historical_sales_data: List[Dict]):
        """Train demand forecasting models"""
        try:
            if len(historical_sales_data) < 30:  # Need minimum data points
                logger.warning(f"Insufficient data for training demand forecast for {product.name}")
                return False
            
            # Prepare features and target
            X = self.prepare_features(product, historical_sales_data)
            y = np.array([data['demand'] for data in historical_sales_data])
            
            if X.size == 0 or len(y) == 0:
                return False
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train each model
            for model_name, model in self.models.items():
                try:
                    model.fit(X_scaled, y)
                    logger.info(f"Trained {model_name} for product {product.name}")
                except Exception as e:
                    logger.error(f"Error training {model_name}: {e}")
            
            self.is_trained = True
            return True
        
        except Exception as e:
            logger.error(f"Error training demand forecasting models: {e}")
            return False
    
    def predict_demand(self, product, forecast_date: datetime, external_factors: Dict = None) -> Dict:
        """Predict demand for a specific date"""
        try:
            if not self.is_trained:
                logger.warning("Models not trained. Using fallback prediction.")
                return self._fallback_prediction(product, forecast_date)
            
            # Prepare features for prediction
            if external_factors is None:
                external_factors = {}
            
            feature_vector = np.array([[
                forecast_date.month,
                forecast_date.isocalendar()[1],  # Week of year
                forecast_date.weekday(),
                float(external_factors.get('price', product.current_price)),
                float(external_factors.get('stock_level', product.current_stock)),
                external_factors.get('promotion_active', 0),
                float(external_factors.get('competitor_price', product.current_price * 1.1)),
                external_factors.get('economic_indicator', 1.0),
                external_factors.get('weather_factor', 1.0),
                float(product.seasonal_factor.get(str(forecast_date.month), 1.0))
            ]])
            
            # Scale features
            X_scaled = self.scaler.transform(feature_vector)
            
            # Get predictions from all models
            predictions = {}
            for model_name, model in self.models.items():
                try:
                    pred = model.predict(X_scaled)[0]
                    predictions[model_name] = max(0, int(pred))  # Ensure non-negative
                except Exception as e:
                    logger.error(f"Error predicting with {model_name}: {e}")
                    predictions[model_name] = 0
            
            # Ensemble prediction (weighted average)
            weights = {'random_forest': 0.4, 'gradient_boost': 0.4, 'linear_regression': 0.2}
            ensemble_prediction = sum(predictions[model] * weights[model] for model in predictions)
            
            # Calculate confidence interval
            prediction_variance = np.var(list(predictions.values()))
            confidence_interval = int(np.sqrt(prediction_variance) * 1.96)  # 95% confidence
            
            return {
                'predicted_demand': int(ensemble_prediction),
                'confidence_interval_lower': max(0, int(ensemble_prediction - confidence_interval)),
                'confidence_interval_upper': int(ensemble_prediction + confidence_interval),
                'confidence_score': min(1.0, 1.0 - (prediction_variance / ensemble_prediction) if ensemble_prediction > 0 else 0.5),
                'model_predictions': predictions,
                'seasonal_factor': float(product.seasonal_factor.get(str(forecast_date.month), 1.0))
            }
        
        except Exception as e:
            logger.error(f"Error predicting demand: {e}")
            return self._fallback_prediction(product, forecast_date)
    
    def _fallback_prediction(self, product, forecast_date: datetime) -> Dict:
        """Fallback prediction when AI models fail"""
        # Simple moving average approach
        base_demand = max(1, product.current_stock // 30)  # Rough estimate
        # Calculate seasonal adjustment
        if hasattr(product, 'seasonal_factor') and product.seasonal_factor:
            if isinstance(product.seasonal_factor, dict):
                seasonal_factor = float(product.seasonal_factor.get(str(forecast_date.month), 1.0))
            else:
                # If seasonal_factor is a simple float, use it directly
                seasonal_factor = float(product.seasonal_factor)
        else:
            seasonal_factor = 1.0
        predicted_demand = int(base_demand * seasonal_factor)
        
        return {
            'predicted_demand': predicted_demand,
            'confidence_interval_lower': max(0, int(predicted_demand * 0.8)),
            'confidence_interval_upper': int(predicted_demand * 1.2),
            'confidence_score': 0.5,  # Low confidence for fallback
            'model_predictions': {'fallback': predicted_demand},
            'seasonal_factor': seasonal_factor
        }


class DynamicPricingService:
    """AI-driven dynamic pricing optimization"""
    
    def __init__(self):
        self.price_elasticity_models = {}
        self.competitor_data_cache = {}
    
    def calculate_optimal_price(self, product, market_conditions: Dict = None) -> Dict:
        """Calculate optimal price using AI algorithms"""
        try:
            if market_conditions is None:
                market_conditions = {}
            
            # Get current state
            current_price = float(product.current_price)
            current_stock = product.current_stock
            reorder_level = product.reorder_level
            max_stock = product.max_stock_level
            
            # Calculate factors
            inventory_factor = self._calculate_inventory_factor(current_stock, reorder_level, max_stock)
            demand_factor = self._calculate_demand_factor(product, market_conditions)
            competition_factor = self._calculate_competition_factor(product, market_conditions)
            seasonality_factor = self._get_seasonality_factor(product)
            
            # Get configuration
            from .models import SupplyChainConfig
            try:
                config = SupplyChainConfig.objects.first()
                if not config:
                    config = SupplyChainConfig.objects.create()
            except:
                # Fallback configuration
                config = type('Config', (), {
                    'min_profit_margin': Decimal('15.0'),
                    'max_price_adjustment': Decimal('20.0'),
                    'inventory_weight': Decimal('0.3'),
                    'market_weight': Decimal('0.4'),
                    'competitor_weight': Decimal('0.3')
                })()
            
            # Calculate weighted adjustment factor
            total_factor = (
                float(config.inventory_weight) * inventory_factor +
                float(config.market_weight) * demand_factor +
                float(config.competitor_weight) * competition_factor
            ) * seasonality_factor
            
            # Calculate price adjustment
            max_adjustment = float(config.max_price_adjustment) / 100
            price_adjustment = np.clip(total_factor - 1.0, -max_adjustment, max_adjustment)
            
            # Calculate new price
            new_price = current_price * (1 + price_adjustment)
            
            # Ensure minimum profit margin
            min_price = float(product.base_cost) * (1 + float(config.min_profit_margin) / 100)
            new_price = max(new_price, min_price)
            
            # Ensure within product limits
            new_price = np.clip(new_price, float(product.min_price), float(product.max_price))
            
            # Determine pricing strategy
            strategy = self._determine_pricing_strategy(inventory_factor, demand_factor, competition_factor)
            
            # Calculate expected impact
            expected_demand_change = self._estimate_demand_elasticity(product, price_adjustment)
            expected_revenue_impact = self._calculate_revenue_impact(current_price, new_price, expected_demand_change)
            
            return {
                'recommended_price': round(new_price, 2),
                'price_change_percentage': round(price_adjustment * 100, 2),
                'pricing_strategy': strategy,
                'factors': {
                    'inventory_factor': round(inventory_factor, 3),
                    'demand_factor': round(demand_factor, 3),
                    'competition_factor': round(competition_factor, 3),
                    'seasonality_factor': round(seasonality_factor, 3)
                },
                'expected_demand_change': round(expected_demand_change, 2),
                'expected_revenue_impact': round(expected_revenue_impact, 2),
                'confidence_score': self._calculate_pricing_confidence(product, market_conditions)
            }
        
        except Exception as e:
            logger.error(f"Error calculating optimal price: {e}")
            return self._fallback_pricing(product)
    
    def _calculate_inventory_factor(self, current_stock: int, reorder_level: int, max_stock: int) -> float:
        """Calculate inventory-based pricing factor"""
        if max_stock <= reorder_level:
            return 1.0
        
        stock_ratio = (current_stock - reorder_level) / (max_stock - reorder_level)
        stock_ratio = np.clip(stock_ratio, 0, 1)
        
        # Low stock = higher prices, high stock = lower prices
        return 1.2 - (stock_ratio * 0.4)
    
    def _calculate_demand_factor(self, product, market_conditions: Dict) -> float:
        """Calculate demand-based pricing factor"""
        # Simulate demand analysis (in real implementation, this would use actual demand data)
        demand_trend = market_conditions.get('demand_trend', 1.0)
        seasonal_demand = float(product.seasonal_factor.get(str(timezone.now().month), 1.0))
        
        return demand_trend * seasonal_demand
    
    def _calculate_competition_factor(self, product, market_conditions: Dict) -> float:
        """Calculate competition-based pricing factor"""
        competitor_price = market_conditions.get('competitor_avg_price')
        if not competitor_price:
            return 1.0
        
        current_price = float(product.current_price)
        price_ratio = current_price / competitor_price
        
        # If we're more expensive than competitors, suggest price reduction
        # If we're cheaper, we can potentially increase prices
        return 0.8 + (price_ratio * 0.4)
    
    def _get_seasonality_factor(self, product) -> float:
        """Get seasonality factor for current month"""
        current_month = timezone.now().month
        return float(product.seasonal_factor.get(str(current_month), 1.0))
    
    def _determine_pricing_strategy(self, inventory_factor: float, demand_factor: float, competition_factor: float) -> str:
        """Determine optimal pricing strategy"""
        if inventory_factor > 1.1:  # Low stock
            return 'inventory_based'
        elif demand_factor > 1.2:  # High demand
            return 'demand_based'
        elif competition_factor < 0.9:  # Competitors are cheaper
            return 'competitive'
        elif demand_factor < 0.8:  # Low demand
            return 'penetration'
        else:
            return 'premium'
    
    def _estimate_demand_elasticity(self, product, price_change: float) -> float:
        """Estimate demand change based on price elasticity"""
        # Price elasticity (simplified model)
        elasticity = float(product.demand_volatility) * -2.0  # Negative elasticity
        return elasticity * price_change * 100
    
    def _calculate_revenue_impact(self, old_price: float, new_price: float, demand_change: float) -> float:
        """Calculate expected revenue impact"""
        price_change_pct = (new_price - old_price) / old_price
        revenue_change_pct = price_change_pct + (demand_change / 100)
        return revenue_change_pct * 100
    
    def _calculate_pricing_confidence(self, product, market_conditions: Dict) -> float:
        """Calculate confidence score for pricing recommendation"""
        # Factors that affect confidence
        data_quality = 0.8  # Assume good data quality
        market_stability = market_conditions.get('market_stability', 0.7)
        competition_data_quality = 0.6 if market_conditions.get('competitor_avg_price') else 0.4
        
        return (data_quality + market_stability + competition_data_quality) / 3
    
    def _fallback_pricing(self, product) -> Dict:
        """Fallback pricing when AI calculation fails"""
        return {
            'recommended_price': float(product.current_price),
            'price_change_percentage': 0.0,
            'pricing_strategy': 'maintain',
            'factors': {
                'inventory_factor': 1.0,
                'demand_factor': 1.0,
                'competition_factor': 1.0,
                'seasonality_factor': 1.0
            },
            'expected_demand_change': 0.0,
            'expected_revenue_impact': 0.0,
            'confidence_score': 0.3
        }


class RouteOptimizationService:
    """AI-powered route optimization using advanced algorithms"""
    
    def __init__(self):
        self.earth_radius_km = 6371
    
    def optimize_route(self, start_location, delivery_locations: List, constraints: Dict = None) -> Dict:
        """Optimize delivery route using AI algorithms"""
        try:
            if not delivery_locations:
                return {'error': 'No delivery locations provided'}
            
            if constraints is None:
                constraints = {}
            
            # Calculate distance matrix
            distance_matrix = self._calculate_distance_matrix(start_location, delivery_locations)
            
            # Apply optimization algorithm
            if len(delivery_locations) <= 10:
                # Use exact algorithm for small problems
                optimized_route = self._branch_and_bound_tsp(distance_matrix)
            else:
                # Use heuristic for larger problems
                optimized_route = self._genetic_algorithm_tsp(distance_matrix)
            
            # Calculate route metrics
            route_metrics = self._calculate_route_metrics(
                start_location, delivery_locations, optimized_route, constraints
            )
            
            return {
                'optimized_route': optimized_route,
                'total_distance_km': route_metrics['total_distance'],
                'total_time_hours': route_metrics['total_time'],
                'total_cost': route_metrics['total_cost'],
                'fuel_cost': route_metrics['fuel_cost'],
                'driver_cost': route_metrics['driver_cost'],
                'cost_savings_percentage': route_metrics['cost_savings'],
                'algorithm_used': route_metrics['algorithm']
            }
        
        except Exception as e:
            logger.error(f"Error optimizing route: {e}")
            return {'error': str(e)}
    
    def _calculate_distance_matrix(self, start_location, delivery_locations: List) -> np.ndarray:
        """Calculate distance matrix between all locations"""
        all_locations = [start_location] + delivery_locations
        n = len(all_locations)
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = self._haversine_distance(
                        float(all_locations[i].latitude),
                        float(all_locations[i].longitude),
                        float(all_locations[j].latitude),
                        float(all_locations[j].longitude)
                    )
        
        return distance_matrix
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return self.earth_radius_km * c
    
    def _branch_and_bound_tsp(self, distance_matrix: np.ndarray) -> List[int]:
        """Solve TSP using branch and bound for small instances"""
        n = len(distance_matrix)
        if n <= 1:
            return list(range(n))
        
        # Simple nearest neighbor heuristic for now
        # In production, implement full branch and bound
        return self._nearest_neighbor_tsp(distance_matrix)
    
    def _genetic_algorithm_tsp(self, distance_matrix: np.ndarray, generations: int = 100) -> List[int]:
        """Solve TSP using genetic algorithm for larger instances"""
        n = len(distance_matrix)
        if n <= 1:
            return list(range(n))
        
        # Initialize population
        population_size = min(50, n * 2)
        population = []
        
        for _ in range(population_size):
            route = list(range(1, n))  # Exclude start location (index 0)
            np.random.shuffle(route)
            population.append([0] + route)  # Start from location 0
        
        best_route = None
        best_distance = float('inf')
        
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = []
            for route in population:
                distance = self._calculate_route_distance(distance_matrix, route)
                fitness_scores.append(1 / (1 + distance))  # Higher fitness for shorter routes
                
                if distance < best_distance:
                    best_distance = distance
                    best_route = route.copy()
            
            # Selection and crossover
            new_population = []
            for _ in range(population_size):
                parent1 = self._tournament_selection(population, fitness_scores)
                parent2 = self._tournament_selection(population, fitness_scores)
                child = self._order_crossover(parent1, parent2)
                
                # Mutation
                if np.random.random() < 0.1:  # 10% mutation rate
                    child = self._mutate_route(child)
                
                new_population.append(child)
            
            population = new_population
        
        return best_route if best_route else self._nearest_neighbor_tsp(distance_matrix)
    
    def _nearest_neighbor_tsp(self, distance_matrix: np.ndarray) -> List[int]:
        """Solve TSP using nearest neighbor heuristic"""
        n = len(distance_matrix)
        route = [0]  # Start from depot
        unvisited = set(range(1, n))
        
        current = 0
        while unvisited:
            nearest = min(unvisited, key=lambda x: distance_matrix[current][x])
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return route
    
    def _calculate_route_distance(self, distance_matrix: np.ndarray, route: List[int]) -> float:
        """Calculate total distance for a route"""
        total_distance = 0
        for i in range(len(route)):
            current = route[i]
            next_location = route[(i + 1) % len(route)]
            total_distance += distance_matrix[current][next_location]
        return total_distance
    
    def _tournament_selection(self, population: List, fitness_scores: List, tournament_size: int = 3) -> List[int]:
        """Tournament selection for genetic algorithm"""
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        return population[winner_index].copy()
    
    def _order_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """Order crossover for genetic algorithm"""
        if len(parent1) <= 2:
            return parent1.copy()
        
        start, end = sorted(np.random.choice(range(1, len(parent1)), 2, replace=False))
        child = [None] * len(parent1)
        child[0] = 0  # Always start from depot
        
        # Copy segment from parent1
        child[start:end] = parent1[start:end]
        
        # Fill remaining positions from parent2
        remaining = [x for x in parent2 if x not in child[start:end] and x != 0]
        j = 0
        for i in range(1, len(child)):
            if child[i] is None:
                child[i] = remaining[j]
                j += 1
        
        return child
    
    def _mutate_route(self, route: List[int]) -> List[int]:
        """Mutate route by swapping two random cities"""
        if len(route) <= 3:
            return route
        
        mutated = route.copy()
        i, j = np.random.choice(range(1, len(route)), 2, replace=False)
        mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated
    
    def _calculate_route_metrics(self, start_location, delivery_locations: List, 
                                optimized_route: List[int], constraints: Dict) -> Dict:
        """Calculate comprehensive route metrics"""
        try:
            from .models import SupplyChainConfig
            
            # Get configuration
            try:
                config = SupplyChainConfig.objects.first()
                if not config:
                    config = SupplyChainConfig.objects.create()
            except:
                # Fallback configuration
                config = type('Config', (), {
                    'fuel_cost_per_km': Decimal('1.5'),
                    'driver_cost_per_hour': Decimal('25.0')
                })()
            
            all_locations = [start_location] + delivery_locations
            total_distance = 0
            total_time = 0
            
            # Calculate route metrics
            for i in range(len(optimized_route)):
                current_idx = optimized_route[i]
                next_idx = optimized_route[(i + 1) % len(optimized_route)]
                
                current_loc = all_locations[current_idx]
                next_loc = all_locations[next_idx]
                
                # Distance
                distance = self._haversine_distance(
                    float(current_loc.latitude), float(current_loc.longitude),
                    float(next_loc.latitude), float(next_loc.longitude)
                )
                total_distance += distance
                
                # Time (assuming average speed of 50 km/h in city)
                travel_time = distance / 50  # hours
                service_time = 0.5  # 30 minutes per stop
                total_time += travel_time + service_time
            
            # Calculate costs
            fuel_cost = total_distance * float(config.fuel_cost_per_km)
            driver_cost = total_time * float(config.driver_cost_per_hour)
            total_cost = fuel_cost + driver_cost
            
            # Calculate savings (compared to naive route)
            naive_distance = self._calculate_naive_route_distance(start_location, delivery_locations)
            cost_savings = ((naive_distance - total_distance) / naive_distance * 100) if naive_distance > 0 else 0
            
            return {
                'total_distance': round(total_distance, 2),
                'total_time': round(total_time, 2),
                'total_cost': round(total_cost, 2),
                'fuel_cost': round(fuel_cost, 2),
                'driver_cost': round(driver_cost, 2),
                'cost_savings': max(0, round(cost_savings, 2)),
                'algorithm': 'genetic_algorithm' if len(delivery_locations) > 10 else 'branch_and_bound'
            }
        
        except Exception as e:
            logger.error(f"Error calculating route metrics: {e}")
            return {
                'total_distance': 0,
                'total_time': 0,
                'total_cost': 0,
                'fuel_cost': 0,
                'driver_cost': 0,
                'cost_savings': 0,
                'algorithm': 'fallback'
            }
    
    def _calculate_naive_route_distance(self, start_location, delivery_locations: List) -> float:
        """Calculate distance for naive (unoptimized) route"""
        total_distance = 0
        current_location = start_location
        
        for location in delivery_locations:
            distance = self._haversine_distance(
                float(current_location.latitude), float(current_location.longitude),
                float(location.latitude), float(location.longitude)
            )
            total_distance += distance
            current_location = location
        
        # Return to start
        total_distance += self._haversine_distance(
            float(current_location.latitude), float(current_location.longitude),
            float(start_location.latitude), float(start_location.longitude)
        )
        
        return total_distance


class RiskManagementService:
    """AI-powered supply chain risk management"""
    
    def __init__(self):
        self.risk_indicators = {}
        self.external_data_sources = {
            'weather': config('WEATHER_API_KEY', default=''),
            'economic': config('ECONOMIC_API_KEY', default=''),
            'news': config('NEWS_API_KEY', default='')
        }
    
    def assess_supply_chain_risks(self) -> List[Dict]:
        """Comprehensive risk assessment using AI"""
        try:
            risks = []
            
            # Analyze different risk categories
            risks.extend(self._analyze_supplier_risks())
            risks.extend(self._analyze_demand_risks())
            risks.extend(self._analyze_logistics_risks())
            risks.extend(self._analyze_external_risks())
            
            # Sort by risk score
            risks.sort(key=lambda x: x['risk_score'], reverse=True)
            
            return risks
        
        except Exception as e:
            logger.error(f"Error assessing supply chain risks: {e}")
            return []
    
    def _analyze_supplier_risks(self) -> List[Dict]:
        """Analyze supplier-related risks"""
        risks = []
        
        try:
            from .models import Supplier, Product
            
            suppliers = Supplier.objects.filter(is_active=True)
            
            for supplier in suppliers:
                risk_factors = []
                risk_score = 0
                
                # Delivery performance risk
                if supplier.on_time_delivery_rate < 80:
                    risk_factors.append("Poor on-time delivery performance")
                    risk_score += 0.3
                
                # Quality risk
                if supplier.quality_score < 7.0:
                    risk_factors.append("Quality issues")
                    risk_score += 0.2
                
                # Financial stability risk
                if supplier.financial_stability < 0.6:
                    risk_factors.append("Financial instability")
                    risk_score += 0.4
                
                # Geographic risk
                if supplier.geographic_risk > 0.5:
                    risk_factors.append("High geographic risk")
                    risk_score += 0.3
                
                # Single supplier dependency
                products_count = Product.objects.filter(
                    # This would need proper supplier relationship in Product model
                ).count()
                
                if products_count > 10:  # High dependency
                    risk_factors.append("High supplier dependency")
                    risk_score += 0.2
                
                if risk_score > 0.3:  # Only report significant risks
                    risks.append({
                        'type': 'supplier_risk',
                        'title': f"Supplier Risk: {supplier.name}",
                        'description': f"Multiple risk factors identified for supplier {supplier.name}",
                        'risk_score': min(10, risk_score * 10),
                        'probability': min(1.0, risk_score),
                        'factors': risk_factors,
                        'affected_entity': supplier.name,
                        'recommendations': self._get_supplier_risk_recommendations(supplier, risk_factors)
                    })
        
        except Exception as e:
            logger.error(f"Error analyzing supplier risks: {e}")
        
        return risks
    
    def _analyze_demand_risks(self) -> List[Dict]:
        """Analyze demand-related risks"""
        risks = []
        
        try:
            from .models import Product, DemandForecast
            
            products = Product.objects.filter(enable_demand_forecasting=True)
            
            for product in products:
                # Check for demand volatility
                if product.demand_volatility > 0.5:
                    risk_score = product.demand_volatility * 5  # Scale to 0-10
                    
                    risks.append({
                        'type': 'demand_volatility',
                        'title': f"High Demand Volatility: {product.name}",
                        'description': f"Product {product.name} shows high demand volatility",
                        'risk_score': risk_score,
                        'probability': float(product.demand_volatility),
                        'factors': ["High demand volatility", "Unpredictable sales patterns"],
                        'affected_entity': product.name,
                        'recommendations': [
                            "Increase safety stock levels",
                            "Implement more frequent forecasting",
                            "Consider demand smoothing strategies"
                        ]
                    })
                
                # Check for low stock vs. demand
                recent_forecasts = DemandForecast.objects.filter(
                    product=product,
                    forecast_date__gte=timezone.now().date()
                ).order_by('forecast_date')[:7]  # Next 7 days
                
                if recent_forecasts:
                    total_predicted_demand = sum(f.predicted_demand for f in recent_forecasts)
                    if product.current_stock < total_predicted_demand:
                        shortage_risk = min(1.0, total_predicted_demand / max(1, product.current_stock))
                        
                        risks.append({
                            'type': 'stock_shortage',
                            'title': f"Potential Stock Shortage: {product.name}",
                            'description': f"Current stock may not meet predicted demand",
                            'risk_score': shortage_risk * 8,
                            'probability': shortage_risk,
                            'factors': ["Low current stock", "High predicted demand"],
                            'affected_entity': product.name,
                            'recommendations': [
                                "Immediate reordering required",
                                "Expedite supplier delivery",
                                "Consider substitute products"
                            ]
                        })
        
        except Exception as e:
            logger.error(f"Error analyzing demand risks: {e}")
        
        return risks
    
    def _analyze_logistics_risks(self) -> List[Dict]:
        """Analyze logistics and transportation risks"""
        risks = []
        
        try:
            from .models import RouteOptimization, DeliveryLocation
            
            # Check for route concentration risk
            recent_routes = RouteOptimization.objects.filter(
                delivery_date__gte=timezone.now().date() - timedelta(days=30)
            )
            
            if recent_routes.count() > 0:
                # Analyze route efficiency
                avg_cost_savings = recent_routes.aggregate(
                    avg_savings=models.Avg('cost_savings_percentage')
                )['avg_savings'] or 0
                
                if avg_cost_savings < 5:  # Low savings indicate potential issues
                    risks.append({
                        'type': 'logistics_efficiency',
                        'title': "Low Logistics Efficiency",
                        'description': "Route optimization showing minimal cost savings",
                        'risk_score': 6.0,
                        'probability': 0.7,
                        'factors': ["Low route optimization savings", "Inefficient delivery patterns"],
                        'affected_entity': "Logistics Operations",
                        'recommendations': [
                            "Review route optimization algorithms",
                            "Analyze delivery location clustering",
                            "Consider delivery time window adjustments"
                        ]
                    })
            
            # Check for delivery location risks
            locations = DeliveryLocation.objects.filter(is_active=True)
            high_difficulty_locations = locations.filter(access_difficulty_score__gte=4)
            
            if high_difficulty_locations.count() > locations.count() * 0.3:  # More than 30%
                risks.append({
                    'type': 'delivery_difficulty',
                    'title': "High Delivery Difficulty Locations",
                    'description': "Many delivery locations have high access difficulty",
                    'risk_score': 5.0,
                    'probability': 0.8,
                    'factors': ["High access difficulty scores", "Delivery delays"],
                    'affected_entity': "Delivery Operations",
                    'recommendations': [
                        "Negotiate alternative delivery points",
                        "Increase delivery time allowances",
                        "Consider specialized delivery equipment"
                    ]
                })
        
        except Exception as e:
            logger.error(f"Error analyzing logistics risks: {e}")
        
        return risks
    
    def _analyze_external_risks(self) -> List[Dict]:
        """Analyze external risks (weather, economic, etc.)"""
        risks = []
        
        try:
            # Weather risks (simplified - in production, integrate with weather APIs)
            current_season = self._get_current_season()
            if current_season in ['winter', 'monsoon']:
                risks.append({
                    'type': 'weather_risk',
                    'title': f"Seasonal Weather Risk ({current_season.title()})",
                    'description': f"Increased delivery delays expected during {current_season}",
                    'risk_score': 4.0,
                    'probability': 0.6,
                    'factors': ["Seasonal weather patterns", "Historical delivery delays"],
                    'affected_entity': "Delivery Operations",
                    'recommendations': [
                        "Increase delivery time buffers",
                        "Prepare alternative routes",
                        "Stock up critical items"
                    ]
                })
            
            # Economic indicators (simplified)
            # In production, integrate with economic data APIs
            risks.append({
                'type': 'economic_risk',
                'title': "Economic Uncertainty",
                'description': "General economic conditions may affect supply chain",
                'risk_score': 3.0,
                'probability': 0.4,
                'factors': ["Market volatility", "Economic indicators"],
                'affected_entity': "Overall Supply Chain",
                'recommendations': [
                    "Monitor economic indicators",
                    "Diversify supplier base",
                    "Maintain flexible inventory levels"
                ]
            })
        
        except Exception as e:
            logger.error(f"Error analyzing external risks: {e}")
        
        return risks
    
    def _get_current_season(self) -> str:
        """Determine current season (simplified)"""
        month = timezone.now().month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def _get_supplier_risk_recommendations(self, supplier, risk_factors: List[str]) -> List[str]:
        """Generate recommendations for supplier risks"""
        recommendations = []
        
        if "Poor on-time delivery performance" in risk_factors:
            recommendations.append("Negotiate improved delivery SLAs")
            recommendations.append("Identify backup suppliers")
        
        if "Quality issues" in risk_factors:
            recommendations.append("Implement additional quality checks")
            recommendations.append("Provide supplier quality training")
        
        if "Financial instability" in risk_factors:
            recommendations.append("Monitor supplier financial health")
            recommendations.append("Secure payment terms protection")
        
        if "High geographic risk" in risk_factors:
            recommendations.append("Diversify supplier geographic locations")
            recommendations.append("Develop local supplier alternatives")
        
        return recommendations or ["Monitor supplier performance closely"]
    
    def predict_disruption_probability(self, risk_type: str, time_horizon_days: int = 30) -> Dict:
        """Predict probability of supply chain disruption"""
        try:
            # This is a simplified model - in production, use ML models trained on historical data
            base_probabilities = {
                'supplier_delay': 0.15,
                'demand_spike': 0.10,
                'logistics_disruption': 0.08,
                'quality_issue': 0.05,
                'external_event': 0.03
            }
            
            base_prob = base_probabilities.get(risk_type, 0.05)
            
            # Adjust based on time horizon
            time_factor = min(1.0, time_horizon_days / 30)
            adjusted_prob = base_prob * time_factor
            
            return {
                'risk_type': risk_type,
                'time_horizon_days': time_horizon_days,
                'disruption_probability': adjusted_prob,
                'confidence_score': 0.7,  # Model confidence
                'contributing_factors': self._get_disruption_factors(risk_type)
            }
        
        except Exception as e:
            logger.error(f"Error predicting disruption probability: {e}")
            return {
                'risk_type': risk_type,
                'time_horizon_days': time_horizon_days,
                'disruption_probability': 0.05,
                'confidence_score': 0.3,
                'contributing_factors': []
            }
    
    def _get_disruption_factors(self, risk_type: str) -> List[str]:
        """Get factors that contribute to disruption risk"""
        factor_map = {
            'supplier_delay': [
                "Historical delivery performance",
                "Supplier capacity utilization",
                "Geographic location risks"
            ],
            'demand_spike': [
                "Seasonal patterns",
                "Market trends",
                "Economic indicators"
            ],
            'logistics_disruption': [
                "Weather conditions",
                "Route complexity",
                "Transportation capacity"
            ],
            'quality_issue': [
                "Supplier quality scores",
                "Historical defect rates",
                "Process changes"
            ],
            'external_event': [
                "Economic conditions",
                "Political stability",
                "Natural disaster risk"
            ]
        }
        
        return factor_map.get(risk_type, [])
