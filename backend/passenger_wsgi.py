"""
Punto de entrada para cPanel (Phusion Passenger)
Usando a2wsgi con lazy loading para FastAPI
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Lazy loading - no importar hasta que Passenger llame a la aplicación
# Esto evita errores de importación en el arranque de cPanel

def application(environ, start_response):
    """WSGI entry point con lazy loading usando a2wsgi"""
    from a2wsgi import ASGIMiddleware
    
    # Importar la app FastAPI solo cuando se necesita
    from app.main import app
    
    # Convertir ASGI a WSGI sin threading
    asgi_middleware = ASGIMiddleware(app, use_asgi_loop=False)
    
    return asgi_middleware(environ, start_response)
