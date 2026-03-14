from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from math import ceil

from app.database import get_db
from app.models.models import User
from app.models.payroll import Employee, Payroll, PayrollConfig
from app.models.payroll_schemas import (
    EmployeeCreate, EmployeeResponse,
    PayrollCreate, PayrollResponse,
    PayrollConfigCreate, PayrollConfigResponse
)
from app.routers.auth import get_current_user

router = APIRouter()

def calculate_inss_laboral(salario_bruto: float, inss_porcentaje: float = 6.75) -> float:
    return round(salario_bruto * (inss_porcentaje / 100), 2)

def calculate_ir(salario_neto: float) -> float:
    if salario_neto <= 1500:
        return 0
    elif salario_neto <= 3000:
        return round((salario_neto - 1500) * 0.15, 2)
    elif salario_neto <= 5000:
        return round(225 + (salario_neto - 3000) * 0.20, 2)
    else:
        return round(625 + (salario_neto - 5000) * 0.25, 2)

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Employee).filter(
        Employee.cedula == data.cedula,
        Employee.tenant_id == current_user.tenant_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un empleado con esta cédula")
    
    employee = Employee(
        tenant_id=current_user.tenant_id,
        **data.model_dump()
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.get("/employees", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Employee).filter(
        Employee.tenant_id == current_user.tenant_id
    ).offset(skip).limit(limit).all()

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    for key, value in data.model_dump().items():
        setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    db.delete(employee)
    db.commit()
    return {"message": "Empleado eliminado"}

@router.post("/payrolls", response_model=PayrollResponse, status_code=status.HTTP_201_CREATED)
def create_payroll(
    data: PayrollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = db.query(Employee).filter(
        Employee.id == data.employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    config = db.query(PayrollConfig).filter(
        PayrollConfig.tenant_id == current_user.tenant_id
    ).first()
    if not config:
        config = PayrollConfig(tenant_id=current_user.tenant_id)
        db.add(config)
        db.commit()
        db.refresh(config)
    
    hora_extra_valor = employee.hora_extra * data.horas_extra if data.horas_extra > 0 else 0
    bonificacion_valor = data.bonificacion if data.bonificacion > 0 else employee.bonificacion
    
    dias_factor = data.dias_trabajados / 30
    salario_base_mensual = employee.salario_base * dias_factor
    
    salario_bruto = round(salario_base_mensual + hora_extra_valor + bonificacion_valor, 2)
    inss_laboral = calculate_inss_laboral(salario_bruto, config.inss_porcentaje)
    salario_neto_inss = salario_bruto - inss_laboral
    ir = calculate_ir(salario_neto_inss)
    total_deducciones = inss_laboral + ir
    salario_neto = round(salario_bruto - total_deducciones, 2)
    
    payroll = Payroll(
        tenant_id=current_user.tenant_id,
        employee_id=data.employee_id,
        periodo=data.periodo,
        fecha_pago=data.fecha_pago,
        dias_trabajados=data.dias_trabajados,
        horas_extra=data.horas_extra,
        bonificacion=bonificacion_valor,
        salario_bruto=salario_bruto,
        inss_laboral=inss_laboral,
        IR=ir,
        total_deducciones=total_deducciones,
        salario_neto=salario_neto,
        estado="completado"
    )
    db.add(payroll)
    db.commit()
    db.refresh(payroll)
    return payroll

@router.get("/payrolls", response_model=List[PayrollResponse])
def list_payrolls(
    employee_id: int = None,
    periodo: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Payroll).filter(Payroll.tenant_id == current_user.tenant_id)
    if employee_id:
        query = query.filter(Payroll.employee_id == employee_id)
    if periodo:
        query = query.filter(Payroll.periodo == periodo)
    return query.order_by(Payroll.fecha_pago.desc()).offset(skip).limit(limit).all()

@router.get("/payrolls/{payroll_id}", response_model=PayrollResponse)
def get_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id,
        Payroll.tenant_id == current_user.tenant_id
    ).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Nómina no encontrada")
    return payroll

@router.get("/payroll-summary/{periodo}")
def get_payroll_summary(
    periodo: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payrolls = db.query(Payroll).filter(
        Payroll.tenant_id == current_user.tenant_id,
        Payroll.periodo == periodo
    ).all()
    
    total_bruto = sum(p.salario_bruto for p in payrolls)
    total_inss = sum(p.inss_laboral for p in payrolls)
    total_ir = sum(p.IR for p in payrolls)
    total_neto = sum(p.salario_neto for p in payrolls)
    
    return {
        "periodo": periodo,
        "total_empleados": len(payrolls),
        "total_salario_bruto": round(total_bruto, 2),
        "total_inss_laboral": round(total_inss, 2),
        "total_IR": round(total_ir, 2),
        "total_salario_neto": round(total_neto, 2)
    }

@router.post("/payroll-config", response_model=PayrollConfigResponse, status_code=status.HTTP_201_CREATED)
def create_payroll_config(
    data: PayrollConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(PayrollConfig).filter(
        PayrollConfig.tenant_id == current_user.tenant_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Configuración de nómina ya existe")
    
    config = PayrollConfig(
        tenant_id=current_user.tenant_id,
        **data.model_dump()
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config

@router.get("/payroll-config", response_model=PayrollConfigResponse)
def get_payroll_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    config = db.query(PayrollConfig).filter(
        PayrollConfig.tenant_id == current_user.tenant_id
    ).first()
    if not config:
        config = PayrollConfig(tenant_id=current_user.tenant_id)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config
