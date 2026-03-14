from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    ruc: Optional[str] = None
    dv: Optional[str] = None
    razon_social: str
    nombre_comercial: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    movil: Optional[str] = None
    address: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    tipo_identificacion: str = "1"
    tipo_cliente: str = "general"
    limite_credito: float = 0
    notas: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    razon_social: Optional[str] = None
    nombre_comercial: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    movil: Optional[str] = None
    address: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    tipo_cliente: Optional[str] = None
    limite_credito: Optional[float] = None
    notas: Optional[str] = None
    is_active: Optional[bool] = None

class ClientResponse(ClientBase):
    id: int
    tenant_id: int
    saldo_actual: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProviderBase(BaseModel):
    ruc: Optional[str] = None
    dv: Optional[str] = None
    razon_social: str
    nombre_comercial: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    movil: Optional[str] = None
    address: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    tipo_identificacion: str = "1"
    tipo_proveedor: str = "general"
    cuenta_contable: Optional[str] = None
    notas: Optional[str] = None

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(BaseModel):
    razon_social: Optional[str] = None
    nombre_comercial: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    movil: Optional[str] = None
    address: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    tipo_proveedor: Optional[str] = None
    cuenta_contable: Optional[str] = None
    notas: Optional[str] = None
    is_active: Optional[bool] = None

class ProviderResponse(ProviderBase):
    id: int
    tenant_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
