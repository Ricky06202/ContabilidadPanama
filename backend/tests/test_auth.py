import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ContabilidadPanama API", "version": "1.0.0"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_success():
    response = client.post("/api/auth/login", json={
        "email": "admin@contabilidad.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == "admin@contabilidad.com"

def test_login_invalid_credentials():
    response = client.post("/api/auth/login", json={
        "email": "admin@contabilidad.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_current_user_unauthorized():
    response = client.get("/api/auth/me")
    assert response.status_code == 401
