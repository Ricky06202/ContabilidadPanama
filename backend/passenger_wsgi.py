import os
import sys

# 1. Agregamos el directorio actual al Path de Python
sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    """
    Patrón de Carga Perezosa (Lazy Loading):
    Importamos dentro de la función para asegurar que el entorno esté 100% listo 
    antes de cargar FastAPI. Esto es más robusto en ciertos servidores cPanel.
    """
    from a2wsgi import ASGIMiddleware
    from main import app as fastapi_app
    
    # Creamos el puente y lo ejecutamos
    app_bridge = ASGIMiddleware(fastapi_app)
    return app_bridge(environ, start_response)
