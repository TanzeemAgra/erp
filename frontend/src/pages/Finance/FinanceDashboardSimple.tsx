import React from 'react';
import {
  Container,
  Paper,
  Typography,
  Card,
  CardContent,
  Box,
  Chip
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  AccountBalance,
  Receipt,
  CreditCard,
  Analytics
} from '@mui/icons-material';

interface MetricCardProps {
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  icon: React.ReactNode;
  color: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, change, trend, icon, color }) => (
  <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${color}20, ${color}10)` }}>
    <CardContent>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <Box sx={{ color: color, fontSize: 40 }}>
          {icon}
        </Box>
        <Chip
          icon={trend === 'up' ? <TrendingUp /> : <TrendingDown />}
          label={change}
          color={trend === 'up' ? 'success' : 'error'}
          size="small"
        />
      </Box>
      <Typography variant="h4" fontWeight="bold" color="text.primary">
        {value}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {title}
      </Typography>
    </CardContent>
  </Card>
);

const FinanceDashboardSimple: React.FC = () => {
  const financialMetrics = [
    {
      title: 'Total Revenue',
      value: '$2,450,000',
      change: '+12.5%',
      trend: 'up' as const,
      icon: <AccountBalance />,
      color: '#1976d2'
    },
    {
      title: 'Total Expenses',
      value: '$1,850,000',
      change: '+8.2%',
      trend: 'up' as const,
      icon: <Receipt />,
      color: '#d32f2f'
    },
    {
      title: 'Net Profit',
      value: '$600,000',
      change: '+18.9%',
      trend: 'up' as const,
      icon: <TrendingUp />,
      color: '#2e7d32'
    },
    {
      title: 'Cash Flow',
      value: '$420,000',
      change: '-3.1%',
      trend: 'down' as const,
      icon: <CreditCard />,
      color: '#ed6c02'
    },
    {
      title: 'Outstanding Invoices',
      value: '$180,000',
      change: '-15.6%',
      trend: 'down' as const,
      icon: <Analytics />,
      color: '#9c27b0'
    },
    {
      title: 'Monthly Growth',
      value: '24.8%',
      change: '+5.2%',
      trend: 'up' as const,
      icon: <TrendingUp />,
      color: '#00695c'
    }
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom fontWeight="bold" color="primary">
        Finance Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={4}>
        Overview of financial performance and key metrics
      </Typography>

      <Box 
        sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 3,
          mb: 3
        }}
      >
        {financialMetrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </Box>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Financial Summary
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This is a simplified finance dashboard. The complete financial management system 
          includes detailed reporting, budgeting, expense tracking, invoice management, 
          and comprehensive financial analytics.
        </Typography>
      </Paper>
    </Container>
  );
};

export default FinanceDashboardSimple;