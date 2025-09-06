"""
Finance App URLs - Financial Management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'account-types', views.AccountTypeViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'journal-entries', views.JournalEntryViewSet)
router.register(r'vendors', views.VendorViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'budgets', views.BudgetViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'forecasts', views.FinancialForecastViewSet)
router.register(r'anomalies', views.AnomalyDetectionViewSet)
router.register(r'dashboard', views.FinanceDashboardViewSet, basename='finance-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
