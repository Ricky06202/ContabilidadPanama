from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.models import User
from app.models.banking import BankAccount, BankTransaction, Reconciliation
from app.models.banking_schemas import (
    BankAccountCreate, BankAccountResponse,
    BankTransactionCreate, BankTransactionResponse,
    ReconciliationCreate, ReconciliationResponse
)
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/bank-accounts", response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
def create_bank_account(
    data: BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = BankAccount(
        tenant_id=current_user.tenant_id,
        current_balance=data.initial_balance,
        **data.model_dump()
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.get("/bank-accounts", response_model=List[BankAccountResponse])
def list_bank_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(BankAccount).filter(BankAccount.tenant_id == current_user.tenant_id).all()

@router.get("/bank-accounts/{account_id}", response_model=BankAccountResponse)
def get_bank_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.tenant_id == current_user.tenant_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    return account

@router.post("/bank-transactions", response_model=BankTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_bank_transaction(
    data: BankTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(BankAccount).filter(
        BankAccount.id == data.account_id,
        BankAccount.tenant_id == current_user.tenant_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    
    if data.transaction_type in ["deposit", "transfer"]:
        new_balance = account.current_balance + data.amount
    elif data.transaction_type in ["withdrawal", "payment", "fee"]:
        new_balance = account.current_balance - data.amount
        if new_balance < 0:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
    else:
        new_balance = account.current_balance
    
    account.current_balance = new_balance
    
    transaction = BankTransaction(
        tenant_id=current_user.tenant_id,
        balance_after=new_balance,
        status="completed",
        **data.model_dump()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.get("/bank-transactions", response_model=List[BankTransactionResponse])
def list_bank_transactions(
    account_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(BankTransaction).filter(BankTransaction.tenant_id == current_user.tenant_id)
    if account_id:
        query = query.filter(BankTransaction.account_id == account_id)
    return query.order_by(BankTransaction.date.desc()).offset(skip).limit(limit).all()

@router.post("/reconciliations", response_model=ReconciliationResponse, status_code=status.HTTP_201_CREATED)
def create_reconciliation(
    data: ReconciliationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(BankAccount).filter(
        BankAccount.id == data.account_id,
        BankAccount.tenant_id == current_user.tenant_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    
    result = db.query(
        func.sum(
            case(
                (BankTransaction.transaction_type.in_(["deposit", "transfer"]), BankTransaction.amount),
                else_=-BankTransaction.amount
            )
        )
    ).filter(
        BankTransaction.account_id == data.account_id,
        BankTransaction.date >= data.period_start,
        BankTransaction.date <= data.period_end,
        BankTransaction.status == "completed"
    ).scalar() or 0
    
    system_balance = account.initial_balance + result
    difference = data.statement_balance - system_balance
    
    reconciliation = Reconciliation(
        tenant_id=current_user.tenant_id,
        account_id=data.account_id,
        period_start=data.period_start,
        period_end=data.period_end,
        statement_balance=data.statement_balance,
        system_balance=system_balance,
        difference=difference,
        status="completed" if difference == 0 else "pending"
    )
    db.add(reconciliation)
    db.commit()
    db.refresh(reconciliation)
    return reconciliation

@router.get("/reconciliations", response_model=List[ReconciliationResponse])
def list_reconciliations(
    account_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Reconciliation).filter(Reconciliation.tenant_id == current_user.tenant_id)
    if account_id:
        query = query.filter(Reconciliation.account_id == account_id)
    return query.all()
