from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    cedula = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    
    fecha_nacimiento = Column(DateTime)
    fecha_ingreso = Column(DateTime, nullable=False)
    fecha_salida = Column(DateTime)
    
    departamento = Column(String(100))
    cargo = Column(String(100))
    
    salario_base = Column(Float, nullable=False)
    hora_extra = Column(Float, default=0)
    bonificacion = Column(Float, default=0)
    
    tipo_contrato = Column(String(20), default="indefinido")
    es_activo = Column(Boolean, default=True)
    
    notas = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="employees")
    payrolls = relationship("Payroll", back_populates="employee", cascade="all, delete")

class Payroll(Base):
    __tablename__ = "payrolls"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    periodo = Column(String(20), nullable=False)
    fecha_pago = Column(DateTime, nullable=False)
    
    dias_trabajados = Column(Integer, default=30)
    horas_extra = Column(Float, default=0)
    bonificacion = Column(Float, default=0)
    
    salario_bruto = Column(Float, nullable=False)
    inss_laboral = Column(Float, default=0)
    IR = Column(Float, default=0)
    total_deducciones = Column(Float, default=0)
    
    salario_neto = Column(Float, nullable=False)
    
    estado = Column(String(20), default="pendiente")
    notas = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    tenant = relationship("Tenant")
    employee = relationship("Employee", back_populates="payrolls")

class PayrollConfig(Base):
    __tablename__ = "payroll_config"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, unique=True)
    
    inss_porcentaje = Column(Float, default=6.75)
    inss_empleador_porcentaje = Column(Float, default=12.5)
    
    fecha_decimo_tercero_inicio = Column(Integer, default=4)
    fecha_decimo_tercero_fin = Column(Integer, default=3)
    fecha_decimo_cuarto_inicio = Column(Integer, default=8)
    fecha_decimo_cuarto_fin = Column(Integer, default=7)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", backref="payroll_config")
