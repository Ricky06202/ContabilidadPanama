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

### Fase 4: Gestión de Clientes y Proveedores ✅
- [x] CRUD clientes
- [x] CRUD proveedores
- [x] Contactos y direcciones
- [x] Límites de crédito

### Fase 5: Gestión de Productos e Inventario ✅
- [x] Catálogo de productos
- [x] Control de inventario
- [x] Variantes (talla, color, etc.)
- [x] Unidades de medida

### Fase 6: Módulo de Gastos y Compras ✅
- [x] Registro de gastos
- [x] Órdenes de compra
- [x] Recibos de proveedores
- [x] Categorización de gastos

### Fase 7: Módulo de Bancos y Conciliación ✅
- [x] Gestión de cuentas bancarias
- [x] Registro de transacciones bancarias
- [x] Conciliación automática
- [x] Depósitos y retiros

### Fase 8: Módulo de Nómina ✅
- [x] Empleados
- [x] Liquidación de nómina
- [x] Generar planillas (PT, IDSS)
- [x] Roles de pago

### Fase 9: Reportes y Dashboard Financiero ✅
- [x] Balance general
- [x] Estado de resultados
- [x] Flujo de caja
- [x] Reportes de impuestos
- [x] Dashboard interactivo

### Fase 10: Integración con MYOB y otros sistemas ✅
- [x] API para importar/exportar datos
- [x] Configuración de integraciones (MYOB, Stripe, WooCommerce)
- [x] Logs de sincronización

---

## Estado Actual

### ✅ Completado:
- Landing Page funcionando en puerto 4321
- Backend API funcionando en puerto 8000
- Frontend Blazor funcionando en puerto 5000
- ✅ Todas las fases completadas (1-10)

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

# ContabilidadPanama - Plan de Desarrollo

*Última actualización: 2026-03-14 - TODAS LAS FASES COMPLETADAS*

---

# 🚀 FASE 11: Frontend Moderno con UX Premium (EN PROGRESO)

## Objetivo
Crear la interfaz de usuario más moderna e intuitiva para contadores en Panamá, superando la experiencia de aplicaciones legacy como MYOB.

### Progreso
- [x] ThemeService con Dark/Light mode
- [x] ApiService para conexión con backend
- [x] MainLayout mejorado con navegación moderna
- [ ] Dashboard con datos reales
- [ ] Páginas de CRUD (Clients, Products, Invoices, Expenses)
- [ ] Búsqueda global (Ctrl+K)
- [ ] Keyboard shortcuts
- [ ] Floating Action Button

### 🎯 Principios de UX
- **Orientado al Contador**: Cada decisión de diseño pensando en cómo trabaja un contador, no un desarrollador
- **Mínima Curva de Aprendizaje**: El usuario debe sentirse cómodo desde el primer día
- **Eficiencia Máxima**: Acciones frecuentes a un clic de distancia
- **Contexto Siempre Visible**: Información relevante sin necesidad de navegar

### ⚡ Acciones Rápidas (Quick Actions)
- [ ] Botón flotante de acciones rápidas (FAB) en todas las páginas
- [ ] Shortcuts de teclado (Ctrl+N = Nueva Factura, etc.)
- [ ] Búsqueda global con Ctrl+K
- [ ] Recent items / Favoritos

### 🎨 Sistema de Diseño

#### Paleta de Colores - Modo Claro
```
--primary: #2563EB (Azul Empresarial)
--secondary: #7C3AED (Púrpura Innovador)
--success: #10B981 (Verde Panamá)
--warning: #F59E0B (Ámbar Alerta)
--error: #EF4444 (Rojo Error)
--background: #F8FAFC (Fondo Limpio)
--surface: #FFFFFF (Tarjetas)
--text-primary: #1E293B (Texto Principal)
--text-secondary: #64748B (Texto Secundario)
```

