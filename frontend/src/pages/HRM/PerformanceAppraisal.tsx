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
  Rating,
  IconButton,
  Tooltip,
  Tab,
  Tabs,
} from '@mui/material';
import {
  Search,
  TrendingUp,
  Assignment,
  Star,
  Timeline,
  Person,
  CalendarToday,
  Assessment,
  Add,
  Edit,
  Visibility,
  Download,
} from '@mui/icons-material';

interface PerformanceReview {
  id: string;
  employeeId: string;
  employeeName: string;
  department: string;
  reviewPeriod: string;
  overallRating: number;
  goals: {
    completed: number;
    total: number;
  };
  competencies: {
    technical: number;
    communication: number;
    leadership: number;
    teamwork: number;
  };
  status: 'Completed' | 'In Progress' | 'Pending' | 'Overdue';
  reviewDate: string;
  nextReview: string;
}

interface Goal {
  id: string;
  employeeId: string;
  employeeName: string;
  title: string;
  description: string;
  targetDate: string;
  progress: number;
  category: 'Professional' | 'Technical' | 'Personal' | 'Leadership';
  status: 'On Track' | 'At Risk' | 'Completed' | 'Overdue';
}

interface AppraisalCycle {
  id: string;
  title: string;
  period: string;
  startDate: string;
  endDate: string;
  participants: number;
  completed: number;
  status: 'Active' | 'Draft' | 'Completed';
}

