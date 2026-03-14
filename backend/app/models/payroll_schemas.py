from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[datetime] = None
    fecha_ingreso: datetime
    fecha_salida: Optional[datetime] = None
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    salario_base: float
    hora_extra: float = 0
    bonificacion: float = 0
    tipo_contrato: str = "indefinido"
    notas: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    tenant_id: int
    es_activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PayrollBase(BaseModel):
    employee_id: int
    periodo: str
    fecha_pago: datetime
    dias_trabajados: int = 30
    horas_extra: float = 0
    bonificacion: float = 0

class PayrollCreate(PayrollBase):
    pass

class PayrollResponse(PayrollBase):
    id: int
    tenant_id: int
    employee_id: int
    salario_bruto: float
    inss_laboral: float
    IR: float
    total_deducciones: float
    salario_neto: float
    estado: str
    notas: Optional[str] = None
    created_at: datetime
    
    employee: Optional[EmployeeResponse] = None

    class Config:
        from_attributes = True

class PayrollConfigBase(BaseModel):
    inss_porcentaje: float = 6.75
    inss_empleador_porcentaje: float = 12.5
    fecha_decimo_tercero_inicio: int = 4
    fecha_decimo_tercero_fin: int = 3
    fecha_decimo_cuarto_inicio: int = 8
    fecha_decimo_cuarto_fin: int = 7

class PayrollConfigCreate(PayrollConfigBase):
    pass

class PayrollConfigResponse(PayrollConfigBase):
    id: int
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
