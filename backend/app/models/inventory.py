from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="categories")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    code = Column(String(50), index=True)
    barcode = Column(String(50))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    unit_code = Column(String(3), default="UND")
    
    cost_price = Column(Float, default=0)
    sale_price = Column(Float, default=0)
    sale_price_with_tax = Column(Float, default=0)
    
    itbms_rate = Column(Float, default=0.07)
    
    has_inventory = Column(Boolean, default=True)
    min_stock = Column(Float, default=0)
    max_stock = Column(Float, default=0)
    
    is_active = Column(Boolean, default=True)
    notas = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="products")
    category = relationship("Category", back_populates="products", cascade="all, delete")
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    
    quantity = Column(Float, default=0)
    reserved_quantity = Column(Float, default=0)
    available_quantity = Column(Float, default=0)
    
    location = Column(String(100))
    last_movement_date = Column(DateTime)
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="inventory")

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    movement_type = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    reference = Column(String(100))
    notes = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product")
    tenant = relationship("Tenant")
