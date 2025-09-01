# Main Admin SaaS Backend

## 🎯 Project Overview

A **Main Admin SaaS Backend** built with FastAPI, implementing a comprehensive Role-Based Access Control (RBAC) system using a **functional approach**. This system allows main administrators to create custom roles with predefined permissions, manage enterprise clients, and assign permissions granularly.

## 🏗️ Architecture Pattern

**Functional Approach** with clear separation of concerns:

- **Models**: Database entities using SQLModel with UUID primary keys
- **Controllers**: Business logic functions (no classes)
- **Routes**: API endpoints and HTTP handling
- **Utils**: Shared functionality and dependencies

## 🛠️ Technology Stack

### Core Framework

- **FastAPI** - High-performance async web framework
- **SQLModel** - SQL database library combining SQLAlchemy + Pydantic
- **PyMySQL** - Pure Python MySQL client
- **MySQL** - Reliable relational database
- **UV** - Fast Python package manager

### Authentication & Security

- **JWT** - JSON Web Tokens for stateless authentication
- **python-jose** - JWT encoding/decoding
- **passlib** - Password hashing with bcrypt

## 📁 Project Structure

```
backend/
├── 📄 pyproject.toml              # UV project configuration
├── 📄 uv.lock                     # UV lock file
├── 📄 run.py                      # Application entry point
├── 📄 README.md                   # Project documentation
├── 📄 Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker services
│
├── 📁 app/                        # Main application
│   ├── 📄 __init__.py            # App initialization
│   ├── 📄 app.py                 # FastAPI app setup
│   │
│   ├── 📁 config/                # Configuration
│   │   ├── 📄 __init__.py
│   │   ├── my_settings.py     # Settings
│   │   ├── database.py        # Database config
│   │   └── init_db.py         # Database initialization
│   │
│   ├── 📁 models/                # Data models (SQLModel)
│   │   ├── 📄 __init__.py
│   │   ├── main_admin_user_model.py      # Main admin users
│   │   ├── main_admin_role_model.py      # Main admin roles
│   │   ├── main_admin_permission_model.py # Main admin permissions
│   │   └── enterprise_client_model.py    # Enterprise clients
│   │
│   ├── 📁 controllers/           # Business logic (functional)
│   │   ├── 📄 __init__.py
│   │   └── main_admin_controller.py # Main admin functions
│   │
│   ├── 📁 routes/                # API routes
│   │   ├── 📄 __init__.py
│   │   └── main_admin_routes.py  # Main admin endpoints
│   │
│   └── 📁 utils/                 # Utilities
│       ├── 📄 __init__.py
│       ├── auth_utils.py      # Authentication
│       ├── 📄 database_dependency.py # DB dependency
│       └── my_logger.py       # Logging
```

## 🗄️ Database Schema

### Core Tables (UUID Primary Keys)

```sql
-- Main admin users table
CREATE TABLE main_admin_users (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id CHAR(36),
    permissions TEXT DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES main_admin_roles(id)
);

-- Main admin roles table
CREATE TABLE main_admin_roles (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Main admin permissions table
CREATE TABLE main_admin_permissions (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Enterprise clients table
CREATE TABLE enterprise_clients (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔐 RBAC System

### Core Concepts

1. **Main Admin Users**: System administrators with authentication
2. **Roles**: Named collections of permissions (admin, finance, support, etc.)
3. **Permissions**: Individual permissions (resource:action format)
4. **Enterprise Clients**: Organizations managed by main admin

### Permission Format

- **Format**: `resource:action`
- **Examples**:
  - `enterprise:create` - Create enterprise clients
  - `enterprise:read` - View enterprise information
  - `main_admin_user:manage` - Manage main admin users
  - `role:manage` - Manage roles and permissions

## 🚀 API Endpoints

### Main Admin User Management

```
POST   /main-admin/users              → Create new main admin user
GET    /main-admin/users              → Get all main admin users
GET    /main-admin/users/{user_id}    → Get main admin user by ID
PUT    /main-admin/users/{user_id}    → Update main admin user
DELETE /main-admin/users/{user_id}    → Delete main admin user
```

### Main Admin Role Management

```
POST   /main-admin/roles              → Create new role
GET    /main-admin/roles              → Get all roles
GET    /main-admin/roles/{role_id}    → Get role by ID
```

### Main Admin Permission Management

```
POST   /main-admin/permissions        → Create new permission
GET    /main-admin/permissions        → Get all permissions
```

### Enterprise Client Management

```
POST   /main-admin/enterprise-clients → Create new enterprise client
GET    /main-admin/enterprise-clients → Get all enterprise clients
GET    /main-admin/enterprise-clients/{client_id} → Get enterprise client by ID
```

## 🔧 Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- UV package manager

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd backend
```

2. **Install dependencies with UV**

```bash
uv sync
```

3. **Set up environment variables**

```bash
# Create .env file with your database credentials
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
SECRET_KEY=your-secret-key
```

4. **Start the application**

```bash
uv run python run.py
```

## 🐳 Docker Setup

```bash
# Start all services
docker-compose up --build

# Start only MySQL
docker-compose up -d mysql
```

## 🧪 Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=app
```

## 🔑 Default Data

The system includes predefined roles and permissions:

### Default Roles

- `main_admin` - Main system administrator with full access
- `finance_manager` - Finance team manager
- `support_manager` - Support team manager
- `account_manager` - Account management team

### Default Permissions

- `create_enterprise` - Create new enterprise clients
- `view_enterprise` - View enterprise client information
- `update_enterprise` - Update enterprise client information
- `delete_enterprise` - Delete enterprise clients
- `create_main_admin_user` - Create main admin users
- `view_main_admin_users` - View main admin users
- `update_main_admin_user` - Update main admin users
- `delete_main_admin_user` - Delete main admin users
- `manage_roles` - Manage roles and permissions

### Default Main Admin User

- **Email**: `mainadmin@example.com`
- **Password**: `mainadmin123`
- **Role**: `main_admin` with all permissions

## 🔒 Security Features

- **JWT Authentication** with refresh tokens
- **Password Hashing** with bcrypt
- **Role-Based Access Control** (RBAC)
- **Granular Permissions** with resource:action format
- **Foreign Key Constraints** for data integrity
- **UUID Primary Keys** to avoid ID conflicts

## 📚 Key Benefits

### ✅ **Simple and Clean Architecture**

- **Functional approach** - No complex classes
- **Direct role assignment** - role_id foreign key
- **JSON permissions** - Flexible permission storage
- **Easy to understand** and maintain

### ✅ **Production Ready**

- **Comprehensive error handling**
- **Structured logging**
- **Docker containerization**
- **Health check endpoints**

### ✅ **Scalable Design**

- **UUID primary keys** for distributed systems
- **Proper indexing** on foreign keys
- **Efficient permission checking**

## 🚀 Future Enhancements

- **Enterprise Level** - Enterprise users and their permissions
- **End Client Level** - Individual end users
- **Permission Caching** with Redis
- **Audit Logging** for all changes
- **Dynamic Permission Checking** middleware

---

**This Main Admin system provides a solid foundation for scalable, secure SaaS applications with clean architecture and no complexity.**
