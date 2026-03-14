from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, get_db
from app.models.models import Base as ModelBase
from app.models.invoice import Base as InvoiceBase

ModelBase.metadata.create_all(bind=engine)
InvoiceBase.metadata.create_all(bind=engine)

app = FastAPI(title="ContabilidadPanama API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, tenants, users, invoices
app.include_router(auth.router, prefix="/api")
app.include_router(tenants.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(invoices.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "ContabilidadPanama API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
