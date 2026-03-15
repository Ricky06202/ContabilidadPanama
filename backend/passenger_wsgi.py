"""
Punto de entrada para cPanel (Phusion Passenger)
Intentar usar xvicorn directamente
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Activar el virtualenv si existe
venv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "python")
if os.path.exists(venv) and sys.executable != venv:
    os.execl(venv, venv, *sys.argv)

# Importar la app FastAPI
from app.main import app

# Usar la app directamente - esto requiere que cPanel esté configurado para ASGI
application = app
