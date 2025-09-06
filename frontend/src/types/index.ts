// TypeScript type definitions for ERP System

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  full_name: string;
  phone_number?: string;
  date_of_birth?: string;
  employee_id?: string;
  department?: string;
  department_name?: string;
  designation?: string;
  joining_date?: string;
  profile_picture?: string;
  bio?: string;
  is_hr_manager: boolean;
  is_project_manager: boolean;
  is_finance_manager: boolean;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  emergency_contact_relation?: string;
  is_active: boolean;
  is_staff: boolean;
  date_joined: string;
  last_login?: string;
  created_at: string;
  updated_at: string;
}

export interface Department {
  id: number;
  name: string;
  description?: string;
  head?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Designation {
  id: number;
  title: string;
  description?: string;
  department: number;
  department_name: string;
  level: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  phone_number?: string;
  employee_id?: string;
  department?: string;
  designation?: string;
  joining_date?: string;
}

export interface ApiResponse<T> {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: T[];
  data?: T;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

// Navigation Menu Items
export interface MenuItem {
  id: string;
  title: string;
  icon: React.ComponentType;
  path: string;
  subItems?: MenuItem[];
  permissions?: string[];
}

// Dashboard Stats
export interface DashboardStats {
  total_employees: number;
  active_projects: number;
  pending_leaves: number;
  monthly_revenue: number;
  growth_rate: number;
}
