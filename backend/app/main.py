from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, get_db
from app.models.models import Base as ModelBase
from app.models.invoice import Base as InvoiceBase
from app.models.entities import Base as EntityBase
from app.models.inventory import Base as InventoryBase
from app.models.expenses import Base as ExpenseBase
from app.models.banking import Base as BankingBase
from app.models.payroll import Base as PayrollBase
from app.models.reports import Base as ReportsBase
from app.models.integrations import Base as IntegrationsBase

ModelBase.metadata.create_all(bind=engine)
InvoiceBase.metadata.create_all(bind=engine)
EntityBase.metadata.create_all(bind=engine)
InventoryBase.metadata.create_all(bind=engine)
ExpenseBase.metadata.create_all(bind=engine)
BankingBase.metadata.create_all(bind=engine)
PayrollBase.metadata.create_all(bind=engine)
ReportsBase.metadata.create_all(bind=engine)
IntegrationsBase.metadata.create_all(bind=engine)

app = FastAPI(title="ContabilidadPanama API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