#### Paleta de Colores - Modo Oscuro
```
--primary: #3B82F6 (Azul Brillante)
--secondary: #8B5CF6 (Púrpura Luminoso)
--success: #34D399 (Verde Neón)
--warning: #FBBF24 (Ámbar Brillante)
--error: #F87171 (Rojo Suave)
--background: #0F172A (Fondo Oscuro Profundo)
--surface: #1E293B (Superficies Oscuras)
--text-primary: #F1F5F9 (Texto Brillante)
--text-secondary: #94A3B8 (Texto Suave)
```

#### Tipografía
- **Encabezados**: Inter (700) - Limpia y profesional
- **Cuerpo**: Inter (400/500) - Alta legibilidad
- **Números**: JetBrains Mono - Para datos financieros

### 📱 Responsive Design
- [ ] Mobile-first approach
- [ ] Breakpoints: Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)
- [ ] Navigation: Sidebar en desktop → Bottom nav en mobile
- [ ] Tables: Scroll horizontal en mobile, cards en mobile

## 11.2 Componentes UI Modernos

### Navigation (Navegación)
- [ ] Sidebar colapsable con iconos grandes
- [ ] Breadcrumbs dinámicos
- [ ] Indicador de sección actual
- [ ] Mini sidebar para más espacio

### Dashboard
- [ ] KPI Cards con gradientes y animaciones
- [ ] Gráficos interactivos (ventas vs gastos)
- [ ] Alertas/notificaciones visuales
- [ ] Acciones rápidas prominence

### Data Tables (Tablas de Datos)
- [ ] Sorting, filtering, pagination
- [ ] Columnas reordenables
- [ ] Export to Excel/PDF
- [ ] Row selection con acciones masivas

### Forms (Formularios)
- [ ] Validación en tiempo real
- [ ] Auto-save drafts
- [ ] Calculadora automática de impuestos
- [ ] Selects con búsqueda

### Dialogs (Diálogos)
- [ ] Slide-overs para edición rápida
- [ ] Confirm dialogs atractivos
- [ ] Loading states con skeletons

## 11.3 Funcionalidades Avanzadas

### 🔍 Búsqueda Global
- [ ] Ctrl+K para abrir búsqueda
- [ ] Buscar en: facturas, clientes, productos, proveedores
- [ ] Resultados categorizados
- [ ] Acciones desde resultados

### ⌨️ Keyboard Shortcuts
| Shortcut | Acción |
|----------|--------|
| Ctrl+N | Nueva Factura |
| Ctrl+G | Nuevo Gasto |
| Ctrl+K | Búsqueda Global |
| Ctrl+S | Guardar |
| Escape | Cerrar diálogo |

### 🔔 Sistema de Notificaciones
- [ ] Toast notifications
- [ ] Alertas de facturas pendientes
- [ ] Recordatorios de pagos
- [ ] Estado de sincronización

### 📊 Dashboard Contextual
- [ ] Resumen del día
- [ ] Facturas pendientes de enviar
- [ ] Próximos vencimientos
- [ ] Alertas de inventario bajo

## 11.4 Páginas a Implementar

### Pages List
1. **Login** - Modern login con branding
2. **Dashboard** - KPI overview + acciones rápidas
3. **Facturas** - CRUD completo con filtros
4. **Clientes** - Gestión de clientes
5. **Proveedores** - Gestión de proveedores  
6. **Productos** - Catálogo e inventario
7. **Gastos** - Registro de gastos
8. **Bancos** - Cuentas y transacciones
9. **Nómina** - Empleados y planillas
10. **Reportes** - Reportes financieros
11. **Configuración** - Empresa, usuario, integraciones
12. **Perfil** - Usuario y preferencias

## 11.5 Tech Stack Frontend
- Blazor WebAssembly
- MudBlazor (componentes)
- Chart.js o ApexCharts para gráficos
- Blazored LocalStorage para preferencias
- AutoMapper para datos

## 11.6 Testing Frontend
- [ ] Tests de componentes con bUnit
- [ ] Tests de integración con Playwright
- [ ] Verificar responsive design
- [ ] Verificar dark/light mode
