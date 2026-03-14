from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.models import User, Tenant
from app.models.invoice import Invoice, InvoiceDetail
from app.models.invoice_schemas import (
    InvoiceCreate, InvoiceResponse, InvoiceWithDetails, 
    InvoiceXMLResponse, CreditDebitNoteCreate
)
from app.routers.auth import get_current_user
from app.utils.invoice_generator import (
    create_invoice_from_data, generate_sfep_xml, generate_cufe
)

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant no encontrado"
        )
    
    invoice, details = create_invoice_from_data(
        invoice_data=invoice_data,
        tenant_id=current_user.tenant_id,
        sender_ruc=tenant.ruc,
        sender_razon_social=tenant.name,
        sender_address=tenant.address,
        sender_phone=tenant.phone
    )
    
    db.add(invoice)
    db.flush()
    
    for detail in details:
        detail.invoice_id = invoice.id
        db.add(detail)
    
    db.commit()
    db.refresh(invoice)
    
    return InvoiceResponse(
        id=invoice.id,
        tenant_id=invoice.tenant_id,
        number=invoice.number,
        type=invoice.type,
        status=invoice.status,
        issue_date=invoice.issue_date,
        issue_time=invoice.issue_time,
        sender_ruc=invoice.sender_ruc,
        sender_razon_social=invoice.sender_razon_social,
        receiver_ruc=invoice.receiver_ruc,
        receiver_razon_social=invoice.receiver_razon_social,
        subtotal=invoice.subtotal,
        descuento=invoice.descuento,
        itbms=invoice.itbms,
        total=invoice.total,
        currency=invoice.currency,
        exchange_rate=invoice.exchange_rate,
        xml_content=invoice.xml_content,
        cufe=invoice.cufe,
        signature=invoice.signature,
        created_at=invoice.created_at
    )

@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    type_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Invoice).filter(Invoice.tenant_id == current_user.tenant_id)
    
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    if type_filter:
        query = query.filter(Invoice.type == type_filter)
    
    invoices = query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        InvoiceResponse(
            id=inv.id,
            tenant_id=inv.tenant_id,
            number=inv.number,
            type=inv.type,
            status=inv.status,
            issue_date=inv.issue_date,
            issue_time=inv.issue_time,
            sender_ruc=inv.sender_ruc,
            sender_razon_social=inv.sender_razon_social,
            receiver_ruc=inv.receiver_ruc,
            receiver_razon_social=inv.receiver_razon_social,
            subtotal=inv.subtotal,
            descuento=inv.descuento,
            itbms=inv.itbms,
            total=inv.total,
            currency=inv.currency,
            exchange_rate=inv.exchange_rate,
            xml_content=inv.xml_content,
            cufe=inv.cufe,
            signature=inv.signature,
            created_at=inv.created_at
        )
        for inv in invoices
    ]

@router.get("/{invoice_id}", response_model=InvoiceWithDetails)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.tenant_id == current_user.tenant_id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    details = db.query(InvoiceDetail).filter(InvoiceDetail.invoice_id == invoice.id).all()
    
    return InvoiceWithDetails(
        id=invoice.id,
        tenant_id=invoice.tenant_id,
        number=invoice.number,
        type=invoice.type,
        status=invoice.status,
        issue_date=invoice.issue_date,
        issue_time=invoice.issue_time,
        sender_ruc=invoice.sender_ruc,
        sender_razon_social=invoice.sender_razon_social,
        receiver_ruc=invoice.receiver_ruc,
        receiver_razon_social=invoice.receiver_razon_social,
        subtotal=invoice.subtotal,
        descuento=invoice.descuento,
        itbms=invoice.itbms,
        total=invoice.total,
        currency=invoice.currency,
        exchange_rate=invoice.exchange_rate,
        xml_content=invoice.xml_content,
        cufe=invoice.cufe,
        signature=invoice.signature,
        created_at=invoice.created_at,
        details=[
            type('DetailResponse', (), {
                'id': d.id,
                'line_number': d.line_number,
                'code': d.code,
                'description': d.description,
                'quantity': d.quantity,
                'unit_code': d.unit_code,
                'unit_price': d.unit_price,
                'discount_percent': d.discount_percent,
                'discount_amount': d.discount_amount,
                'subtotal': d.subtotal,
                'itbms_rate': d.itbms_rate,
                'itbms_amount': d.itbms_amount,
                'total': d.total
            })()
            for d in details
        ]
    )

@router.post("/{invoice_id}/generate-xml", response_model=InvoiceXMLResponse)
def generate_xml(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.tenant_id == current_user.tenant_id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status not in ["draft", "generated"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede generar XML en estado: {invoice.status}"
        )
    
    details = db.query(InvoiceDetail).filter(InvoiceDetail.invoice_id == invoice.id).all()
    
    invoice.cufe = generate_cufe({
        "sender_ruc": invoice.sender_ruc,
        "issue_date": invoice.issue_date.strftime("%Y-%m-%d"),
        "total": invoice.total,
        "currency": invoice.currency
    })
    
    xml_content = generate_sfep_xml(invoice, details)
    invoice.xml_content = xml_content
    invoice.status = "generated"
    
    db.commit()
    db.refresh(invoice)
    
    return InvoiceXMLResponse(
        xml_content=xml_content,
        cufe=invoice.cufe
    )

@router.post("/{invoice_id}/sign")
def sign_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.tenant_id == current_user.tenant_id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if not invoice.xml_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe generar el XML primero"
        )
    
    invoice.signature = f"SIGNATURE_PLACEHOLDER_{invoice.cufe[:16]}"
    invoice.status = "signed"
    
    db.commit()
    
    return {"message": "Factura firmada (simulado)", "signature": invoice.signature}

@router.post("/{invoice_id}/send")
def send_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.tenant_id == current_user.tenant_id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if not invoice.signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe firmar la factura primero"
        )
    
    invoice.status = "sent"
    invoice.dgi_response = '{"status": "received", "message": "Documento recibido por DGI"}'
    
    db.commit()
    
    return {"message": "Factura enviada a DGI (simulado)", "dgi_response": invoice.dgi_response}
