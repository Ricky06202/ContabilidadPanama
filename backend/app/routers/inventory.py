from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.models import User
from app.models.inventory import Product, Category, Inventory, InventoryMovement
from app.models.inventory_schemas import (
    ProductCreate, ProductUpdate, ProductResponse, ProductWithInventory,
    CategoryCreate, CategoryUpdate, CategoryResponse,
    InventoryMovementCreate, InventoryMovementResponse
)
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = Category(tenant_id=current_user.tenant_id, **category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Category).filter(Category.tenant_id == current_user.tenant_id).all()

@router.post("/products", response_model=ProductWithInventory, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale_price_with_tax = product_data.sale_price * (1 + product_data.itbms_rate)
    
    product = Product(
        tenant_id=current_user.tenant_id,
        sale_price_with_tax=sale_price_with_tax,
        **{k: v for k, v in product_data.model_dump().items() if k not in ['initial_quantity', 'location']}
    )
    db.add(product)
    db.flush()
    
    initial_qty = 0
    if product_data.has_inventory:
        initial_qty = product_data.initial_quantity or 0
        inventory = Inventory(
            product_id=product.id,
            quantity=initial_qty,
            available_quantity=initial_qty,
            location=product_data.location
        )
        db.add(inventory)
    
    db.commit()
    db.refresh(product)
    
    return {
        "id": product.id,
        "tenant_id": product.tenant_id,
        "code": product.code,
        "barcode": product.barcode,
        "name": product.name,
        "description": product.description,
        "category_id": product.category_id,
        "unit_code": product.unit_code,
        "cost_price": product.cost_price,
        "sale_price": product.sale_price,
        "sale_price_with_tax": product.sale_price_with_tax,
        "itbms_rate": product.itbms_rate,
        "has_inventory": product.has_inventory,
        "min_stock": product.min_stock,
        "max_stock": product.max_stock,
        "notas": product.notas,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "quantity": initial_qty,
        "reserved_quantity": 0,
        "available_quantity": initial_qty
    }

@router.get("/products", response_model=List[ProductWithInventory])
def list_products(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product).filter(Product.tenant_id == current_user.tenant_id)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    products = query.offset(skip).limit(limit).all()
    
    result = []
    for p in products:
        inv = db.query(Inventory).filter(Inventory.product_id == p.id).first()
        product_dict = {
            "id": p.id,
            "tenant_id": p.tenant_id,
            "code": p.code,
            "barcode": p.barcode,
            "name": p.name,
            "description": p.description,
            "category_id": p.category_id,
            "unit_code": p.unit_code,
            "cost_price": p.cost_price,
            "sale_price": p.sale_price,
            "sale_price_with_tax": p.sale_price_with_tax,
            "itbms_rate": p.itbms_rate,
            "has_inventory": p.has_inventory,
            "min_stock": p.min_stock,
            "max_stock": p.max_stock,
            "notas": p.notas,
            "is_active": p.is_active,
            "created_at": p.created_at,
            "quantity": inv.quantity if inv else 0,
            "reserved_quantity": inv.reserved_quantity if inv else 0,
            "available_quantity": inv.available_quantity if inv else 0
        }
        result.append(product_dict)
    
    return result

@router.get("/products/{product_id}", response_model=ProductWithInventory)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    inv = db.query(Inventory).filter(Inventory.product_id == product.id).first()
    
    return {
        "id": product.id,
        "tenant_id": product.tenant_id,
        "code": product.code,
        "barcode": product.barcode,
        "name": product.name,
        "description": product.description,
        "category_id": product.category_id,
        "unit_code": product.unit_code,
        "cost_price": product.cost_price,
        "sale_price": product.sale_price,
        "sale_price_with_tax": product.sale_price_with_tax,
        "itbms_rate": product.itbms_rate,
        "has_inventory": product.has_inventory,
        "min_stock": product.min_stock,
        "max_stock": product.max_stock,
        "notas": product.notas,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "quantity": inv.quantity if inv else 0,
        "reserved_quantity": inv.reserved_quantity if inv else 0,
        "available_quantity": inv.available_quantity if inv else 0
    }

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = product_data.model_dump(exclude_unset=True)
    
    if 'sale_price' in update_data or 'itbms_rate' in update_data:
        sale_price = update_data.get('sale_price', product.sale_price)
        itbms_rate = update_data.get('itbms_rate', product.itbms_rate)
        product.sale_price_with_tax = sale_price * (1 + itbms_rate)
    
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(product)
    db.commit()
    return None

@router.post("/inventory/movements", response_model=InventoryMovementResponse)
def create_movement(
    movement_data: InventoryMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == movement_data.product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if not product.has_inventory:
        raise HTTPException(status_code=400, detail="El producto no tiene inventario habilitado")
    
    inv = db.query(Inventory).filter(Inventory.product_id == product.id).first()
    if not inv:
        raise HTTPException(status_code=400, detail="El producto no tiene registro de inventario")
    
    if movement_data.movement_type == "entrada":
        inv.quantity += movement_data.quantity
        inv.available_quantity += movement_data.quantity
    elif movement_data.movement_type == "salida":
        if inv.available_quantity < movement_data.quantity:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        inv.quantity -= movement_data.quantity
        inv.available_quantity -= movement_data.quantity
    elif movement_data.movement_type == "reserva":
        if inv.available_quantity < movement_data.quantity:
            raise HTTPException(status_code=400, detail="Stock insuficiente para reservar")
        inv.reserved_quantity += movement_data.quantity
        inv.available_quantity -= movement_data.quantity
    elif movement_data.movement_type == "liberar":
        inv.reserved_quantity -= movement_data.quantity
        inv.available_quantity += movement_data.quantity
    
    inv.last_movement_date = datetime.now()
    
    movement = InventoryMovement(
        tenant_id=current_user.tenant_id,
        **movement_data.model_dump()
    )
    db.add(movement)
    db.commit()
    
    return movement

@router.get("/inventory/movements", response_model=List[InventoryMovementResponse])
def list_movements(
    product_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(InventoryMovement).filter(InventoryMovement.tenant_id == current_user.tenant_id)
    if product_id:
        query = query.filter(InventoryMovement.product_id == product_id)
    return query.order_by(InventoryMovement.created_at.desc()).offset(skip).limit(limit).all()
