from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IntegrationConfigBase(BaseModel):
    myob_enabled: bool = False
    stripe_enabled: bool = False
    woocommerce_enabled: bool = False

class IntegrationConfigResponse(IntegrationConfigBase):
    id: int
    tenant_id: int
    myob_company_file: Optional[str] = None
    woocommerce_url: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SyncLogResponse(BaseModel):
    id: int
    tenant_id: int
    integration: str
    direction: str
    entity_type: str
    entity_id: Optional[int] = None
    status: str
    message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ExportDataRequest(BaseModel):
    entity_type: str
    format: str = "json"

class ImportDataRequest(BaseModel):
    entity_type: str
    data: dict
