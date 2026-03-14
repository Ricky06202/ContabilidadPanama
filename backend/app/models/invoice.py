from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class InvoiceType(str, enum.Enum):
    FACTURA = "01"
    NOTA_CREDITO = "02"
    NOTA_DEBITO = "03"
    FACTURA_EXPORTACION = "10"

class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    SIGNED = "signed"
    SENT = "sent"
    VALIDATED = "validated"
    REJECTED = "rejected"

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    number = Column(String(20), unique=True, index=True, nullable=False)
    type = Column(String(2), default=InvoiceType.FACTURA.value)
    status = Column(String(20), default=InvoiceStatus.DRAFT.value)
    
    issue_date = Column(DateTime, nullable=False)
    issue_time = Column(String(8), nullable=False)
    
    sender_ruc = Column(String(20), nullable=False)
    sender_razon_social = Column(String(200), nullable=False)
    sender_dv = Column(String(5))
    sender_address = Column(String(300))
    sender_phone = Column(String(20))
    sender_email = Column(String(100))
    
    receiver_ruc = Column(String(20), nullable=False)
    receiver_razon_social = Column(String(200), nullable=False)
    receiver_dv = Column(String(5))
    receiver_address = Column(String(300))
    receiver_email = Column(String(100))
    receiver_tipo = Column(String(2), default="1")
    
    subtotal = Column(Float, default=0)
    descuento = Column(Float, default=0)
    itbms = Column(Float, default=0)
    total = Column(Float, default=0)
    total_itbms = Column(Float, default=0)
    
    currency = Column(String(3), default="PAB")
    exchange_rate = Column(Float, default=1.0)
    
    xml_content = Column(Text)
    cufe = Column(String(100))
    signature = Column(String(500))
    dgi_response = Column(Text)
    
    related_invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    reason = Column(String(300))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="invoices")
    details = relationship("InvoiceDetail", back_populates="invoice", cascade="all, delete-orphan")
    related_invoice = relationship("Invoice", remote_side=[id], backref="credit_debit_notes")

class InvoiceDetail(Base):
    __tablename__ = "invoice_details"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    
    line_number = Column(Integer, nullable=False)
    code = Column(String(50))
    description = Column(String(500), nullable=False)
    quantity = Column(Float, default=1)
    unit_code = Column(String(3), default="UND")
    unit_price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    subtotal = Column(Float, nullable=False)
    itbms_rate = Column(Float, default=0.07)
    itbms_amount = Column(Float, default=0)
    total = Column(Float, nullable=False)
    
    invoice = relationship("Invoice", back_populates="details")
