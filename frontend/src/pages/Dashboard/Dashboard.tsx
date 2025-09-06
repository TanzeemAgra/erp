import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Avatar,
  Chip,
  IconButton,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  People,
  Person,
  CheckCircle,
  PersonAdd,
  Star,
  ArrowForward,
  Visibility,
  Schedule,
  Work,
  Assessment,
} from '@mui/icons-material';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  
  const [stats] = useState({
    totalEmployees: 150,
    totalDepartments: 8,
    activeTasks: 42,
    totalRevenue: '$2.4M',
    newHires: 12,
    pendingReviews: 8,
    attendanceRate: 95.2,
    activeProjects: 24
  });

  const recentEmployees = [
    { 
      id: 1, 
      name: 'Sarah Johnson', 
      position: 'Senior Developer', 
      department: 'Engineering',
      avatar: 'SJ',
      status: 'Active',
      joinDate: '2024-08-15',
      performance: 4.8
    },
    { 
      id: 2, 
      name: 'Michael Chen', 
      position: 'Product Manager', 
      department: 'Product',
      avatar: 'MC',
      status: 'Active',
      joinDate: '2024-08-12',
      performance: 4.6
    },
    { 
      id: 3, 
      name: 'Emily Rodriguez', 
      position: 'UX Designer', 
      department: 'Design',
      avatar: 'ER',
      status: 'Active',
      joinDate: '2024-08-10',
      performance: 4.9
    },
    { 
      id: 4, 
      name: 'David Wilson', 
      position: 'Data Analyst', 
      department: 'Analytics',
      avatar: 'DW',
      status: 'Active',
      joinDate: '2024-08-08',
      performance: 4.5
    }
  ];

  const hrMetrics = [
    { label: 'New Hires This Month', value: 12, target: 15, color: '#1976d2' },
    { label: 'Pending Performance Reviews', value: 8, target: 20, color: '#ed6c02' },
    { label: 'Training Completion', value: 85, target: 90, color: '#2e7d32' },
    { label: 'Employee Satisfaction', value: 4.6, target: 5.0, color: '#9c27b0' }
  ];

  const quickActions = [
    {
      title: 'Employee Database',
      description: 'View and manage all employee profiles',
      icon: <People />,
      color: '#1976d2',
      path: '/employees',
      count: stats.totalEmployees
    },
    {
      title: 'Payroll & Attendance',
      description: 'Process payroll and track attendance',
      icon: <Schedule />,
      color: '#2e7d32',
      path: '/hrm/payroll-attendance',
      count: `${stats.attendanceRate}%`
    },
    {
      title: 'Performance Reviews',
      description: 'Manage employee performance and appraisals',
      icon: <Assessment />,
      color: '#ed6c02',
      path: '/hrm/performance-appraisal',
      count: stats.pendingReviews
    },
    {
      title: 'Recruitment',
      description: 'Manage hiring and onboarding processes',
      icon: <PersonAdd />,
      color: '#9c27b0',
      path: '/hrm/recruitment-onboarding',
      count: stats.newHires
    }
  ];

  const handleQuickAction = (path: string) => {
    navigate(path);
  };

  const activities = [
    { id: 1, user: 'John Doe', action: 'completed task "UI Design"', time: '2 hours ago' },
    { id: 2, user: 'Jane Smith', action: 'joined HR Department', time: '4 hours ago' },
    { id: 3, user: 'Mike Johnson', action: 'updated project status', time: '6 hours ago' },
    { id: 4, user: 'Sarah Wilson', action: 'created new invoice', time: '8 hours ago' },
  ];

  const tasks = [
    { id: 1, title: 'Review Q4 Reports', dueDate: 'Dec 15', priority: 'High' },
    { id: 2, title: 'Team Meeting Prep', dueDate: 'Dec 12', priority: 'Medium' },
    { id: 3, title: 'Budget Analysis', dueDate: 'Dec 18', priority: 'Low' },
    { id: 4, title: 'Client Presentation', dueDate: 'Dec 14', priority: 'High' },
  ];

  const departments = [
    { name: 'Engineering', count: 45, color: '#1976d2' },
    { name: 'Sales', count: 32, color: '#2e7d32' },
    { name: 'Marketing', count: 28, color: '#ed6c02' },
    { name: 'HR', count: 15, color: '#9c27b0' },
    { name: 'Finance', count: 20, color: '#d32f2f' },
    { name: 'Support', count: 10, color: '#7b1fa2' },
  ];

  return (
    <Box sx={{ p: 3, maxWidth: '1400px', margin: '0 auto' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight="bold" gutterBottom>
          Employee Management Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome back! Here's your comprehensive employee management overview.
        </Typography>
      </Box>

      {/* Quick Action Cards */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" fontWeight="bold" gutterBottom>
          Employee Management Quick Actions
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' },
          gap: 3 
        }}>
          {quickActions.map((action, index) => (
            <Box key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                  }
                }}
                onClick={() => handleQuickAction(action.path)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
                    <Box 
                      sx={{ 
                        p: 1.5, 
                        borderRadius: 2, 
                        backgroundColor: `${action.color}15`,
                        color: action.color 
                      }}
                    >
                      {action.icon}
                    </Box>
                    <Typography variant="h4" fontWeight="bold" color={action.color}>
                      {action.count}
                    </Typography>
                  </Box>
                  <Typography variant="h6" fontWeight="bold" gutterBottom>
                    {action.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {action.description}
                  </Typography>
                  <Button 
                    variant="contained" 
                    size="small" 
                    endIcon={<ArrowForward />}
                    sx={{ 
                      backgroundColor: action.color,
                      '&:hover': { backgroundColor: action.color + 'dd' }
                    }}
                  >
                    Open
                  </Button>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      </Box>

      {/* Stats Overview */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' },
        gap: 3,
        mb: 4 
      }}>
        <Card sx={{ background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {stats.totalEmployees}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Total Employees
                </Typography>
              </Box>
              <People sx={{ fontSize: 48, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #2e7d32 30%, #4caf50 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {stats.attendanceRate}%
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Attendance Rate
                </Typography>
              </Box>
              <CheckCircle sx={{ fontSize: 48, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #ed6c02 30%, #ff9800 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {stats.newHires}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  New Hires
                </Typography>
              </Box>
              <PersonAdd sx={{ fontSize: 48, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ background: 'linear-gradient(45deg, #9c27b0 30%, #e91e63 90%)', color: 'white' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h4" fontWeight="bold">
                  {stats.activeProjects}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Active Projects
                </Typography>
              </Box>
              <Work sx={{ fontSize: 48, opacity: 0.8 }} />
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Main Content Grid */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
        gap: 3 
      }}>
        {/* Recent Employees */}
        <Box>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h6" fontWeight="bold">
                  Recent Employees
                </Typography>
                <Button 
                  variant="outlined" 
                  size="small"
                  onClick={() => navigate('/employees')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {recentEmployees.map((employee) => (
                  <ListItem 
                    key={employee.id}
                    sx={{ 
                      px: 0,
                      '&:hover': { backgroundColor: 'rgba(0,0,0,0.04)' },
                      borderRadius: 1,
                      cursor: 'pointer'
                    }}
                    onClick={() => navigate('/employees')}
                  >
                    <ListItemIcon>
                      <Avatar sx={{ bgcolor: '#1976d2' }}>
                        {employee.avatar}
                      </Avatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body1" fontWeight="bold">
                            {employee.name}
                          </Typography>
                          <Chip 
                            label={employee.status} 
                            size="small" 
                            color="success"
                            variant="outlined"
                          />
                        </Box>
                      }
                      secondary={
                        <React.Fragment>
                          <Typography variant="body2" color="text.secondary" component="span" display="block">
                            {employee.position} • {employee.department}
                          </Typography>
                          <Typography variant="caption" component="span" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
                            <Star sx={{ fontSize: 16, color: '#ffc107' }} />
                            {employee.performance}/5.0
                          </Typography>
                        </React.Fragment>
                      }
                    />
                    <Tooltip title="View Profile">
                      <IconButton size="small">
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Box>

        {/* HR Metrics */}
        <Box>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                HR Metrics & Goals
              </Typography>
              <Box sx={{ mt: 3 }}>
                {hrMetrics.map((metric, index) => (
                  <Box key={index} sx={{ mb: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        {metric.label}
                      </Typography>
                      <Typography variant="body2" color={metric.color}>
                        {metric.value}{metric.label.includes('Satisfaction') ? '/5.0' : ''}
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={(metric.value / metric.target) * 100}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        backgroundColor: `${metric.color}20`,
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: metric.color,
                          borderRadius: 4,
                        },
                      }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      Target: {metric.target}{metric.label.includes('Satisfaction') ? '/5.0' : ''}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Box>
      {/* Charts Row */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', md: '2fr 1fr' },
        gap: 3,
        mb: 4 
      }}>
        {/* Revenue Chart */}
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6" fontWeight="bold">
                Revenue Overview
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Last 6 months
              </Typography>
            </Box>
            <Box sx={{ 
              height: 300, 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              bgcolor: 'grey.50',
              borderRadius: 1
            }}>
              <Typography variant="body1" color="text.secondary">
                Revenue Chart Placeholder
              </Typography>
            </Box>
          </CardContent>
        </Card>

        {/* Department Distribution */}
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Department Distribution
            </Typography>
            <Box sx={{ mt: 2 }}>
              {departments.map((dept, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2">{dept.name}</Typography>
                    <Typography variant="body2" fontWeight="bold">{dept.count}</Typography>
                  </Box>
                  <Box sx={{ 
                    height: 6, 
                    bgcolor: 'grey.200', 
                    borderRadius: 3,
                    overflow: 'hidden'
                  }}>
                    <Box sx={{ 
                      height: '100%', 
                      bgcolor: dept.color,
                      width: `${(dept.count / 150) * 100}%`,
                      borderRadius: 3
                    }} />
                  </Box>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Bottom Row */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
        gap: 3
      }}>
        {/* Recent Activities */}
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Recent Activities
            </Typography>
            <Box sx={{ mt: 2 }}>
              {activities.map((activity) => (
                <Box key={activity.id} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Person sx={{ mr: 2, color: 'primary.main' }} />
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2">
                      <strong>{activity.user}</strong> {activity.action}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {activity.time}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>

        {/* Upcoming Tasks */}
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Upcoming Tasks
            </Typography>
            <Box sx={{ mt: 2 }}>
              {tasks.map((task) => (
                <Box key={task.id} sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between',
                  p: 1.5,
                  mb: 1,
                  bgcolor: 'grey.50',
                  borderRadius: 1,
                  border: '1px solid',
                  borderColor: 'grey.200'
                }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <CheckCircle sx={{ mr: 1, color: 'success.main', fontSize: 16 }} />
                    <Box>
                      <Typography variant="body2" fontWeight="bold">
                        {task.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Due: {task.dueDate}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ 
                    px: 1.5, 
                    py: 0.5, 
                    borderRadius: 1,
                    bgcolor: task.priority === 'High' ? 'error.light' : 
                             task.priority === 'Medium' ? 'warning.light' : 'success.light',
                    color: task.priority === 'High' ? 'error.contrastText' : 
                           task.priority === 'Medium' ? 'warning.contrastText' : 'success.contrastText'
                  }}>
                    <Typography variant="caption" fontWeight="bold">
                      {task.priority}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default Dashboard;
