import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Avatar,
  Tabs,
  Tab,
  LinearProgress,
  Snackbar,
  Alert,
  Tooltip,
  Fab,
  Menu,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  Add as AddIcon,
  Business as BusinessIcon,
  Person as PersonIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
  TrendingUp as TrendingUpIcon,
  Assignment as AssignmentIcon,
  Schedule as ScheduleIcon,
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  CallMade as CallIcon,
  MonetizationOn as MoneyIcon,
  Assessment as AssessmentIcon,
  Group as GroupIcon,
  FilterList as FilterIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format } from 'date-fns';

// API Base URL
const API_BASE = 'http://127.0.0.1:8000/api/v1/crm';

interface Client {
  id: number;
  company_name: string;
  contact_person: string;
  email: string;
  phone: string;
  website?: string;
  industry: string;
  industry_display: string;
  category: string;
  category_display: string;
  status: string;
  status_display: string;
  city: string;
  state: string;
  country: string;
  account_manager?: number;
  account_manager_name?: string;
  assigned_to?: number;
  assigned_to_name?: string;
  first_contact_date: string;
  last_contact_date?: string;
  next_follow_up?: string;
  contacts_count: number;
  interactions_count: number;
  opportunities_count: number;
  tasks_count: number;
  created_at: string;
  updated_at: string;
}

interface DashboardStats {
  total_clients: number;
  total_leads: number;
  total_opportunities: number;
  total_opportunity_value: number;
  pending_tasks: number;
  recent_interactions: number;
  clients_by_status: Array<{ status: string; count: number }>;
  clients_by_industry: Array<{ industry: string; count: number }>;
  opportunities_by_stage: Array<{ stage: string; count: number }>;
  monthly_interactions: Array<{ month: string; count: number }>;
}

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  full_name: string;
}

interface Choices {
  client_categories: Array<{ value: string; label: string }>;
  client_statuses: Array<{ value: string; label: string }>;
  industries: Array<{ value: string; label: string }>;
  interaction_types: Array<{ value: string; label: string }>;
  opportunity_stages: Array<{ value: string; label: string }>;
  task_priorities: Array<{ value: string; label: string }>;
  task_statuses: Array<{ value: string; label: string }>;
}

