import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tab,
  Tabs,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Search,
  Download,
  Payment,
  Schedule,
  TrendingUp,
  Person,
  CalendarToday,
  AccessTime,
  AttachMoney,
  Add,
  Edit,
  Visibility,
} from '@mui/icons-material';

interface Employee {
  id: string;
  name: string;
  department: string;
  position: string;
  salary: number;
  attendance: {
    present: number;
    absent: number;
    late: number;
    overtime: number;
  };
  lastPayroll: string;
  status: 'Active' | 'On Leave' | 'Terminated';
}

interface PayrollRecord {
  id: string;
  employeeId: string;
  employeeName: string;
  month: string;
  basicSalary: number;
  allowances: number;
  deductions: number;
  netSalary: number;
  status: 'Paid' | 'Pending' | 'Processing';
}

interface AttendanceRecord {
  id: string;
  employeeId: string;
  employeeName: string;
  date: string;
  timeIn: string;
  timeOut: string;
  hours: number;
  status: 'Present' | 'Absent' | 'Late' | 'Half Day';
}

const PayrollAttendance: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('All');
  const [monthFilter, setMonthFilter] = useState('December 2024');
  const [dialogOpen, setDialogOpen] = useState(false);

  // Mock data
  const mockEmployees: Employee[] = [
    {
      id: 'EMP001',
      name: 'John Doe',
      department: 'Engineering',
      position: 'Senior Developer',
      salary: 85000,
      attendance: { present: 22, absent: 1, late: 2, overtime: 15 },
      lastPayroll: '2024-11-30',
      status: 'Active',
    },
    {
      id: 'EMP002',
      name: 'Jane Smith',
      department: 'HR',
      position: 'HR Manager',
      salary: 75000,
      attendance: { present: 23, absent: 0, late: 0, overtime: 5 },
      lastPayroll: '2024-11-30',
      status: 'Active',
    },
    {
      id: 'EMP003',
      name: 'Mike Johnson',
      department: 'Marketing',
      position: 'Marketing Specialist',
      salary: 65000,
      attendance: { present: 20, absent: 3, late: 1, overtime: 8 },
      lastPayroll: '2024-11-30',
      status: 'Active',
    },
  ];

  const mockPayrollRecords: PayrollRecord[] = [
    {
      id: 'PAY001',
      employeeId: 'EMP001',
      employeeName: 'John Doe',
      month: 'December 2024',
      basicSalary: 85000,
      allowances: 5000,
      deductions: 8500,
      netSalary: 81500,
      status: 'Paid',
    },
    {
      id: 'PAY002',
      employeeId: 'EMP002',
      employeeName: 'Jane Smith',
      month: 'December 2024',
      basicSalary: 75000,
      allowances: 3000,
      deductions: 7500,
      netSalary: 70500,
      status: 'Processing',
    },
  ];

  const mockAttendanceRecords: AttendanceRecord[] = [
    {
      id: 'ATT001',
      employeeId: 'EMP001',
      employeeName: 'John Doe',
      date: '2024-12-20',
      timeIn: '09:00',
      timeOut: '18:00',
      hours: 9,
      status: 'Present',
    },
    {
      id: 'ATT002',
      employeeId: 'EMP002',
      employeeName: 'Jane Smith',
      date: '2024-12-20',
      timeIn: '09:15',
      timeOut: '18:00',
      hours: 8.75,
      status: 'Late',
    },
  ];

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Paid':
      case 'Present':
        return 'success';
      case 'Processing':
      case 'Late':
        return 'warning';
      case 'Pending':
      case 'Absent':
        return 'error';
      default:
        return 'default';
    }
  };

  const totalPayroll = mockPayrollRecords.reduce((sum, record) => sum + record.netSalary, 0);
  const avgAttendance = mockEmployees.reduce((sum, emp) => sum + emp.attendance.present, 0) / mockEmployees.length;

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
          Payroll & Attendance System
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage employee payroll, attendance tracking, and time management
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' },
        gap: 3,
        mb: 4 
      }}>
        <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  ${(totalPayroll / 1000).toFixed(0)}K
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Monthly Payroll
                </Typography>
              </Box>
              <AttachMoney sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {avgAttendance.toFixed(1)}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Avg Attendance
                </Typography>
              </Box>
              <Schedule sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {mockPayrollRecords.filter(p => p.status === 'Processing').length}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Processing
                </Typography>
              </Box>
              <Payment sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  96%
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Attendance Rate
                </Typography>
              </Box>
              <TrendingUp sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Tabs */}
      <Card sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="payroll attendance tabs">
          <Tab label="Payroll Management" />
          <Tab label="Attendance Tracking" />
          <Tab label="Time Sheets" />
        </Tabs>
      </Card>

      {/* Search and Filter Section */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', md: '1fr auto auto auto' },
        gap: 2,
        mb: 3 
      }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search employees..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
        <FormControl variant="outlined" sx={{ minWidth: 150 }}>
          <InputLabel>Department</InputLabel>
          <Select
            value={departmentFilter}
            onChange={(e) => setDepartmentFilter(e.target.value)}
            label="Department"
          >
            <MenuItem value="All">All Departments</MenuItem>
            <MenuItem value="Engineering">Engineering</MenuItem>
            <MenuItem value="HR">HR</MenuItem>
            <MenuItem value="Marketing">Marketing</MenuItem>
          </Select>
        </FormControl>
        <FormControl variant="outlined" sx={{ minWidth: 150 }}>
          <InputLabel>Month</InputLabel>
          <Select
            value={monthFilter}
            onChange={(e) => setMonthFilter(e.target.value)}
            label="Month"
          >
            <MenuItem value="December 2024">December 2024</MenuItem>
            <MenuItem value="November 2024">November 2024</MenuItem>
            <MenuItem value="October 2024">October 2024</MenuItem>
          </Select>
        </FormControl>
        <Button
          variant="contained"
          startIcon={<Download />}
          sx={{ minWidth: 150 }}
        >
          Export Report
        </Button>
      </Box>

      {/* Tab Content */}
      {tabValue === 0 && (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" fontWeight="bold">
                Payroll Records
              </Typography>
              <Button variant="contained" startIcon={<Add />}>
                Process Payroll
              </Button>
            </Box>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Employee</TableCell>
                    <TableCell>Month</TableCell>
                    <TableCell>Basic Salary</TableCell>
                    <TableCell>Allowances</TableCell>
                    <TableCell>Deductions</TableCell>
                    <TableCell>Net Salary</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockPayrollRecords.map((record) => (
                    <TableRow key={record.id}>
                      <TableCell>{record.employeeName}</TableCell>
                      <TableCell>{record.month}</TableCell>
                      <TableCell>${record.basicSalary.toLocaleString()}</TableCell>
                      <TableCell>${record.allowances.toLocaleString()}</TableCell>
                      <TableCell>${record.deductions.toLocaleString()}</TableCell>
                      <TableCell>
                        <Typography fontWeight="bold">
                          ${record.netSalary.toLocaleString()}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={record.status} 
                          color={getStatusColor(record.status) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Tooltip title="View Details">
                          <IconButton size="small">
                            <Visibility />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit">
                          <IconButton size="small">
                            <Edit />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {tabValue === 1 && (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" fontWeight="bold">
                Daily Attendance
              </Typography>
              <Button variant="contained" startIcon={<Add />}>
                Mark Attendance
              </Button>
            </Box>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Employee</TableCell>
                    <TableCell>Date</TableCell>
                    <TableCell>Time In</TableCell>
                    <TableCell>Time Out</TableCell>
                    <TableCell>Total Hours</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockAttendanceRecords.map((record) => (
                    <TableRow key={record.id}>
                      <TableCell>{record.employeeName}</TableCell>
                      <TableCell>{record.date}</TableCell>
                      <TableCell>{record.timeIn}</TableCell>
                      <TableCell>{record.timeOut}</TableCell>
                      <TableCell>{record.hours}h</TableCell>
                      <TableCell>
                        <Chip 
                          label={record.status} 
                          color={getStatusColor(record.status) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Tooltip title="Edit">
                          <IconButton size="small">
                            <Edit />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {tabValue === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Employee Time Sheets
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Detailed time tracking and overtime management coming soon...
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default PayrollAttendance;
