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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Fab,
} from '@mui/material';
import {
  Inventory,
  LocalShipping,
  Factory,
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  Add,
  Edit,
  Delete,
  Visibility,
  Assignment,
  Build,
  ShoppingCart,
  Receipt,
  Analytics,
  PrecisionManufacturing,
  Store,
  Psychology,
  Timeline,
  Notifications,
  Assessment,
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
      id={`asset-tabpanel-${index}`}
      aria-labelledby={`asset-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const AssetManagement: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const mockData = {
        // Asset Dashboard
        assets: {
          total_assets: 1247,
          active_assets: 1156,
          maintenance_due: 23,
          total_value: 8750000,
          depreciation_this_year: 425000
        },
        // Inventory Dashboard
        inventory: {
          total_items: 3450,
          low_stock_items: 45,
          total_stock_value: 2850000,
          pending_pos: 12,
          recent_movements: 156
        },
        // Supply Chain Dashboard
        supply_chain: {
          active_vendors: 89,
          pending_deliveries: 23,
          overdue_deliveries: 5,
          average_lead_time: 12.5,
          vendor_performance: 87.5
        },
        // Recent data
        recent_assets: [
          { id: 1, asset_tag: 'AST-001', name: 'Dell Laptop ProBook', status: 'ACTIVE', value: 1250 },
          { id: 2, asset_tag: 'AST-002', name: 'Conference Room Projector', status: 'MAINTENANCE', value: 850 },
          { id: 3, asset_tag: 'AST-003', name: 'Server Rack Unit', status: 'ACTIVE', value: 5500 }
        ],
        low_stock_items: [
          { id: 1, sku: 'SKU-001', name: 'A4 Paper Reams', current_stock: 5, reorder_level: 20 },
          { id: 2, sku: 'SKU-002', name: 'Printer Toner Cartridge', current_stock: 2, reorder_level: 10 },
          { id: 3, sku: 'SKU-003', name: 'Network Cables Cat6', current_stock: 8, reorder_level: 25 }
        ],
        recent_pos: [
          { id: 1, po_number: 'PO-2025-001', vendor: 'Tech Solutions Ltd', status: 'CONFIRMED', amount: 25000 },
          { id: 2, po_number: 'PO-2025-002', vendor: 'Office Supplies Co', status: 'PENDING', amount: 1500 },
          { id: 3, po_number: 'PO-2025-003', vendor: 'Hardware Express', status: 'DELIVERED', amount: 8750 }
        ],
        demand_forecasts: [
          { item: 'Office Chairs', predicted_demand: 45, confidence: 92, period: '30 days' },
          { item: 'Laptop Batteries', predicted_demand: 23, confidence: 87, period: '30 days' },
          { item: 'Network Equipment', predicted_demand: 12, confidence: 78, period: '30 days' }
        ]
      };
      
      setDashboardData(mockData);
      setLoading(false);
    };
    
    fetchDashboardData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const handleOpenDialog = (type: string) => {
    setDialogType(type);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setDialogType('');
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh', flexDirection: 'column' }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading Asset Management System...</Typography>
        <Typography variant="body2" color="text.secondary">Initializing inventory and supply chain data</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Asset & Supply Chain Management
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Comprehensive asset tracking, inventory management, and intelligent supply chain optimization
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" startIcon={<Analytics />}>
            Reports
          </Button>
          <Button variant="outlined" startIcon={<Psychology />}>
            AI Insights
          </Button>
          <Button variant="contained" startIcon={<Add />} onClick={() => handleOpenDialog('asset')}>
            Add Asset
          </Button>
        </Box>
      </Box>

      {/* Key Metrics Dashboard */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: 3, 
        mb: 4 
      }}>
        {/* Asset Metrics */}
        <Card sx={{ background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Total Assets
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  {dashboardData?.assets?.total_assets?.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">+5.2% this month</Typography>
                </Box>
              </Box>
              <Inventory sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #2e7d32 30%, #4caf50 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Stock Value
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  ${(dashboardData?.inventory?.total_stock_value / 1000000).toFixed(1)}M
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">+8.7% vs last month</Typography>
                </Box>
              </Box>
              <Store sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #ed6c02 30%, #ff9800 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Active Vendors
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  {dashboardData?.supply_chain?.active_vendors}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <CheckCircle sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">{dashboardData?.supply_chain?.vendor_performance}% performance</Typography>
                </Box>
              </Box>
              <LocalShipping sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #d32f2f 30%, #f44336 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Alerts & Issues
                </Typography>
                <Typography variant="h4" fontWeight="bold">
                  {dashboardData?.inventory?.low_stock_items + dashboardData?.supply_chain?.overdue_deliveries}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <Warning sx={{ fontSize: 16, mr: 0.5 }} />
                  <Typography variant="body2">Needs attention</Typography>
                </Box>
              </Box>
              <Notifications sx={{ fontSize: 40, opacity: 0.8 }} />
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
          <Tab icon={<Assessment />} label="Dashboard" />
          <Tab icon={<Inventory />} label="Assets" />
          <Tab icon={<Store />} label="Inventory" />
          <Tab icon={<LocalShipping />} label="Supply Chain" />
          <Tab icon={<ShoppingCart />} label="Purchase Orders" />
          <Tab icon={<Receipt />} label="Goods Receipt" />
          <Tab icon={<Build />} label="Maintenance" />
          <Tab icon={<Psychology />} label="AI Forecasting" />
        </Tabs>
      </Box>

      {/* Tab Content */}
      <TabPanel value={selectedTab} index={0}>
        <Typography variant="h5" gutterBottom>
          Executive Dashboard
        </Typography>
        
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
          gap: 3, 
          mt: 3 
        }}>
          {/* Asset Status Chart */}
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Asset Status Distribution
            </Typography>
            <Box sx={{ height: 250, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
              <Box sx={{ position: 'relative', display: 'inline-flex', mb: 2 }}>
                <CircularProgress 
                  variant="determinate" 
                  value={(dashboardData?.assets?.active_assets / dashboardData?.assets?.total_assets) * 100} 
                  size={120} 
                  thickness={4} 
                />
                <Box sx={{ position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Typography variant="h6" component="div" color="text.secondary">
                    {Math.round((dashboardData?.assets?.active_assets / dashboardData?.assets?.total_assets) * 100)}%
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">Assets Active</Typography>
            </Box>
          </Card>

          {/* Low Stock Alerts */}
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom color="warning.main">
              ⚠️ Low Stock Alerts
            </Typography>
            <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
              {dashboardData?.low_stock_items?.map((item: any) => (
                <Box key={item.id} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', py: 1, borderBottom: '1px solid #eee' }}>
                  <Box>
                    <Typography variant="body2" fontWeight="bold">{item.name}</Typography>
                    <Typography variant="caption" color="text.secondary">{item.sku}</Typography>
                  </Box>
                  <Chip 
                    label={`${item.current_stock}/${item.reorder_level}`} 
                    color="warning" 
                    size="small" 
                  />
                </Box>
              ))}
            </Box>
          </Card>
        </Box>
      </TabPanel>

      <TabPanel value={selectedTab} index={1}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5">Fixed Assets Management</Typography>
          <Button variant="contained" startIcon={<Add />} onClick={() => handleOpenDialog('asset')}>
            Add New Asset
          </Button>
        </Box>
        
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Asset Tag</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Current Value</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {dashboardData?.recent_assets?.map((asset: any) => (
                <TableRow key={asset.id}>
                  <TableCell>{asset.asset_tag}</TableCell>
                  <TableCell>{asset.name}</TableCell>
                  <TableCell>
                    <Chip 
                      label={asset.status} 
                      color={asset.status === 'ACTIVE' ? 'success' : 'warning'} 
                      size="small" 
                    />
                  </TableCell>
                  <TableCell>${asset.value.toLocaleString()}</TableCell>
                  <TableCell>
                    <IconButton size="small"><Visibility /></IconButton>
                    <IconButton size="small"><Edit /></IconButton>
                    <IconButton size="small"><Assignment /></IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={selectedTab} index={2}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5">Inventory & Stock Management</Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button variant="outlined" startIcon={<Analytics />}>Stock Report</Button>
            <Button variant="contained" startIcon={<Add />} onClick={() => handleOpenDialog('inventory')}>
              Add Item
            </Button>
          </Box>
        </Box>

        <Alert severity="info" sx={{ mb: 3 }}>
          {dashboardData?.inventory?.low_stock_items} items are below reorder level. Consider creating purchase orders.
        </Alert>

        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Stock Summary</Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
            <Box>
              <Typography variant="body2" color="text.secondary">Total Items</Typography>
              <Typography variant="h6">{dashboardData?.inventory?.total_items}</Typography>
            </Box>
            <Box>
              <Typography variant="body2" color="text.secondary">Stock Value</Typography>
              <Typography variant="h6">${(dashboardData?.inventory?.total_stock_value / 1000).toFixed(0)}K</Typography>
            </Box>
            <Box>
              <Typography variant="body2" color="text.secondary">Recent Movements</Typography>
              <Typography variant="h6">{dashboardData?.inventory?.recent_movements}</Typography>
            </Box>
          </Box>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={3}>
        <Typography variant="h5" gutterBottom>Supply Chain Management</Typography>
        
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 3, 
          mb: 3 
        }}>
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Vendor Performance</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h4" color="primary">
                {dashboardData?.supply_chain?.vendor_performance}%
              </Typography>
              <Typography variant="body2" sx={{ ml: 1 }}>Average Rating</Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={dashboardData?.supply_chain?.vendor_performance} 
              sx={{ mb: 1 }} 
            />
          </Card>

          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Delivery Metrics</Typography>
            <Typography variant="body2" color="text.secondary">Average Lead Time</Typography>
            <Typography variant="h4" color="primary">
              {dashboardData?.supply_chain?.average_lead_time} days
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              {dashboardData?.supply_chain?.overdue_deliveries} overdue deliveries
            </Typography>
          </Card>
        </Box>

        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Vendor Management</Typography>
          <Typography variant="body2" color="text.secondary">
            Manage supplier relationships, track performance, and optimize procurement processes.
          </Typography>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={4}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5">Purchase Orders</Typography>
          <Button variant="contained" startIcon={<Add />} onClick={() => handleOpenDialog('po')}>
            Create PO
          </Button>
        </Box>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>PO Number</TableCell>
                <TableCell>Vendor</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Amount</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {dashboardData?.recent_pos?.map((po: any) => (
                <TableRow key={po.id}>
                  <TableCell>{po.po_number}</TableCell>
                  <TableCell>{po.vendor}</TableCell>
                  <TableCell>
                    <Chip 
                      label={po.status} 
                      color={po.status === 'DELIVERED' ? 'success' : po.status === 'CONFIRMED' ? 'primary' : 'warning'} 
                      size="small" 
                    />
                  </TableCell>
                  <TableCell>${po.amount.toLocaleString()}</TableCell>
                  <TableCell>
                    <IconButton size="small"><Visibility /></IconButton>
                    <IconButton size="small"><Edit /></IconButton>
                    <IconButton size="small"><Receipt /></IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={selectedTab} index={5}>
        <Typography variant="h5" gutterBottom>Goods Receipt Notes (GRN)</Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Process incoming deliveries and update stock levels automatically with quality checks.
        </Alert>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Recent Receipts</Typography>
          <Typography variant="body2" color="text.secondary">
            Track received goods, quality inspection, and automatic stock updates.
          </Typography>
        </Paper>
      </TabPanel>

      <TabPanel value={selectedTab} index={6}>
        <Typography variant="h5" gutterBottom>Maintenance Management</Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 3 
        }}>
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>🔧 Scheduled Maintenance</Typography>
            <Typography variant="h4" color="primary" gutterBottom>
              {dashboardData?.assets?.maintenance_due}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Assets due for maintenance in next 7 days
            </Typography>
          </Card>

          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>💰 Maintenance Costs</Typography>
            <Typography variant="h4" color="primary" gutterBottom>
              $45,250
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total maintenance cost this quarter
            </Typography>
          </Card>
        </Box>
      </TabPanel>

      <TabPanel value={selectedTab} index={7}>
        <Typography variant="h5" gutterBottom>AI-Powered Demand Forecasting</Typography>
        <Alert severity="success" sx={{ mb: 3 }}>
          Machine learning algorithms analyze historical data to predict future demand patterns.
        </Alert>
        
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 3 
        }}>
          {dashboardData?.demand_forecasts?.map((forecast: any, index: number) => (
            <Card key={index} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom color="primary">
                🎯 {forecast.item}
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Predicted demand: <strong>{forecast.predicted_demand} units</strong> in {forecast.period}
              </Typography>
              <LinearProgress variant="determinate" value={forecast.confidence} sx={{ mb: 1 }} />
              <Typography variant="caption">{forecast.confidence}% Confidence</Typography>
            </Card>
          ))}
        </Box>
      </TabPanel>

      {/* Floating Action Button */}
      <Fab 
        color="primary" 
        aria-label="add" 
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => handleOpenDialog('quick-action')}
      >
        <Add />
      </Fab>

      {/* Dialogs */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {dialogType === 'asset' && 'Add New Asset'}
          {dialogType === 'inventory' && 'Add Inventory Item'}
          {dialogType === 'po' && 'Create Purchase Order'}
          {dialogType === 'quick-action' && 'Quick Actions'}
        </DialogTitle>
        <DialogContent>
          {dialogType === 'asset' && (
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2, mt: 2 }}>
              <TextField fullWidth label="Asset Name" />
              <TextField fullWidth label="Asset Tag" />
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select defaultValue="">
                  <MenuItem value="IT">IT Equipment</MenuItem>
                  <MenuItem value="FURNITURE">Furniture</MenuItem>
                  <MenuItem value="VEHICLE">Vehicles</MenuItem>
                </Select>
              </FormControl>
              <TextField fullWidth label="Purchase Cost" type="number" />
            </Box>
          )}
          {dialogType === 'inventory' && (
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2, mt: 2 }}>
              <TextField fullWidth label="Item Name" />
              <TextField fullWidth label="SKU" />
              <TextField fullWidth label="Unit Cost" type="number" />
              <TextField fullWidth label="Reorder Level" type="number" />
            </Box>
          )}
          {dialogType === 'quick-action' && (
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2, mt: 2 }}>
              <Button variant="outlined" startIcon={<Add />} fullWidth>Add Asset</Button>
              <Button variant="outlined" startIcon={<Store />} fullWidth>Add Inventory</Button>
              <Button variant="outlined" startIcon={<ShoppingCart />} fullWidth>Create PO</Button>
              <Button variant="outlined" startIcon={<Build />} fullWidth>Schedule Maintenance</Button>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AssetManagement;
