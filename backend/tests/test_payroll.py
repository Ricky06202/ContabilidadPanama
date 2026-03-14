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

def test_create_employee(auth_headers):
    response = client.post("/api/employees", json={
        "cedula": "8-123-456",
        "nombre": "Juan",
        "apellido": "Pérez",
        "fecha_ingreso": "2026-01-15T10:00:00",
        "departamento": "Contabilidad",
        "cargo": "Contador",
        "salario_base": 1500.0,
        "hora_extra": 10.0,
        "tipo_contrato": "indefinido"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Juan"
    assert data["salario_base"] == 1500.0

def test_list_employees(auth_headers):
    response = client.get("/api/employees", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_employee(auth_headers):
    create_resp = client.post("/api/employees", json={
        "cedula": "8-234-567",
        "nombre": "María",
        "apellido": "García",
        "fecha_ingreso": "2026-02-01T10:00:00",
        "salario_base": 2000.0
    }, headers=auth_headers)
    employee_id = create_resp.json()["id"]
    
    response = client.get(f"/api/employees/{employee_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == "María"

def test_update_employee(auth_headers):
    create_resp = client.post("/api/employees", json={
        "cedula": "8-345-678",
        "nombre": "Pedro",
        "apellido": "López",
        "fecha_ingreso": "2026-01-01T10:00:00",
        "salario_base": 1200.0
    }, headers=auth_headers)
    employee_id = create_resp.json()["id"]
    
    response = client.put(f"/api/employees/{employee_id}", json={
        "cedula": "8-345-678",
        "nombre": "Pedro",
        "apellido": "López",
        "fecha_ingreso": "2026-01-01T10:00:00",
        "salario_base": 1500.0,
        "cargo": "Gerente"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["salario_base"] == 1500.0
    assert response.json()["cargo"] == "Gerente"

def test_delete_employee(auth_headers):
    create_resp = client.post("/api/employees", json={
        "cedula": "8-456-789",
        "nombre": "Ana",
        "apellido": "Rodríguez",
        "fecha_ingreso": "2026-01-01T10:00:00",
        "salario_base": 1000.0
    }, headers=auth_headers)
    employee_id = create_resp.json()["id"]
    
    response = client.delete(f"/api/employees/{employee_id}", headers=auth_headers)
    assert response.status_code == 200
    
    get_resp = client.get(f"/api/employees/{employee_id}", headers=auth_headers)
    assert get_resp.status_code == 404

def test_create_payroll(auth_headers):
    emp_resp = client.post("/api/employees", json={
        "cedula": "8-567-890",
        "nombre": "Carlos",
        "apellido": "Mendoza",
        "fecha_ingreso": "2025-01-01T10:00:00",
        "salario_base": 1800.0
    }, headers=auth_headers)
    employee_id = emp_resp.json()["id"]
    
    response = client.post("/api/payrolls", json={
        "employee_id": employee_id,
        "periodo": "2026-03",
        "fecha_pago": "2026-03-31T10:00:00",
        "dias_trabajados": 30,
        "horas_extra": 5,
        "bonificacion": 50.0
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["salario_bruto"] is not None
    assert data["inss_laboral"] is not None
    assert data["salario_neto"] is not None

def test_list_payrolls(auth_headers):
    response = client.get("/api/payrolls", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_payroll(auth_headers):
    emp_resp = client.post("/api/employees", json={
        "cedula": "8-678-901",
        "nombre": "Laura",
        "apellido": "Fernández",
        "fecha_ingreso": "2025-01-01T10:00:00",
        "salario_base": 2200.0
    }, headers=auth_headers)
    employee_id = emp_resp.json()["id"]
    
    payroll_resp = client.post("/api/payrolls", json={
        "employee_id": employee_id,
        "periodo": "2026-02",
        "fecha_pago": "2026-02-28T10:00:00",
        "dias_trabajados": 30
    }, headers=auth_headers)
    payroll_id = payroll_resp.json()["id"]
    
    response = client.get(f"/api/payrolls/{payroll_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["periodo"] == "2026-02"

def test_payroll_summary(auth_headers):
    emp_resp = client.post("/api/employees", json={
        "cedula": "8-789-012",
        "nombre": "Roberto",
        "apellido": "Arias",
        "fecha_ingreso": "2025-01-01T10:00:00",
        "salario_base": 1600.0
    }, headers=auth_headers)
    employee_id = emp_resp.json()["id"]
    
    client.post("/api/payrolls", json={
        "employee_id": employee_id,
        "periodo": "2026-03",
        "fecha_pago": "2026-03-31T10:00:00",
        "dias_trabajados": 30
    }, headers=auth_headers)
    
    response = client.get("/api/payroll-summary/2026-03", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["periodo"] == "2026-03"
    assert data["total_empleados"] >= 1
    assert data["total_salario_neto"] > 0

def test_payroll_config(auth_headers):
    response = client.get("/api/payroll-config", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "inss_porcentaje" in data

def test_duplicate_employee_cedula(auth_headers):
    client.post("/api/employees", json={
        "cedula": "8-999-999",
        "nombre": "Test",
        "apellido": "User",
        "fecha_ingreso": "2026-01-01T10:00:00",
        "salario_base": 1000.0
    }, headers=auth_headers)
    
    response = client.post("/api/employees", json={
        "cedula": "8-999-999",
        "nombre": "Test2",
        "apellido": "User2",
        "fecha_ingreso": "2026-01-01T10:00:00",
        "salario_base": 1200.0
    }, headers=auth_headers)
    assert response.status_code == 400
    assert "Ya existe" in response.json()["detail"]
