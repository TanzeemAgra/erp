import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Tab,
  Tabs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Avatar,
  Alert,
  Snackbar
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Timeline as TimelineIcon,
  Assignment as TaskIcon,
  TrendingUp as ProgressIcon,
  AccessTime as TimeIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Schedule as ScheduleIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format } from 'date-fns';

// Types
interface Project {
  id: number;
  name: string;
  description: string;
  status: 'planning' | 'in_progress' | 'on_hold' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'critical';
  start_date: string;
  end_date: string;
  progress_percentage: number;
  budget: number;
  spent_amount: number;
  budget_utilization: number;
  client_name: string;
  client_email: string;
  project_manager?: User;
  team_members?: User[];
  is_overdue: boolean;
  task_count: number;
  completed_tasks: number;
  created_at: string;
  updated_at: string;
}

interface Task {
  id: number;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'review' | 'done' | 'blocked';
  priority: 'low' | 'medium' | 'high' | 'critical';
  start_date: string;
  due_date: string;
  estimated_hours?: number;
  actual_hours?: number;
  assigned_to?: User;
  created_by?: User;
  is_overdue: boolean;
  project: number;
  created_at: string;
  updated_at: string;
}

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

interface DashboardStats {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  overdue_projects: number;
  budget_stats: {
    total_budget: number;
    total_spent: number;
  };
  recent_projects: Project[];
}

