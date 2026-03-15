"""
Punto de entrada para cPanel (Phusion Passenger)
Usando asgiref para convertir FastAPI a WSGI
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def application(environ, start_response):
    """WSGI entry point"""
    from asgiref.wsgi import AsgiApp
    from app.main import app
    
    asgi_app = AsgiApp(app)
    return asgi_app(environ, start_response)
