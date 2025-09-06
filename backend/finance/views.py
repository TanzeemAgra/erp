from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q, F, Count
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random
import json

from .models import (
    Currency, AccountType, Account, JournalEntry, JournalEntryLine,
    Vendor, Customer, Invoice, BudgetCategory, Budget, BudgetLine,
    ExpenseCategory, Expense, TaxAuthority, TaxRate,
    FinancialForecast, AnomalyDetection
)
from .serializers import (
    CurrencySerializer, AccountTypeSerializer, AccountSerializer,
    JournalEntrySerializer, JournalEntryLineSerializer,
    VendorSerializer, CustomerSerializer, InvoiceSerializer,
    BudgetCategorySerializer, BudgetSerializer, BudgetLineSerializer,
    ExpenseCategorySerializer, ExpenseSerializer,
    TaxAuthoritySerializer, TaxRateSerializer,
    FinancialForecastSerializer, AnomalyDetectionSerializer,
    FinanceDashboardSerializer
)

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def update_exchange_rates(self, request):
        """AI-powered exchange rate updates (mock implementation)"""
        currencies = Currency.objects.filter(is_active=True, is_base_currency=False)
        
        for currency in currencies:
            # Mock AI prediction for exchange rates
            variance = random.uniform(-0.05, 0.05)  # ±5% variance
            new_rate = currency.exchange_rate * (1 + variance)
            currency.exchange_rate = round(new_rate, 6)
            currency.save()
        
        return Response({'message': 'Exchange rates updated successfully'})

