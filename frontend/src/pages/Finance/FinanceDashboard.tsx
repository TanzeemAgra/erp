import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Tabs,
  Tab,
  Paper,
  Chip,
  Alert,
  LinearProgress,
  CircularProgress,
} from '@mui/material';
import {
  AccountBalance,
  TrendingUp,
  TrendingDown,
  AttachMoney,
  Receipt,
  Assessment,
  Warning,
  CheckCircle,
  CurrencyExchange,
  Add,
  Refresh,
  Download,
  Psychology,
} from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`finance-tabpanel-${index}`}
      aria-labelledby={`finance-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const FinanceDashboard: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<any>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const mockData = {
        total_revenue: 2485672.50,
        total_expenses: 1876234.30,
        net_profit: 609438.20,
        accounts_receivable: 456789.12,
        cash_balance: 1234567.89,
        profit_margin: 24.52,
      };
      
      setDashboardData(mockData);
      setLoading(false);
    };
    
    fetchDashboardData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh', flexDirection: 'column' }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading Finance Dashboard...</Typography>
        <Typography variant="body2" color="text.secondary">AI is analyzing your financial data</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            AI-Powered Finance Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Comprehensive financial management with artificial intelligence insights
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" startIcon={<Refresh />}>
            Refresh Data
          </Button>
          <Button variant="outlined" startIcon={<Download />}>
            Export Report
          </Button>
          <Button variant="contained" startIcon={<Psychology />}>
            AI Analysis
          </Button>
        </Box>
      </Box>

      {/* Key Metrics Cards */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
        gap: 3, 
        mb: 4 
      }}>
        <Card sx={{ background: 'linear-gradient(45deg, #2e7d32 30%, #4caf50 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Total Revenue
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  ${dashboardData?.total_revenue?.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">+12.5%</Typography>
                </Box>
              </Box>
              <AttachMoney sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Net Profit
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  ${dashboardData?.net_profit?.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">+8.2%</Typography>
                </Box>
              </Box>
              <TrendingUp sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #ed6c02 30%, #ff9800 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Cash Balance
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  ${dashboardData?.cash_balance?.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">+5.8%</Typography>
                </Box>
              </Box>
              <AccountBalance sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #9c27b0 30%, #e91e63 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Outstanding AR
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  ${dashboardData?.accounts_receivable?.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingDown sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">-3.1%</Typography>
                </Box>
              </Box>
              <Receipt sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Tab Navigation */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs 
          value={selectedTab} 
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab icon={<Assessment />} label="Analytics" />
          <Tab icon={<AccountBalance />} label="General Ledger" />
          <Tab icon={<Receipt />} label="Accounts" />
          <Tab icon={<AttachMoney />} label="Budgeting" />
          <Tab icon={<Receipt />} label="Expenses" />
          <Tab icon={<CurrencyExchange />} label="Multi-Currency" />
          <Tab icon={<Psychology />} label="AI Insights" />
        </Tabs>
      </Box>

      {/* Tab Content */}
      <TabPanel value={selectedTab} index={0}>
        <Alert severity="success" sx={{ mb: 3 }}>
          <Typography variant="body1">
            AI Analysis Complete: Your financial health score is <strong>85/100</strong> - Excellent performance!
          </Typography>
        </Alert>
        
        <Typography variant="h5" gutterBottom>
          Analytics Overview
        </Typography>
        
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
          gap: 3, 
          mt: 3 
        }}>
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Revenue vs Expenses Trend
            </Typography>
            <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                📊 Interactive Chart Component (Recharts Integration)
              </Typography>
            </Box>
          </Card>

          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Financial Health Score
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 200, flexDirection: 'column' }}>
              <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                <CircularProgress variant="determinate" value={85} size={120} thickness={4} />
                <Box sx={{
                  top: 0,
                  left: 0,
                  bottom: 0,
                  right: 0,
                  position: 'absolute',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}>
                  <Typography variant="h4" component="div" color="text.secondary">
                    85
                  </Typography>
                </Box>
              </Box>
              <Typography variant="h6" sx={{ mt: 2 }}>Excellent</Typography>
            </Box>
          </Card>
        </Box>
      </TabPanel>

      <TabPanel value={selectedTab} index={1}>
        <Typography variant="h5" gutterBottom>
          General Ledger
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Complete chart of accounts and journal entry management with double-entry bookkeeping.
        </Alert>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Chart of Accounts</Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 2 }}>
            <Box>
              <Typography variant="subtitle2" color="primary">Assets</Typography>
              <Typography variant="body2">• Cash - Operating: $1,234,568</Typography>
              <Typography variant="body2">• Accounts Receivable: $456,789</Typography>
              <Typography variant="body2">• Inventory: $234,568</Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2" color="error">Liabilities</Typography>
              <Typography variant="body2">• Accounts Payable: $234,568</Typography>
              <Typography variant="body2">• Bank Loan: $500,000</Typography>
              <Typography variant="body2">• Accrued Expenses: $45,000</Typography>
            </Box>
          </Box>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={2}>
        <Typography variant="h5" gutterBottom>
          Accounts Payable & Receivable
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Manage invoices, payments, and customer/vendor relationships efficiently.
        </Alert>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Outstanding Invoices</Typography>
          <Typography variant="body2" color="text.secondary">
            Real-time tracking of receivables and payables with aging reports and automated follow-ups.
          </Typography>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={3}>
        <Typography variant="h5" gutterBottom>
          Budgeting & Planning
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Create comprehensive budgets and track variance with AI-powered insights.
        </Alert>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Budget Performance</Typography>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2">Operations Budget</Typography>
            <LinearProgress variant="determinate" value={77} sx={{ mt: 1, mb: 1 }} />
            <Typography variant="caption">77% utilized - Under budget by 23%</Typography>
          </Box>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={4}>
        <Typography variant="h5" gutterBottom>
          Expense Management
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Track and approve expenses with intelligent categorization and receipt management.
        </Alert>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Recent Expenses</Typography>
          <Typography variant="body2" color="text.secondary">
            Automated expense categorization and approval workflows with mobile receipt capture.
          </Typography>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={5}>
        <Typography variant="h5" gutterBottom>
          Multi-Currency Operations
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Handle multiple currencies with real-time exchange rates and conversion tracking.
        </Alert>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Currency Breakdown</Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
            <Box>
              <Typography variant="subtitle2">USD</Typography>
              <Typography variant="h6">$1,234,567</Typography>
              <Typography variant="body2" color="text.secondary">65.2%</Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2">EUR</Typography>
              <Typography variant="h6">€423,681</Typography>
              <Typography variant="body2" color="text.secondary">22.4%</Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2">GBP</Typography>
              <Typography variant="h6">£234,567</Typography>
              <Typography variant="body2" color="text.secondary">12.4%</Typography>
            </Box>
          </Box>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={6}>
        <Typography variant="h5" gutterBottom>
          AI Insights & Predictions
        </Typography>
        <Alert severity="success" sx={{ mb: 3 }}>
          Advanced AI-powered financial forecasting and anomaly detection active.
        </Alert>
        
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 3 
        }}>
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom color="primary">
              🎯 Financial Forecasting
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              AI predicts next quarter revenue: <strong>$2.8M</strong> (confidence: 92%)
            </Typography>
            <LinearProgress variant="determinate" value={92} sx={{ mb: 1 }} />
            <Typography variant="caption">Prediction Confidence</Typography>
          </Card>

          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom color="warning.main">
              ⚠️ Anomaly Detection
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              2 unusual transactions detected in the last 30 days requiring review.
            </Typography>
            <Chip label="Review Required" color="warning" size="small" />
          </Card>

          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom color="success.main">
              ✅ Budget Insights
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Operating expenses are 8% under budget. Excellent cost management!
            </Typography>
            <Chip label="On Track" color="success" size="small" />
          </Card>
        </Box>
      </TabPanel>
    </Box>
  );
};

export default FinanceDashboard;
