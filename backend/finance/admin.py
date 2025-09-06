from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Currency, AccountType, Account, JournalEntry, JournalEntryLine,
    Vendor, Customer, Invoice, BudgetCategory, Budget, BudgetLine,
    ExpenseCategory, Expense, TaxAuthority, TaxRate,
    FinancialForecast, AnomalyDetection
)

@admin.register(Currency)
class CurrencyAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'symbol', 'exchange_rate', 'is_base_currency', 'is_active']
    list_filter = ['is_base_currency', 'is_active']
    search_fields = ['code', 'name']

@admin.register(AccountType)
class AccountTypeAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['code', 'name']

@admin.register(Account)
class AccountAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'account_type', 'currency', 'balance', 'is_active']
    list_filter = ['account_type__category', 'currency', 'is_active']
    search_fields = ['code', 'name']
    raw_id_fields = ['created_by']

class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 2

@admin.register(JournalEntry)
class JournalEntryAdmin(SimpleHistoryAdmin):
    list_display = ['entry_number', 'date', 'description', 'total_amount', 'status', 'created_by']
    list_filter = ['status', 'date']
    search_fields = ['entry_number', 'description']
    inlines = [JournalEntryLineInline]
    raw_id_fields = ['created_by', 'approved_by']

@admin.register(Vendor)
class VendorAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'email', 'currency', 'payment_terms', 'is_active']
    list_filter = ['currency', 'is_active']
    search_fields = ['code', 'name', 'email']

@admin.register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'email', 'currency', 'credit_limit', 'is_active']
    list_filter = ['currency', 'is_active']
    search_fields = ['code', 'name', 'email']

@admin.register(Invoice)
class InvoiceAdmin(SimpleHistoryAdmin):
    list_display = ['invoice_number', 'invoice_type', 'customer', 'vendor', 'total_amount', 'status', 'due_date']
    list_filter = ['invoice_type', 'status', 'currency']
    search_fields = ['invoice_number']
    raw_id_fields = ['customer', 'vendor', 'created_by']

@admin.register(BudgetCategory)
class BudgetCategoryAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'parent_category', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name']

class BudgetLineInline(admin.TabularInline):
    model = BudgetLine
    extra = 1

@admin.register(Budget)
class BudgetAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'period_type', 'start_date', 'end_date', 'total_budget', 'total_actual', 'is_active']
    list_filter = ['period_type', 'is_active']
    search_fields = ['name']
    inlines = [BudgetLineInline]
    raw_id_fields = ['created_by']

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'account', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name']

@admin.register(Expense)
class ExpenseAdmin(SimpleHistoryAdmin):
    list_display = ['expense_number', 'title', 'category', 'amount', 'currency', 'status', 'submitted_by']
    list_filter = ['status', 'category', 'currency']
    search_fields = ['expense_number', 'title']
    raw_id_fields = ['submitted_by', 'approved_by', 'vendor']

@admin.register(TaxAuthority)
class TaxAuthorityAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'country', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['code', 'name']

@admin.register(TaxRate)
class TaxRateAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'name', 'rate', 'tax_authority', 'effective_date', 'is_active']
    list_filter = ['tax_authority', 'is_active']
    search_fields = ['code', 'name']

@admin.register(FinancialForecast)
class FinancialForecastAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'forecast_type', 'period_start', 'period_end', 'predicted_amount', 'confidence_score']
    list_filter = ['forecast_type']
    search_fields = ['name']
    raw_id_fields = ['created_by']

@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(SimpleHistoryAdmin):
    list_display = ['anomaly_type', 'severity', 'detection_date', 'anomaly_score', 'is_resolved']
    list_filter = ['anomaly_type', 'severity', 'is_resolved']
    search_fields = ['description']
    raw_id_fields = ['resolved_by']
