from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Currency, AccountType, Account, JournalEntry, JournalEntryLine,
    Vendor, Customer, Invoice, BudgetCategory, Budget, BudgetLine,
    ExpenseCategory, Expense, TaxAuthority, TaxRate,
    FinancialForecast, AnomalyDetection
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    account_type_name = serializers.CharField(source='account_type.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Account
        fields = '__all__'

class JournalEntryLineSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    account_code = serializers.CharField(source='account.code', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    
    class Meta:
        model = JournalEntryLine
        fields = '__all__'

class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = JournalEntry
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    
    class Meta:
        model = Vendor
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    days_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = '__all__'
    
    def get_days_overdue(self, obj):
        from django.utils import timezone
        if obj.status not in ['PAID', 'CANCELLED'] and obj.due_date < timezone.now().date():
            return (timezone.now().date() - obj.due_date).days
        return 0

class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = '__all__'

class BudgetLineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    account_name = serializers.CharField(source='account.name', read_only=True)
    variance_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = BudgetLine
        fields = '__all__'
    
    def get_variance_percentage(self, obj):
        if obj.budgeted_amount > 0:
            return round((obj.variance / obj.budgeted_amount) * 100, 2)
        return 0

class BudgetSerializer(serializers.ModelSerializer):
    budget_lines = BudgetLineSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    variance_amount = serializers.SerializerMethodField()
    variance_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = '__all__'
    
    def get_variance_amount(self, obj):
        return obj.total_actual - obj.total_budget
    
    def get_variance_percentage(self, obj):
        if obj.total_budget > 0:
            return round(((obj.total_actual - obj.total_budget) / obj.total_budget) * 100, 2)
        return 0

class ExpenseCategorySerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    submitted_by_name = serializers.CharField(source='submitted_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'

class TaxAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxAuthority
        fields = '__all__'

class TaxRateSerializer(serializers.ModelSerializer):
    tax_authority_name = serializers.CharField(source='tax_authority.name', read_only=True)
    account_name = serializers.CharField(source='account.name', read_only=True)
    rate_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = TaxRate
        fields = '__all__'
    
    def get_rate_percentage(self, obj):
        return round(obj.rate * 100, 4)

class FinancialForecastSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    confidence_percentage = serializers.SerializerMethodField()
    accuracy_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = FinancialForecast
        fields = '__all__'
    
    def get_confidence_percentage(self, obj):
        return round(obj.confidence_score * 100, 2)
    
    def get_accuracy_percentage(self, obj):
        if obj.accuracy_score:
            return round(obj.accuracy_score * 100, 2)
        return None

class AnomalyDetectionSerializer(serializers.ModelSerializer):
    related_account_name = serializers.CharField(source='related_account.name', read_only=True)
    related_transaction_number = serializers.CharField(source='related_transaction.entry_number', read_only=True)
    related_expense_number = serializers.CharField(source='related_expense.expense_number', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.get_full_name', read_only=True)
    anomaly_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = AnomalyDetection
        fields = '__all__'
    
    def get_anomaly_percentage(self, obj):
        return round(obj.anomaly_score * 100, 2)

# Dashboard Serializers
class FinanceDashboardSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=15, decimal_places=2)
    accounts_receivable = serializers.DecimalField(max_digits=15, decimal_places=2)
    accounts_payable = serializers.DecimalField(max_digits=15, decimal_places=2)
    cash_balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_assets = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_liabilities = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_equity = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    # Recent data
    recent_invoices = InvoiceSerializer(many=True, read_only=True)
    recent_expenses = ExpenseSerializer(many=True, read_only=True)
    overdue_invoices = InvoiceSerializer(many=True, read_only=True)
    pending_expenses = ExpenseSerializer(many=True, read_only=True)
    
    # AI insights
    anomalies = AnomalyDetectionSerializer(many=True, read_only=True)
    forecasts = FinancialForecastSerializer(many=True, read_only=True)
    
    # Charts data
    revenue_chart = serializers.JSONField()
    expense_chart = serializers.JSONField()
    cash_flow_chart = serializers.JSONField()
    budget_variance_chart = serializers.JSONField()
    
    # Currency breakdown
    currency_breakdown = serializers.JSONField()
    
    # KPIs
    profit_margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    current_ratio = serializers.DecimalField(max_digits=5, decimal_places=2)
    debt_ratio = serializers.DecimalField(max_digits=5, decimal_places=2)
    roe = serializers.DecimalField(max_digits=5, decimal_places=2)  # Return on Equity
