import enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    USER = "user"
    VIEWER = "viewer"

class TenantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    ruc: str = Field(..., min_length=5, max_length=20)
    address: Optional[str] = None
    phone: Optional[str] = None

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class TenantResponse(TenantBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    tenant_id: Optional[int] = None
    role: str = "user"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    tenant_id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserWithTenant(UserResponse):
    tenant_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)
