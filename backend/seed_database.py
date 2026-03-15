import pymysql
from datetime import datetime, timedelta
import random

# Configuración de conexión
DB_CONFIG = {
    'host': 'ricardosanjur.com',
    'user': 'rsanjur_amado',
    'password': 'Amado_620',
    'database': 'rsanjur_contapanama',
    'charset': 'utf8mb4'
}

def create_tables():
    """Crear todas las tablas necesarias"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    tables = [
        """
        CREATE TABLE IF NOT EXISTS tenants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            ruc VARCHAR(20) UNIQUE,
            address VARCHAR(255),
            phone VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(100) NOT NULL UNIQUE,
            name VARCHAR(100) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            tenant_id INT NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            ruc VARCHAR(20),
            dv VARCHAR(5),
            razon_social VARCHAR(200) NOT NULL,
            nombre_comercial VARCHAR(200),
            email VARCHAR(100),
            phone VARCHAR(20),
            movil VARCHAR(20),
            address VARCHAR(300),
            ciudad VARCHAR(100),
            provincia VARCHAR(100),
            tipo_identificacion VARCHAR(2) DEFAULT '1',
            tipo_cliente VARCHAR(20) DEFAULT 'general',
            limite_credito FLOAT DEFAULT 0,
            saldo_actual FLOAT DEFAULT 0,
            notas TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS providers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            ruc VARCHAR(20),
            dv VARCHAR(5),
            razon_social VARCHAR(200) NOT NULL,
            nombre_comercial VARCHAR(200),
            email VARCHAR(100),
            phone VARCHAR(20),
            movil VARCHAR(20),
            address VARCHAR(300),
            ciudad VARCHAR(100),
            provincia VARCHAR(100),
            tipo_identificacion VARCHAR(2) DEFAULT '1',
            tipo_proveedor VARCHAR(20) DEFAULT 'general',
            cuenta_contable VARCHAR(20),
            notas TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS invoices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            number VARCHAR(20) NOT NULL UNIQUE,
            type VARCHAR(2) DEFAULT '01',
            status VARCHAR(20) DEFAULT 'draft',
            issue_date DATETIME NOT NULL,
            issue_time VARCHAR(8) NOT NULL,
            sender_ruc VARCHAR(20) NOT NULL,
            sender_razon_social VARCHAR(200) NOT NULL,
            sender_dv VARCHAR(5),
            sender_address VARCHAR(300),
            sender_phone VARCHAR(20),
            sender_email VARCHAR(100),
            receiver_ruc VARCHAR(20) NOT NULL,
            receiver_razon_social VARCHAR(200) NOT NULL,
            receiver_dv VARCHAR(5),
            receiver_address VARCHAR(300),
            receiver_email VARCHAR(100),
            receiver_tipo VARCHAR(2) DEFAULT '1',
            subtotal FLOAT DEFAULT 0,
            descuento FLOAT DEFAULT 0,
            itbms FLOAT DEFAULT 0,
            total FLOAT DEFAULT 0,
            total_itbms FLOAT DEFAULT 0,
            currency VARCHAR(3) DEFAULT 'PAB',
            exchange_rate FLOAT DEFAULT 1.0,
            xml_content TEXT,
            cufe VARCHAR(100),
            signature VARCHAR(500),
            dgi_response TEXT,
            related_invoice_id INT,
            reason VARCHAR(300),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (related_invoice_id) REFERENCES invoices(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS invoice_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_id INT NOT NULL,
            line_number INT NOT NULL,
            code VARCHAR(50),
            description VARCHAR(500) NOT NULL,
            quantity FLOAT DEFAULT 1,
            unit_code VARCHAR(3) DEFAULT 'UND',
            unit_price FLOAT NOT NULL,
            discount_percent FLOAT DEFAULT 0,
            discount_amount FLOAT DEFAULT 0,
            subtotal FLOAT NOT NULL,
            itbms_rate FLOAT DEFAULT 0.07,
            itbms_amount FLOAT DEFAULT 0,
            total FLOAT NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            description VARCHAR(300),
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            category_id INT,
            code VARCHAR(50),
            barcode VARCHAR(50),
            name VARCHAR(200) NOT NULL,
            description TEXT,
            unit_code VARCHAR(3) DEFAULT 'UND',
            cost_price FLOAT DEFAULT 0,
            sale_price FLOAT DEFAULT 0,
            sale_price_with_tax FLOAT DEFAULT 0,
            itbms_rate FLOAT DEFAULT 0.07,
            has_inventory BOOLEAN DEFAULT TRUE,
            min_stock FLOAT DEFAULT 0,
            max_stock FLOAT DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            notas TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL UNIQUE,
            quantity FLOAT DEFAULT 0,
            reserved_quantity FLOAT DEFAULT 0,
            available_quantity FLOAT DEFAULT 0,
            location VARCHAR(100),
            last_movement_date DATETIME,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS inventory_movements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            tenant_id INT NOT NULL,
            movement_type VARCHAR(20) NOT NULL,
            quantity FLOAT NOT NULL,
            reference VARCHAR(100),
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS expense_categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            description VARCHAR(300),
            cuenta_contable VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            provider_id INT,
            category_id INT,
            description VARCHAR(300) NOT NULL,
            amount FLOAT NOT NULL,
            itbms_amount FLOAT DEFAULT 0,
            total_amount FLOAT NOT NULL,
            itbms_rate FLOAT DEFAULT 0.07,
            expense_date DATETIME NOT NULL,
            payment_date DATETIME,
            payment_method VARCHAR(20),
            reference VARCHAR(100),
            status VARCHAR(20) DEFAULT 'pending',
            is_deductible BOOLEAN DEFAULT TRUE,
            notas TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (provider_id) REFERENCES providers(id),
            FOREIGN KEY (category_id) REFERENCES expense_categories(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            provider_id INT,
            number VARCHAR(20) UNIQUE,
            status VARCHAR(20) DEFAULT 'draft',
            order_date DATETIME NOT NULL,
            expected_date DATETIME,
            received_date DATETIME,
            subtotal FLOAT DEFAULT 0,
            discount FLOAT DEFAULT 0,
            itbms FLOAT DEFAULT 0,
            total FLOAT DEFAULT 0,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (provider_id) REFERENCES providers(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS purchase_order_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT,
            description VARCHAR(300) NOT NULL,
            quantity FLOAT DEFAULT 1,
            unit_price FLOAT NOT NULL,
            discount_percent FLOAT DEFAULT 0,
            subtotal FLOAT DEFAULT 0,
            received_quantity FLOAT DEFAULT 0,
            FOREIGN KEY (order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS bank_accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            bank_name VARCHAR(100) NOT NULL,
            account_number VARCHAR(50) NOT NULL,
            account_type VARCHAR(20) DEFAULT 'checking',
            initial_balance FLOAT DEFAULT 0,
            current_balance FLOAT DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            notas TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS bank_transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            tenant_id INT NOT NULL,
            date DATETIME NOT NULL,
            description VARCHAR(300) NOT NULL,
            reference VARCHAR(100),
            transaction_type VARCHAR(20) NOT NULL,
            amount FLOAT NOT NULL,
            balance_after FLOAT,
            status VARCHAR(20) DEFAULT 'completed',
            is_reconciled BOOLEAN DEFAULT FALSE,
            reconciliation_date DATETIME,
            notas TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES bank_accounts(id),
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reconciliations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            account_id INT NOT NULL,
            period_start DATETIME NOT NULL,
            period_end DATETIME NOT NULL,
            statement_balance FLOAT NOT NULL,
            system_balance FLOAT NOT NULL,
            difference FLOAT NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (account_id) REFERENCES bank_accounts(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            cedula VARCHAR(20) NOT NULL UNIQUE,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            fecha_nacimiento DATETIME,
            fecha_ingreso DATETIME NOT NULL,
            fecha_salida DATETIME,
            departamento VARCHAR(100),
            cargo VARCHAR(100),
            salario_base FLOAT NOT NULL,
            hora_extra FLOAT DEFAULT 0,
            bonificacion FLOAT DEFAULT 0,
            tipo_contrato VARCHAR(20) DEFAULT 'indefinido',
            es_activo BOOLEAN DEFAULT TRUE,
            notas TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS payrolls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL,
            employee_id INT NOT NULL,
            periodo VARCHAR(20) NOT NULL,
            fecha_pago DATETIME NOT NULL,
            dias_trabajados INT DEFAULT 30,
            horas_extra FLOAT DEFAULT 0,
            bonificacion FLOAT DEFAULT 0,
            salario_bruto FLOAT NOT NULL,
            inss_laboral FLOAT DEFAULT 0,
            IR FLOAT DEFAULT 0,
            total_deducciones FLOAT DEFAULT 0,
            salario_neto FLOAT NOT NULL,
            estado VARCHAR(20) DEFAULT 'pendiente',
            notas TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS payroll_config (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id INT NOT NULL UNIQUE,
            inss_porcentaje FLOAT DEFAULT 6.75,
            inss_empleador_porcentaje FLOAT DEFAULT 12.5,
            fecha_decimo_tercero_inicio INT DEFAULT 4,
            fecha_decimo_tercero_fin INT DEFAULT 3,
            fecha_decimo_cuarto_inicio INT DEFAULT 8,
            fecha_decimo_cuarto_fin INT DEFAULT 7,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
        """
    ]
    
    for table_sql in tables:
        cursor.execute(table_sql)
    
    conn.commit()
    print("✓ Tablas creadas correctamente")
    cursor.close()
    conn.close()

def seed_data():
    """Insertar datos de prueba"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 1. Tenant (Empresa)
    cursor.execute("""
        INSERT INTO tenants (name, ruc, address, phone, is_active)
        VALUES ('Mi Empresa Contable', '1234567-1-123456', 'Ciudad de Panamá, Panama', '+507 123-4567', TRUE)
    """)
    tenant_id = cursor.lastrowid
    print(f"✓ Tenant creado: ID {tenant_id}")
    
    # 2. Usuario Admin
    cursor.execute("""
        INSERT INTO users (email, name, password_hash, tenant_id, role, is_active)
        VALUES ('admin@micontapanama.com', 'Administrador', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS.xJ5m2S', 1, 'admin', TRUE)
    """)
    print("✓ Usuario admin creado")
    
    # 3. Clientes
    clients = [
        ('8-890-1234', '1', 'Empresa ABC S.A.', 'info@empresaabc.com', 'Panamá', '2500.00'),
        ('3-700-5678', '1', 'Corporación XYZ', 'contacto@corpxyz.com', 'Colón', '1800.00'),
        ('4-100-9012', '1', 'Industrias 123', 'compras@industrias123.com', 'David', '3200.00'),
        ('8-750-3456', '1', 'Servicios Generales', 'admin@serviciosgrales.com', 'Panamá Oeste', '950.00'),
        ('9-500-7890', '1', 'Comercial Panameña', 'ventas@comercialpan.com', 'Santiago', '4100.00'),
    ]
    for ruc, dv, name, email, city, saldo in clients:
        cursor.execute("""
            INSERT INTO clients (tenant_id, ruc, dv, razon_social, email, ciudad, saldo_actual, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (tenant_id, ruc, dv, name, email, city, saldo))
    print(f"✓ {len(clients)} clientes creados")
    
    # 4. Proveedores
    providers = [
        ('15555555555', '1', 'Proveedor Principal S.A.', 'proveedor@principal.com', 'Panamá'),
        ('2-100-2000', '1', 'Suministros del Norte', 'orden@suministrosnorte.com', 'Colón'),
        ('3-200-3000', '1', 'Materiales Industriales', 'compras@materialesind.com', 'David'),
        ('4-300-4000', '1', 'Servicios Técnicos', 'facturacion@servtec.com', 'Panamá Oeste'),
        ('5-400-5000', '1', 'Tecnología Avanzada', 'ventas@techadv.com', 'Santiago'),
    ]
    for ruc, dv, name, email, city in providers:
        cursor.execute("""
            INSERT INTO providers (tenant_id, ruc, dv, razon_social, email, ciudad, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
        """, (tenant_id, ruc, dv, name, email, city))
    print(f"✓ {len(providers)} proveedores creados")
    
    # 5. Categorías de Productos
    categories = ['Electrónica', 'Accesorios', 'Suministros', 'Muebles', 'Software']
    for cat in categories:
        cursor.execute("""
            INSERT INTO categories (tenant_id, name, is_active)
            VALUES (%s, %s, TRUE)
        """, (tenant_id, cat))
    print(f"✓ {len(categories)} categorías creadas")
    
    # 6. Productos
    products = [
        ('PROD-001', 'Laptop Dell XPS 15', 1, 850.00, 1200.00, 25),
        ('PROD-002', 'Monitor LG 27"', 1, 250.00, 350.00, 8),
        ('PROD-003', 'Teclado Mecánico', 2, 50.00, 85.00, 25),
        ('PROD-004', 'Mouse Inalámbrico', 2, 15.00, 25.00, 50),
        ('PROD-005', 'Escritorio Ejecutivo', 4, 350.00, 550.00, 5),
        ('PROD-006', 'Silla Ergonómica', 4, 200.00, 350.00, 10),
        ('PROD-007', 'Licencia Office 365', 5, 80.00, 120.00, 100),
        ('PROD-008', 'Webcam HD', 1, 45.00, 75.00, 30),
    ]
    for code, name, cat_id, cost, price, stock in products:
        cursor.execute("""
            INSERT INTO products (tenant_id, category_id, code, name, cost_price, sale_price, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
        """, (tenant_id, cat_id, code, name, cost, price))
        product_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO inventory (product_id, quantity, available_quantity)
            VALUES (%s, %s, %s)
        """, (product_id, stock, stock))
    print(f"✓ {len(products)} productos creados con inventario")
    
    # 7. Facturas
    base_date = datetime.now()
    for i in range(1, 11):
        issue_date = base_date - timedelta(days=i*3)
        cursor.execute("""
            INSERT INTO invoices (tenant_id, number, type, status, issue_date, issue_time,
                sender_ruc, sender_razon_social, sender_address,
                receiver_ruc, receiver_razon_social, receiver_address,
                subtotal, itbms, total, currency)
            VALUES (%s, %s, '01', 'validated', %s, '10:30:00',
                '1234567-1-123456', 'Mi Empresa Contable', 'Panamá',
                '8-890-1234', 'Empresa ABC S.A.', 'Panamá',
                %s, %s, %s, 'USD')
        """, (tenant_id, f'FAC-{i:04d}', issue_date, 1000*i*0.93, 70*i, 1070*i))
    print("✓ 10 facturas creadas")
    
    # 8. Categorías de Gastos
    expense_cats = ['Inmuebles', 'Servicios', 'Suministros', 'Mantenimiento', 'Transporte', 'Marketing', 'Administración', 'Otros']
    for cat in expense_cats:
        cursor.execute("""
            INSERT INTO expense_categories (tenant_id, name, is_active)
            VALUES (%s, %s, TRUE)
        """, (tenant_id, cat))
    print(f"✓ {len(expense_cats)} categorías de gastos creadas")
    
    # 9. Gastos
    expense_desc = [
        ('Alquiler oficina', 1500.00, 1, 'Pagado'),
        ('Servicios públicos', 350.00, 2, 'Pendiente'),
        ('Materiales oficina', 225.50, 3, 'Pagado'),
        ('Mantenimiento equipo', 180.00, 4, 'Pagado'),
        ('Transporte empleados', 400.00, 5, 'Pagado'),
    ]
    for desc, amount, cat_id, status in expense_desc:
        cursor.execute("""
            INSERT INTO expenses (tenant_id, description, amount, itbms_amount, total_amount, category_id, expense_date, status, is_deductible)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (tenant_id, desc, amount, amount*0.07, amount*1.07, cat_id, base_date - timedelta(days=random.randint(1,30)), status))
    print(f"✓ {len(expense_desc)} gastos creados")
    
    # 10. Cuentas Bancarias
    banks = [
        ('Banco General - Cuenta Corriente', 'Banco General', '****4521', 'checking', 25000.00),
        ('Banistmo - Ahorros', 'Banistmo', '****7832', 'savings', 15230.00),
        ('Global Bank - Empresarial', 'Global Bank', '****9012', 'checking', 5000.00),
    ]
    for name, bank, acc_num, acc_type, balance in banks:
        cursor.execute("""
            INSERT INTO bank_accounts (tenant_id, name, bank_name, account_number, account_type, initial_balance, current_balance, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (tenant_id, name, bank, acc_num, acc_type, balance, balance))
    print(f"✓ {len(banks)} cuentas bancarias creadas")
    
    # 11. Transacciones Bancarias
    cursor.execute("SELECT id FROM bank_accounts WHERE tenant_id = %s", (tenant_id,))
    account_ids = [row[0] for row in cursor.fetchall()]
    
    for acc_id in account_ids:
        for i in range(1, 6):
            cursor.execute("""
                INSERT INTO bank_transactions (account_id, tenant_id, date, description, reference, transaction_type, amount, balance_after, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'completed')
            """, (acc_id, tenant_id, base_date - timedelta(days=i), f'Transacción #{i}', f'REF-{i:04d}', 'deposit', random.randint(500, 5000), random.randint(10000, 30000)))
    print("✓ Transacciones bancarias creadas")
    
    # 12. Empleados
    employees = [
        ('8-890-1234', 'Juan', 'Pérez', 'Gerente', 'Administración', 2500.00),
        ('3-700-5678', 'María', 'González', 'Contadora', 'Contabilidad', 1800.00),
        ('4-100-9012', 'Carlos', 'López', 'Asistente', 'Ventas', 1200.00),
        ('8-750-3456', 'Ana', 'Rodríguez', 'Secretaria', 'Administración', 900.00),
        ('9-500-7890', 'Pedro', 'Martínez', 'Técnico', 'Soporte', 1100.00),
    ]
    for cedula, nombre, apellido, cargo, depto, salario in employees:
        cursor.execute("""
            INSERT INTO employees (tenant_id, cedula, nombre, apellido, cargo, departamento, salario_base, fecha_ingreso, es_activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (tenant_id, cedula, nombre, apellido, cargo, depto, salario, base_date - timedelta(days=random.randint(90, 730))))
    print(f"✓ {len(employees)} empleados creados")
    
    # 13. Nómina (últimos 3 meses)
    months = ['Enero 2026', 'Febrero 2026', 'Marzo 2026']
    cursor.execute("SELECT id, salario_base FROM employees WHERE tenant_id = %s", (tenant_id,))
    employee_data = cursor.fetchall()
    
    for month in months:
        for emp_id, salario in employee_data:
            ir = max(0, (salario - 600) * 0.15)  # IR simple
            inss = salario * 0.0675
            deducciones = ir + inss
            neto = salario - deducciones
            cursor.execute("""
                INSERT INTO payrolls (tenant_id, employee_id, periodo, fecha_pago, dias_trabajados, salario_bruto, inss_laboral, IR, total_deducciones, salario_neto, estado)
                VALUES (%s, %s, %s, %s, 30, %s, %s, %s, %s, %s, 'pagado')
            """, (tenant_id, emp_id, month, base_date, salario, inss, ir, deducciones, neto))
    print("✓ Nómina de 3 meses creada")
    
    # 14. Configuración de Nómina
    cursor.execute("""
        INSERT INTO payroll_config (tenant_id) VALUES (%s)
    """, (tenant_id,))
    print("✓ Configuración de nómina creada")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "="*50)
    print("🎉 Seed completado exitosamente!")
    print("="*50)
    print(f"\nDatos insertedos:")
    print(f"  - 1 Empresa (tenant)")
    print(f"  - 1 Usuario admin")
    print(f"  - {len(clients)} Clientes")
    print(f"  - {len(providers)} Proveedores")
    print(f"  - {len(categories)} Categorías")
    print(f"  - {len(products)} Productos")
    print(f"  - 10 Facturas")
    print(f"  - {len(expense_cats)} Categorías de gastos")
    print(f"  - {len(expense_desc)} Gastos")
    print(f"  - {len(banks)} Cuentas bancarias")
    print(f"  - Transacciones bancarias")
    print(f"  - {len(employees)} Empleados")
    print(f"  - Nómina de 3 meses")
    print("\n🔑 Credenciales de acceso:")
    print("   Email: admin@micontapanama.com")
    print("   Contraseña: password123")

if __name__ == "__main__":
    print("Conectando a MySQL...")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"Database: {DB_CONFIG['database']}")
    print()
    
    try:
        create_tables()
        seed_data()
    except Exception as e:
        print(f"❌ Error: {e}")
