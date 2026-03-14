from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import User
from app.models.entities import Client, Provider
from app.models.entity_schemas import (
    ClientCreate, ClientUpdate, ClientResponse,
    ProviderCreate, ProviderUpdate, ProviderResponse
)
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = Client(
        tenant_id=current_user.tenant_id,
        **client_data.model_dump()
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/clients", response_model=List[ClientResponse])
def list_clients(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Client).filter(Client.tenant_id == current_user.tenant_id)
    if search:
        query = query.filter(Client.razon_social.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/clients/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in client_data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    
    db.commit()
    db.refresh(client)
    return client

@router.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(client)
    db.commit()
    return None

@router.post("/providers", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
def create_provider(
    provider_data: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = Provider(
        tenant_id=current_user.tenant_id,
        **provider_data.model_dump()
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider

@router.get("/providers", response_model=List[ProviderResponse])
def list_providers(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Provider).filter(Provider.tenant_id == current_user.tenant_id)
    if search:
        query = query.filter(Provider.razon_social.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/providers/{provider_id}", response_model=ProviderResponse)
def get_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = db.query(Provider).filter(
        Provider.id == provider_id,
        Provider.tenant_id == current_user.tenant_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return provider

@router.put("/providers/{provider_id}", response_model=ProviderResponse)
def update_provider(
    provider_id: int,
    provider_data: ProviderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = db.query(Provider).filter(
        Provider.id == provider_id,
        Provider.tenant_id == current_user.tenant_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    for key, value in provider_data.model_dump(exclude_unset=True).items():
        setattr(provider, key, value)
    
    db.commit()
    db.refresh(provider)
    return provider

@router.delete("/providers/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = db.query(Provider).filter(
        Provider.id == provider_id,
        Provider.tenant_id == current_user.tenant_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(provider)
    db.commit()
    return None
