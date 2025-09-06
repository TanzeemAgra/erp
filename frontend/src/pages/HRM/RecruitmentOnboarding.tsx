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
  LinearProgress,
  IconButton,
  Tooltip,
  Tab,
  Tabs,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import {
  Search,
  People,
  PersonAdd,
  School,
  Work,
  TrendingUp,
  Add,
  Edit,
  Visibility,
  Download,
  CheckCircle,
  Schedule,
  Assignment,
} from '@mui/icons-material';

interface JobPosting {
  id: string;
  title: string;
  department: string;
  location: string;
  type: 'Full-time' | 'Part-time' | 'Contract' | 'Internship';
  level: 'Entry' | 'Mid' | 'Senior' | 'Executive';
  applicants: number;
  status: 'Active' | 'Closed' | 'Draft' | 'On Hold';
  postedDate: string;
  deadline: string;
}

interface Candidate {
  id: string;
  name: string;
  email: string;
  phone: string;
  position: string;
  experience: number;
  education: string;
  skills: string[];
  stage: 'Applied' | 'Screening' | 'Interview' | 'Assessment' | 'Offer' | 'Hired' | 'Rejected';
  rating: number;
  appliedDate: string;
  source: 'Website' | 'LinkedIn' | 'Referral' | 'Job Board';
}

interface OnboardingTask {
  id: string;
  employeeId: string;
  employeeName: string;
  task: string;
  category: 'Documentation' | 'Training' | 'Setup' | 'Orientation';
  assignedTo: string;
  dueDate: string;
  status: 'Pending' | 'In Progress' | 'Completed' | 'Overdue';
  priority: 'High' | 'Medium' | 'Low';
}

