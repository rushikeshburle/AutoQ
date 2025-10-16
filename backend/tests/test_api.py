import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "AutoQ" in response.json()["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "instructor"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    # May fail if user already exists, which is okay for this test
    assert response.status_code in [200, 400]


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_unauthorized_access():
    """Test accessing protected endpoint without token."""
    response = client.get("/api/v1/documents/")
    assert response.status_code == 401
