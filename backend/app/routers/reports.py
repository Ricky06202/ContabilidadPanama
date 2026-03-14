from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.database import get_db
from app.models.models import User
from app.models.entities import Client, Provider
from app.models.inventory import Product, Inventory
from app.models.payroll import Employee
from app.models.invoice import Invoice
from app.models.expenses import Expense
from app.models.banking import BankAccount, BankTransaction
from app.models.reports_schemas import (
    DashboardResponse,
    BalanceGeneralResponse,
    EstadoResultadosResponse,
    FlujoCajaResponse,
    ResumenImpuestosResponse
)
from app.routers.auth import get_current_user

router = APIRouter()

def get_month_date_range(month_offset=0):
    today = datetime.now()
    target_month = today + relativedelta(months=month_offset)
    start = target_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = start + relativedelta(months=1, seconds=-1)
    return start, end

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_clientes = db.query(Client).filter(Client.tenant_id == current_user.tenant_id).count()
    total_proveedores = db.query(Provider).filter(Provider.tenant_id == current_user.tenant_id).count()
    total_productos = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).count()
    total_empleados = db.query(Employee).filter(Employee.tenant_id == current_user.tenant_id, Employee.es_activo == True).count()
    
    start, end = get_month_date_range(0)
    
    ventas_mes = db.query(Invoice).filter(
        Invoice.tenant_id == current_user.tenant_id,
        Invoice.status == "completed",
        Invoice.issue_date >= start,
        Invoice.issue_date <= end
    ).with_entities(func.sum(Invoice.total)).scalar() or 0
    
    gastos_mes = db.query(Expense).filter(
        Expense.tenant_id == current_user.tenant_id,
        Expense.expense_date >= start,
        Expense.expense_date <= end
    ).with_entities(func.sum(Expense.total_amount)).scalar() or 0
    
    bancos_total = db.query(BankAccount).filter(
        BankAccount.tenant_id == current_user.tenant_id,
        BankAccount.is_active == True
    ).with_entities(func.sum(BankAccount.current_balance)).scalar() or 0
    
    return {
        "total_clientes": total_clientes,
        "total_proveedores": total_proveedores,
        "total_productos": total_productos,
        "total_empleados": total_empleados,
        "ventas_mes": float(ventas_mes),
        "gastos_mes": float(gastos_mes),
        "ingresos_mes": float(ventas_mes),
        "bancos_total": float(bancos_total)
    }

