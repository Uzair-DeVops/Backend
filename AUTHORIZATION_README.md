# Admin API Authorization Implementation

This document describes the authorization system implemented for the admin API endpoints to ensure only authenticated admin users can access administrative functions.

## 🔐 Overview

The admin API now requires Bearer token authentication for all administrative operations. Users must first login to obtain an access token, which must then be included in the `Authorization` header for subsequent API calls.

## 🏗️ Architecture

### Authentication Flow

1. **Login**: Admin user provides email/password credentials
2. **Token Generation**: System validates credentials and returns JWT access token
3. **API Access**: Client includes token in `Authorization: Bearer <token>` header
4. **Authorization Check**: Each protected endpoint validates the token and user permissions

### Key Components

#### 1. Auth Utilities (`app/utils/auth_utils.py`)

- `get_current_admin_user()`: Extracts and validates Bearer token
- `require_admin_user()`: Dependency that enforces admin authentication
- JWT token verification and user validation
- Password hashing and verification

#### 2. Protected Routes

All admin-related routes now require authentication:

- **Admin Users**: `/users/*`
- **Admin Roles**: `/roles/*`
- **Admin Permissions**: `/permissions/*`
- **Enterprise Admins**: `/enterprise-admins/*`
- **Enterprise Clients**: `/enterprise-clients/*`

## 🚀 Usage

### 1. Login to Get Access Token

```bash
POST /auth/login
Content-Type: application/json

{
    "email": "admin@example.com",
    "password": "admin123"
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user_id": "uuid-here",
  "email": "admin@example.com",
  "username": "admin",
  "full_name": "Admin User",
  "role_ids": [],
  "permissions": [],
  "user_type": "admin"
}
```

### 2. Use Token in API Calls

Include the access token in the `Authorization` header:

```bash
GET /users
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 3. Example API Calls

#### Create Admin User

```bash
POST /users
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "email": "newadmin@example.com",
    "username": "newadmin",
    "full_name": "New Admin User",
    "password": "securepassword123"
}
```

#### Get All Admin Users

```bash
GET /users
Authorization: Bearer <your_token>
```

#### Get Admin Roles

```bash
GET /roles
Authorization: Bearer <your_token>
```

#### Get Admin Permissions

```bash
GET /permissions
Authorization: Bearer <your_token>
```

## 🛡️ Security Features

### Token Validation

- **JWT Verification**: Tokens are cryptographically signed and verified
- **Expiration**: Tokens expire after 7 days (configurable)
- **User Validation**: Token payload is validated against database
- **Active User Check**: Only active users can use their tokens

### Error Handling

- **401 Unauthorized**: Invalid or missing token
- **401 Unauthorized**: Inactive user
- **401 Unauthorized**: User not found
- **Proper Headers**: WWW-Authenticate headers for proper client handling

### Logging

All authentication and authorization events are logged:

- Login attempts (success/failure)
- Token creation and validation
- API access with user identification
- Authorization failures

## 🔧 Configuration

### JWT Settings (`app/utils/auth_utils.py`)

```python
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
```

### Environment Variables

Set these in your environment or `.env` file:

```bash
SECRET_KEY=your-super-secret-key-here
```

## 🧪 Testing

### Test Script

Use the provided `test_auth.py` script to test the authorization:

```bash
python test_auth.py
```

The script will:

1. Test access without authentication (should fail)
2. Test login to get access token
3. Test access with valid token (should succeed)
4. Test access with invalid token (should fail)

### Manual Testing with curl

#### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

#### Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/users" \
  -H "Authorization: Bearer <your_token_here>"
```

## 📝 Protected Endpoints

### Admin Users (`/users`)

- `POST /` - Create admin user
- `GET /` - Get all admin users
- `GET /{user_id}` - Get specific admin user
- `PUT /{user_id}` - Update admin user
- `PATCH /{user_id}/activate` - Activate user
- `PATCH /{user_id}/deactivate` - Deactivate user
- `DELETE /{user_id}` - Delete admin user

### Admin Roles (`/roles`)

- `POST /` - Create admin role
- `GET /` - Get all admin roles
- `GET /{role_id}` - Get specific admin role

### Admin Permissions (`/permissions`)

- `POST /` - Create admin permission
- `GET /` - Get all admin permissions

### Enterprise Management

- **Enterprise Admins**: `/enterprise-admins/*`
- **Enterprise Clients**: `/enterprise-clients/*`

## 🚨 Error Responses

### Authentication Required

```json
{
  "detail": "Could not validate credentials"
}
```

### Invalid Token

```json
{
  "detail": "Could not validate credentials"
}
```

### Inactive User

```json
{
  "detail": "Inactive user"
}
```

### User Not Found

```json
{
  "detail": "User not found"
}
```

## 🔄 Token Refresh

Tokens can be refreshed using the refresh endpoint:

```bash
POST /auth/refresh
Authorization: Bearer <current_token>
```

## 🗑️ Logout

Logout endpoint (tokens remain valid until expiration):

```bash
POST /auth/logout
Authorization: Bearer <your_token>
```

## 📚 Dependencies

The authorization system relies on:

- `fastapi` - Web framework
- `fastapi.security.HTTPBearer` - Bearer token security
- `jose` - JWT handling
- `passlib` - Password hashing
- `sqlmodel` - Database operations

## 🔐 Best Practices

1. **Secure Storage**: Store tokens securely on the client side
2. **HTTPS**: Always use HTTPS in production
3. **Token Expiration**: Implement token refresh logic
4. **Secret Management**: Use environment variables for secrets
5. **Regular Rotation**: Rotate JWT secret keys periodically
6. **Monitoring**: Monitor authentication logs for suspicious activity

## 🚀 Next Steps

Future enhancements could include:

- Role-based access control (RBAC)
- Permission-based authorization
- Token blacklisting for logout
- Rate limiting for authentication endpoints
- Multi-factor authentication (MFA)
- Session management
