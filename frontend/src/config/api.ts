// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: '/auth/login/',
    REGISTER: '/auth/register/',
    REFRESH: '/auth/token/refresh/',
    PROFILE: '/auth/profile/',
    CHANGE_PASSWORD: '/auth/change-password/',
  },
  
  // User Management
  USERS: '/auth/users/',
  DEPARTMENTS: '/auth/departments/',
  DESIGNATIONS: '/auth/designations/',
  
  // HR
  HR: {
    BASE: '/hr/',
  },
  
  // CRM
  CRM: {
    BASE: '/crm/',
  },
  
  // Projects
  PROJECTS: {
    BASE: '/projects/',
  },
  
  // Finance
  FINANCE: {
    BASE: '/finance/',
  },
  
  // Assets
  ASSETS: {
    BASE: '/assets/',
  },
};

export default API_BASE_URL;
