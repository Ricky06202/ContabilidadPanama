from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DashboardResponse(BaseModel):
    total_clientes: int
    total_proveedores: int
    total_productos: int
    total_empleados: int
    ventas_mes: float
    gastos_mes: float
    ingresos_mes: float
    bancos_total: float

class BalanceGeneralResponse(BaseModel):
    activos: dict
    pasivos: dict
    patrimonio: dict
    total_activos: float
    total_pasivos: float
    total_patrimonio: float

class EstadoResultadosResponse(BaseModel):
    ingresos: float
    costo_ventas: float
    utilidad_bruta: float
    gastos_operativos: float
    utilidad_operativa: float
    otros_gastos: float
    utilidad_neta: float

class FlujoCajaResponse(BaseModel):
    saldo_inicial: float
    entradas: float
    salidas: float
    saldo_final: float
    detalle_entradas: list
    detalle_salidas: list

class ResumenImpuestosResponse(BaseModel):
    itbms_vendido: float
    itbms_comprado: float
    itbms_neto: float
    retenciones: float
    saldo_pendiente: float

class ReportConfigBase(BaseModel):
    ejercicio_fiscal: int = 2026
    periodo_inicio: int = 1
    periodo_fin: int = 12

class ReportConfigResponse(ReportConfigBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True
