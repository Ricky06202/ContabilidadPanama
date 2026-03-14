from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class InvoiceDetailCreate(BaseModel):
    line_number: int
    code: Optional[str] = None
    description: str
    quantity: float = Field(default=1, ge=0)
    unit_code: str = "UND"
    unit_price: float = Field(..., ge=0)
    discount_percent: float = Field(default=0, ge=0, le=100)
    discount_amount: float = Field(default=0, ge=0)
    itbms_rate: float = Field(default=0.07, ge=0, le=1)

class InvoiceDetailResponse(InvoiceDetailCreate):
    id: int
    subtotal: float
    itbms_amount: float
    total: float

    class Config:
        from_attributes = True

class SenderInfo(BaseModel):
    ruc: str = Field(..., min_length=5, max_length=20)
    razon_social: str = Field(..., min_length=1, max_length=200)
    dv: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ReceiverInfo(BaseModel):
    ruc: str = Field(..., min_length=5, max_length=20)
    razon_social: str = Field(..., min_length=1, max_length=200)
    dv: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    tipo: str = "1"

class InvoiceCreate(BaseModel):
    type: str = "01"
    issue_date: datetime
    issue_time: str
    sender: SenderInfo
    receiver: ReceiverInfo
    details: List[InvoiceDetailCreate]
    currency: str = "PAB"
    exchange_rate: float = 1.0
    related_invoice_id: Optional[int] = None
    reason: Optional[str] = None

class InvoiceUpdate(BaseModel):
    status: Optional[str] = None

class InvoiceResponse(BaseModel):
    id: int
    tenant_id: int
    number: str
    type: str
    status: str
    issue_date: datetime
    issue_time: str
    sender_ruc: str
    sender_razon_social: str
    receiver_ruc: str
    receiver_razon_social: str
    subtotal: float
    descuento: float
    itbms: float
    total: float
    currency: str
    exchange_rate: float
    xml_content: Optional[str] = None
    cufe: Optional[str] = None
    signature: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class InvoiceWithDetails(InvoiceResponse):
    details: List[InvoiceDetailResponse] = []

class InvoiceXMLResponse(BaseModel):
    xml_content: str
    cufe: str

class CreditDebitNoteCreate(BaseModel):
    related_invoice_id: int
    type: str = Field(..., pattern="^(02|03)$")
    reason: str
    details: List[InvoiceDetailCreate]
