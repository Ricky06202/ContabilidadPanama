from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    tenant_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    code: Optional[str] = None
    barcode: Optional[str] = None
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit_code: str = "UND"
    cost_price: float = 0
    sale_price: float = 0
    itbms_rate: float = 0.07
    has_inventory: bool = True
    min_stock: float = 0
    max_stock: float = 0
    notas: Optional[str] = None

class ProductCreate(ProductBase):
    initial_quantity: Optional[float] = 0
    location: Optional[str] = None

class ProductUpdate(BaseModel):
    code: Optional[str] = None
    barcode: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit_code: Optional[str] = None
    cost_price: Optional[float] = None
    sale_price: Optional[float] = None
    itbms_rate: Optional[float] = None
    has_inventory: Optional[bool] = None
    min_stock: Optional[float] = None
    max_stock: Optional[float] = None
    notas: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    tenant_id: int
    sale_price_with_tax: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProductWithInventory(ProductResponse):
    quantity: Optional[float] = 0
    reserved_quantity: Optional[float] = 0
    available_quantity: Optional[float] = 0

class InventoryBase(BaseModel):
    product_id: int
    quantity: float
    location: Optional[str] = None

class InventoryUpdate(BaseModel):
    quantity: Optional[float] = None
    location: Optional[str] = None

class InventoryResponse(BaseModel):
    id: int
    product_id: int
    quantity: float
    reserved_quantity: float
    available_quantity: float
    location: Optional[str] = None
    last_movement_date: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True

class InventoryMovementCreate(BaseModel):
    product_id: int
    movement_type: str
    quantity: float
    reference: Optional[str] = None
    notes: Optional[str] = None

class InventoryMovementResponse(InventoryMovementCreate):
    id: int
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
