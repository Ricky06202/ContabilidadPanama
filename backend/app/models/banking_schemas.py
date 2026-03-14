from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BankAccountBase(BaseModel):
    name: str
    bank_name: str
    account_number: str
    account_type: str = "checking"
    initial_balance: float = 0
    notas: Optional[str] = None

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountResponse(BankAccountBase):
    id: int
    tenant_id: int
    current_balance: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BankTransactionCreate(BaseModel):
    account_id: int
    date: datetime
    description: str
    reference: Optional[str] = None
    transaction_type: str
    amount: float

class BankTransactionResponse(BankTransactionCreate):
    id: int
    tenant_id: int
    balance_after: Optional[float] = None
    status: str
    is_reconciled: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ReconciliationCreate(BaseModel):
    account_id: int
    period_start: datetime
    period_end: datetime
    statement_balance: float

class ReconciliationResponse(BaseModel):
    id: int
    tenant_id: int
    account_id: int
    period_start: datetime
    period_end: datetime
    statement_balance: float
    system_balance: float
    difference: float
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
