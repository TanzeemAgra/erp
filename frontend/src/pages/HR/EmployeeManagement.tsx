import React, { useState, useEffect } from 'react';
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
  Avatar,
  Chip,
  IconButton,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Fab,
} from '@mui/material';
import {
  Search,
  Add,
  Edit,
  Delete,
  Email,
  Phone,
  FilterList,
} from '@mui/icons-material';

// Mock employee data
const mockEmployees = [
  {
    id: 1,
    username: 'john.doe',
    email: 'john.doe@company.com',
    first_name: 'John',
    last_name: 'Doe',
    phone_number: '+1 (555) 123-4567',
    employee_id: 'EMP001',
    department: 'Information Technology',
    designation: 'Senior Software Developer',
    joining_date: '2023-01-15',
    is_active: true,
  },
  {
    id: 2,
    username: 'sarah.smith',
    email: 'sarah.smith@company.com',
    first_name: 'Sarah',
    last_name: 'Smith',
    phone_number: '+1 (555) 234-5678',
    employee_id: 'EMP002',
    department: 'Human Resources',
    designation: 'HR Manager',
    joining_date: '2022-11-20',
    is_active: true,
  },
  {
    id: 3,
    username: 'mike.johnson',
    email: 'mike.johnson@company.com',
    first_name: 'Mike',
    last_name: 'Johnson',
    phone_number: '+1 (555) 345-6789',
    employee_id: 'EMP003',
    department: 'Information Technology',
    designation: 'Project Manager',
    joining_date: '2023-03-10',
    is_active: true,
  },
  {
    id: 4,
    username: 'emily.davis',
    email: 'emily.davis@company.com',
    first_name: 'Emily',
    last_name: 'Davis',
    phone_number: '+1 (555) 456-7890',
    employee_id: 'EMP004',
    department: 'Finance',
    designation: 'Finance Manager',
    joining_date: '2023-02-28',
    is_active: false,
  },
];

const departments = ['All', 'Information Technology', 'Human Resources', 'Finance', 'Operations'];

const EmployeeManagement: React.FC = () => {
  const [employees, setEmployees] = useState(mockEmployees);
  const [filteredEmployees, setFilteredEmployees] = useState(mockEmployees);
  const [searchTerm, setSearchTerm] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('All');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<any>(null);

  // Filter employees based on search and department
  useEffect(() => {
    let filtered = employees;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(
        (emp) =>
          emp.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          emp.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          emp.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
          emp.employee_id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Department filter
    if (departmentFilter !== 'All') {
      filtered = filtered.filter((emp) => emp.department === departmentFilter);
    }

    setFilteredEmployees(filtered);
  }, [employees, searchTerm, departmentFilter]);

  const handleAddEmployee = () => {
    setEditingEmployee(null);
    setOpenDialog(true);
  };

  const handleEditEmployee = (employee: any) => {
    setEditingEmployee(employee);
    setOpenDialog(true);
  };

  const handleDeleteEmployee = (id: number) => {
    setEmployees(employees.filter((emp) => emp.id !== id));
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingEmployee(null);
  };

  const getStatusChip = (isActive: boolean) => (
    <Chip
      label={isActive ? 'Active' : 'Inactive'}
      color={isActive ? 'success' : 'error'}
      size="small"
      variant="outlined"
    />
  );

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" fontWeight="bold">
          Employee Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleAddEmployee}
          sx={{ borderRadius: 2 }}
        >
          Add Employee
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, alignItems: 'center' }}>
            <Box sx={{ flex: 1 }}>
              <TextField
                fullWidth
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
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
              />
            </Box>
            <Box sx={{ minWidth: 200 }}>
              <FormControl fullWidth>
                <InputLabel>Department</InputLabel>
                <Select
                  value={departmentFilter}
                  label="Department"
                  onChange={(e) => setDepartmentFilter(e.target.value)}
                  sx={{ borderRadius: 2 }}
                >
                  {departments.map((dept) => (
                    <MenuItem key={dept} value={dept}>
                      {dept}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ minWidth: 150 }}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<FilterList />}
                sx={{ py: 1.5, borderRadius: 2 }}
              >
                More Filters
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Employee Table */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow sx={{ bgcolor: 'grey.50' }}>
                  <TableCell>Employee</TableCell>
                  <TableCell>Contact</TableCell>
                  <TableCell>Department</TableCell>
                  <TableCell>Designation</TableCell>
                  <TableCell>Joining Date</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredEmployees.map((employee) => (
                  <TableRow key={employee.id} hover>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Avatar
                          sx={{
                            bgcolor: 'primary.main',
                            width: 40,
                            height: 40,
                          }}
                        >
                          {employee.first_name.charAt(0)}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle2" fontWeight="medium">
                            {employee.first_name} {employee.last_name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {employee.employee_id}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                          <Email fontSize="small" color="action" />
                          <Typography variant="body2">{employee.email}</Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Phone fontSize="small" color="action" />
                          <Typography variant="body2">{employee.phone_number}</Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{employee.department}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{employee.designation}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(employee.joining_date).toLocaleDateString()}
                      </Typography>
                    </TableCell>
                    <TableCell>{getStatusChip(employee.is_active)}</TableCell>
                    <TableCell align="center">
                      <IconButton
                        size="small"
                        onClick={() => handleEditEmployee(employee)}
                        sx={{ mr: 1 }}
                      >
                        <Edit fontSize="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteEmployee(employee.id)}
                        color="error"
                      >
                        <Delete fontSize="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Add/Edit Employee Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingEmployee ? 'Edit Employee' : 'Add New Employee'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ 
            display: 'grid', 
            gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
            gap: 2,
            mt: 1 
          }}>
            <Box>
              <TextField
                fullWidth
                label="First Name"
                defaultValue={editingEmployee?.first_name || ''}
                required
              />
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Last Name"
                defaultValue={editingEmployee?.last_name || ''}
                required
              />
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Email"
                type="email"
                defaultValue={editingEmployee?.email || ''}
                required
              />
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Phone Number"
                defaultValue={editingEmployee?.phone_number || ''}
              />
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Employee ID"
                defaultValue={editingEmployee?.employee_id || ''}
                required
              />
            </Box>
            <Box>
              <FormControl fullWidth>
                <InputLabel>Department</InputLabel>
                <Select
                  defaultValue={editingEmployee?.department || ''}
                  label="Department"
                >
                  {departments.filter(d => d !== 'All').map((dept) => (
                    <MenuItem key={dept} value={dept}>
                      {dept}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Designation"
                defaultValue={editingEmployee?.designation || ''}
              />
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Joining Date"
                type="date"
                defaultValue={editingEmployee?.joining_date || ''}
                InputLabelProps={{ shrink: true }}
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button variant="contained" onClick={handleCloseDialog}>
            {editingEmployee ? 'Update' : 'Add'} Employee
          </Button>
        </DialogActions>
      </Dialog>

      {/* Floating Action Button */}
      <Fab
        color="primary"
        aria-label="add"
        onClick={handleAddEmployee}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
        }}
      >
        <Add />
      </Fab>
    </Box>
  );
};

export default EmployeeManagement;
