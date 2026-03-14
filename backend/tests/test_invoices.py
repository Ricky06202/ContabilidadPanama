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

def test_create_invoice(auth_headers):
    invoice_data = {
        "type": "01",
        "issue_date": "2026-03-14T10:00:00",
        "issue_time": "10:00:00",
        "sender": {"ruc": "12345678901", "razon_social": "Empresa Demo"},
        "receiver": {"ruc": "98765432101", "razon_social": "Cliente Test"},
        "details": [
            {"line_number": 1, "description": "Servicio prueba", "quantity": 1, "unit_price": 100, "itbms_rate": 0.07}
        ]
    }
    response = client.post("/api/invoices/", json=invoice_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["number"] is not None
    assert data["total"] == 107.0
    assert data["status"] == "draft"

def test_list_invoices(auth_headers):
    response = client.get("/api/invoices/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_invoice(auth_headers):
    invoice_data = {
        "type": "01",
        "issue_date": "2026-03-14T10:00:00",
        "issue_time": "10:00:00",
        "sender": {"ruc": "12345678901", "razon_social": "Empresa Demo"},
        "receiver": {"ruc": "98765432101", "razon_social": "Cliente Test"},
        "details": [
            {"line_number": 1, "description": "Test get", "quantity": 2, "unit_price": 50, "itbms_rate": 0.07}
        ]
    }
    create_resp = client.post("/api/invoices/", json=invoice_data, headers=auth_headers)
    invoice_id = create_resp.json()["id"]
    
    response = client.get(f"/api/invoices/{invoice_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == invoice_id
    assert len(data["details"]) > 0

def test_generate_xml(auth_headers):
    invoice_data = {
        "type": "01",
        "issue_date": "2026-03-14T10:00:00",
        "issue_time": "10:00:00",
        "sender": {"ruc": "12345678901", "razon_social": "Empresa Demo"},
        "receiver": {"ruc": "98765432101", "razon_social": "Cliente Test"},
        "details": [
            {"line_number": 1, "description": "Test XML", "quantity": 1, "unit_price": 200, "itbms_rate": 0.07}
        ]
    }
    create_resp = client.post("/api/invoices/", json=invoice_data, headers=auth_headers)
    invoice_id = create_resp.json()["id"]
    
    response = client.post(f"/api/invoices/{invoice_id}/generate-xml", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "xml_content" in data
    assert "cufe" in data
    assert data["cufe"] is not None

def test_sign_invoice(auth_headers):
    invoice_data = {
        "type": "01",
        "issue_date": "2026-03-14T10:00:00",
        "issue_time": "10:00:00",
        "sender": {"ruc": "12345678901", "razon_social": "Empresa Demo"},
        "receiver": {"ruc": "98765432101", "razon_social": "Cliente Test"},
        "details": [
            {"line_number": 1, "description": "Test sign", "quantity": 1, "unit_price": 100, "itbms_rate": 0.07}
        ]
    }
    create_resp = client.post("/api/invoices/", json=invoice_data, headers=auth_headers)
    invoice_id = create_resp.json()["id"]
    
    client.post(f"/api/invoices/{invoice_id}/generate-xml", headers=auth_headers)
    
    response = client.post(f"/api/invoices/{invoice_id}/sign", headers=auth_headers)
    assert response.status_code == 200
    assert "signature" in response.json()

def test_invoice_calculations(auth_headers):
    invoice_data = {
        "type": "01",
        "issue_date": "2026-03-14T10:00:00",
        "issue_time": "10:00:00",
        "sender": {"ruc": "12345678901", "razon_social": "Empresa Demo"},
        "receiver": {"ruc": "98765432101", "razon_social": "Cliente Test"},
        "details": [
            {"line_number": 1, "description": "Item 1", "quantity": 2, "unit_price": 100, "discount_percent": 10, "itbms_rate": 0.07},
            {"line_number": 2, "description": "Item 2", "quantity": 1, "unit_price": 50, "itbms_rate": 0.07}
        ]
    }
    response = client.post("/api/invoices/", json=invoice_data, headers=auth_headers)
    data = response.json()
    
    assert data["subtotal"] == 230.0
    assert data["descuento"] == 20.0
    assert abs(data["total"] - 246.1) < 0.01