const RecruitmentOnboarding: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [dialogOpen, setDialogOpen] = useState(false);

  // Mock data
  const mockJobPostings: JobPosting[] = [
    {
      id: 'JOB001',
      title: 'Senior Frontend Developer',
      department: 'Engineering',
      location: 'Remote',
      type: 'Full-time',
      level: 'Senior',
      applicants: 45,
      status: 'Active',
      postedDate: '2024-11-15',
      deadline: '2025-01-15',
    },
    {
      id: 'JOB002',
      title: 'HR Generalist',
      department: 'HR',
      location: 'New York',
      type: 'Full-time',
      level: 'Mid',
      applicants: 28,
      status: 'Active',
      postedDate: '2024-12-01',
      deadline: '2025-01-31',
    },
    {
      id: 'JOB003',
      title: 'Marketing Intern',
      department: 'Marketing',
      location: 'San Francisco',
      type: 'Internship',
      level: 'Entry',
      applicants: 67,
      status: 'Closed',
      postedDate: '2024-10-15',
      deadline: '2024-12-15',
    },
  ];

  const mockCandidates: Candidate[] = [
    {
      id: 'CAN001',
      name: 'Alice Johnson',
      email: 'alice.johnson@email.com',
      phone: '+1-555-0123',
      position: 'Senior Frontend Developer',
      experience: 5,
      education: 'MS Computer Science',
      skills: ['React', 'TypeScript', 'Node.js', 'AWS'],
      stage: 'Interview',
      rating: 4.5,
      appliedDate: '2024-11-20',
      source: 'LinkedIn',
    },
    {
      id: 'CAN002',
      name: 'Bob Wilson',
      email: 'bob.wilson@email.com',
      phone: '+1-555-0124',
      position: 'HR Generalist',
      experience: 3,
      education: 'BA Human Resources',
      skills: ['Recruitment', 'Employee Relations', 'HRIS'],
      stage: 'Assessment',
      rating: 4.2,
      appliedDate: '2024-12-05',
      source: 'Website',
    },
    {
      id: 'CAN003',
      name: 'Carol Davis',
      email: 'carol.davis@email.com',
      phone: '+1-555-0125',
      position: 'Marketing Intern',
      experience: 0,
      education: 'BA Marketing (In Progress)',
      skills: ['Social Media', 'Content Creation', 'Analytics'],
      stage: 'Offer',
      rating: 4.0,
      appliedDate: '2024-10-20',
      source: 'Referral',
    },
  ];

  const mockOnboardingTasks: OnboardingTask[] = [
    {
      id: 'TASK001',
      employeeId: 'EMP004',
      employeeName: 'David Miller',
      task: 'Complete I-9 Form',
      category: 'Documentation',
      assignedTo: 'HR Team',
      dueDate: '2024-12-25',
      status: 'Pending',
      priority: 'High',
    },
    {
      id: 'TASK002',
      employeeId: 'EMP004',
      employeeName: 'David Miller',
      task: 'IT Equipment Setup',
      category: 'Setup',
      assignedTo: 'IT Department',
      dueDate: '2024-12-24',
      status: 'In Progress',
      priority: 'High',
    },
    {
      id: 'TASK003',
      employeeId: 'EMP005',
      employeeName: 'Emma Brown',
      task: 'Company Orientation',
      category: 'Orientation',
      assignedTo: 'HR Team',
      dueDate: '2024-12-23',
      status: 'Completed',
      priority: 'Medium',
    },
  ];

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active':
      case 'Completed':
      case 'Hired':
        return 'success';
      case 'In Progress':
      case 'Interview':
      case 'Assessment':
        return 'primary';
      case 'Pending':
      case 'Applied':
      case 'Screening':
        return 'warning';
      case 'Closed':
      case 'Rejected':
      case 'Overdue':
        return 'error';
      case 'Offer':
        return 'info';
      default:
        return 'default';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Full-time':
        return 'primary';
      case 'Part-time':
        return 'secondary';
      case 'Contract':
        return 'warning';
      case 'Internship':
        return 'info';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'error';
      case 'Medium':
        return 'warning';
      case 'Low':
        return 'success';
      default:
        return 'default';
    }
  };

  const activeJobs = mockJobPostings.filter(job => job.status === 'Active').length;
  const totalApplicants = mockJobPostings.reduce((sum, job) => sum + job.applicants, 0);
  const candidatesInPipeline = mockCandidates.filter(c => !['Hired', 'Rejected'].includes(c.stage)).length;
  const completedTasks = mockOnboardingTasks.filter(task => task.status === 'Completed').length;

  const onboardingSteps = ['Applied', 'Screening', 'Interview', 'Assessment', 'Offer', 'Hired'];

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
          Recruitment & Onboarding
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage job postings, candidate pipeline, and employee onboarding process
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
                  {activeJobs}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Active Jobs
                </Typography>
              </Box>
              <Work sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {totalApplicants}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Total Applicants
                </Typography>
              </Box>
              <People sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {candidatesInPipeline}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  In Pipeline
                </Typography>
              </Box>
              <TrendingUp sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {Math.round((completedTasks / mockOnboardingTasks.length) * 100)}%
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Onboarding
                </Typography>
              </Box>
              <CheckCircle sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Tabs */}
      <Card sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="recruitment tabs">
          <Tab label="Job Postings" />
          <Tab label="Candidate Pipeline" />
          <Tab label="Onboarding" />
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
          placeholder="Search..."
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
          <InputLabel>Status</InputLabel>
          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            label="Status"
          >
            <MenuItem value="All">All Status</MenuItem>
            <MenuItem value="Active">Active</MenuItem>
            <MenuItem value="Closed">Closed</MenuItem>
            <MenuItem value="Draft">Draft</MenuItem>
          </Select>
        </FormControl>
        <Button
          variant="contained"
          startIcon={<Add />}
          sx={{ minWidth: 150 }}
        >
          {tabValue === 0 ? 'Post Job' : tabValue === 1 ? 'Add Candidate' : 'New Employee'}
        </Button>
      </Box>

      {/* Tab Content */}
      {tabValue === 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Job Postings
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Position</TableCell>
                    <TableCell>Department</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Level</TableCell>
                    <TableCell>Applicants</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Deadline</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockJobPostings.map((job) => (
                    <TableRow key={job.id}>
                      <TableCell>
                        <Box>
                          <Typography variant="body2" fontWeight="bold">
                            {job.title}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {job.location}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>{job.department}</TableCell>
                      <TableCell>
                        <Chip 
                          label={job.type} 
                          color={getTypeColor(job.type) as any}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>{job.level}</TableCell>
                      <TableCell>
                        <Typography variant="body2" fontWeight="bold">
                          {job.applicants}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={job.status} 
                          color={getStatusColor(job.status) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{job.deadline}</TableCell>
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
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Candidate Pipeline
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Candidate</TableCell>
                    <TableCell>Position</TableCell>
                    <TableCell>Experience</TableCell>
                    <TableCell>Skills</TableCell>
                    <TableCell>Stage</TableCell>
                    <TableCell>Rating</TableCell>
                    <TableCell>Source</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockCandidates.map((candidate) => (
                    <TableRow key={candidate.id}>
                      <TableCell>
                        <Box>
                          <Typography variant="body2" fontWeight="bold">
                            {candidate.name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {candidate.email}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>{candidate.position}</TableCell>
                      <TableCell>{candidate.experience} years</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {candidate.skills.slice(0, 2).map((skill) => (
                            <Chip key={skill} label={skill} size="small" variant="outlined" />
                          ))}
                          {candidate.skills.length > 2 && (
                            <Chip label={`+${candidate.skills.length - 2}`} size="small" variant="outlined" />
                          )}
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={candidate.stage} 
                          color={getStatusColor(candidate.stage) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {candidate.rating}/5.0
                        </Typography>
                      </TableCell>
                      <TableCell>{candidate.source}</TableCell>
                      <TableCell>
                        <Tooltip title="View Profile">
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

      {tabValue === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Onboarding Tasks
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Employee</TableCell>
                    <TableCell>Task</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Assigned To</TableCell>
                    <TableCell>Due Date</TableCell>
                    <TableCell>Priority</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockOnboardingTasks.map((task) => (
                    <TableRow key={task.id}>
                      <TableCell>{task.employeeName}</TableCell>
                      <TableCell>{task.task}</TableCell>
                      <TableCell>
                        <Chip 
                          label={task.category} 
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>{task.assignedTo}</TableCell>
                      <TableCell>{task.dueDate}</TableCell>
                      <TableCell>
                        <Chip 
                          label={task.priority} 
                          color={getPriorityColor(task.priority) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={task.status} 
                          color={getStatusColor(task.status) as any}
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
    </Box>
  );
};

export default RecruitmentOnboarding;
