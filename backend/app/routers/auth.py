from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

from app.database import get_db
from app.models.models import User, Tenant
from app.models.schemas import (
    UserCreate, UserResponse, LoginRequest, TokenResponse,
    TenantCreate, TenantResponse, PasswordChange, RegisterRequest
)
from app.utils.auth import hash_password, verify_password
from app.utils.jwt import create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
    return user

def require_role(*allowed_roles: str):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_tenant = None
    if user_data.tenant_id:
        existing_tenant = db.query(Tenant).filter(Tenant.id == user_data.tenant_id).first()
        if not existing_tenant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant not found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant is required"
        )
    
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_pw,
        tenant_id=user_data.tenant_id,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": str(new_user.id), "role": new_user.role})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            tenant_id=new_user.tenant_id,
            role=new_user.role,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
    )

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            tenant_id=user.tenant_id,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
    )

@router.post("/register-complete", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_complete(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_tenant = db.query(Tenant).filter(Tenant.ruc == data.ruc).first()
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RUC already registered"
        )
    
    new_tenant = Tenant(
        name=data.company_name,
        ruc=data.ruc,
        phone=data.phone,
        is_active=True
    )
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    
    hashed_pw = hash_password(data.password)
    new_user = User(
        email=data.email,
        name=data.name,
        password_hash=hashed_pw,
        tenant_id=new_tenant.id,
        role="admin",
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": str(new_user.id), "role": new_user.role})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            tenant_id=new_user.tenant_id,
            role=new_user.role,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
    )
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            tenant_id=user.tenant_id,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        tenant_id=current_user.tenant_id,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    current_user.password_hash = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}