class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated]

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def chart_of_accounts(self, request):
        """Get structured chart of accounts"""
        accounts = Account.objects.filter(is_active=True).select_related('account_type', 'currency')
        
        chart = {}
        for account in accounts:
            category = account.account_type.category
            if category not in chart:
                chart[category] = []
            
            chart[category].append({
                'id': account.id,
                'code': account.code,
                'name': account.name,
                'balance': account.balance,
                'currency': account.currency.code,
                'account_type': account.account_type.name
            })
        
        return Response(chart)

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def post_entry(self, request, pk=None):
        """Post a journal entry and update account balances"""
        entry = self.get_object()
        
        if entry.status == 'POSTED':
            return Response({'error': 'Entry already posted'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate that debits equal credits
        total_debits = entry.lines.aggregate(Sum('debit_amount'))['debit_amount__sum'] or 0
        total_credits = entry.lines.aggregate(Sum('credit_amount'))['credit_amount__sum'] or 0
        
        if total_debits != total_credits:
            return Response({'error': 'Debits must equal credits'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update account balances
        for line in entry.lines.all():
            account = line.account
            if account.account_type.category in ['ASSET', 'EXPENSE']:
                account.balance += (line.debit_amount - line.credit_amount)
            else:  # LIABILITY, EQUITY, REVENUE
                account.balance += (line.credit_amount - line.debit_amount)
            account.save()
        
        entry.status = 'POSTED'
        entry.save()
        
        return Response({'message': 'Journal entry posted successfully'})

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue invoices"""
        overdue_invoices = Invoice.objects.filter(
            due_date__lt=timezone.now().date(),
            status__in=['SENT']
        )
        serializer = self.get_serializer(overdue_invoices, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def aging_report(self, request):
        """AI-powered aging analysis"""
        today = timezone.now().date()
        
        aging_buckets = {
            'current': Invoice.objects.filter(due_date__gte=today, status='SENT'),
            '1-30_days': Invoice.objects.filter(
                due_date__lt=today,
                due_date__gte=today - timedelta(days=30),
                status='SENT'
            ),
            '31-60_days': Invoice.objects.filter(
                due_date__lt=today - timedelta(days=30),
                due_date__gte=today - timedelta(days=60),
                status='SENT'
            ),
            '61-90_days': Invoice.objects.filter(
                due_date__lt=today - timedelta(days=60),
                due_date__gte=today - timedelta(days=90),
                status='SENT'
            ),
            'over_90_days': Invoice.objects.filter(
                due_date__lt=today - timedelta(days=90),
                status='SENT'
            )
        }
        
        aging_report = {}
        for bucket, queryset in aging_buckets.items():
            aging_report[bucket] = {
                'count': queryset.count(),
                'total_amount': queryset.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            }
        
        return Response(aging_report)

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def variance_analysis(self, request, pk=None):
        """AI-powered budget variance analysis"""
        budget = self.get_object()
        
        variances = []
        for line in budget.budget_lines.all():
            variance_pct = 0
            if line.budgeted_amount > 0:
                variance_pct = (line.variance / line.budgeted_amount) * 100
            
            variances.append({
                'category': line.category.name,
                'budgeted': line.budgeted_amount,
                'actual': line.actual_amount,
                'variance': line.variance,
                'variance_percentage': round(variance_pct, 2),
                'status': 'over' if line.variance > 0 else 'under'
            })
        
        # AI insights (mock)
        insights = []
        for variance in variances:
            if abs(variance['variance_percentage']) > 20:
                insights.append({
                    'category': variance['category'],
                    'message': f"Significant variance detected: {variance['variance_percentage']:.1f}%",
                    'recommendation': "Review spending patterns and adjust future budgets"
                })
        
        return Response({
            'variances': variances,
            'ai_insights': insights
        })

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """AI-powered expense analytics"""
        # Expense trends
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_expenses = Expense.objects.filter(expense_date__gte=thirty_days_ago)
        
        # Category breakdown
        category_breakdown = recent_expenses.values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Monthly trends
        monthly_trends = []
        for i in range(6):
            month_start = (timezone.now() - timedelta(days=30*i)).replace(day=1).date()
            month_end = (month_start.replace(month=month_start.month % 12 + 1, year=month_start.year + (month_start.month // 12)) - timedelta(days=1))
            
            month_total = Expense.objects.filter(
                expense_date__gte=month_start,
                expense_date__lte=month_end,
                status='APPROVED'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            monthly_trends.append({
                'month': month_start.strftime('%B %Y'),
                'total': month_total
            })
        
        return Response({
            'category_breakdown': list(category_breakdown),
            'monthly_trends': monthly_trends,
            'total_pending': recent_expenses.filter(status='SUBMITTED').aggregate(Sum('amount'))['amount__sum'] or 0
        })

class FinancialForecastViewSet(viewsets.ModelViewSet):
    queryset = FinancialForecast.objects.all()
    serializer_class = FinancialForecastSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_forecast(self, request):
        """AI-powered financial forecasting"""
        forecast_type = request.data.get('forecast_type', 'REVENUE')
        period_days = int(request.data.get('period_days', 30))
        
        # Mock AI forecasting logic
        historical_data = self._get_historical_data(forecast_type, period_days * 2)
        predicted_amount = self._predict_amount(historical_data)
        confidence_score = random.uniform(0.7, 0.95)
        
        forecast = FinancialForecast.objects.create(
            name=f"{forecast_type} Forecast - {timezone.now().date()}",
            forecast_type=forecast_type,
            period_start=timezone.now().date(),
            period_end=timezone.now().date() + timedelta(days=period_days),
            currency=Currency.objects.filter(is_base_currency=True).first(),
            predicted_amount=predicted_amount,
            confidence_score=confidence_score,
            model_version="v1.0",
            training_data_points=len(historical_data),
            created_by=request.user
        )
        
        serializer = self.get_serializer(forecast)
        return Response(serializer.data)
    
    def _get_historical_data(self, forecast_type, days):
        """Get historical data for forecasting"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        if forecast_type == 'REVENUE':
            return list(Invoice.objects.filter(
                invoice_type='SALES',
                invoice_date__gte=start_date,
                status='PAID'
            ).values_list('total_amount', flat=True))
        elif forecast_type == 'EXPENSE':
            return list(Expense.objects.filter(
                expense_date__gte=start_date,
                status='APPROVED'
            ).values_list('amount', flat=True))
        
        return []
    
    def _predict_amount(self, historical_data):
        """Simple prediction algorithm (in real implementation, use ML models)"""
        if not historical_data:
            return Decimal('0.00')
        
        # Simple moving average with trend
        avg = sum(historical_data) / len(historical_data)
        trend = random.uniform(0.95, 1.15)  # ±15% trend
        
        return Decimal(str(round(avg * trend, 2)))

class AnomalyDetectionViewSet(viewsets.ModelViewSet):
    queryset = AnomalyDetection.objects.all()
    serializer_class = AnomalyDetectionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def run_detection(self, request):
        """Run AI-powered anomaly detection"""
        anomalies_found = []
        
        # Detect unusual transactions
        unusual_transactions = self._detect_unusual_transactions()
        anomalies_found.extend(unusual_transactions)
        
        # Detect budget deviations
        budget_deviations = self._detect_budget_deviations()
        anomalies_found.extend(budget_deviations)
        
        # Detect suspicious expenses
        suspicious_expenses = self._detect_suspicious_expenses()
        anomalies_found.extend(suspicious_expenses)
        
        return Response({
            'anomalies_detected': len(anomalies_found),
            'anomalies': anomalies_found
        })
    
    def _detect_unusual_transactions(self):
        """Detect unusual journal entries"""
        anomalies = []
        
        # Find transactions significantly larger than average
        avg_amount = JournalEntry.objects.filter(status='POSTED').aggregate(
            avg=Sum('total_amount')
        )['avg'] or 0
        
        unusual_entries = JournalEntry.objects.filter(
            total_amount__gt=avg_amount * 3,  # 3x average
            status='POSTED'
        )
        
        for entry in unusual_entries:
            anomaly = AnomalyDetection.objects.create(
                anomaly_type='UNUSUAL_TRANSACTION',
                severity='MEDIUM',
                description=f"Transaction amount ({entry.total_amount}) is significantly higher than average ({avg_amount:.2f})",
                related_transaction=entry,
                anomaly_score=0.75
            )
            anomalies.append(AnomalyDetectionSerializer(anomaly).data)
        
        return anomalies
    
    def _detect_budget_deviations(self):
        """Detect significant budget deviations"""
        anomalies = []
        
        # Find budget lines with >50% variance
        significant_variances = BudgetLine.objects.filter(
            budget__is_active=True
        ).annotate(
            variance_pct=F('variance') / F('budgeted_amount') * 100
        ).filter(variance_pct__gt=50)
        
        for line in significant_variances:
            severity = 'HIGH' if line.variance > line.budgeted_amount else 'MEDIUM'
            anomaly = AnomalyDetection.objects.create(
                anomaly_type='BUDGET_DEVIATION',
                severity=severity,
                description=f"Budget variance of {line.variance} detected for {line.category.name}",
                anomaly_score=0.85
            )
            anomalies.append(AnomalyDetectionSerializer(anomaly).data)
        
        return anomalies
    
    def _detect_suspicious_expenses(self):
        """Detect potentially suspicious expenses"""
        anomalies = []
        
        # Find expenses submitted outside business hours or on weekends
        suspicious_expenses = Expense.objects.filter(
            created_at__week_day__in=[1, 7],  # Sunday=1, Saturday=7
            status='SUBMITTED'
        )
        
        for expense in suspicious_expenses:
            anomaly = AnomalyDetection.objects.create(
                anomaly_type='SUSPICIOUS_EXPENSE',
                severity='LOW',
                description=f"Expense submitted on weekend: {expense.title}",
                related_expense=expense,
                anomaly_score=0.45
            )
            anomalies.append(AnomalyDetectionSerializer(anomaly).data)
        
        return anomalies

class FinanceDashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get comprehensive finance dashboard data"""
        
        # Basic financial metrics
        revenue_accounts = Account.objects.filter(account_type__category='REVENUE')
        expense_accounts = Account.objects.filter(account_type__category='EXPENSE')
        asset_accounts = Account.objects.filter(account_type__category='ASSET')
        liability_accounts = Account.objects.filter(account_type__category='LIABILITY')
        equity_accounts = Account.objects.filter(account_type__category='EQUITY')
        
        total_revenue = revenue_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        total_expenses = expense_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        total_assets = asset_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        total_liabilities = liability_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        total_equity = equity_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Cash and receivables
        cash_accounts = asset_accounts.filter(name__icontains='cash')
        cash_balance = cash_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        accounts_receivable = Invoice.objects.filter(
            invoice_type='SALES',
            status__in=['SENT']
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        accounts_payable = Invoice.objects.filter(
            invoice_type='PURCHASE',
            status__in=['SENT']
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Recent data
        recent_invoices = Invoice.objects.all()[:5]
        recent_expenses = Expense.objects.all()[:5]
        overdue_invoices = Invoice.objects.filter(
            due_date__lt=timezone.now().date(),
            status='SENT'
        )[:5]
        pending_expenses = Expense.objects.filter(status='SUBMITTED')[:5]
        
        # AI insights
        recent_anomalies = AnomalyDetection.objects.filter(
            is_resolved=False
        ).order_by('-detection_date')[:5]
        
        recent_forecasts = FinancialForecast.objects.all()[:3]
        
        # Chart data (mock data for demonstration)
        revenue_chart = self._generate_chart_data('revenue')
        expense_chart = self._generate_chart_data('expense')
        cash_flow_chart = self._generate_chart_data('cash_flow')
        budget_variance_chart = self._generate_chart_data('budget_variance')
        
        # Currency breakdown
        currency_breakdown = {}
        for currency in Currency.objects.filter(is_active=True):
            currency_accounts = Account.objects.filter(currency=currency)
            total_balance = currency_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
            currency_breakdown[currency.code] = {
                'total_balance': total_balance,
                'exchange_rate': currency.exchange_rate
            }
        
        # KPIs
        profit_margin = (total_revenue - total_expenses) / total_revenue * 100 if total_revenue > 0 else 0
        current_ratio = total_assets / total_liabilities if total_liabilities > 0 else 0
        debt_ratio = total_liabilities / total_assets if total_assets > 0 else 0
        roe = (total_revenue - total_expenses) / total_equity * 100 if total_equity > 0 else 0
        
        dashboard_data = {
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_profit': total_revenue - total_expenses,
            'accounts_receivable': accounts_receivable,
            'accounts_payable': accounts_payable,
            'cash_balance': cash_balance,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'total_equity': total_equity,
            'recent_invoices': InvoiceSerializer(recent_invoices, many=True).data,
            'recent_expenses': ExpenseSerializer(recent_expenses, many=True).data,
            'overdue_invoices': InvoiceSerializer(overdue_invoices, many=True).data,
            'pending_expenses': ExpenseSerializer(pending_expenses, many=True).data,
            'anomalies': AnomalyDetectionSerializer(recent_anomalies, many=True).data,
            'forecasts': FinancialForecastSerializer(recent_forecasts, many=True).data,
            'revenue_chart': revenue_chart,
            'expense_chart': expense_chart,
            'cash_flow_chart': cash_flow_chart,
            'budget_variance_chart': budget_variance_chart,
            'currency_breakdown': currency_breakdown,
            'profit_margin': round(profit_margin, 2),
            'current_ratio': round(current_ratio, 2),
            'debt_ratio': round(debt_ratio, 2),
            'roe': round(roe, 2)
        }
        
        return Response(dashboard_data)
    
    def _generate_chart_data(self, chart_type):
        """Generate mock chart data"""
        months = []
        values = []
        
        for i in range(6):
            month_date = timezone.now() - timedelta(days=30*i)
            months.append(month_date.strftime('%b %Y'))
            
            if chart_type == 'revenue':
                values.append(random.randint(50000, 150000))
            elif chart_type == 'expense':
                values.append(random.randint(30000, 80000))
            elif chart_type == 'cash_flow':
                values.append(random.randint(-20000, 50000))
            elif chart_type == 'budget_variance':
                values.append(random.randint(-15, 25))
        
        return {
            'labels': list(reversed(months)),
            'data': list(reversed(values))
        }
