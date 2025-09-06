from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
import random

from finance.models import (
    Currency, AccountType, Account, JournalEntry, JournalEntryLine,
    Vendor, Customer, Invoice, BudgetCategory, Budget, BudgetLine,
    ExpenseCategory, Expense, TaxAuthority, TaxRate,
    FinancialForecast, AnomalyDetection
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample finance data with AI-powered features'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample finance data...'))
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@company.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Create Currencies
        self.stdout.write('Creating currencies...')
        usd, _ = Currency.objects.get_or_create(
            code='USD',
            defaults={
                'name': 'US Dollar',
                'symbol': '$',
                'exchange_rate': Decimal('1.00'),
                'is_base_currency': True
            }
        )
        
        eur, _ = Currency.objects.get_or_create(
            code='EUR',
            defaults={
                'name': 'Euro',
                'symbol': '€',
                'exchange_rate': Decimal('0.85')
            }
        )
        
        gbp, _ = Currency.objects.get_or_create(
            code='GBP',
            defaults={
                'name': 'British Pound',
                'symbol': '£',
                'exchange_rate': Decimal('0.79')
            }
        )
        
        # Create Account Types
        self.stdout.write('Creating account types...')
        account_types = [
            ('CASH', 'Cash', 'ASSET'),
            ('AR', 'Accounts Receivable', 'ASSET'),
            ('INV', 'Inventory', 'ASSET'),
            ('PPE', 'Property, Plant & Equipment', 'ASSET'),
            ('AP', 'Accounts Payable', 'LIABILITY'),
            ('LL', 'Long-term Liabilities', 'LIABILITY'),
            ('EQ', 'Owner\'s Equity', 'EQUITY'),
            ('REV', 'Revenue', 'REVENUE'),
            ('EXP', 'Operating Expenses', 'EXPENSE'),
        ]
        
        for code, name, category in account_types:
            AccountType.objects.get_or_create(
                code=code,
                defaults={'name': name, 'category': category}
            )
        
        # Create Accounts
        self.stdout.write('Creating accounts...')
        accounts_data = [
            ('1000', 'Cash - Operating', 'CASH', Decimal('1234567.89')),
            ('1100', 'Accounts Receivable', 'AR', Decimal('456789.12')),
            ('1200', 'Inventory', 'INV', Decimal('234567.89')),
            ('1500', 'Office Equipment', 'PPE', Decimal('123456.78')),
            ('2000', 'Accounts Payable', 'AP', Decimal('234567.89')),
            ('2100', 'Bank Loan', 'LL', Decimal('500000.00')),
            ('3000', 'Owner\'s Equity', 'EQ', Decimal('1000000.00')),
            ('4000', 'Sales Revenue', 'REV', Decimal('2485672.50')),
            ('5000', 'Office Expenses', 'EXP', Decimal('125000.00')),
            ('5100', 'Marketing Expenses', 'EXP', Decimal('85000.00')),
            ('5200', 'Travel Expenses', 'EXP', Decimal('45000.00')),
            ('5300', 'Technology Expenses', 'EXP', Decimal('120000.00')),
        ]
        
        for code, name, type_code, balance in accounts_data:
            account_type = AccountType.objects.get(code=type_code)
            Account.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'account_type': account_type,
                    'currency': usd,
                    'balance': balance,
                    'created_by': admin_user
                }
            )
        
        # Create Vendors
        self.stdout.write('Creating vendors...')
        vendors_data = [
            ('V001', 'Microsoft Corporation', 'licensing@microsoft.com', '+1-800-642-7676'),
            ('V002', 'Amazon Web Services', 'billing@aws.com', '+1-206-266-4064'),
            ('V003', 'Google Workspace', 'support@google.com', '+1-650-253-0000'),
            ('V004', 'Office Depot', 'business@officedepot.com', '+1-800-463-3768'),
            ('V005', 'FedEx Corporation', 'billing@fedex.com', '+1-800-463-3339'),
        ]
        
        for code, name, email, phone in vendors_data:
            Vendor.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'currency': usd,
                    'payment_terms': 30
                }
            )
        
        # Create Customers
        self.stdout.write('Creating customers...')
        customers_data = [
            ('C001', 'TechCorp Ltd', 'finance@techcorp.com', '+1-555-0001'),
            ('C002', 'Innovation Inc', 'billing@innovation.com', '+1-555-0002'),
            ('C003', 'Digital Solutions', 'accounts@digitalsol.com', '+1-555-0003'),
            ('C004', 'Future Tech', 'finance@futuretech.com', '+1-555-0004'),
            ('C005', 'Smart Systems', 'billing@smartsys.com', '+1-555-0005'),
            ('C006', 'CloudCorp', 'finance@cloudcorp.com', '+1-555-0006'),
            ('C007', 'DataDriven LLC', 'accounts@datadriven.com', '+1-555-0007'),
            ('C008', 'AI Innovations', 'billing@aiinnovations.com', '+1-555-0008'),
        ]
        
        for code, name, email, phone in customers_data:
            Customer.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'currency': usd,
                    'credit_limit': Decimal('100000.00'),
                    'payment_terms': 30
                }
            )
        
        # Create Sample Invoices
        self.stdout.write('Creating sample invoices...')
        customers = list(Customer.objects.all())
        vendors = list(Vendor.objects.all())
        
        for i in range(1, 26):  # 25 invoices
            customer = random.choice(customers) if i % 2 == 0 else None
            vendor = random.choice(vendors) if i % 2 == 1 else None
            
            invoice_date = timezone.now().date() - timedelta(days=random.randint(1, 90))
            due_date = invoice_date + timedelta(days=30)
            
            subtotal = Decimal(str(random.randint(10000, 100000)))
            tax_amount = subtotal * Decimal('0.08')  # 8% tax
            total_amount = subtotal + tax_amount
            
            status = random.choice(['DRAFT', 'SENT', 'PAID', 'OVERDUE'])
            paid_amount = total_amount if status == 'PAID' else Decimal('0.00')
            
            Invoice.objects.get_or_create(
                invoice_number=f'INV-2024-{i:03d}',
                defaults={
                    'invoice_type': 'SALES' if customer else 'PURCHASE',
                    'customer': customer,
                    'vendor': vendor,
                    'invoice_date': invoice_date,
                    'due_date': due_date,
                    'currency': usd,
                    'subtotal': subtotal,
                    'tax_amount': tax_amount,
                    'total_amount': total_amount,
                    'paid_amount': paid_amount,
                    'status': status,
                    'created_by': admin_user
                }
            )
        
        # Create Expense Categories
        self.stdout.write('Creating expense categories...')
        expense_categories = [
            ('TECH', 'Technology', '5300'),
            ('TRAVEL', 'Travel & Entertainment', '5200'),
            ('OFFICE', 'Office Supplies', '5000'),
            ('MARKETING', 'Marketing & Advertising', '5100'),
            ('ADMIN', 'Administrative', '5000'),
        ]
        
        for code, name, account_code in expense_categories:
            account = Account.objects.get(code=account_code)
            ExpenseCategory.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'account': account
                }
            )
        
        # Create Sample Expenses
        self.stdout.write('Creating sample expenses...')
        categories = list(ExpenseCategory.objects.all())
        
        expenses_data = [
            ('Software License - Adobe Creative Suite', 'TECH', 2400),
            ('Business Trip to New York', 'TRAVEL', 1850),
            ('Office Supplies - Q3', 'OFFICE', 450),
            ('Google Ads Campaign', 'MARKETING', 3200),
            ('Legal Consultation', 'ADMIN', 1500),
            ('AWS Cloud Services', 'TECH', 890),
            ('Conference Registration', 'TRAVEL', 650),
            ('Printer Cartridges', 'OFFICE', 180),
            ('Trade Show Booth', 'MARKETING', 4500),
            ('Accounting Software', 'ADMIN', 299),
        ]
        
        for i, (title, cat_code, amount) in enumerate(expenses_data, 1):
            category = ExpenseCategory.objects.get(code=cat_code)
            vendor = random.choice(vendors) if random.choice([True, False]) else None
            
            expense_date = timezone.now().date() - timedelta(days=random.randint(1, 60))
            status = random.choice(['DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED', 'PAID'])
            
            Expense.objects.get_or_create(
                expense_number=f'EXP-2024-{i:03d}',
                defaults={
                    'title': title,
                    'category': category,
                    'amount': Decimal(str(amount)),
                    'currency': usd,
                    'expense_date': expense_date,
                    'vendor': vendor,
                    'status': status,
                    'submitted_by': admin_user,
                    'approved_by': admin_user if status in ['APPROVED', 'PAID'] else None
                }
            )
        
        # Create Budget Categories
        self.stdout.write('Creating budget categories...')
        budget_categories = [
            ('OPS', 'Operations'),
            ('TECH', 'Technology'),
            ('MKT', 'Marketing'),
            ('ADMIN', 'Administration'),
            ('TRAVEL', 'Travel & Events'),
        ]
        
        for code, name in budget_categories:
            BudgetCategory.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
        
        # Create Sample Budget
        self.stdout.write('Creating sample budget...')
        current_year = timezone.now().year
        budget, created = Budget.objects.get_or_create(
            name=f'Annual Budget {current_year}',
            defaults={
                'period_type': 'YEARLY',
                'start_date': datetime(current_year, 1, 1).date(),
                'end_date': datetime(current_year, 12, 31).date(),
                'currency': usd,
                'total_budget': Decimal('500000.00'),
                'total_actual': Decimal('385000.00'),
                'created_by': admin_user
            }
        )
        
        if created:
            # Create Budget Lines
            budget_lines_data = [
                ('OPS', '5000', 150000, 128000),
                ('TECH', '5300', 120000, 95000),
                ('MKT', '5100', 100000, 85000),
                ('ADMIN', '5000', 80000, 77000),
                ('TRAVEL', '5200', 50000, 35000),
            ]
            
            for cat_code, acc_code, budgeted, actual in budget_lines_data:
                category = BudgetCategory.objects.get(code=cat_code)
                account = Account.objects.get(code=acc_code)
                
                BudgetLine.objects.create(
                    budget=budget,
                    category=category,
                    account=account,
                    budgeted_amount=Decimal(str(budgeted)),
                    actual_amount=Decimal(str(actual))
                )
        
        # Create AI Forecasts
        self.stdout.write('Creating AI forecasts...')
        forecast_types = ['REVENUE', 'EXPENSE', 'CASH_FLOW']
        
        for i, forecast_type in enumerate(forecast_types, 1):
            base_amount = random.randint(50000, 200000)
            confidence = random.uniform(0.75, 0.95)
            
            current_month_year = timezone.now().strftime("%B %Y")
            forecast_name = f'{forecast_type.title()} Forecast - {current_month_year}'
            
            FinancialForecast.objects.get_or_create(
                name=forecast_name,
                defaults={
                    'forecast_type': forecast_type,
                    'period_start': timezone.now().date(),
                    'period_end': timezone.now().date() + timedelta(days=30),
                    'currency': usd,
                    'predicted_amount': Decimal(str(base_amount)),
                    'confidence_score': Decimal(str(round(confidence, 4))),
                    'model_version': 'v1.0',
                    'training_data_points': random.randint(100, 500),
                    'created_by': admin_user
                }
            )
        
        # Create Sample Anomalies
        self.stdout.write('Creating sample anomalies...')
        anomaly_data = [
            ('UNUSUAL_TRANSACTION', 'HIGH', 'Large expense claim submitted outside business hours'),
            ('BUDGET_DEVIATION', 'MEDIUM', 'Marketing budget exceeded by 25%'),
            ('SUSPICIOUS_EXPENSE', 'LOW', 'Duplicate vendor payment detected'),
            ('CASH_FLOW_ANOMALY', 'MEDIUM', 'Unexpected cash flow variance detected'),
        ]
        
        for anomaly_type, severity, description in anomaly_data:
            score = random.uniform(0.6, 0.95)
            
            AnomalyDetection.objects.get_or_create(
                description=description,
                defaults={
                    'anomaly_type': anomaly_type,
                    'severity': severity,
                    'anomaly_score': Decimal(str(round(score, 4)))
                }
            )
        
        # Create Tax Authority and Rates
        self.stdout.write('Creating tax authorities and rates...')
        tax_authority, _ = TaxAuthority.objects.get_or_create(
            code='IRS',
            defaults={
                'name': 'Internal Revenue Service',
                'country': 'United States',
                'website': 'https://www.irs.gov'
            }
        )
        
        # Create some journal entries
        self.stdout.write('Creating sample journal entries...')
        cash_account = Account.objects.get(code='1000')
        revenue_account = Account.objects.get(code='4000')
        
        for i in range(5):
            entry_date = timezone.now().date() - timedelta(days=random.randint(1, 30))
            amount = Decimal(str(random.randint(5000, 50000)))
            
            journal_entry = JournalEntry.objects.create(
                entry_number=f'JE-2024-{i+1:03d}',
                date=entry_date,
                description=f'Sample journal entry {i+1}',
                total_amount=amount,
                status='POSTED',
                created_by=admin_user
            )
            
            # Debit Cash
            JournalEntryLine.objects.create(
                journal_entry=journal_entry,
                account=cash_account,
                debit_amount=amount,
                credit_amount=Decimal('0.00'),
                currency=usd
            )
            
            # Credit Revenue
            JournalEntryLine.objects.create(
                journal_entry=journal_entry,
                account=revenue_account,
                debit_amount=Decimal('0.00'),
                credit_amount=amount,
                currency=usd
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created comprehensive finance sample data with:\n'
                f'- {Currency.objects.count()} currencies\n'
                f'- {AccountType.objects.count()} account types\n'
                f'- {Account.objects.count()} accounts\n'
                f'- {Vendor.objects.count()} vendors\n'
                f'- {Customer.objects.count()} customers\n'
                f'- {Invoice.objects.count()} invoices\n'
                f'- {Expense.objects.count()} expenses\n'
                f'- {Budget.objects.count()} budgets\n'
                f'- {FinancialForecast.objects.count()} AI forecasts\n'
                f'- {AnomalyDetection.objects.count()} anomaly detections\n'
                f'- {JournalEntry.objects.count()} journal entries'
            )
        )
