from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpenseCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    cuenta_contable: Optional[str] = None

class ExpenseCategoryCreate(ExpenseCategoryBase):
    pass

class ExpenseCategoryResponse(ExpenseCategoryBase):
    id: int
    tenant_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    description: str
    amount: float = Field(..., ge=0)
    itbms_rate: float = Field(default=0.07, ge=0, le=1)
    provider_id: Optional[int] = None
    category_id: Optional[int] = None
    expense_date: datetime
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    status: str = "pending"
    is_deductible: bool = True
    notas: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    itbms_rate: Optional[float] = None
    provider_id: Optional[int] = None
    category_id: Optional[int] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    status: Optional[str] = None
    is_deductible: Optional[bool] = None
    notas: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    id: int
    tenant_id: int
    itbms_amount: float
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True

class PurchaseOrderDetailCreate(BaseModel):
    product_id: Optional[int] = None
    description: str
    quantity: float = Field(default=1, ge=0)
    unit_price: float = Field(..., ge=0)
    discount_percent: float = Field(default=0, ge=0, le=100)

class PurchaseOrderDetailResponse(PurchaseOrderDetailCreate):
    id: int
    subtotal: float
    received_quantity: float

    class Config:
        from_attributes = True

class PurchaseOrderCreate(BaseModel):
    provider_id: Optional[int] = None
    order_date: datetime
    expected_date: Optional[datetime] = None
    notes: Optional[str] = None
    details: list[PurchaseOrderDetailCreate]

class PurchaseOrderUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    received_date: Optional[datetime] = None

class PurchaseOrderResponse(BaseModel):
    id: int
    tenant_id: int
    provider_id: Optional[int] = None
    number: str
    status: str
    order_date: datetime
    expected_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    subtotal: float
    discount: float
    itbms: float
    total: float
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PurchaseOrderWithDetails(PurchaseOrderResponse):
    details: list[PurchaseOrderDetailResponse] = []