@router.get("/balance-general", response_model=BalanceGeneralResponse)
def get_balance_general(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bancos = db.query(BankAccount).filter(
        BankAccount.tenant_id == current_user.tenant_id,
        BankAccount.is_active == True
    ).with_entities(func.sum(BankAccount.current_balance)).scalar() or 0
    
    products_cost = db.query(Product).join(Inventory).filter(
        Product.tenant_id == current_user.tenant_id
    ).with_entities(func.sum(Product.cost_price * Inventory.quantity)).scalar() or 0
    
    activos = {
        "bancos": float(bancos),
        "inventario": float(products_cost),
        "cuentas_por_cobrar": 0
    }
    
    pasivos = {
        "cuentas_por_pagar": 0,
        "impuestos_por_pagar": 0
    }
    
    patrimonio = {
        "capital_social": 0,
        "utilidades_acumuladas": 0
    }
    
    total_activos = sum(activos.values())
    total_pasivos = sum(pasivos.values())
    total_patrimonio = total_activos - total_pasivos
    
    return {
        "activos": activos,
        "pasivos": pasivos,
        "patrimonio": {**patrimonio, "resultado_ejercicio": float(total_patrimonio)},
        "total_activos": round(total_activos, 2),
        "total_pasivos": round(total_pasivos, 2),
        "total_patrimonio": round(total_patrimonio, 2)
    }

@router.get("/estado-resultados", response_model=EstadoResultadosResponse)
def get_estado_resultados(
    periodo: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if periodo:
        year, month = map(int, periodo.split("-"))
        start = datetime(year, month, 1)
        end = start + relativedelta(months=1, seconds=-1)
    else:
        start, end = get_month_date_range(0)
    
    ingresos = db.query(Invoice).filter(
        Invoice.tenant_id == current_user.tenant_id,
        Invoice.status == "completed",
        Invoice.issue_date >= start,
        Invoice.issue_date <= end
    ).with_entities(func.sum(Invoice.subtotal)).scalar() or 0
    
    costo_ventas = 0
    
    gastos_operativos = db.query(Expense).filter(
        Expense.tenant_id == current_user.tenant_id,
        Expense.expense_date >= start,
        Expense.expense_date <= end
    ).with_entities(func.sum(Expense.total_amount)).scalar() or 0
    
    utilidad_bruta = float(ingresos) - float(costo_ventas)
    utilidad_operativa = utilidad_bruta - float(gastos_operativos)
    otros_gastos = 0
    utilidad_neta = utilidad_operativa - otros_gastos
    
    return {
        "ingresos": float(ingresos),
        "costo_ventas": float(costo_ventas),
        "utilidad_bruta": round(utilidad_bruta, 2),
        "gastos_operativos": float(gastos_operativos),
        "utilidad_operativa": round(utilidad_operativa, 2),
        "otros_gastos": float(otros_gastos),
        "utilidad_neta": round(utilidad_neta, 2)
    }

@router.get("/flujo-caja", response_model=FlujoCajaResponse)
def get_flujo_caja(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start, end = get_month_date_range(0)
    
    accounts = db.query(BankAccount).filter(
        BankAccount.tenant_id == current_user.tenant_id,
        BankAccount.is_active == True
    ).all()
    
    saldo_inicial = sum(a.initial_balance for a in accounts)
    
    entradas = db.query(BankTransaction).filter(
        BankTransaction.tenant_id == current_user.tenant_id,
        BankTransaction.transaction_type.in_(["deposit", "transfer"]),
        BankTransaction.status == "completed",
        BankTransaction.date >= start,
        BankTransaction.date <= end
    ).with_entities(func.sum(BankTransaction.amount)).scalar() or 0
    
    salidas = db.query(BankTransaction).filter(
        BankTransaction.tenant_id == current_user.tenant_id,
        BankTransaction.transaction_type.in_(["withdrawal", "payment", "fee"]),
        BankTransaction.status == "completed",
        BankTransaction.date >= start,
        BankTransaction.date <= end
    ).with_entities(func.sum(BankTransaction.amount)).scalar() or 0
    
    saldo_final = saldo_inicial + float(entradas) - float(salidas)
    
    return {
        "saldo_inicial": round(saldo_inicial, 2),
        "entradas": float(entradas),
        "salidas": float(salidas),
        "saldo_final": round(saldo_final, 2),
        "detalle_entradas": [{"tipo": "ventas", "monto": float(entradas)}],
        "detalle_salidas": [{"tipo": "gastos", "monto": float(salidas)}]
    }

@router.get("/resumen-impuestos", response_model=ResumenImpuestosResponse)
def get_resumen_impuestos(
    periodo: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if periodo:
        year, month = map(int, periodo.split("-"))
        start = datetime(year, month, 1)
        end = start + relativedelta(months=1, seconds=-1)
    else:
        start, end = get_month_date_range(0)
    
    itbms_vendido = db.query(Invoice).filter(
        Invoice.tenant_id == current_user.tenant_id,
        Invoice.status == "completed",
        Invoice.issue_date >= start,
        Invoice.issue_date <= end
    ).with_entities(func.sum(Invoice.itbms)).scalar() or 0
    
    itbms_comprado = db.query(Expense).filter(
        Expense.tenant_id == current_user.tenant_id,
        Expense.expense_date >= start,
        Expense.expense_date <= end
    ).with_entities(func.sum(Expense.itbms_amount)).scalar() or 0
    
    itbms_neto = float(itbms_vendido) - float(itbms_comprado)
    retenciones = 0
    saldo_pendiente = itbms_neto - retenciones
    
    return {
        "itbms_vendido": float(itbms_vendido),
        "itbms_comprado": float(itbms_comprado),
        "itbms_neto": round(itbms_neto, 2),
        "retenciones": float(retenciones),
        "saldo_pendiente": round(saldo_pendiente, 2)
    }
