import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Provider } from 'react-redux';
import { store } from './store/store';

// Components
import Layout from './components/Layout/Layout';
import EnhancedLayout from './components/Layout/EnhancedLayout';
import Login from './pages/Auth/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import EmployeeManagement from './pages/HR/EmployeeManagement';
import ProjectManagement from './components/ProjectManagement';
import ClientManagement from './pages/CRM/ClientManagementFixed';
import FinanceDashboard from './pages/Finance/FinanceDashboard';
import AssetManagement from './pages/Assets/AssetManagement';
import Profile from './pages/Profile/Profile';

// HRM Components
import EmployeeDatabase from './pages/HRM/EmployeeDatabase';
import PayrollAttendance from './pages/HRM/PayrollAttendance';
import PerformanceAppraisal from './pages/HRM/PerformanceAppraisal';
import RecruitmentOnboarding from './pages/HRM/RecruitmentOnboarding';

// Theme configuration
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
    success: {
      main: '#2e7d32',
    },
    warning: {
      main: '#ed6c02',
    },
    error: {
      main: '#d32f2f',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

// Mock authentication check
const isAuthenticated = () => {
  return localStorage.getItem('access_token') !== null;
};

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return isAuthenticated() ? <>{children}</> : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/*"
              element={
                <ProtectedRoute>
                  <EnhancedLayout>
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/employees" element={<EmployeeDatabase />} />
                      <Route path="/hr/employees" element={<EmployeeManagement />} />
                      <Route path="/hrm/employee-database" element={<EmployeeDatabase />} />
                      <Route path="/hrm/payroll-attendance" element={<PayrollAttendance />} />
                      <Route path="/hrm/performance-appraisal" element={<PerformanceAppraisal />} />
                      <Route path="/hrm/recruitment-onboarding" element={<RecruitmentOnboarding />} />
                      <Route path="/projects" element={<ProjectManagement />} />
                      <Route path="/crm/clients" element={<ClientManagement />} />
                      <Route path="/finance" element={<FinanceDashboard />} />
                      <Route path="/assets" element={<AssetManagement />} />
                      <Route path="/profile" element={<Profile />} />
                      <Route path="*" element={<Navigate to="/dashboard" replace />} />
                    </Routes>
                  </EnhancedLayout>
                </ProtectedRoute>
              }
            />
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
