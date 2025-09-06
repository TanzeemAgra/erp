from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Category, Vendor, Warehouse, Asset, InventoryItem, StockLevel,
    PurchaseOrder, PurchaseOrderItem, GoodsReceiptNote, GoodsReceiptItem,
    DemandForecast, StockMovement, MaintenanceSchedule
)

@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']

@admin.register(Vendor)
class VendorAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'contact_person', 'email', 'rating', 'is_active']
    list_filter = ['is_active', 'rating', 'country']
    search_fields = ['name', 'code', 'email', 'contact_person']
    ordering = ['name']

@admin.register(Warehouse)
class WarehouseAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'manager', 'capacity', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

class StockLevelInline(admin.TabularInline):
    model = StockLevel
    extra = 0

@admin.register(Asset)
class AssetAdmin(SimpleHistoryAdmin):
    list_display = ['asset_tag', 'name', 'category', 'status', 'purchase_date', 'current_value']
    list_filter = ['status', 'category', 'location']
    search_fields = ['asset_tag', 'name', 'serial_number']
    date_hierarchy = 'purchase_date'
    ordering = ['-purchase_date']

@admin.register(InventoryItem)
class InventoryItemAdmin(SimpleHistoryAdmin):
    list_display = ['sku', 'name', 'category', 'item_type', 'unit_cost', 'reorder_level']
    list_filter = ['item_type', 'category', 'is_active']
    search_fields = ['sku', 'name']
    inlines = [StockLevelInline]

@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ['item', 'warehouse', 'quantity', 'reserved_quantity', 'last_updated']
    list_filter = ['warehouse', 'item__category']
    search_fields = ['item__name', 'item__sku']

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(SimpleHistoryAdmin):
    list_display = ['po_number', 'vendor', 'order_date', 'status', 'total_amount']
    list_filter = ['status', 'vendor']
    search_fields = ['po_number']
    date_hierarchy = 'order_date'
    inlines = [PurchaseOrderItemInline]

class GoodsReceiptItemInline(admin.TabularInline):
    model = GoodsReceiptItem
    extra = 0

@admin.register(GoodsReceiptNote)
class GoodsReceiptNoteAdmin(SimpleHistoryAdmin):
    list_display = ['grn_number', 'purchase_order', 'received_date', 'received_by']
    list_filter = ['received_date', 'warehouse']
    search_fields = ['grn_number']
    inlines = [GoodsReceiptItemInline]

@admin.register(DemandForecast)
class DemandForecastAdmin(SimpleHistoryAdmin):
    list_display = ['item', 'forecast_date', 'forecast_period', 'predicted_demand', 'confidence_score']
    list_filter = ['forecast_date', 'algorithm_used']
    search_fields = ['item__name', 'item__sku']

@admin.register(StockMovement)
class StockMovementAdmin(SimpleHistoryAdmin):
    list_display = ['item', 'warehouse', 'movement_type', 'quantity', 'created_at', 'created_by']
    list_filter = ['movement_type', 'warehouse', 'created_at']
    search_fields = ['item__name', 'reference_number']
    date_hierarchy = 'created_at'

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(SimpleHistoryAdmin):
    list_display = ['asset', 'maintenance_type', 'scheduled_date', 'is_completed', 'cost']
    list_filter = ['maintenance_type', 'is_completed', 'scheduled_date']
    search_fields = ['asset__name', 'asset__asset_tag']
