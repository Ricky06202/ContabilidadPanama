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

def test_create_client(auth_headers):
    response = client.post("/api/clients", json={
        "ruc": "98765432101",
        "razon_social": "Cliente Test",
        "email": "cliente@test.com",
        "phone": "+507 600-0000"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["ruc"] == "98765432101"

def test_list_clients(auth_headers):
    response = client.get("/api/clients", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_provider(auth_headers):
    response = client.post("/api/providers", json={
        "ruc": "55555555555",
        "razon_social": "Proveedor Test",
        "email": "proveedor@test.com",
        "phone": "+507 700-0000"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["ruc"] == "55555555555"

def test_list_providers(auth_headers):
    response = client.get("/api/providers", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_client(auth_headers):
    create_resp = client.post("/api/clients", json={
        "ruc": "11111111111",
        "razon_social": "Cliente Get"
    }, headers=auth_headers)
    client_id = create_resp.json()["id"]
    
    response = client.get(f"/api/clients/{client_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["razon_social"] == "Cliente Get"

def test_update_client(auth_headers):
    create_resp = client.post("/api/clients", json={
        "ruc": "22222222222",
        "razon_social": "Cliente Original"
    }, headers=auth_headers)
    client_id = create_resp.json()["id"]
    
    response = client.put(f"/api/clients/{client_id}", json={
        "razon_social": "Cliente Modificado"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["razon_social"] == "Cliente Modificado"

def test_delete_client(auth_headers):
    create_resp = client.post("/api/clients", json={
        "ruc": "33333333333",
        "razon_social": "Cliente Delete"
    }, headers=auth_headers)
    client_id = create_resp.json()["id"]
    
    response = client.delete(f"/api/clients/{client_id}", headers=auth_headers)
    assert response.status_code == 204
    
    get_resp = client.get(f"/api/clients/{client_id}", headers=auth_headers)
    assert get_resp.status_code == 404
