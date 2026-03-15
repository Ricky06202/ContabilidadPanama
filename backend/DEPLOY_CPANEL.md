# Deploy en cPanel - ContabilidadPanama

## Requisitos previos

1. Subdominio configurado en cPanel (ej: `app.contapanama.rsanjur.com`)
2. Python App creada en cPanel (Setup Python App)
3. MySQL con la base de datos creada

## Dependencias requeridas en requirements.txt

```
fastapi
sqlalchemy
pymysql
cryptography
bcrypt
python-jose
python-dotenv
uvicorn
pydantic
pydantic-core
email-validator
httpx
a2wsgi
python-dateutil
```

**Importante**: Asegurarse de tener `a2wsgi` y `bcrypt` en requirements.txt.

## Estructura de carpetas

```
/home/usuario/
├── passenger_wsgi.py (entrada para Passenger)
├── app/                 (código de la API)
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   └── ...
├── requirements.txt     (dependencias)
└── venv/               (entorno virtual - opcional)
```

## Opción 1: Python App de cPanel (Recomendado)

### Paso 1: Crear aplicación Python
1. Entrar a cPanel → **Setup Python App**
2. Crear nueva aplicación:
   - Domain: `app.contapanama.rsanjur.com`
   - Python version: `3.11` o `3.12`
   - App root: `/app.contapanama` (o la carpeta que prefieras)
   - App startup file: `passenger_wsgi.py`
   - App mode: `Production`

### Paso 2: Instalar dependencias
```bash
# En la terminal de cPanel o SSH:
pip install -r requirements.txt
```

### Paso 3: Archivo passenger_wsgi.py

El archivo debe usar el patrón de carga perezosa con a2wsgi:

```python
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
    from app.main import app as fastapi_app
    
    # Creamos el puente y lo ejecutamos
    app_bridge = ASGIMiddleware(fastapi_app)
    return app_bridge(environ, start_response)
```

### Paso 4: Instalar dependencias en el servidor

```bash
# Activar el virtualenv de la aplicación
source /home/rsanjur/virtualenv/app.contapanama.rsanjur.com/api/3.11/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Verificar que funciona

```bash
# Probar la app
curl https://app.contapanama.rsanjur.com/api/
```

## Solución de problemas

### Error: can't start new thread
El servidor no permite threads. Asegúrate de usar el patrón de carga perezosa mostrado arriba.

### Error: ModuleNotFoundError
Verifica que:
1. El virtualenv tenga instalado a2wsgi: `pip install a2wsgi`
2. El import sea correcto: `from app.main import app`
3. La estructura de carpetas sea: `/api/passenger_wsgi.py` y `/api/app/main.py`

### Error: Password verification fails
El hash de contraseña en la base de datos debe ser bcrypt (no argon2). Actualiza auth.py para usar bcrypt directamente:
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
```

### Paso 4: Configurar Base de Datos

Editar `app/database.py` con tus credenciales MySQL:

```python
DATABASE_URL = "mysql+pymysql://usuario:password@hostname:3306/database"
```

## Opción 2: Subdominio con .htaccess

### Paso 1: Crear subdominio
- En cPanel → **Subdomains**
- Crear: `app.contapanama.rsanjur.com`
- Document Root: `/public_html/app.contapanama`

### Paso 2: Archivo .htaccess
```apache
<IfModule mod_proxy.c>
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ http://127.0.0.1:8000/$1 [P,L]
</IfModule>
```

## Variables de Entorno

En cPanel, puedes设置:
- `DATABASE_URL` - Conexión a MySQL
- `SECRET_KEY` - Clave secreta para JWT
- `DEBUG=False` - Modo producción

## Rutas de la API

```
https://app.contapanama.rsanjur.com/api/
├── /api/auth/login
├── /api/clients
├── /api/providers
├── /api/products
├── /api/invoices
├── /api/expenses
├── /api/banking
├── /api/employees
├── /api/payrolls
└── /api/reports
```

## Testing local antes de deploy

```bash
# Instalar dependencias
pip install -r requirements.txt

# Probar que funciona
python -c "from app.main import app; print('OK')"

# Ejecutar servidor local
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Notas

- El archivo `passenger_wsgi.py` debe estar en la raíz de la aplicación
- Asegúrate de que la carpeta `app/` esté en el mismo nivel
- MySQL debe estar configurado en `app/database.py`
- El password en la BD debe estar hasheado con bcrypt
