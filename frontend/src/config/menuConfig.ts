import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Business as BusinessIcon,
  Assignment as ProjectIcon,
  Group as GroupIcon,
  AccountBalance as FinanceIcon,
  Computer as AssetIcon,
  Work as HRMIcon,
  PersonAdd as RecruitmentIcon,
  Payment as PayrollIcon,
  Assessment as PerformanceIcon,
  EventAvailable as LeaveIcon,
  Badge as EmployeeProfileIcon,
  SmartToy as ChatbotIcon,
} from '@mui/icons-material';

export interface MenuSubItem {
  text: string;
  icon: React.ComponentType;
  path: string;
  description?: string;
}

export interface MenuItem {
  text: string;
  icon: React.ComponentType;
  path?: string;
  subItems?: MenuSubItem[];
  category?: string;
}

export const menuConfig: MenuItem[] = [
  {
    text: 'Dashboard',
    icon: DashboardIcon,
    path: '/dashboard',
    category: 'main'
  },
  {
    text: 'Human Resource Management',
    icon: HRMIcon,
    category: 'hrm',
    subItems: [
      {
        text: 'Employee Database & Profiles',
        icon: EmployeeProfileIcon,
        path: '/hrm/employees',
        description: 'Manage employee information, profiles, and personal details'
      },
      {
        text: 'Payroll & Attendance System',
        icon: PayrollIcon,
        path: '/hrm/payroll',
        description: 'Handle payroll processing, attendance tracking, and timesheets'
      },
      {
        text: 'Leave, Appraisal & Performance',
        icon: PerformanceIcon,
        path: '/hrm/performance',
        description: 'Track leave applications, performance reviews, and appraisals'
      },
      {
        text: 'Recruitment & Onboarding',
        icon: RecruitmentIcon,
        path: '/hrm/recruitment',
        description: 'Manage recruitment process, job postings, and new employee onboarding'
      }
    ]
  },
  // Legacy items for backward compatibility
  {
    text: 'Employees',
    icon: PeopleIcon,
    path: '/hr/employees',
    category: 'legacy'
  },
  {
    text: 'Departments',
    icon: BusinessIcon,
    path: '/hr/departments',
    category: 'legacy'
  },
  {
    text: 'Projects',
    icon: ProjectIcon,
    path: '/projects',
    category: 'main'
  },
  {
    text: 'Clients',
    icon: GroupIcon,
    path: '/crm/clients',
    category: 'main'
  },
  {
    text: 'Finance',
    icon: FinanceIcon,
    path: '/finance',
    category: 'main'
  },
  {
    text: 'Assets',
    icon: AssetIcon,
    path: '/assets',
    category: 'main'
  },
  {
    text: 'Smart Chatbot',
    icon: ChatbotIcon,
    path: '/chatbot',
    category: 'ai'
  }
];

// Filter function to get menu items by category
export const getMenuItemsByCategory = (category: string) => {
  return menuConfig.filter(item => item.category === category);
};

// Get all main menu items (excluding legacy unless specified)
export const getMainMenuItems = (includeLegacy = false) => {
  return menuConfig.filter(item => 
    item.category === 'main' || 
    item.category === 'hrm' || 
    item.category === 'ai' ||
    (includeLegacy && item.category === 'legacy')
  );
};

export default menuConfig;
