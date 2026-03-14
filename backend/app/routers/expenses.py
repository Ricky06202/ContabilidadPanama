from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from app.database import get_db
from app.models.models import User
from app.models.expenses import Expense, ExpenseCategory, PurchaseOrder, PurchaseOrderDetail
from app.models.expense_schemas import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse,
    ExpenseCategoryCreate, ExpenseCategoryResponse,
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse, PurchaseOrderWithDetails
)
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/expense-categories", response_model=ExpenseCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_expense_category(
    data: ExpenseCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cat = ExpenseCategory(tenant_id=current_user.tenant_id, **data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("/expense-categories", response_model=List[ExpenseCategoryResponse])
def list_expense_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(ExpenseCategory).filter(ExpenseCategory.tenant_id == current_user.tenant_id).all()

@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    itbms_amount = data.amount * data.itbms_rate
    total = data.amount + itbms_amount
    
    expense = Expense(
        tenant_id=current_user.tenant_id,
        itbms_amount=itbms_amount,
        total_amount=total,
        **data.model_dump()
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

@router.get("/expenses", response_model=List[ExpenseResponse])
def list_expenses(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Expense).filter(Expense.tenant_id == current_user.tenant_id)
    if status_filter:
        query = query.filter(Expense.status == status_filter)
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    return query.order_by(Expense.expense_date.desc()).offset(skip).limit(limit).all()

@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.tenant_id == current_user.tenant_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return expense

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.tenant_id == current_user.tenant_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    update_data = data.model_dump(exclude_unset=True)
    
    if 'amount' in update_data or 'itbms_rate' in update_data:
        amount = update_data.get('amount', expense.amount)
        itbms_rate = update_data.get('itbms_rate', expense.itbms_rate)
        expense.itbms_amount = amount * itbms_rate
        expense.total_amount = amount + expense.itbms_amount
    
    for key, value in update_data.items():
        setattr(expense, key, value)
    
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.tenant_id == current_user.tenant_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    db.delete(expense)
    db.commit()
    return None

@router.post("/purchase-orders", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    data: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order_number = f"OC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    subtotal = 0
    for detail in data.details:
        line_subtotal = detail.quantity * detail.unit_price
        discount = line_subtotal * (detail.discount_percent / 100)
        subtotal += line_subtotal - discount
    
    discount_total = 0
    itbms = subtotal * 0.07
    total = subtotal - discount_total + itbms
    
    order = PurchaseOrder(
        tenant_id=current_user.tenant_id,
        number=order_number,
        provider_id=data.provider_id,
        order_date=data.order_date,
        expected_date=data.expected_date,
        notes=data.notes,
        subtotal=subtotal,
        discount=discount_total,
        itbms=itbms,
        total=total
    )
    db.add(order)
    db.flush()
    
    for detail in data.details:
        line_subtotal = detail.quantity * detail.unit_price
        discount = line_subtotal * (detail.discount_percent / 100)
        order_detail = PurchaseOrderDetail(
            order_id=order.id,
            product_id=detail.product_id,
            description=detail.description,
            quantity=detail.quantity,
            unit_price=detail.unit_price,
            discount_percent=detail.discount_percent,
            subtotal=line_subtotal - discount
        )
        db.add(order_detail)
    
    db.commit()
    db.refresh(order)
    return order

@router.get("/purchase-orders", response_model=List[PurchaseOrderResponse])
def list_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(PurchaseOrder).filter(PurchaseOrder.tenant_id == current_user.tenant_id)
    if status_filter:
        query = query.filter(PurchaseOrder.status == status_filter)
    return query.order_by(PurchaseOrder.order_date.desc()).offset(skip).limit(limit).all()

@router.get("/purchase-orders/{order_id}", response_model=PurchaseOrderWithDetails)
def get_purchase_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id,
        PurchaseOrder.tenant_id == current_user.tenant_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    details = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.order_id == order.id).all()
    
    return {
        "id": order.id,
        "tenant_id": order.tenant_id,
        "provider_id": order.provider_id,
        "number": order.number,
        "status": order.status,
        "order_date": order.order_date,
        "expected_date": order.expected_date,
        "received_date": order.received_date,
        "subtotal": order.subtotal,
        "discount": order.discount,
        "itbms": order.itbms,
        "total": order.total,
        "notes": order.notes,
        "created_at": order.created_at,
        "details": details
    }

@router.put("/purchase-orders/{order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(
    order_id: int,
    data: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id,
        PurchaseOrder.tenant_id == current_user.tenant_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    
    db.commit()
    db.refresh(order)
    return order
