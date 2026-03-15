"""
Punto de entrada para cPanel (Phusion Passenger)
Patrón de carga perezosa (Lazy Loading)
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Activar virtualenv si existe
venv_bin = os.path.join(os.path.dirname(__file__), "bin")
if os.path.exists(venv_bin) and os.path.exists(os.path.join(venv_bin, "python")):
    venv_lib = os.path.join(os.path.dirname(__file__), "lib")
    sys.path.insert(0, venv_lib)

def application(environ, start_response):
    """Carga perezosa para evitar errores al inicio"""
    from a2wsgi import ASGIMiddleware
    from app.main import app as fastapi_app
    
    app_bridge = ASGIMiddleware(fastapi_app)
    return app_bridge(environ, start_response)
