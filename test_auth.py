#!/usr/bin/env python3
"""
Test script to demonstrate admin API authorization
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"  # Adjust if your server runs on different port
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
ADMIN_USERS_ENDPOINT = f"{BASE_URL}/users"
ADMIN_ROLES_ENDPOINT = f"{BASE_URL}/roles"
ADMIN_PERMISSIONS_ENDPOINT = f"{BASE_URL}/permissions"

def test_admin_api_authorization():
    """Test admin API endpoints with and without authorization"""
    
    print("🔐 Testing Admin API Authorization")
    print("=" * 50)
    
    # Test 1: Try to access admin endpoints without authentication
    print("\n1️⃣ Testing access WITHOUT authentication:")
    print("-" * 40)
    
    endpoints_to_test = [
        ("GET", ADMIN_USERS_ENDPOINT, "Get all admin users"),
        ("POST", ADMIN_USERS_ENDPOINT, "Create admin user"),
        ("GET", ADMIN_ROLES_ENDPOINT, "Get all admin roles"),
        ("GET", ADMIN_PERMISSIONS_ENDPOINT, "Get all admin permissions")
    ]
    
    for method, endpoint, description in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(endpoint)
            elif method == "POST":
                response = requests.post(endpoint, json={})
            
            print(f"❌ {description}: {response.status_code} - {response.reason}")
            if response.status_code == 401:
                print(f"   ✅ Correctly blocked - Authentication required")
            else:
                print(f"   ⚠️  Unexpected status code")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    # Test 2: Login to get access token
    print("\n2️⃣ Testing login to get access token:")
    print("-" * 40)
    
    login_data = {
        "email": "admin@example.com",  # Replace with actual admin credentials
        "password": "admin123"         # Replace with actual admin password
    }
    
    try:
        response = requests.post(LOGIN_ENDPOINT, json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"✅ Login successful!")
            print(f"   Access Token: {access_token[:50]}...")
            print(f"   Token Type: {token_data.get('token_type')}")
            print(f"   User ID: {token_data.get('user_id')}")
            print(f"   Email: {token_data.get('email')}")
            
            # Test 3: Access admin endpoints WITH authentication
            print("\n3️⃣ Testing access WITH authentication:")
            print("-" * 40)
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            for method, endpoint, description in endpoints_to_test:
                try:
                    if method == "GET":
                        response = requests.get(endpoint, headers=headers)
                    elif method == "POST":
                        response = requests.post(endpoint, headers=headers, json={})
                    
                    if response.status_code == 200:
                        print(f"✅ {description}: {response.status_code} - Success")
                    elif response.status_code == 422:  # Validation error for POST with empty data
                        print(f"✅ {description}: {response.status_code} - Success (validation error expected)")
                    else:
                        print(f"❌ {description}: {response.status_code} - {response.reason}")
                        
                except Exception as e:
                    print(f"❌ {description}: Error - {e}")
                    
        else:
            print(f"❌ Login failed: {response.status_code} - {response.reason}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 4: Test with invalid token
    print("\n4️⃣ Testing with invalid token:")
    print("-" * 40)
    
    invalid_headers = {"Authorization": "Bearer invalid_token_here"}
    
    try:
        response = requests.get(ADMIN_USERS_ENDPOINT, headers=invalid_headers)
        if response.status_code == 401:
            print(f"✅ Correctly blocked invalid token: {response.status_code} - {response.reason}")
        else:
            print(f"❌ Unexpected response with invalid token: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing invalid token: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Authorization testing completed!")

def show_usage_examples():
    """Show examples of how to use the admin API with authorization"""
    
    print("\n📚 Usage Examples:")
    print("=" * 50)
    
    print("\n1️⃣ Login to get access token:")
    print("""
POST /auth/login
Content-Type: application/json

{
    "email": "admin@example.com",
    "password": "admin123"
}
    """)
    
    print("\n2️⃣ Use access token in Authorization header:")
    print("""
GET /users
Authorization: Bearer <your_access_token_here>
    """)
    
    print("\n3️⃣ Create new admin user:")
    print("""
POST /users
Authorization: Bearer <your_access_token_here>
Content-Type: application/json

{
    "email": "newadmin@example.com",
    "username": "newadmin",
    "full_name": "New Admin User",
    "password": "securepassword123"
}
    """)
    
    print("\n4️⃣ Get all admin roles:")
    print("""
GET /roles
Authorization: Bearer <your_access_token_here>
    """)
    
    print("\n5️⃣ Get all admin permissions:")
    print("""
GET /permissions
Authorization: Bearer <your_access_token_here>
    """)

if __name__ == "__main__":
    test_admin_api_authorization()
    show_usage_examples()