const ClientManagement: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [clients, setClients] = useState<Client[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [choices, setChoices] = useState<Choices | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);
  const [clientDialogOpen, setClientDialogOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const [filterStatus, setFilterStatus] = useState('');
  const [filterIndustry, setFilterIndustry] = useState('');

  // Form state
  const [clientForm, setClientForm] = useState({
    company_name: '',
    contact_person: '',
    email: '',
    phone: '',
    website: '',
    industry: 'other',
    company_size: '',
    annual_revenue: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'United States',
    category: 'lead',
    status: 'potential',
    source: '',
    account_manager: '',
    assigned_to: '',
    credit_limit: '',
    payment_terms: '',
    notes: '',
    tags: ''
  });

  // Fetch data functions
  const fetchClients = async () => {
    try {
      let url = `${API_BASE}/clients/`;
      const params = new URLSearchParams();
      if (filterStatus) params.append('status', filterStatus);
      if (filterIndustry) params.append('industry', filterIndustry);
      if (params.toString()) url += `?${params.toString()}`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch clients');
      const data = await response.json();
      setClients(data.results || data);
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to load clients', severity: 'error' });
    }
  };

  const fetchDashboard = async () => {
    try {
      const response = await fetch(`${API_BASE}/clients/dashboard/`);
      if (!response.ok) throw new Error('Failed to fetch dashboard');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to load dashboard', severity: 'error' });
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_BASE}/users/`);
      if (!response.ok) throw new Error('Failed to fetch users');
      const data = await response.json();
      setUsers(data.results || data);
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to load users', severity: 'error' });
    }
  };

  const fetchChoices = async () => {
    try {
      const response = await fetch(`${API_BASE}/choices/`);
      if (!response.ok) throw new Error('Failed to fetch choices');
      const data = await response.json();
      setChoices(data);
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to load choices', severity: 'error' });
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchClients(), fetchDashboard(), fetchUsers(), fetchChoices()]);
      setLoading(false);
    };
    loadData();
  }, [filterStatus, filterIndustry]);

  const handleClientSubmit = async () => {
    try {
      const url = selectedClient
        ? `${API_BASE}/clients/${selectedClient.id}/`
        : `${API_BASE}/clients/`;
      
      const method = selectedClient ? 'PUT' : 'POST';
      
      const formData = {
        ...clientForm,
        company_size: clientForm.company_size ? parseInt(clientForm.company_size) : null,
        annual_revenue: clientForm.annual_revenue ? parseFloat(clientForm.annual_revenue) : null,
        credit_limit: clientForm.credit_limit ? parseFloat(clientForm.credit_limit) : null,
        account_manager: clientForm.account_manager || null,
        assigned_to: clientForm.assigned_to || null,
      };

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Failed to save client');

      setSnackbar({ open: true, message: 'Client saved successfully!', severity: 'success' });
      setClientDialogOpen(false);
      fetchClients();
      fetchDashboard();
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to save client', severity: 'error' });
    }
  };

  const handleEditClient = (client: Client) => {
    setSelectedClient(client);
    setClientForm({
      company_name: client.company_name,
      contact_person: client.contact_person,
      email: client.email,
      phone: client.phone,
      website: client.website || '',
      industry: client.industry,
      company_size: '',
      annual_revenue: '',
      address_line1: '',
      address_line2: '',
      city: client.city,
      state: client.state,
      postal_code: '',
      country: client.country,
      category: client.category,
      status: client.status,
      source: '',
      account_manager: client.account_manager?.toString() || '',
      assigned_to: client.assigned_to?.toString() || '',
      credit_limit: '',
      payment_terms: '',
      notes: '',
      tags: ''
    });
    setClientDialogOpen(true);
  };

  const handleAddClient = () => {
    setSelectedClient(null);
    setClientForm({
      company_name: '',
      contact_person: '',
      email: '',
      phone: '',
      website: '',
      industry: 'other',
      company_size: '',
      annual_revenue: '',
      address_line1: '',
      address_line2: '',
      city: '',
      state: '',
      postal_code: '',
      country: 'United States',
      category: 'lead',
      status: 'potential',
      source: '',
      account_manager: '',
      assigned_to: '',
      credit_limit: '',
      payment_terms: '',
      notes: '',
      tags: ''
    });
    setClientDialogOpen(true);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'potential': return 'warning';
      case 'inactive': return 'default';
      case 'lost': return 'error';
      default: return 'default';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'lead': return 'info';
      case 'prospect': return 'warning';
      case 'customer': return 'success';
      case 'partner': return 'secondary';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <LinearProgress sx={{ width: '50%', mb: 2 }} />
        <Typography>Loading CRM...</Typography>
      </Box>
    );
  }

  const TabPanel = ({ children, value, index }: { children: React.ReactNode; value: number; index: number }) => (
    <Box role="tabpanel" hidden={value !== index} sx={{ pt: 3 }}>
      {value === index && children}
    </Box>
  );

  const StatsCard = ({ icon, value, label, color = 'primary.main' }: { icon: React.ReactNode; value: number | string; label: string; color?: string }) => (
    <Card sx={{ textAlign: 'center', p: 2, minHeight: 120 }}>
      <Box sx={{ color, fontSize: 40, mb: 1 }}>{icon}</Box>
      <Typography variant="h4" fontWeight="bold">{value}</Typography>
      <Typography variant="body2" color="text.secondary">{label}</Typography>
    </Card>
  );

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        {/* Header */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Box>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
              Client Relationship Management
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Manage your clients, opportunities, and business relationships
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddClient}
            size="large"
            sx={{ borderRadius: 2 }}
          >
            Add Client
          </Button>
        </Box>

        {/* Tabs */}
        <Tabs value={selectedTab} onChange={(_, newValue) => setSelectedTab(newValue)} sx={{ mb: 3 }}>
          <Tab icon={<AssessmentIcon />} label="Dashboard" />
          <Tab icon={<BusinessIcon />} label="Clients" />
          <Tab icon={<TrendingUpIcon />} label="Opportunities" />
          <Tab icon={<AssignmentIcon />} label="Tasks" />
        </Tabs>

        {/* Dashboard Tab */}
        <TabPanel value={selectedTab} index={0}>
          {stats && (
            <Box>
              {/* Stats Cards */}
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(3, 1fr)', lg: 'repeat(6, 1fr)' }, gap: 3, mb: 4 }}>
                <StatsCard
                  icon={<BusinessIcon />}
                  value={stats.total_clients}
                  label="Total Clients"
                  color="primary.main"
                />
                <StatsCard
                  icon={<PersonIcon />}
                  value={stats.total_leads}
                  label="Leads"
                  color="info.main"
                />
                <StatsCard
                  icon={<TrendingUpIcon />}
                  value={stats.total_opportunities}
                  label="Opportunities"
                  color="success.main"
                />
                <StatsCard
                  icon={<MoneyIcon />}
                  value={`$${stats.total_opportunity_value.toLocaleString()}`}
                  label="Pipeline Value"
                  color="warning.main"
                />
                <StatsCard
                  icon={<AssignmentIcon />}
                  value={stats.pending_tasks}
                  label="Pending Tasks"
                  color="error.main"
                />
                <StatsCard
                  icon={<CallIcon />}
                  value={stats.recent_interactions}
                  label="Recent Interactions"
                  color="secondary.main"
                />
              </Box>

              {/* Charts Section */}
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
                <Card sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>Clients by Status</Typography>
                  {stats.clients_by_status.map((item, index) => (
                    <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                        {item.status}
                      </Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {item.count}
                      </Typography>
                    </Box>
                  ))}
                </Card>

                <Card sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>Clients by Industry</Typography>
                  {stats.clients_by_industry.slice(0, 5).map((item, index) => (
                    <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                        {item.industry}
                      </Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {item.count}
                      </Typography>
                    </Box>
                  ))}
                </Card>
              </Box>
            </Box>
          )}
        </TabPanel>

        {/* Clients Tab */}
        <TabPanel value={selectedTab} index={1}>
          {/* Filters */}
          <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Status</InputLabel>
              <Select
                value={filterStatus}
                label="Status"
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                {choices?.client_statuses.map((status) => (
                  <MenuItem key={status.value} value={status.value}>
                    {status.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Industry</InputLabel>
              <Select
                value={filterIndustry}
                label="Industry"
                onChange={(e) => setFilterIndustry(e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                {choices?.industries.map((industry) => (
                  <MenuItem key={industry.value} value={industry.value}>
                    {industry.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          {/* Clients Table */}
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Company</TableCell>
                  <TableCell>Contact Person</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Phone</TableCell>
                  <TableCell>Category</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Industry</TableCell>
                  <TableCell>Location</TableCell>
                  <TableCell>Manager</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {clients.map((client) => (
                  <TableRow key={client.id}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                          {client.company_name.charAt(0)}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle2">{client.company_name}</Typography>
                          {client.website && (
                            <Typography variant="caption" color="text.secondary">
                              {client.website}
                            </Typography>
                          )}
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>{client.contact_person}</TableCell>
                    <TableCell>{client.email}</TableCell>
                    <TableCell>{client.phone}</TableCell>
                    <TableCell>
                      <Chip
                        label={client.category_display}
                        color={getCategoryColor(client.category) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={client.status_display}
                        color={getStatusColor(client.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{client.industry_display}</TableCell>
                    <TableCell>{client.city}, {client.state}</TableCell>
                    <TableCell>{client.account_manager_name || 'Unassigned'}</TableCell>
                    <TableCell>
                      <IconButton onClick={() => handleEditClient(client)} size="small">
                        <EditIcon />
                      </IconButton>
                      <IconButton size="small">
                        <ViewIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Client Dialog */}
        <Dialog open={clientDialogOpen} onClose={() => setClientDialogOpen(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            {selectedClient ? 'Edit Client' : 'Add New Client'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2, mt: 1 }}>
              <TextField
                fullWidth
                label="Company Name"
                value={clientForm.company_name}
                onChange={(e) => setClientForm({ ...clientForm, company_name: e.target.value })}
                required
              />
              <TextField
                fullWidth
                label="Contact Person"
                value={clientForm.contact_person}
                onChange={(e) => setClientForm({ ...clientForm, contact_person: e.target.value })}
                required
              />
              <TextField
                fullWidth
                label="Email"
                type="email"
                value={clientForm.email}
                onChange={(e) => setClientForm({ ...clientForm, email: e.target.value })}
                required
              />
              <TextField
                fullWidth
                label="Phone"
                value={clientForm.phone}
                onChange={(e) => setClientForm({ ...clientForm, phone: e.target.value })}
                required
              />
              <TextField
                fullWidth
                label="Website"
                value={clientForm.website}
                onChange={(e) => setClientForm({ ...clientForm, website: e.target.value })}
              />
              <FormControl fullWidth>
                <InputLabel>Industry</InputLabel>
                <Select
                  value={clientForm.industry}
                  label="Industry"
                  onChange={(e) => setClientForm({ ...clientForm, industry: e.target.value })}
                >
                  {choices?.industries.map((industry) => (
                    <MenuItem key={industry.value} value={industry.value}>
                      {industry.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={clientForm.category}
                  label="Category"
                  onChange={(e) => setClientForm({ ...clientForm, category: e.target.value })}
                >
                  {choices?.client_categories.map((category) => (
                    <MenuItem key={category.value} value={category.value}>
                      {category.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={clientForm.status}
                  label="Status"
                  onChange={(e) => setClientForm({ ...clientForm, status: e.target.value })}
                >
                  {choices?.client_statuses.map((status) => (
                    <MenuItem key={status.value} value={status.value}>
                      {status.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="Address"
                value={clientForm.address_line1}
                onChange={(e) => setClientForm({ ...clientForm, address_line1: e.target.value })}
                sx={{ mb: 2 }}
              />
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 2, mb: 2 }}>
                <TextField
                  fullWidth
                  label="City"
                  value={clientForm.city}
                  onChange={(e) => setClientForm({ ...clientForm, city: e.target.value })}
                />
                <TextField
                  fullWidth
                  label="State"
                  value={clientForm.state}
                  onChange={(e) => setClientForm({ ...clientForm, state: e.target.value })}
                />
                <TextField
                  fullWidth
                  label="Country"
                  value={clientForm.country}
                  onChange={(e) => setClientForm({ ...clientForm, country: e.target.value })}
                />
              </Box>
              <TextField
                fullWidth
                label="Notes"
                multiline
                rows={3}
                value={clientForm.notes}
                onChange={(e) => setClientForm({ ...clientForm, notes: e.target.value })}
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setClientDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleClientSubmit} variant="contained">
              {selectedClient ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Snackbar */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </LocalizationProvider>
  );
};

export default ClientManagement;
