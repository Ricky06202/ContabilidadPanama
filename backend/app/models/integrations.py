from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

class IntegrationConfig(Base):
    __tablename__ = "integration_config"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, unique=True)
    
    myob_enabled = Column(Boolean, default=False)
    myob_company_file = Column(String(200))
    myob_client_id = Column(String(200))
    myob_client_secret = Column(String(200))
    
    stripe_enabled = Column(Boolean, default=False)
    stripe_api_key = Column(String(200))
    
    woocommerce_enabled = Column(Boolean, default=False)
    woocommerce_url = Column(String(200))
    woocommerce_consumer_key = Column(String(200))
    woocommerce_consumer_secret = Column(String(200))
    
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    tenant = relationship("Tenant", backref="integration_config")

class SyncLog(Base):
    __tablename__ = "sync_logs"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    integration = Column(String(50), nullable=False)
    direction = Column(String(20), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    status = Column(String(20), nullable=False)
    message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    tenant = relationship("Tenant", backref="sync_logs")
