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

def test_create_bank_account(auth_headers):
    response = client.post("/api/bank-accounts", json={
        "name": "Cuenta Corriente",
        "bank_name": "Banco General",
        "account_number": "123456789",
        "account_type": "checking",
        "initial_balance": 1000.0
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Cuenta Corriente"
    assert data["current_balance"] == 1000.0

def test_list_bank_accounts(auth_headers):
    response = client.get("/api/bank-accounts", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_bank_account(auth_headers):
    create_resp = client.post("/api/bank-accounts", json={
        "name": "Cuenta Prueba",
        "bank_name": "Banco del Pacífico",
        "account_number": "987654321",
        "account_type": "savings",
        "initial_balance": 500.0
    }, headers=auth_headers)
    account_id = create_resp.json()["id"]
    
    response = client.get(f"/api/bank-accounts/{account_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Cuenta Prueba"

def test_create_bank_transaction_deposit(auth_headers):
    account_resp = client.post("/api/bank-accounts", json={
        "name": "Cuenta Depósito",
        "bank_name": "Banco Nacional",
        "account_number": "111222333",
        "initial_balance": 100.0
    }, headers=auth_headers)
    account_id = account_resp.json()["id"]
    
    response = client.post("/api/bank-transactions", json={
        "account_id": account_id,
        "date": "2026-03-14T10:00:00",
        "description": "Depósito de cliente",
        "reference": "DEP-001",
        "transaction_type": "deposit",
        "amount": 500.0
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 500.0
    assert data["balance_after"] == 600.0

def test_create_bank_transaction_withdrawal(auth_headers):
    account_resp = client.post("/api/bank-accounts", json={
        "name": "Cuenta Retiro",
        "bank_name": "Banco Internacional",
        "account_number": "444555666",
        "initial_balance": 1000.0
    }, headers=auth_headers)
    account_id = account_resp.json()["id"]
    
    response = client.post("/api/bank-transactions", json={
        "account_id": account_id,
        "date": "2026-03-14T11:00:00",
        "description": "Pago proveedor",
        "reference": "RET-001",
        "transaction_type": "withdrawal",
        "amount": 300.0
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 300.0
    assert data["balance_after"] == 700.0

def test_create_bank_transaction_insufficient_funds(auth_headers):
    account_resp = client.post("/api/bank-accounts", json={
        "name": "Cuenta Sin Fondos",
        "bank_name": "Banco Prueba",
        "account_number": "777888999",
        "initial_balance": 100.0
    }, headers=auth_headers)
    account_id = account_resp.json()["id"]
    
    response = client.post("/api/bank-transactions", json={
        "account_id": account_id,
        "date": "2026-03-14T12:00:00",
        "description": "Intento de retiro",
        "transaction_type": "withdrawal",
        "amount": 200.0
    }, headers=auth_headers)
    assert response.status_code == 400
    assert "Saldo insuficiente" in response.json()["detail"]

def test_list_bank_transactions(auth_headers):
    response = client.get("/api/bank-transactions", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_bank_transactions_by_account(auth_headers):
    account_resp = client.post("/api/bank-accounts", json={
        "name": "Cuenta Listado",
        "bank_name": "Banco Listado",
        "account_number": "101010101",
        "initial_balance": 500.0
    }, headers=auth_headers)
    account_id = account_resp.json()["id"]
    
    client.post("/api/bank-transactions", json={
        "account_id": account_id,
        "date": "2026-03-14T13:00:00",
        "description": "Transacción 1",
        "transaction_type": "deposit",
        "amount": 100.0
    }, headers=auth_headers)
    
    response = client.get(f"/api/bank-transactions?account_id={account_id}", headers=auth_headers)
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) >= 1

def test_create_reconciliation(auth_headers):
    account_resp = client.post("/api/bank-accounts", json={
        "name": "Cuenta Conciliación",
        "bank_name": "Banco Conciliación",
        "account_number": "202020202",
        "initial_balance": 1000.0
    }, headers=auth_headers)
    account_id = account_resp.json()["id"]
    
    client.post("/api/bank-transactions", json={
        "account_id": account_id,
        "date": "2026-03-01T10:00:00",
        "description": "Depósito",
        "transaction_type": "deposit",
        "amount": 500.0
    }, headers=auth_headers)
    
    response = client.post("/api/reconciliations", json={
        "account_id": account_id,
        "period_start": "2026-03-01T00:00:00",
        "period_end": "2026-03-31T23:59:59",
        "statement_balance": 1500.0
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["system_balance"] == 1500.0
    assert data["difference"] == 0.0
    assert data["status"] == "completed"

def test_list_reconciliations(auth_headers):
    response = client.get("/api/reconciliations", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
