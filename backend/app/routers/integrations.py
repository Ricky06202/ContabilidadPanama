from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models.models import User
from app.models.entities import Client, Provider
from app.models.inventory import Product
from app.models.invoice import Invoice
from app.models.expenses import Expense
from app.models.payroll import Employee
from app.models.integrations import IntegrationConfig, SyncLog
from app.models.integrations_schemas import IntegrationConfigResponse, SyncLogResponse
from app.routers.auth import get_current_user

router = APIRouter()

ENTITY_HANDLERS = {
    "clients": Client,
    "providers": Provider,
    "products": Product,
    "invoices": Invoice,
    "expenses": Expense,
    "employees": Employee
}

@router.get("/integration-config", response_model=IntegrationConfigResponse)
def get_integration_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    config = db.query(IntegrationConfig).filter(
        IntegrationConfig.tenant_id == current_user.tenant_id
    ).first()
    if not config:
        config = IntegrationConfig(tenant_id=current_user.tenant_id)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

@router.put("/integration-config", response_model=IntegrationConfigResponse)
def update_integration_config(
    config_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    config = db.query(IntegrationConfig).filter(
        IntegrationConfig.tenant_id == current_user.tenant_id
    ).first()
    if not config:
        config = IntegrationConfig(tenant_id=current_user.tenant_id)
        db.add(config)
    
    for key, value in config_data.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    db.commit()
    db.refresh(config)
    return config

@router.get("/export/{entity_type}")
def export_data(
    entity_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if entity_type not in ENTITY_HANDLERS:
        raise HTTPException(status_code=400, detail=f"Invalid entity type: {entity_type}")
    
    model = ENTITY_HANDLERS[entity_type]
    records = db.query(model).filter(model.tenant_id == current_user.tenant_id).all()
    
    result = []
    for r in records:
        record_dict = {}
        for col in r.__table__.columns:
            if col.name not in ["tenant_id"]:
                value = getattr(r, col.name)
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                record_dict[col.name] = value
        result.append(record_dict)
    
    log = SyncLog(
        tenant_id=current_user.tenant_id,
        integration="export",
        direction="outbound",
        entity_type=entity_type,
        status="success",
        message=f"Exported {len(result)} records"
    )
    db.add(log)
    db.commit()
    
    return {
        "entity_type": entity_type,
        "count": len(result),
        "data": result
    }

@router.post("/import/{entity_type}")
def import_data(
    entity_type: str,
    records: List[dict],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if entity_type not in ENTITY_HANDLERS:
        raise HTTPException(status_code=400, detail=f"Invalid entity type: {entity_type}")
    
    model = ENTITY_HANDLERS[entity_type]
    imported = 0
    errors = []
    
    for record in records:
        try:
            record["tenant_id"] = current_user.tenant_id
            obj = model(**record)
            db.add(obj)
            imported += 1
        except Exception as e:
            errors.append({"record": record, "error": str(e)})
    
    db.commit()
    
    log = SyncLog(
        tenant_id=current_user.tenant_id,
        integration="import",
        direction="inbound",
        entity_type=entity_type,
        status="success" if not errors else "partial",
        message=f"Imported {imported} records, {len(errors)} errors"
    )
    db.add(log)
    db.commit()
    
    return {
        "entity_type": entity_type,
        "imported": imported,
        "errors": errors
    }

@router.get("/sync-logs", response_model=List[SyncLogResponse])
def get_sync_logs(
    integration: str = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(SyncLog).filter(SyncLog.tenant_id == current_user.tenant_id)
    if integration:
        query = query.filter(SyncLog.integration == integration)
    return query.order_by(SyncLog.created_at.desc()).limit(limit).all()

@router.get("/available-entities")
def get_available_entities():
    return {
        "entities": list(ENTITY_HANDLERS.keys()),
        "descriptions": {
            "clients": "Clientes registrados",
            "providers": "Proveedores registrados",
            "products": "Catálogo de productos",
            "invoices": "Facturas emitidas",
            "expenses": "Gastos registrados",
            "employees": "Empleados"
        }
    }
