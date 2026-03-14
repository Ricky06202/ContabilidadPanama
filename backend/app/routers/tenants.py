from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import User, Tenant
from app.models.schemas import (
    TenantCreate, TenantUpdate, TenantResponse, UserResponse
)
from app.routers.auth import get_current_user, require_role

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    existing_tenant = db.query(Tenant).filter(Tenant.ruc == tenant_data.ruc).first()
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RUC already registered"
        )
    
    new_tenant = Tenant(
        name=tenant_data.name,
        ruc=tenant_data.ruc,
        address=tenant_data.address,
        phone=tenant_data.phone
    )
    
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    
    return TenantResponse(
        id=new_tenant.id,
        name=new_tenant.name,
        ruc=new_tenant.ruc,
        address=new_tenant.address,
        phone=new_tenant.phone,
        is_active=new_tenant.is_active,
        created_at=new_tenant.created_at
    )

@router.get("/", response_model=List[TenantResponse])
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "accountant"))
):
    tenants = db.query(Tenant).offset(skip).limit(limit).all()
    return [
        TenantResponse(
            id=t.id,
            name=t.name,
            ruc=t.ruc,
            address=t.address,
            phone=t.phone,
            is_active=t.is_active,
            created_at=t.created_at
        )
        for t in tenants
    ]

@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        ruc=tenant.ruc,
        address=tenant.address,
        phone=tenant.phone,
        is_active=tenant.is_active,
        created_at=tenant.created_at
    )

@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    if tenant_data.name is not None:
        tenant.name = tenant_data.name
    if tenant_data.address is not None:
        tenant.address = tenant_data.address
    if tenant_data.phone is not None:
        tenant.phone = tenant_data.phone
    if tenant_data.is_active is not None:
        tenant.is_active = tenant_data.is_active
    
    db.commit()
    db.refresh(tenant)
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        ruc=tenant.ruc,
        address=tenant.address,
        phone=tenant.phone,
        is_active=tenant.is_active,
        created_at=tenant.created_at
    )

@router.get("/{tenant_id}/users", response_model=List[UserResponse])
def get_tenant_users(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    users = db.query(User).filter(User.tenant_id == tenant_id).all()
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            name=u.name,
            tenant_id=u.tenant_id,
            role=u.role,
            is_active=u.is_active,
            created_at=u.created_at
        )
        for u in users
    ]
