from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class BankAccountType(str, enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    name = Column(String(100), nullable=False)
    bank_name = Column(String(100), nullable=False)
    account_number = Column(String(50), nullable=False)
    account_type = Column(String(20), default=BankAccountType.CHECKING.value)
    
    initial_balance = Column(Float, default=0)
    current_balance = Column(Float, default=0)
    
    is_active = Column(Boolean, default=True)
    notas = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="bank_accounts")
    transactions = relationship("BankTransaction", back_populates="account", cascade="all, delete")

class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    FEE = "fee"
    INTEREST = "interest"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    RECONCILED = "reconciled"
    VOIDED = "voided"

class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    date = Column(DateTime, nullable=False)
    description = Column(String(300), nullable=False)
    reference = Column(String(100))
    
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    
    balance_after = Column(Float)
    
    status = Column(String(20), default=TransactionStatus.COMPLETED.value)
    
    is_reconciled = Column(Boolean, default=False)
    reconciliation_date = Column(DateTime)
    
    notas = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    account = relationship("BankAccount", back_populates="transactions")
    tenant = relationship("Tenant", backref="bank_transactions")

class Reconciliation(Base):
    __tablename__ = "reconciliations"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    statement_balance = Column(Float, nullable=False)
    system_balance = Column(Float, nullable=False)
    difference = Column(Float, nullable=False)
    
    status = Column(String(20), default="pending")
    
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    tenant = relationship("Tenant")
    account = relationship("BankAccount")
