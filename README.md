# ERP System - Enterprise Resource Planning

A comprehensive Enterprise Resource Planning (ERP) system designed specifically for IT companies, built with Django REST Framework backend, React TypeScript frontend, and PostgreSQL database.

## 🏗️ Architecture Overview

### Technology Stack
- **Backend**: Django 4.2.7 + Django REST Framework
- **Frontend**: React 18 with TypeScript
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: DRF Spectacular (Swagger/OpenAPI)
- **Task Queue**: Celery with Redis
- **State Management**: Redux Toolkit

### Project Structure
```
ERP/
├── backend/                 # Django REST API
│   ├── erp_core/           # Django project settings
│   ├── accounts/           # User management & authentication
│   ├── hr/                 # Human Resources management
│   ├── crm/                # Customer Relationship Management
│   ├── projects/           # Project management
│   ├── finance/            # Financial management
│   ├── assets/             # Asset management
│   ├── static/             # Static files
│   ├── media/              # Media uploads
│   ├── templates/          # Email templates
│   └── logs/               # Application logs
├── frontend/               # React TypeScript application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── store/          # Redux store configuration
│   │   ├── services/       # API service functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
└── docs/                   # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Redis (for Celery tasks)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update database credentials and other settings

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies** (already done):
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

## 📋 ERP Modules

### 1. User Management & Authentication (`accounts`)
- Custom User model with employee profile
- JWT-based authentication
- Role-based access control
- Department and designation management
- User registration and profile management

### 2. Human Resources (`hr`)
- Employee onboarding and management
- Leave management system
- Attendance tracking
- Performance reviews
- Payroll management

### 3. Customer Relationship Management (`crm`)
- Lead management
- Client portfolio
- Communication tracking
- Sales pipeline
- Contact management

### 4. Project Management (`projects`)
- Project planning and tracking
- Task management
- Resource allocation
- Time tracking
- Project reporting

### 5. Financial Management (`finance`)
- Invoicing system
- Expense tracking
- Budget management
- Tax management
- Financial reporting

### 6. Asset Management (`assets`)
- IT equipment tracking
- Software license management
- Asset allocation
- Maintenance schedules
- Asset depreciation

## 🔧 Key Features

### Backend Features
- **RESTful API**: Well-structured API endpoints with DRF
- **Authentication**: JWT-based authentication with refresh tokens
- **Database**: PostgreSQL with optimized queries
- **Documentation**: Auto-generated API documentation with Swagger
- **Security**: Built-in security features and validation
- **Audit Trail**: Track all data changes with django-simple-history
- **File Handling**: Secure file upload and management
- **Background Tasks**: Celery for email, notifications, and reports

### Frontend Features
- **Modern UI**: Material-UI design components
- **TypeScript**: Type-safe development
- **State Management**: Redux Toolkit for efficient state handling
- **Routing**: React Router for navigation
- **Responsive**: Mobile-friendly responsive design
- **Charts & Analytics**: Data visualization with Recharts
- **Form Handling**: Robust form validation
- **Real-time Updates**: WebSocket support for live updates

## 🛠️ Development Guidelines

### Backend Development
- Follow Django best practices
- Use Django REST Framework for API development
- Implement proper error handling and validation
- Write unit tests for models and views
- Use Django's built-in security features
- Follow PEP 8 coding standards

### Frontend Development
- Follow React best practices and hooks
- Use TypeScript for type safety
- Implement responsive design with Material-UI
- Use Redux Toolkit for state management
- Write unit tests with Jest and React Testing Library
- Follow ESLint and Prettier configurations

## 📊 Database Schema

### Core Models
- **User**: Extended user model with employee information
- **Department**: Organizational departments
- **Designation**: Job titles and positions

### HR Models
- Employee profiles, leaves, attendance, payroll

### CRM Models
- Clients, leads, contacts, communications

### Project Models
- Projects, tasks, time entries, resources

### Finance Models
- Invoices, expenses, budgets, transactions

### Asset Models
- Equipment, software licenses, allocations

## 🔐 Security Features

- JWT authentication with access and refresh tokens
- Role-based access control (RBAC)
- Input validation and sanitization
- SQL injection protection
- XSS protection
- CSRF protection
- Secure file upload handling
- Password hashing with Django's built-in system

## 📈 API Documentation

Once the server is running, access API documentation at:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in production
2. Configure proper database settings
3. Set up static file serving (nginx/Apache)
4. Configure email settings
5. Set up SSL certificates
6. Configure Redis for production
7. Set up Celery workers

### Docker Deployment
Docker configurations can be added for containerized deployment.

## 📞 Support & Contributing

For support or contributions:
1. Create detailed issue reports
2. Follow coding standards
3. Write tests for new features
4. Update documentation

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for IT Companies**
