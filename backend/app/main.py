from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events - ejecuta solo una vez al iniciar"""
    # Importar y crear tablas solo si no existen
    from app.database import engine
    from app.models.models import Base as ModelBase
    from app.models.invoice import Base as InvoiceBase
    from app.models.entities import Base as EntityBase
    from app.models.inventory import Base as InventoryBase
    from app.models.expenses import Base as ExpenseBase
    from app.models.banking import Base as BankingBase
    from app.models.payroll import Base as PayrollBase
    from app.models.reports import Base as ReportsBase
    from app.models.integrations import Base as IntegrationsBase
    
    # Crear tablas si no existen (solo estructura, no borra datos)
    for base in [ModelBase, InvoiceBase, EntityBase, InventoryBase, 
                 ExpenseBase, BankingBase, PayrollBase, ReportsBase, IntegrationsBase]:
        base.metadata.create_all(bind=engine)
    
    yield
    # Shutdown - si necesitas algo al cerrar

app = FastAPI(
    title="ContabilidadPanama API", 
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers después de definir app para evitar ciclos
from app.routers import auth, tenants, users, invoices, entities, inventory, expenses, banking, payroll, reports, integrations
app.include_router(auth.router, prefix="/api")
app.include_router(tenants.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(invoices.router, prefix="/api")
app.include_router(entities.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")
app.include_router(banking.router, prefix="/api")
app.include_router(payroll.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(integrations.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "ContabilidadPanama API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
