from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base

class ReportConfig(Base):
    __tablename__ = "report_config"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, unique=True)
    
    ejercicio_fiscal = Column(Integer, default=2026)
    periodo_inicio = Column(Integer, default=1)
    periodo_fin = Column(Integer, default=12)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="report_config")
