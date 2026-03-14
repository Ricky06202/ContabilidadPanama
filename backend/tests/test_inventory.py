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

def test_create_category(auth_headers):
    response = client.post("/api/categories", json={
        "name": "Electrónicos"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Electrónicos"

def test_create_product_with_inventory(auth_headers):
    response = client.post("/api/products", json={
        "name": "Producto Test Inv",
        "code": "PROD-TEST-INV-001",
        "sale_price": 100,
        "cost_price": 50,
        "has_inventory": True,
        "initial_quantity": 10,
        "location": "Bodega A"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Producto Test Inv"
    assert data["quantity"] == 10
    assert data["available_quantity"] == 10

def test_list_products(auth_headers):
    response = client.get("/api/products", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product(auth_headers):
    create_resp = client.post("/api/products", json={
        "name": "Producto Get",
        "sale_price": 100,
        "has_inventory": True,
        "initial_quantity": 5
    }, headers=auth_headers)
    product_id = create_resp.json()["id"]
    
    response = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Producto Get"

def test_inventory_movement_entrada(auth_headers):
    create_resp = client.post("/api/products", json={
        "name": "Producto Movimiento",
        "sale_price": 100,
        "has_inventory": True,
        "initial_quantity": 0
    }, headers=auth_headers)
    product_id = create_resp.json()["id"]
    
    response = client.post("/api/inventory/movements", json={
        "product_id": product_id,
        "movement_type": "entrada",
        "quantity": 20,
        "reference": "OC-001"
    }, headers=auth_headers)
    assert response.status_code == 200
    
    product_resp = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert product_resp.json()["quantity"] == 20
    assert product_resp.json()["available_quantity"] == 20

def test_inventory_movement_salida(auth_headers):
    create_resp = client.post("/api/products", json={
        "name": "Producto Salida",
        "sale_price": 100,
        "has_inventory": True,
        "initial_quantity": 10
    }, headers=auth_headers)
    product_id = create_resp.json()["id"]
    
    response = client.post("/api/inventory/movements", json={
        "product_id": product_id,
        "movement_type": "salida",
        "quantity": 3,
        "reference": "FV-001"
    }, headers=auth_headers)
    assert response.status_code == 200
    
    product_resp = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert product_resp.json()["quantity"] == 7

def test_update_product_price(auth_headers):
    create_resp = client.post("/api/products", json={
        "name": "Producto Precio",
        "sale_price": 100,
        "itbms_rate": 0.07
    }, headers=auth_headers)
    product_id = create_resp.json()["id"]
    
    response = client.put(f"/api/products/{product_id}", json={
        "sale_price": 150
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["sale_price"] == 150
    assert response.json()["sale_price_with_tax"] == 160.5

def test_delete_product(auth_headers):
    create_resp = client.post("/api/products", json={
        "name": "Producto Delete",
        "code": "PROD-DEL-001",
        "sale_price": 100
    }, headers=auth_headers)
    product_id = create_resp.json()["id"]
    
    response = client.delete(f"/api/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204
    
    get_resp = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert get_resp.status_code == 404
