from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count, Avg, F
from django.utils import timezone
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

from .models import (
    Category, Vendor, Warehouse, Asset, InventoryItem, StockLevel,
    PurchaseOrder, PurchaseOrderItem, GoodsReceiptNote, GoodsReceiptItem,
    DemandForecast, StockMovement, MaintenanceSchedule
)
from .serializers import (
    CategorySerializer, VendorSerializer, WarehouseSerializer, AssetSerializer,
    InventoryItemSerializer, StockLevelSerializer, PurchaseOrderSerializer,
    PurchaseOrderItemSerializer, GoodsReceiptNoteSerializer, GoodsReceiptItemSerializer,
    DemandForecastSerializer, StockMovementSerializer, MaintenanceScheduleSerializer,
    AssetDashboardSerializer, InventoryDashboardSerializer, SupplyChainDashboardSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    @action(detail=False, methods=['get'])
    def performance_metrics(self, request):
        """Get vendor performance metrics"""
        vendors = Vendor.objects.filter(is_active=True)
        metrics = []
        
        for vendor in vendors:
            pos = PurchaseOrder.objects.filter(vendor=vendor)
            on_time_deliveries = pos.filter(
                status='COMPLETED',
                goodsreceiptnote__received_date__lte=F('expected_delivery_date')
            ).count()
            total_deliveries = pos.filter(status='COMPLETED').count()
            
            performance = {
                'vendor_id': vendor.id,
                'vendor_name': vendor.name,
                'total_orders': pos.count(),
                'completed_orders': total_deliveries,
                'on_time_delivery_rate': (on_time_deliveries / total_deliveries * 100) if total_deliveries > 0 else 0,
                'average_lead_time': pos.aggregate(
                    avg_lead=Avg('expected_delivery_date') - Avg('order_date')
                )['avg_lead'] or 0,
                'rating': vendor.rating
            }
            metrics.append(performance)
        
        return Response(metrics)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    
    @action(detail=True, methods=['get'])
    def stock_summary(self, request, pk=None):
        """Get stock summary for a warehouse"""
        warehouse = self.get_object()
        stock_levels = StockLevel.objects.filter(warehouse=warehouse)
        
        summary = {
            'total_items': stock_levels.count(),
            'total_quantity': stock_levels.aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'low_stock_items': stock_levels.filter(
                quantity__lte=F('item__reorder_level')
            ).count(),
            'stock_value': sum(
                level.quantity * level.item.unit_cost for level in stock_levels
            ),
            'capacity_utilization': 0  # Can be calculated based on actual space usage
        }
        
        return Response(summary)

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get asset dashboard statistics"""
        assets = Asset.objects.filter(is_active=True)
        
        stats = {
            'total_assets': assets.count(),
            'active_assets': assets.filter(status='ACTIVE').count(),
            'maintenance_due': MaintenanceSchedule.objects.filter(
                scheduled_date__lte=timezone.now().date() + timedelta(days=7),
                is_completed=False
            ).count(),
            'total_value': assets.aggregate(Sum('current_value'))['current_value__sum'] or 0,
            'depreciation_this_year': self._calculate_depreciation_this_year(assets)
        }
        
        serializer = AssetDashboardSerializer(stats)
        return Response(serializer.data)
    
    def _calculate_depreciation_this_year(self, assets):
        """Calculate total depreciation for current year"""
        current_year = timezone.now().year
        total_depreciation = 0
        
        for asset in assets:
            if asset.purchase_date.year <= current_year:
                annual_depreciation = asset.purchase_cost * (asset.depreciation_rate / 100)
                total_depreciation += annual_depreciation
                
        return total_depreciation
    
    @action(detail=False, methods=['get'])
    def maintenance_calendar(self, request):
        """Get upcoming maintenance schedule"""
        schedules = MaintenanceSchedule.objects.filter(
            is_completed=False,
            scheduled_date__gte=timezone.now().date()
        ).order_by('scheduled_date')[:20]
        
        serializer = MaintenanceScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get inventory dashboard statistics"""
        items = InventoryItem.objects.filter(is_active=True)
        
        stats = {
            'total_items': items.count(),
            'low_stock_items': items.filter(
                stock_levels__quantity__lte=F('reorder_level')
            ).distinct().count(),
            'total_stock_value': sum(item.stock_value() for item in items),
            'pending_pos': PurchaseOrder.objects.filter(
                status__in=['SENT', 'CONFIRMED', 'PARTIAL']
            ).count(),
            'recent_movements': StockMovement.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
        }
        
        serializer = InventoryDashboardSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock_alert(self, request):
        """Get items with low stock levels"""
        low_stock_items = InventoryItem.objects.filter(
            stock_levels__quantity__lte=F('reorder_level'),
            is_active=True
        ).distinct()
        
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generate_forecast(self, request, pk=None):
        """Generate AI-powered demand forecast for an item"""
        item = self.get_object()
        forecast_period = int(request.data.get('forecast_period', 30))
        
        try:
            forecast = self._generate_demand_forecast(item, forecast_period)
            serializer = DemandForecastSerializer(forecast)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Failed to generate forecast: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _generate_demand_forecast(self, item, forecast_period):
        """AI-powered demand forecasting using historical data"""
        # Get historical stock movements
        movements = StockMovement.objects.filter(
            item=item,
            movement_type='OUT',
            created_at__gte=timezone.now() - timedelta(days=365)
        ).order_by('created_at')
        
        if movements.count() < 10:
            # Not enough data for ML, use simple average
            recent_avg = movements.aggregate(Avg('quantity'))['quantity__avg'] or 0
            predicted_demand = int(recent_avg * (forecast_period / 7))  # Weekly to period
            confidence = 60.0
        else:
            # Use machine learning for prediction
            predicted_demand, confidence = self._ml_forecast(movements, forecast_period)
        
        # Create or update forecast record
        forecast, created = DemandForecast.objects.update_or_create(
            item=item,
            forecast_date=timezone.now().date(),
            forecast_period=forecast_period,
            defaults={
                'predicted_demand': predicted_demand,
                'confidence_score': confidence,
                'algorithm_used': 'LINEAR_REGRESSION' if movements.count() >= 10 else 'SIMPLE_AVERAGE'
            }
        )
        
        return forecast
    
    def _ml_forecast(self, movements, forecast_period):
        """Machine learning based forecasting"""
        try:
            # Prepare data
            data = []
            for i, movement in enumerate(movements):
                data.append([
                    i,  # Time index
                    movement.quantity,
                    movement.created_at.weekday(),  # Day of week
                    movement.created_at.month  # Month for seasonality
                ])
            
            df = pd.DataFrame(data, columns=['time', 'quantity', 'weekday', 'month'])
            
            # Prepare features
            X = df[['time', 'weekday', 'month']].values
            y = df['quantity'].values
            
            # Use polynomial features for better fitting
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            
            # Train model
            model = LinearRegression()
            model.fit(X_poly, y)
            
            # Make prediction
            future_time = len(movements)
            current_weekday = timezone.now().weekday()
            current_month = timezone.now().month
            
            future_X = poly_features.transform([[future_time, current_weekday, current_month]])
            prediction = model.predict(future_X)[0]
            
            # Calculate confidence based on R² score
            score = model.score(X_poly, y)
            confidence = min(max(score * 100, 30), 95)  # Between 30-95%
            
            # Scale prediction to forecast period
            predicted_demand = max(int(prediction * (forecast_period / 7)), 0)
            
            return predicted_demand, confidence
            
        except Exception as e:
            # Fallback to simple average
            avg_quantity = movements.aggregate(Avg('quantity'))['quantity__avg'] or 0
            return int(avg_quantity * (forecast_period / 7)), 50.0

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a purchase order"""
        po = self.get_object()
        po.status = 'CONFIRMED'
        po.approved_by = request.user
        po.save()
        
        serializer = self.get_serializer(po)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def supply_chain_dashboard(self, request):
        """Get supply chain dashboard metrics"""
        vendors = Vendor.objects.filter(is_active=True)
        pos = PurchaseOrder.objects.all()
        
        stats = {
            'active_vendors': vendors.count(),
            'pending_deliveries': pos.filter(
                status__in=['SENT', 'CONFIRMED', 'PARTIAL']
            ).count(),
            'overdue_deliveries': pos.filter(
                expected_delivery_date__lt=timezone.now().date(),
                status__in=['SENT', 'CONFIRMED', 'PARTIAL']
            ).count(),
            'average_lead_time': self._calculate_average_lead_time(),
            'vendor_performance': self._calculate_vendor_performance()
        }
        
        serializer = SupplyChainDashboardSerializer(stats)
        return Response(serializer.data)
    
    def _calculate_average_lead_time(self):
        """Calculate average lead time across all completed POs"""
        completed_pos = PurchaseOrder.objects.filter(status='COMPLETED')
        if not completed_pos.exists():
            return 0
        
        total_lead_time = 0
        count = 0
        
        for po in completed_pos:
            grns = po.goodsreceiptnote_set.all()
            if grns.exists():
                lead_time = (grns.first().received_date - po.order_date).days
                total_lead_time += lead_time
                count += 1
        
        return total_lead_time / count if count > 0 else 0
    
    def _calculate_vendor_performance(self):
        """Calculate overall vendor performance score"""
        vendors = Vendor.objects.filter(is_active=True)
        if not vendors.exists():
            return 0
        
        total_rating = vendors.aggregate(Avg('rating'))['rating__avg']
        return total_rating or 0

class GoodsReceiptNoteViewSet(viewsets.ModelViewSet):
    queryset = GoodsReceiptNote.objects.all()
    serializer_class = GoodsReceiptNoteSerializer
    
    def create(self, request, *args, **kwargs):
        """Create GRN and update stock levels"""
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 201:
            grn = GoodsReceiptNote.objects.get(id=response.data['id'])
            self._update_stock_levels(grn)
            
        return response
    
    def _update_stock_levels(self, grn):
        """Update stock levels based on GRN"""
        for grn_item in grn.items.all():
            item = grn_item.po_item.item
            warehouse = grn.warehouse
            
            # Update or create stock level
            stock_level, created = StockLevel.objects.get_or_create(
                item=item,
                warehouse=warehouse,
                defaults={'quantity': 0}
            )
            
            stock_level.quantity += grn_item.received_quantity
            stock_level.save()
            
            # Update PO item received quantity
            grn_item.po_item.received_quantity += grn_item.received_quantity
            grn_item.po_item.save()
            
            # Create stock movement record
            StockMovement.objects.create(
                item=item,
                warehouse=warehouse,
                movement_type='IN',
                quantity=grn_item.received_quantity,
                reference_number=f"GRN-{grn.grn_number}",
                created_by=grn.received_by
            )

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get stock movement analytics"""
        movements = StockMovement.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        )
        
        analytics = {
            'total_movements': movements.count(),
            'stock_in': movements.filter(movement_type='IN').aggregate(
                Sum('quantity')
            )['quantity__sum'] or 0,
            'stock_out': movements.filter(movement_type='OUT').aggregate(
                Sum('quantity')
            )['quantity__sum'] or 0,
            'transfers': movements.filter(movement_type='TRANSFER').count(),
            'adjustments': movements.filter(movement_type='ADJUSTMENT').count(),
        }
        
        return Response(analytics)

class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleSerializer
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark maintenance as completed"""
        schedule = self.get_object()
        schedule.is_completed = True
        schedule.completed_date = timezone.now().date()
        schedule.performed_by = request.user
        schedule.cost = request.data.get('cost', 0)
        schedule.save()
        
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)
