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

def test_dashboard(auth_headers):
    response = client.get("/api/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_clientes" in data
    assert "ventas_mes" in data
    assert "gastos_mes" in data
    assert "bancos_total" in data

def test_balance_general(auth_headers):
    response = client.get("/api/balance-general", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "activos" in data
    assert "pasivos" in data
    assert "patrimonio" in data
    assert "total_activos" in data

def test_estado_resultados(auth_headers):
    response = client.get("/api/estado-resultados", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "ingresos" in data
    assert "utilidad_neta" in data

def test_estado_resultados_with_periodo(auth_headers):
    response = client.get("/api/estado-resultados?periodo=2026-03", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "ingresos" in data

def test_flujo_caja(auth_headers):
    response = client.get("/api/flujo-caja", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "saldo_inicial" in data
    assert "entradas" in data
    assert "salidas" in data
    assert "saldo_final" in data

def test_resumen_impuestos(auth_headers):
    response = client.get("/api/resumen-impuestos", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "itbms_vendido" in data
    assert "itbms_comprado" in data
    assert "itbms_neto" in data

def test_resumen_impuestos_with_periodo(auth_headers):
    response = client.get("/api/resumen-impuestos?periodo=2026-03", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "itbms_neto" in data

def test_dashboard_values(auth_headers):
    response = client.get("/api/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["total_clientes"], int)
    assert isinstance(data["ventas_mes"], (int, float))
    assert isinstance(data["gastos_mes"], (int, float))