const PerformanceAppraisal: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');

  // Mock data
  const mockPerformanceReviews: PerformanceReview[] = [
    {
      id: 'REV001',
      employeeId: 'EMP001',
      employeeName: 'John Doe',
      department: 'Engineering',
      reviewPeriod: 'Q4 2024',
      overallRating: 4.2,
      goals: { completed: 8, total: 10 },
      competencies: {
        technical: 4.5,
        communication: 4.0,
        leadership: 3.8,
        teamwork: 4.3,
      },
      status: 'Completed',
      reviewDate: '2024-12-15',
      nextReview: '2025-03-15',
    },
    {
      id: 'REV002',
      employeeId: 'EMP002',
      employeeName: 'Jane Smith',
      department: 'HR',
      reviewPeriod: 'Q4 2024',
      overallRating: 4.7,
      goals: { completed: 9, total: 10 },
      competencies: {
        technical: 4.2,
        communication: 4.8,
        leadership: 4.9,
        teamwork: 4.6,
      },
      status: 'Completed',
      reviewDate: '2024-12-10',
      nextReview: '2025-03-10',
    },
    {
      id: 'REV003',
      employeeId: 'EMP003',
      employeeName: 'Mike Johnson',
      department: 'Marketing',
      reviewPeriod: 'Q4 2024',
      overallRating: 3.8,
      goals: { completed: 6, total: 10 },
      competencies: {
        technical: 3.5,
        communication: 4.2,
        leadership: 3.6,
        teamwork: 4.0,
      },
      status: 'In Progress',
      reviewDate: '2024-12-20',
      nextReview: '2025-03-20',
    },
  ];

  const mockGoals: Goal[] = [
    {
      id: 'GOAL001',
      employeeId: 'EMP001',
      employeeName: 'John Doe',
      title: 'Complete React Certification',
      description: 'Obtain advanced React certification to improve frontend development skills',
      targetDate: '2025-01-31',
      progress: 75,
      category: 'Technical',
      status: 'On Track',
    },
    {
      id: 'GOAL002',
      employeeId: 'EMP002',
      employeeName: 'Jane Smith',
      title: 'Lead Team Building Initiative',
      description: 'Organize and lead quarterly team building activities',
      targetDate: '2025-02-15',
      progress: 60,
      category: 'Leadership',
      status: 'On Track',
    },
    {
      id: 'GOAL003',
      employeeId: 'EMP003',
      employeeName: 'Mike Johnson',
      title: 'Digital Marketing Campaign',
      description: 'Launch comprehensive digital marketing campaign for Q1 2025',
      targetDate: '2025-01-15',
      progress: 30,
      category: 'Professional',
      status: 'At Risk',
    },
  ];

  const mockAppraisalCycles: AppraisalCycle[] = [
    {
      id: 'CYCLE001',
      title: 'Q4 2024 Performance Review',
      period: 'October - December 2024',
      startDate: '2024-12-01',
      endDate: '2024-12-31',
      participants: 50,
      completed: 35,
      status: 'Active',
    },
    {
      id: 'CYCLE002',
      title: 'Mid-Year Review 2024',
      period: 'April - June 2024',
      startDate: '2024-06-01',
      endDate: '2024-06-30',
      participants: 48,
      completed: 48,
      status: 'Completed',
    },
  ];

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed':
      case 'On Track':
        return 'success';
      case 'In Progress':
      case 'Active':
        return 'primary';
      case 'At Risk':
      case 'Overdue':
        return 'warning';
      case 'Pending':
        return 'error';
      default:
        return 'default';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Technical':
        return 'primary';
      case 'Leadership':
        return 'secondary';
      case 'Professional':
        return 'success';
      case 'Personal':
        return 'warning';
      default:
        return 'default';
    }
  };

  const avgRating = mockPerformanceReviews.reduce((sum, review) => sum + review.overallRating, 0) / mockPerformanceReviews.length;
  const completedGoals = mockGoals.filter(goal => goal.status === 'Completed').length;
  const totalGoals = mockGoals.length;
  const onTrackGoals = mockGoals.filter(goal => goal.status === 'On Track').length;

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
          Performance & Appraisal Tracking
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Track employee performance, manage appraisals, and monitor goal achievement
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
                  {avgRating.toFixed(1)}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Avg Rating
                </Typography>
              </Box>
              <Star sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {Math.round((completedGoals / totalGoals) * 100)}%
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Goals Achieved
                </Typography>
              </Box>
              <Assignment sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {mockPerformanceReviews.filter(r => r.status === 'Completed').length}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Reviews Done
                </Typography>
              </Box>
              <Assessment sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {onTrackGoals}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Goals On Track
                </Typography>
              </Box>
              <TrendingUp sx={{ fontSize: 40, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Tabs */}
      <Card sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="performance tabs">
          <Tab label="Performance Reviews" />
          <Tab label="Goal Tracking" />
          <Tab label="Appraisal Cycles" />
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
          placeholder="Search employees or reviews..."
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
            <MenuItem value="Completed">Completed</MenuItem>
            <MenuItem value="In Progress">In Progress</MenuItem>
            <MenuItem value="Pending">Pending</MenuItem>
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
                Performance Reviews
              </Typography>
              <Button variant="contained" startIcon={<Add />}>
                New Review
              </Button>
            </Box>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Employee</TableCell>
                    <TableCell>Period</TableCell>
                    <TableCell>Overall Rating</TableCell>
                    <TableCell>Goals Progress</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Next Review</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockPerformanceReviews.map((review) => (
                    <TableRow key={review.id}>
                      <TableCell>
                        <Box>
                          <Typography variant="body2" fontWeight="bold">
                            {review.employeeName}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {review.department}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>{review.reviewPeriod}</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Rating value={review.overallRating} readOnly size="small" precision={0.1} />
                          <Typography variant="body2">
                            {review.overallRating.toFixed(1)}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box>
                          <Typography variant="body2">
                            {review.goals.completed}/{review.goals.total} completed
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={(review.goals.completed / review.goals.total) * 100}
                            sx={{ mt: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={review.status} 
                          color={getStatusColor(review.status) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{review.nextReview}</TableCell>
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
                Goal Tracking
              </Typography>
              <Button variant="contained" startIcon={<Add />}>
                Set New Goal
              </Button>
            </Box>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Employee</TableCell>
                    <TableCell>Goal</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Progress</TableCell>
                    <TableCell>Target Date</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockGoals.map((goal) => (
                    <TableRow key={goal.id}>
                      <TableCell>{goal.employeeName}</TableCell>
                      <TableCell>
                        <Box>
                          <Typography variant="body2" fontWeight="bold">
                            {goal.title}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {goal.description}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={goal.category} 
                          color={getCategoryColor(goal.category) as any}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Box>
                          <Typography variant="body2">
                            {goal.progress}%
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={goal.progress}
                            sx={{ mt: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>{goal.targetDate}</TableCell>
                      <TableCell>
                        <Chip 
                          label={goal.status} 
                          color={getStatusColor(goal.status) as any}
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
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" fontWeight="bold">
                Appraisal Cycles
              </Typography>
              <Button variant="contained" startIcon={<Add />}>
                Create Cycle
              </Button>
            </Box>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Cycle Title</TableCell>
                    <TableCell>Period</TableCell>
                    <TableCell>Participants</TableCell>
                    <TableCell>Progress</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockAppraisalCycles.map((cycle) => (
                    <TableRow key={cycle.id}>
                      <TableCell>
                        <Typography variant="body2" fontWeight="bold">
                          {cycle.title}
                        </Typography>
                      </TableCell>
                      <TableCell>{cycle.period}</TableCell>
                      <TableCell>{cycle.participants} employees</TableCell>
                      <TableCell>
                        <Box>
                          <Typography variant="body2">
                            {cycle.completed}/{cycle.participants} completed
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={(cycle.completed / cycle.participants) * 100}
                            sx={{ mt: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={cycle.status} 
                          color={getStatusColor(cycle.status) as any}
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
    </Box>
  );
};

export default PerformanceAppraisal;
