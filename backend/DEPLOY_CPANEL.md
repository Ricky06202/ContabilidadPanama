# Deploy en cPanel - ContabilidadPanama

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

```python
"""
Punto de entrada para cPanel (Passenger)
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# Retornar la aplicación ASGI
# Passenger会自动处理ASGI应用
app = app
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
