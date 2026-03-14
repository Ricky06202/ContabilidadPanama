from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    ruc = Column(String(20), index=True)
    dv = Column(String(5))
    razon_social = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    
    email = Column(String(100))
    phone = Column(String(20))
    movil = Column(String(20))
    
    address = Column(String(300))
    ciudad = Column(String(100))
    provincia = Column(String(100))
    
    tipo_identificacion = Column(String(2), default="1")
    tipo_cliente = Column(String(20), default="general")
    
    limite_credito = Column(Float, default=0)
    saldo_actual = Column(Float, default=0)
    
    notas = Column(Text)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="clients")

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    ruc = Column(String(20), index=True)
    dv = Column(String(5))
    razon_social = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    
    email = Column(String(100))
    phone = Column(String(20))
    movil = Column(String(20))
    
    address = Column(String(300))
    ciudad = Column(String(100))
    provincia = Column(String(100))
    
    tipo_identificacion = Column(String(2), default="1")
    tipo_proveedor = Column(String(20), default="general")
    
    cuenta_contable = Column(String(20))
    
    notas = Column(Text)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="providers")
