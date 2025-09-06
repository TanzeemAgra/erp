from rest_framework import serializers
from .models import (
    Category, Vendor, Warehouse, Asset, InventoryItem, StockLevel,
    PurchaseOrder, PurchaseOrderItem, GoodsReceiptNote, GoodsReceiptItem,
    DemandForecast, StockMovement, MaintenanceSchedule
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Warehouse
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Asset
        fields = '__all__'

class StockLevelSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    available_quantity = serializers.ReadOnlyField()
    
    class Meta:
        model = StockLevel
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='preferred_vendor.name', read_only=True)
    current_stock = serializers.ReadOnlyField()
    stock_value = serializers.ReadOnlyField()
    stock_levels = StockLevelSerializer(many=True, read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = '__all__'

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class GoodsReceiptItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='po_item.item.name', read_only=True)
    
    class Meta:
        model = GoodsReceiptItem
        fields = '__all__'

class GoodsReceiptNoteSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(source='purchase_order.po_number', read_only=True)
    vendor_name = serializers.CharField(source='purchase_order.vendor.name', read_only=True)
    received_by_name = serializers.CharField(source='received_by.get_full_name', read_only=True)
    items = GoodsReceiptItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = GoodsReceiptNote
        fields = '__all__'

class DemandForecastSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    
    class Meta:
        model = DemandForecast
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = '__all__'

class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    asset_tag = serializers.CharField(source='asset.asset_tag', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    
    class Meta:
        model = MaintenanceSchedule
        fields = '__all__'

# Dashboard serializers
class AssetDashboardSerializer(serializers.Serializer):
    total_assets = serializers.IntegerField()
    active_assets = serializers.IntegerField()
    maintenance_due = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    depreciation_this_year = serializers.DecimalField(max_digits=15, decimal_places=2)

class InventoryDashboardSerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    low_stock_items = serializers.IntegerField()
    total_stock_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending_pos = serializers.IntegerField()
    recent_movements = serializers.IntegerField()

class SupplyChainDashboardSerializer(serializers.Serializer):
    active_vendors = serializers.IntegerField()
    pending_deliveries = serializers.IntegerField()
    overdue_deliveries = serializers.IntegerField()
    average_lead_time = serializers.DecimalField(max_digits=5, decimal_places=1)
    vendor_performance = serializers.DecimalField(max_digits=5, decimal_places=2)