const ProjectManagement: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Dialog states
  const [projectDialogOpen, setProjectDialogOpen] = useState(false);
  const [taskDialogOpen, setTaskDialogOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  
  // Form states
  const [projectForm, setProjectForm] = useState({
    name: '',
    description: '',
    status: 'planning',
    priority: 'medium',
    start_date: new Date(),
    end_date: new Date(),
    budget: '',
    client_name: '',
    client_email: '',
    project_manager_id: '',
    team_member_ids: [] as number[]
  });
  
  const [taskForm, setTaskForm] = useState({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium',
    start_date: new Date(),
    due_date: new Date(),
    estimated_hours: '',
    assigned_to_id: '',
    project: ''
  });
  
  const [snackbar, setSnackbar] = useState({ 
    open: false, 
    message: '', 
    severity: 'success' as 'success' | 'error' 
  });

  // API Base URL
  const API_BASE = 'http://127.0.0.1:8000/api/projects';

  // Fetch data functions
  const fetchProjects = async () => {
    try {
      const response = await fetch(`${API_BASE}/projects/`);
      if (!response.ok) throw new Error('Failed to fetch projects');
      const data = await response.json();
      setProjects(data.results || data);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error fetching projects:', err);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_BASE}/tasks/`);
      if (!response.ok) throw new Error('Failed to fetch tasks');
      const data = await response.json();
      setTasks(data.results || data);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/projects/dashboard_stats/`);
      if (!response.ok) throw new Error('Failed to fetch stats');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError('Failed to load dashboard stats');
      console.error('Error fetching stats:', err);
    }
  };

  const fetchUsers = async () => {
    try {
      // Create sample users if the endpoint doesn't exist
      const sampleUsers = [
        { id: 1, username: 'admin', first_name: 'John', last_name: 'Doe', email: 'john@example.com' },
        { id: 2, username: 'manager', first_name: 'Jane', last_name: 'Smith', email: 'jane@example.com' },
        { id: 3, username: 'developer', first_name: 'Bob', last_name: 'Johnson', email: 'bob@example.com' }
      ];
      setUsers(sampleUsers);
    } catch (err) {
      setError('Failed to load users');
      console.error('Error fetching users:', err);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchProjects(), fetchTasks(), fetchStats(), fetchUsers()]);
      setLoading(false);
    };
    loadData();
  }, []);

  // Create/Update Project
  const handleProjectSubmit = async () => {
    try {
      const url = selectedProject 
        ? `${API_BASE}/projects/${selectedProject.id}/`
        : `${API_BASE}/projects/`;
      
      const method = selectedProject ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...projectForm,
          start_date: format(projectForm.start_date, 'yyyy-MM-dd'),
          end_date: format(projectForm.end_date, 'yyyy-MM-dd'),
          budget: projectForm.budget ? parseFloat(projectForm.budget) : null,
        }),
      });

      if (!response.ok) throw new Error('Failed to save project');
      
      setSnackbar({ open: true, message: 'Project saved successfully!', severity: 'success' });
      setProjectDialogOpen(false);
      fetchProjects();
      fetchStats();
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to save project', severity: 'error' });
      console.error('Error saving project:', err);
    }
  };

  // Create/Update Task
  const handleTaskSubmit = async () => {
    try {
      const url = selectedTask 
        ? `${API_BASE}/tasks/${selectedTask.id}/`
        : `${API_BASE}/tasks/`;
      
      const method = selectedTask ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...taskForm,
          start_date: format(taskForm.start_date, 'yyyy-MM-dd'),
          due_date: format(taskForm.due_date, 'yyyy-MM-dd'),
          estimated_hours: taskForm.estimated_hours ? parseFloat(taskForm.estimated_hours) : null,
        }),
      });

      if (!response.ok) throw new Error('Failed to save task');
      
      setSnackbar({ open: true, message: 'Task saved successfully!', severity: 'success' });
      setTaskDialogOpen(false);
      fetchTasks();
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to save task', severity: 'error' });
      console.error('Error saving task:', err);
    }
  };

  // Utility functions
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': case 'done': return 'success';
      case 'in_progress': return 'primary';
      case 'on_hold': case 'blocked': return 'warning';
      case 'cancelled': return 'error';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'primary';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount || 0);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <LinearProgress sx={{ width: '50%' }} />
      </Box>
    );
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        {/* Header */}
        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" component="h1" fontWeight="bold">
            Project Management Dashboard
          </Typography>
          <Box>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => {
                setSelectedProject(null);
                setProjectForm({
                  name: '',
                  description: '',
                  status: 'planning',
                  priority: 'medium',
                  start_date: new Date(),
                  end_date: new Date(),
                  budget: '',
                  client_name: '',
                  client_email: '',
                  project_manager_id: '',
                  team_member_ids: []
                });
                setProjectDialogOpen(true);
              }}
              sx={{ mr: 2 }}
            >
              New Project
            </Button>
            <Button
              variant="outlined"
              startIcon={<TaskIcon />}
              onClick={() => {
                setSelectedTask(null);
                setTaskForm({
                  title: '',
                  description: '',
                  status: 'todo',
                  priority: 'medium',
                  start_date: new Date(),
                  due_date: new Date(),
                  estimated_hours: '',
                  assigned_to_id: '',
                  project: ''
                });
                setTaskDialogOpen(true);
              }}
            >
              New Task
            </Button>
          </Box>
        </Box>

        {/* Dashboard Stats */}
        {stats && (
          <Box sx={{ display: 'flex', gap: 3, mb: 3, flexWrap: 'wrap' }}>
            <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
              <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h3" fontWeight="bold">{stats.total_projects}</Typography>
                      <Typography variant="body2">Total Projects</Typography>
                    </Box>
                    <TimelineIcon sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </Card>
            </Box>
            <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
              <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h3" fontWeight="bold">{stats.active_projects}</Typography>
                      <Typography variant="body2">Active Projects</Typography>
                    </Box>
                    <ProgressIcon sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </Card>
            </Box>
            <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
              <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h3" fontWeight="bold">{stats.completed_projects}</Typography>
                      <Typography variant="body2">Completed</Typography>
                    </Box>
                    <CheckIcon sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </Card>
            </Box>
            <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
              <Card sx={{ background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', color: 'white' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h3" fontWeight="bold">{stats.overdue_projects}</Typography>
                      <Typography variant="body2">Overdue</Typography>
                    </Box>
                    <WarningIcon sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </Card>
            </Box>
          </Box>
        )}

        {/* Budget Overview */}
        {stats?.budget_stats && (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Budget Overview</Typography>
              <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px' }}>
                  <Typography variant="body2" color="textSecondary">Total Budget</Typography>
                  <Typography variant="h4" color="primary">
                    {formatCurrency(stats.budget_stats.total_budget)}
                  </Typography>
                </Box>
                <Box sx={{ flex: '1 1 200px' }}>
                  <Typography variant="body2" color="textSecondary">Total Spent</Typography>
                  <Typography variant="h4" color="error">
                    {formatCurrency(stats.budget_stats.total_spent)}
                  </Typography>
                </Box>
                <Box sx={{ flex: '1 1 200px' }}>
                  <Typography variant="body2" color="textSecondary">Remaining</Typography>
                  <Typography variant="h4" color="success.main">
                    {formatCurrency((stats.budget_stats.total_budget || 0) - (stats.budget_stats.total_spent || 0))}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        )}

        {/* Tabs */}
        <Card>
          <Tabs
            value={activeTab}
            onChange={(e, newValue) => setActiveTab(newValue)}
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            <Tab label="Projects" />
            <Tab label="Tasks" />
            <Tab label="Team Overview" />
          </Tabs>

          {/* Projects Tab */}
          {activeTab === 0 && (
            <Box sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                {projects.map((project) => (
                  <Box key={project.id} sx={{ flex: '1 1 350px', minWidth: '350px', maxWidth: '400px' }}>
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                      <CardContent sx={{ flexGrow: 1 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                          <Typography variant="h6" component="h3" noWrap>
                            {project.name}
                          </Typography>
                          <Box>
                            <Chip
                              size="small"
                              label={project.status.replace('_', ' ')}
                              color={getStatusColor(project.status)}
                              sx={{ mr: 1 }}
                            />
                            <Chip
                              size="small"
                              label={project.priority}
                              color={getPriorityColor(project.priority)}
                            />
                          </Box>
                        </Box>
                        
                        <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                          {project.description}
                        </Typography>
                        
                        <Box sx={{ mb: 2 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2">Progress</Typography>
                            <Typography variant="body2">{project.progress_percentage}%</Typography>
                          </Box>
                          <LinearProgress 
                            variant="determinate" 
                            value={project.progress_percentage} 
                            sx={{ height: 8, borderRadius: 4 }}
                          />
                        </Box>
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                          <Box>
                            <Typography variant="body2" color="textSecondary">Tasks</Typography>
                            <Typography variant="h6">{project.completed_tasks}/{project.task_count}</Typography>
                          </Box>
                          <Box sx={{ textAlign: 'right' }}>
                            <Typography variant="body2" color="textSecondary">Budget</Typography>
                            <Typography variant="h6">{formatCurrency(project.budget)}</Typography>
                          </Box>
                        </Box>
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <ScheduleIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                            <Typography variant="body2" color="textSecondary">
                              {format(new Date(project.end_date), 'MMM dd, yyyy')}
                            </Typography>
                          </Box>
                          {project.is_overdue && (
                            <Chip size="small" label="Overdue" color="error" variant="outlined" />
                          )}
                        </Box>
                      </CardContent>
                      
                      <Box sx={{ p: 2, pt: 0 }}>
                        <Button
                          fullWidth
                          variant="outlined"
                          onClick={() => {
                            setSelectedProject(project);
                            setProjectForm({
                              name: project.name,
                              description: project.description,
                              status: project.status,
                              priority: project.priority,
                              start_date: new Date(project.start_date),
                              end_date: new Date(project.end_date),
                              budget: project.budget?.toString() || '',
                              client_name: project.client_name,
                              client_email: project.client_email,
                              project_manager_id: project.project_manager?.id?.toString() || '',
                              team_member_ids: project.team_members?.map(m => m.id) || []
                            });
                            setProjectDialogOpen(true);
                          }}
                        >
                          View Details
                        </Button>
                      </Box>
                    </Card>
                  </Box>
                ))}
              </Box>
            </Box>
          )}

          {/* Tasks Tab */}
          {activeTab === 1 && (
            <Box sx={{ p: 3 }}>
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Task</TableCell>
                      <TableCell>Project</TableCell>
                      <TableCell>Assigned To</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Priority</TableCell>
                      <TableCell>Due Date</TableCell>
                      <TableCell>Progress</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {tasks.map((task) => {
                      const project = projects.find(p => p.id === task.project);
                      return (
                        <TableRow key={task.id}>
                          <TableCell>
                            <Box>
                              <Typography variant="subtitle2">{task.title}</Typography>
                              <Typography variant="body2" color="textSecondary" noWrap>
                                {task.description}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip size="small" label={project?.name || 'Unknown'} />
                          </TableCell>
                          <TableCell>
                            {task.assigned_to ? (
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Avatar sx={{ width: 24, height: 24, mr: 1, fontSize: '0.875rem' }}>
                                  {task.assigned_to.first_name?.[0]}{task.assigned_to.last_name?.[0]}
                                </Avatar>
                                <Typography variant="body2">
                                  {task.assigned_to.first_name} {task.assigned_to.last_name}
                                </Typography>
                              </Box>
                            ) : (
                              <Typography variant="body2" color="textSecondary">Unassigned</Typography>
                            )}
                          </TableCell>
                          <TableCell>
                            <Chip
                              size="small"
                              label={task.status.replace('_', ' ')}
                              color={getStatusColor(task.status)}
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              size="small"
                              label={task.priority}
                              color={getPriorityColor(task.priority)}
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Typography variant="body2">
                                {format(new Date(task.due_date), 'MMM dd')}
                              </Typography>
                              {task.is_overdue && (
                                <WarningIcon sx={{ ml: 1, fontSize: 16, color: 'error.main' }} />
                              )}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <TimeIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                              <Typography variant="body2">
                                {task.actual_hours || 0}h / {task.estimated_hours || 0}h
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <IconButton
                              size="small"
                              onClick={() => {
                                setSelectedTask(task);
                                setTaskForm({
                                  title: task.title,
                                  description: task.description,
                                  status: task.status,
                                  priority: task.priority,
                                  start_date: new Date(task.start_date),
                                  due_date: new Date(task.due_date),
                                  estimated_hours: task.estimated_hours?.toString() || '',
                                  assigned_to_id: task.assigned_to?.id?.toString() || '',
                                  project: task.project.toString()
                                });
                                setTaskDialogOpen(true);
                              }}
                            >
                              <EditIcon fontSize="small" />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}

          {/* Team Overview Tab */}
          {activeTab === 2 && (
            <Box sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Team Performance Overview</Typography>
              <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                {users.map((user) => {
                  const userTasks = tasks.filter(task => task.assigned_to?.id === user.id);
                  const completedTasks = userTasks.filter(task => task.status === 'done').length;
                  const totalHours = userTasks.reduce((sum, task) => sum + (task.actual_hours || 0), 0);
                  
                  return (
                    <Box key={user.id} sx={{ flex: '1 1 300px', minWidth: '300px', maxWidth: '350px' }}>
                      <Card>
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Avatar sx={{ mr: 2 }}>
                              {user.first_name?.[0]}{user.last_name?.[0]}
                            </Avatar>
                            <Box>
                              <Typography variant="h6">
                                {user.first_name} {user.last_name}
                              </Typography>
                              <Typography variant="body2" color="textSecondary">
                                {user.email}
                              </Typography>
                            </Box>
                          </Box>
                          
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2">Tasks</Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {completedTasks}/{userTasks.length}
                            </Typography>
                          </Box>
                          
                          <LinearProgress
                            variant="determinate"
                            value={userTasks.length > 0 ? (completedTasks / userTasks.length) * 100 : 0}
                            sx={{ mb: 2, height: 6, borderRadius: 3 }}
                          />
                          
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body2" color="textSecondary">
                              Total Hours
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {totalHours.toFixed(1)}h
                            </Typography>
                          </Box>
                        </CardContent>
                      </Card>
                    </Box>
                  );
                })}
              </Box>
            </Box>
          )}
        </Card>

        {/* Project Dialog */}
        <Dialog open={projectDialogOpen} onClose={() => setProjectDialogOpen(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            {selectedProject ? 'Edit Project' : 'Create New Project'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  label="Project Name"
                  value={projectForm.name}
                  onChange={(e) => setProjectForm({ ...projectForm, name: e.target.value })}
                />
                <TextField
                  fullWidth
                  label="Client Name"
                  value={projectForm.client_name}
                  onChange={(e) => setProjectForm({ ...projectForm, client_name: e.target.value })}
                />
              </Box>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Description"
                value={projectForm.description}
                onChange={(e) => setProjectForm({ ...projectForm, description: e.target.value })}
              />
              <Box sx={{ display: 'flex', gap: 2 }}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={projectForm.status}
                    onChange={(e) => setProjectForm({ ...projectForm, status: e.target.value })}
                    label="Status"
                  >
                    <MenuItem value="planning">Planning</MenuItem>
                    <MenuItem value="in_progress">In Progress</MenuItem>
                    <MenuItem value="on_hold">On Hold</MenuItem>
                    <MenuItem value="completed">Completed</MenuItem>
                    <MenuItem value="cancelled">Cancelled</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>Priority</InputLabel>
                  <Select
                    value={projectForm.priority}
                    onChange={(e) => setProjectForm({ ...projectForm, priority: e.target.value })}
                    label="Priority"
                  >
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="critical">Critical</MenuItem>
                  </Select>
                </FormControl>
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <DatePicker
                  label="Start Date"
                  value={projectForm.start_date}
                  onChange={(date) => setProjectForm({ ...projectForm, start_date: date || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
                <DatePicker
                  label="End Date"
                  value={projectForm.end_date}
                  onChange={(date) => setProjectForm({ ...projectForm, end_date: date || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  type="number"
                  label="Budget"
                  value={projectForm.budget}
                  onChange={(e) => setProjectForm({ ...projectForm, budget: e.target.value })}
                />
                <TextField
                  fullWidth
                  type="email"
                  label="Client Email"
                  value={projectForm.client_email}
                  onChange={(e) => setProjectForm({ ...projectForm, client_email: e.target.value })}
                />
              </Box>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setProjectDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleProjectSubmit} variant="contained">
              {selectedProject ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Task Dialog */}
        <Dialog open={taskDialogOpen} onClose={() => setTaskDialogOpen(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            {selectedTask ? 'Edit Task' : 'Create New Task'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  sx={{ flex: 2 }}
                  label="Task Title"
                  value={taskForm.title}
                  onChange={(e) => setTaskForm({ ...taskForm, title: e.target.value })}
                />
                <FormControl sx={{ flex: 1 }}>
                  <InputLabel>Project</InputLabel>
                  <Select
                    value={taskForm.project}
                    onChange={(e) => setTaskForm({ ...taskForm, project: e.target.value })}
                    label="Project"
                  >
                    {projects.map((project) => (
                      <MenuItem key={project.id} value={project.id.toString()}>
                        {project.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Description"
                value={taskForm.description}
                onChange={(e) => setTaskForm({ ...taskForm, description: e.target.value })}
              />
              <Box sx={{ display: 'flex', gap: 2 }}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={taskForm.status}
                    onChange={(e) => setTaskForm({ ...taskForm, status: e.target.value })}
                    label="Status"
                  >
                    <MenuItem value="todo">To Do</MenuItem>
                    <MenuItem value="in_progress">In Progress</MenuItem>
                    <MenuItem value="review">In Review</MenuItem>
                    <MenuItem value="done">Done</MenuItem>
                    <MenuItem value="blocked">Blocked</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>Priority</InputLabel>
                  <Select
                    value={taskForm.priority}
                    onChange={(e) => setTaskForm({ ...taskForm, priority: e.target.value })}
                    label="Priority"
                  >
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="critical">Critical</MenuItem>
                  </Select>
                </FormControl>
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <DatePicker
                  label="Start Date"
                  value={taskForm.start_date}
                  onChange={(date) => setTaskForm({ ...taskForm, start_date: date || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
                <DatePicker
                  label="Due Date"
                  value={taskForm.due_date}
                  onChange={(date) => setTaskForm({ ...taskForm, due_date: date || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  type="number"
                  label="Estimated Hours"
                  value={taskForm.estimated_hours}
                  onChange={(e) => setTaskForm({ ...taskForm, estimated_hours: e.target.value })}
                />
                <FormControl fullWidth>
                  <InputLabel>Assigned To</InputLabel>
                  <Select
                    value={taskForm.assigned_to_id}
                    onChange={(e) => setTaskForm({ ...taskForm, assigned_to_id: e.target.value })}
                    label="Assigned To"
                  >
                    <MenuItem value="">Unassigned</MenuItem>
                    {users.map((user) => (
                      <MenuItem key={user.id} value={user.id.toString()}>
                        {user.first_name} {user.last_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setTaskDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleTaskSubmit} variant="contained">
              {selectedTask ? 'Update' : 'Create'}
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

export default ProjectManagement;
