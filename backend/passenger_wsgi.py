"""
Punto de entrada para cPanel (Phusion Passenger)
FastAPI como WSGI directamente
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar la app al inicio
from app.main import app

# FastAPI es ASGI, pero puede ejecutarse como WSGI con el adapter correcto
application = app
