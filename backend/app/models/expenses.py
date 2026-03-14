from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ExpenseCategory(Base):
    __tablename__ = "expense_categories"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    cuenta_contable = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="expense_categories")
    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=True)
    
    description = Column(String(300), nullable=False)
    amount = Column(Float, nullable=False)
    itbms_amount = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    
    itbms_rate = Column(Float, default=0.07)
    
    expense_date = Column(DateTime, nullable=False)
    payment_date = Column(DateTime)
    payment_method = Column(String(20))
    reference = Column(String(100))
    
    status = Column(String(20), default="pending")
    is_deductible = Column(Boolean, default=True)
    
    notas = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="expenses")
    provider = relationship("Provider", backref="expenses")
    category = relationship("ExpenseCategory", back_populates="expenses")

class PurchaseOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    APPROVED = "approved"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=True)
    
    number = Column(String(20), unique=True, index=True)
    status = Column(String(20), default=PurchaseOrderStatus.DRAFT.value)
    
    order_date = Column(DateTime, nullable=False)
    expected_date = Column(DateTime)
    received_date = Column(DateTime)
    
    subtotal = Column(Float, default=0)
    discount = Column(Float, default=0)
    itbms = Column(Float, default=0)
    total = Column(Float, default=0)
    
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="purchase_orders")
    provider = relationship("Provider", backref="purchase_orders")
    details = relationship("PurchaseOrderDetail", back_populates="order", cascade="all, delete-orphan")

class PurchaseOrderDetail(Base):
    __tablename__ = "purchase_order_details"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    
    description = Column(String(300), nullable=False)
    quantity = Column(Float, default=1)
    unit_price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0)
    subtotal = Column(Float, default=0)
    received_quantity = Column(Float, default=0)
    
    order = relationship("PurchaseOrder", back_populates="details")
    product = relationship("Product", backref="purchase_order_details")
