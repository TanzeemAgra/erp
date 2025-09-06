"""
Assets App URLs - Asset Management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'vendors', views.VendorViewSet)
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'assets', views.AssetViewSet)
router.register(r'inventory-items', views.InventoryItemViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'goods-receipt-notes', views.GoodsReceiptNoteViewSet)
router.register(r'stock-movements', views.StockMovementViewSet)
router.register(r'maintenance-schedules', views.MaintenanceScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
