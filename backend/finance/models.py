from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid
from simple_history.models import HistoricalRecords

User = get_user_model()

# Currency Management
class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text="ISO 4217 currency code")
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6, default=1.00)
    is_base_currency = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.code} - {self.name}"

# Chart of Accounts
class AccountType(models.Model):
    ACCOUNT_CATEGORIES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=ACCOUNT_CATEGORIES)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.code} - {self.name}"

class Account(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='accounts')
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_accounts')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='accounts')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

# General Ledger
class JournalEntry(models.Model):
    ENTRY_STATUS = [
        ('DRAFT', 'Draft'),
        ('POSTED', 'Posted'),
        ('REVERSED', 'Reversed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    reference = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=ENTRY_STATUS, default='DRAFT')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Journal Entries"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.entry_number} - {self.description}"

class JournalEntryLine(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='journal_lines')
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    description = models.CharField(max_length=255, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6, default=1.00)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.journal_entry.entry_number} - {self.account.name}"

# Accounts Payable/Receivable
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    tax_number = models.CharField(max_length=50, blank=True)
    payment_terms = models.IntegerField(default=30, help_text="Payment terms in days")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.code} - {self.name}"

class Customer(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    tax_number = models.CharField(max_length=50, blank=True)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_terms = models.IntegerField(default=30, help_text="Payment terms in days")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.code} - {self.name}"

class Invoice(models.Model):
    INVOICE_TYPES = [
        ('SALES', 'Sales Invoice'),
        ('PURCHASE', 'Purchase Invoice'),
    ]
    
    INVOICE_STATUS = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_invoices')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_invoices')
    invoice_date = models.DateField()
    due_date = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='DRAFT')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-invoice_date']

    def __str__(self):
        return f"{self.invoice_number} - {self.get_invoice_type_display()}"

# Budgeting
class BudgetCategory(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_categories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Budget Categories"

    def __str__(self):
        return f"{self.code} - {self.name}"

class Budget(models.Model):
    BUDGET_PERIODS = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]
    
    name = models.CharField(max_length=200)
    period_type = models.CharField(max_length=20, choices=BUDGET_PERIODS)
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_actual = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

class BudgetLine(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='budget_lines')
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='budget_lines')
    budgeted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    variance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.variance = self.actual_amount - self.budgeted_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.budget.name} - {self.category.name}"

# Expense Tracking
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expense_categories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Expense Categories"

    def __str__(self):
        return f"{self.code} - {self.name}"

class Expense(models.Model):
    EXPENSE_STATUS = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PAID', 'Paid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    expense_date = models.DateField()
    description = models.TextField(blank=True)
    receipt_file = models.FileField(upload_to='expenses/receipts/', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=EXPENSE_STATUS, default='DRAFT')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_expenses')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-expense_date']

    def __str__(self):
        return f"{self.expense_number} - {self.title}"

# Tax Compliance
class TaxAuthority(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    contact_info = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Tax Authorities"

    def __str__(self):
        return f"{self.code} - {self.name}"

class TaxRate(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)])
    tax_authority = models.ForeignKey(TaxAuthority, on_delete=models.CASCADE, related_name='tax_rates')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='tax_rates')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.code} - {self.rate * 100}%"

# AI-Powered Features
class FinancialForecast(models.Model):
    FORECAST_TYPES = [
        ('REVENUE', 'Revenue Forecast'),
        ('EXPENSE', 'Expense Forecast'),
        ('CASH_FLOW', 'Cash Flow Forecast'),
        ('BUDGET_VARIANCE', 'Budget Variance Forecast'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    forecast_type = models.CharField(max_length=20, choices=FORECAST_TYPES)
    period_start = models.DateField()
    period_end = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    predicted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)])
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    model_version = models.CharField(max_length=50)
    training_data_points = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_forecast_type_display()}"

class AnomalyDetection(models.Model):
    ANOMALY_TYPES = [
        ('UNUSUAL_TRANSACTION', 'Unusual Transaction'),
        ('BUDGET_DEVIATION', 'Budget Deviation'),
        ('SUSPICIOUS_EXPENSE', 'Suspicious Expense'),
        ('CASH_FLOW_ANOMALY', 'Cash Flow Anomaly'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anomaly_type = models.CharField(max_length=30, choices=ANOMALY_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    description = models.TextField()
    detection_date = models.DateTimeField(auto_now_add=True)
    related_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    related_transaction = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, null=True, blank=True)
    related_expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True, blank=True)
    anomaly_score = models.DecimalField(max_digits=5, decimal_places=4)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-detection_date']

    def __str__(self):
        return f"{self.get_anomaly_type_display()} - {self.severity}"
