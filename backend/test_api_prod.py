#!/usr/bin/env python3
"""Script para probar la API en producción"""

import requests

BASE_URL = "https://app.contapanama.rsanjur.com/api"

def test_login():
    """Prueba el endpoint de login"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@micontapanama.com",
        "password": "password123"
    })
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Token recibido: {data.get('access_token', '')[:50]}...")
        return data.get('access_token')
    else:
        print(f"  ✗ Error: {response.text}")
        return None

def test_clients(token):
    """Prueba el endpoint de clientes"""
    response = requests.get(
        f"{BASE_URL}/clients",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Clients: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ {len(data)} clientes encontrados")
    else:
        print(f"  ✗ Error: {response.text}")

def test_invoices(token):
    """Prueba el endpoint de facturas"""
    response = requests.get(
        f"{BASE_URL}/invoices",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Invoices: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ {len(data)} facturas encontradas")
    else:
        print(f"  ✗ Error: {response.text}")

def test_providers(token):
    """Prueba el endpoint de proveedores"""
    response = requests.get(
        f"{BASE_URL}/providers",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Providers: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ {len(data)} proveedores encontrados")
    else:
        print(f"  ✗ Error: {response.text}")

def test_products(token):
    """Prueba el endpoint de productos"""
    response = requests.get(
        f"{BASE_URL}/products",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Products: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ {len(data)} productos encontrados")
    else:
        print(f"  ✗ Error: {response.text}")

if __name__ == "__main__":
    print("=" * 50)
    print("Probando API de Producción")
    print("=" * 50)
    
    token = test_login()
    
    if token:
        print()
        test_clients(token)
        test_invoices(token)
        test_providers(token)
        test_products(token)
