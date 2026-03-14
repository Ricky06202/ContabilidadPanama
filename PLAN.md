# Plan de Desarrollo - ContabilidadPanama

## Visión
Crear una plataforma de contabilidad para Panamá que supere a MYOB, con:
1. Landing Page (captar clientes)
2. Backend API (gestionar datos)
3. Frontend Blazor con MudBlazor (herramienta de uso diario)
4. Cumplimiento con facturación electrónica SFEP/DGI 2026

---

## Fases de Desarrollo

### Fase 1: Planificación y Arquitectura Base ✅ (Completado)
- [x] Estructura de directorios del proyecto
- [x] Landing Page con Astro + Material UI + Tailwind
- [x] Backend API con FastAPI + SQLite
- [x] Frontend Blazor con MudBlazor
- [x] Navegación y layout básico

### Fase 2: Autenticación y Gestión de Usuarios ✅ (Completado)
- [x] Sistema de registro/login
- [x] Gestión de tenants (multi-empresa)
- [x] Roles y permisos
- [x] JWT tokens

### Fase 3: Módulo de Facturación Electrónica (SFEP/DGI) ✅ (Completado)
- [x] Integración con sistema de DGI Panamá
- [x] Generación de facturas electrónicas
- [x] Envío a clientes
- [x] Validación de XML
- [x] Manejo de notas de crédito/débito

### Fase 4: Gestión de Clientes y Proveedores
- [ ] CRUD clientes
- [ ] CRUD proveedores
- [ ] Contactos y direcciones
- [ ] Historial de transacciones

### Fase 5: Gestión de Productos e Inventario
- [ ] Catálogo de productos
- [ ] Control de inventario
- [ ] Variantes (talla, color, etc.)
- [ ] Unidades de medida

### Fase 6: Módulo de Gastos y Compras
- [ ] Registro de gastos
- [ ] Órdenes de compra
- [ ] Recibos de proveedores
- [ ] Categorización de gastos

### Fase 7: Módulo de Bancos y Conciliación
- [ ] Gestión de cuentas bancarias
- [ ] Registro de transacciones bancarias
- [ ] Conciliación automática
- [ ] Depósitos y retiros

### Fase 8: Módulo de Nómina
- [ ] Empleados
- [ ] Liquidación de nómina
- [ ] Generar planillas (PT, IDSS)
- [ ] Roles de pago

### Fase 9: Reportes y Dashboard Financiero
- [ ] Balance general
- [ ] Estado de resultados
- [ ] Flujo de caja
- [ ] Reportes de impuestos
- [ ] Dashboard interactivo

### Fase 10: Integración con MYOB y otros sistemas
- [ ] API para importar/exportar datos
- [ ] Integración con bancos
- [ ] Integración con sistemas de pago

---

## Estado Actual

### ✅ Completado:
- Landing Page funcionando en puerto 4321
- Backend API funcionando en puerto 8000
- Frontend Blazor funcionando en puerto 5000
- Fase 2: Autenticación y Gestión de Usuarios
- Fase 3: Módulo de Facturación Electrónica (SFEP/DGI)

### 📋 Siguiente Paso:
1. Fase 4: Gestión de Clientes y Proveedores

---

## Problemas Conocidos

1. **Blazor se cierra**: El servidor de Blazor se cierra después de iniciar. Posible causa: límite de inotify alcanzado o problema con `dotnet watch`.
   - Solución temporal: Usar `dotnet run --no-launch-profile`

2. **Facturación electrónica**: Pendiente de implementar integración con SFEP/DGI 2026.

---

## Comandos Útiles

```bash
# Landing Page
cd /home/ricky/Documentos/CSharp/ContabilidadPanama/landing && npm run dev

# Backend API
cd /home/ricky/Documentos/CSharp/ContabilidadPanama/backend && uvicorn app.main:app --reload --port 8000

# Frontend Blazor
cd /home/ricky/Documentos/CSharp/ContabilidadPanama/frontend && dotnet run --no-launch-profile --urls "http://0.0.0.0:5000"
```

---

*Última actualización: 2026-03-14*
