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

def test_create_expense_category(auth_headers):
    response = client.post("/api/expense-categories", json={
        "name": "Servicios",
        "cuenta_contable": "6101"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Servicios"

def test_create_expense(auth_headers):
    response = client.post("/api/expenses", json={
        "description": "Alquiler oficina",
        "amount": 500,
        "expense_date": "2026-03-14T10:00:00",
        "itbms_rate": 0.07
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Alquiler oficina"
    assert data["amount"] == 500
    assert data["itbms_amount"] == 35.0
    assert data["total_amount"] == 535.0

def test_list_expenses(auth_headers):
    response = client.get("/api/expenses", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_purchase_order(auth_headers):
    response = client.post("/api/purchase-orders", json={
        "order_date": "2026-03-14T10:00:00",
        "notes": "Orden de prueba",
        "details": [
            {"description": "Producto 1", "quantity": 2, "unit_price": 100},
            {"description": "Producto 2", "quantity": 1, "unit_price": 50}
        ]
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["number"] is not None
    assert data["subtotal"] == 250.0
    assert data["total"] == 267.5

def test_list_purchase_orders(auth_headers):
    response = client.get("/api/purchase-orders", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_purchase_order_status(auth_headers):
    create_resp = client.post("/api/purchase-orders", json={
        "order_date": "2026-03-14T10:00:00",
        "details": [{"description": "Item", "quantity": 1, "unit_price": 100}]
    }, headers=auth_headers)
    order_id = create_resp.json()["id"]
    
    response = client.put(f"/api/purchase-orders/{order_id}", json={
        "status": "approved"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "approved"

def test_get_purchase_order(auth_headers):
    create_resp = client.post("/api/purchase-orders", json={
        "order_date": "2026-03-14T10:00:00",
        "details": [{"description": "Item Get", "quantity": 1, "unit_price": 100}]
    }, headers=auth_headers)
    order_id = create_resp.json()["id"]
    
    response = client.get(f"/api/purchase-orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["number"] is not None
    assert len(data["details"]) == 1
