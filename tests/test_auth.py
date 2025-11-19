"""
Tests for authentication endpoints
"""
import pytest


def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user_data["email"]
    assert data["user"]["username"] == test_user_data["username"]


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email"""
    # Register first user
    client.post("/auth/register", json=test_user_data)

    # Try to register again with same email
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user_data):
    """Test successful login"""
    # Register user
    client.post("/auth/register", json=test_user_data)

    # Login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client, test_user_data):
    """Test login with wrong password"""
    # Register user
    client.post("/auth/register", json=test_user_data)

    # Try to login with wrong password
    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401


def test_get_current_user(client, test_user_data):
    """Test get current user endpoint"""
    # Register user
    register_response = client.post("/auth/register", json=test_user_data)
    token = register_response.json()["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]


def test_get_current_user_unauthorized(client):
    """Test get current user without token"""
    response = client.get("/auth/me")
    assert response.status_code == 403  # No authorization header
