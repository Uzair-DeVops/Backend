# Multi-Role Dashboard Backend with RBAC

## 🎯 Project Overview

A **Multi-Role Based Dashboard Backend** built with FastAPI, implementing a comprehensive Role-Based Access Control (RBAC) system using a **functional approach**. This system allows administrators to create custom roles with predefined scopes, assign multiple roles to users, and manage permissions granularly.

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
│   │   ├── user_model.py      # User model
│   │   ├── role_model.py      # Role model
│   │   ├── scope_model.py     # Scope model
│   │   ├── user_role_model.py # User-Role relationship
│   │   └── role_scope_model.py # Role-Scope relationship
│   │
│   ├── 📁 controllers/           # Business logic (functional)
│   │   ├── 📄 __init__.py
│   │   ├── user_controller.py # User functions
│   │   ├── role_controller.py # Role functions
│   │   ├── scope_controller.py # Scope functions
│   │   └── rbac_controller.py # RBAC relationship functions
│   │
│   ├── 📁 routes/                # API routes
│   │   ├── 📄 __init__.py
│   │   ├── user_routes.py     # User endpoints
│   │   ├── role_routes.py     # Role endpoints
│   │   ├── scope_routes.py    # Scope endpoints
│   │   └── rbac_routes.py     # RBAC endpoints
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
-- Users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Scopes table
CREATE TABLE scopes (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User-Role relationship table
CREATE TABLE user_roles (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    role_id CHAR(36) NOT NULL,
    assigned_by CHAR(36) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    UNIQUE KEY unique_user_role (user_id, role_id)
);

-- Role-Scope relationship table
CREATE TABLE role_scopes (
    id CHAR(36) PRIMARY KEY,
    role_id CHAR(36) NOT NULL,
    scope_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (scope_id) REFERENCES scopes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_scope (role_id, scope_id)
);
```

## 🔐 RBAC System

### Core Concepts

1. **Users**: System users with authentication
2. **Roles**: Named collections of permissions
3. **Scopes**: Individual permissions (resource:action format)
4. **User-Role Assignment**: Users can have multiple roles
5. **Role-Scope Assignment**: Roles can have multiple scopes

### Permission Format

- **Format**: `resource:action`
- **Examples**:
  - `user:read` - Read user data
  - `user:write` - Create/update users
  - `role:manage` - Manage roles
  - `scope:delete` - Delete scopes

## 🚀 API Endpoints

### Authentication

```
POST   /user/login          → Login with email/password
POST   /user/signup         → Create new user account
GET    /user/me             → Get current user info
```

### User Management

```
GET    /user/               → Get all users
GET    /user/{user_id}      → Get user by ID
PUT    /user/{user_id}      → Update user
DELETE /user/{user_id}      → Delete user
```

### Role Management

```
POST   /role/               → Create new role
GET    /role/               → Get all roles
GET    /role/{role_id}      → Get role by ID
PUT    /role/{role_id}      → Update role
DELETE /role/{role_id}      → Delete role
```

### Scope Management

```
POST   /scope/              → Create new scope
GET    /scope/              → Get all scopes
GET    /scope/{scope_id}    → Get scope by ID
PUT    /scope/{scope_id}    → Update scope
DELETE /scope/{scope_id}    → Delete scope
```

### RBAC Management

```
POST   /rbac/user-role      → Assign role to user
DELETE /rbac/user-role/{user_id}/{role_id} → Remove role from user
GET    /rbac/user-role/{user_id} → Get user's roles
GET    /rbac/role-users/{role_id} → Get users with role

POST   /rbac/role-scope     → Assign scope to role
DELETE /rbac/role-scope/{role_id}/{scope_id} → Remove scope from role
GET    /rbac/role-scope/{role_id} → Get role's scopes

GET    /rbac/user-permissions/{user_id} → Get user's permissions
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

The system includes predefined scopes and roles:

### Default Scopes

- `user:read` - Read user information
- `user:write` - Create/update users
- `user:delete` - Delete users
- `role:read` - Read role information
- `role:write` - Create/update roles
- `role:delete` - Delete roles
- `scope:read` - Read scope information
- `scope:write` - Create/update scopes
- `scope:delete` - Delete scopes

### Default Roles

- `admin` - Full system access
- `finance_team` - Finance-related permissions
- `account_team` - Account management permissions
- `support_team` - Support-related permissions

## 🔒 Security Features

- **JWT Authentication** with refresh tokens
- **Password Hashing** with bcrypt
- **Role-Based Access Control** (RBAC)
- **Granular Permissions** with resource:action format
- **Foreign Key Constraints** for data integrity
- **UUID Primary Keys** to avoid ID conflicts

## 📚 Key Benefits

### ✅ **No Foreign Key Ambiguity**

- Separate relationship tables for user-role and role-scope
- Clear foreign key references
- Proper cascade deletion

### ✅ **Functional Approach**

- No class-based services
- Pure functions for business logic
- Easy to test and maintain

### ✅ **Scalable Architecture**

- UUID primary keys for distributed systems
- Proper indexing on foreign keys
- Efficient permission checking

### ✅ **Production Ready**

- Comprehensive error handling
- Structured logging
- Docker containerization
- Health check endpoints

## 🚀 Future Enhancements

- **Permission Caching** with Redis
- **Audit Logging** for all RBAC changes
- **Dynamic Permission Checking** middleware
- **Bulk Role Assignment** operations
- **Permission Templates** for common use cases

---

**This RBAC system provides a solid foundation for scalable, secure multi-role applications with no foreign key ambiguity issues.**
