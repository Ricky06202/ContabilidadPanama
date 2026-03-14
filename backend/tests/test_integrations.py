import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    login_resp = client.post("/api/auth/login", json={
        "email": "admin@contabilidad.com",
        "password": "admin123"
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_integration_config(auth_headers):
    response = client.get("/api/integration-config", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "myob_enabled" in data

def test_update_integration_config(auth_headers):
    response = client.put("/api/integration-config", 
        json={"myob_enabled": True, "myob_company_file": "test.company"},
        headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["myob_enabled"] == True

def test_get_available_entities(auth_headers):
    response = client.get("/api/available-entities", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "clients" in data["entities"]
    assert "products" in data["entities"]

def test_export_clients(auth_headers):
    response = client.get("/api/export/clients", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["entity_type"] == "clients"
    assert "data" in data

def test_export_products(auth_headers):
    response = client.get("/api/export/products", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["entity_type"] == "products"

def test_export_invalid_entity(auth_headers):
    response = client.get("/api/export/invalid", headers=auth_headers)
    assert response.status_code == 400

def test_import_clients(auth_headers):
    response = client.post("/api/import/clients", 
        json=[
            {"ruc": "12345678901", "name": "Cliente Importado", "email": "test@test.com"}
        ],
        headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "imported" in data

def test_import_invalid_entity(auth_headers):
    response = client.post("/api/import/invalid", 
        json=[{"name": "test"}],
        headers=auth_headers)
    assert response.status_code == 400

def test_get_sync_logs(auth_headers):
    response = client.get("/api/sync-logs", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
