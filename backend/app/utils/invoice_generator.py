import hashlib
import uuid
from datetime import datetime
from typing import List, Dict, Any
from app.models.invoice import Invoice, InvoiceDetail
from app.models.invoice_schemas import InvoiceCreate, InvoiceDetailCreate

def generate_invoice_number(tenant_id: int, invoice_type: str = "01") -> str:
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{tenant_id}-{invoice_type}-{timestamp}-{unique_id}"

def generate_cufe(invoice_data: Dict[str, Any]) -> str:
    ruc = invoice_data.get("sender_ruc", "")
    date = invoice_data.get("issue_date", "")
    total = invoice_data.get("total", 0)
    currency = invoice_data.get("currency", "PAB")
    
    cufe_string = f"{ruc}{date}{total}{currency}{uuid.uuid4().hex[:8]}"
    cufe = hashlib.sha256(cufe_string.encode()).hexdigest()
    return cufe[:100]

def format_decimal(value: float, decimals: int = 2) -> str:
    return f"{value:.{decimals}f}"

def calculate_line_totals(detail: InvoiceDetailCreate) -> Dict[str, float]:
    subtotal = detail.quantity * detail.unit_price
    discount_amount = subtotal * (detail.discount_percent / 100)
    subtotal_after_discount = subtotal - discount_amount
    itbms_amount = subtotal_after_discount * detail.itbms_rate
    total = subtotal_after_discount + itbms_amount
    
    return {
        "subtotal": round(subtotal_after_discount, 2),
        "itbms_amount": round(itbms_amount, 2),
        "total": round(total, 2),
        "discount_amount": round(discount_amount, 2)
    }

def generate_sfep_xml(invoice: Invoice, details: List[InvoiceDetail]) -> str:
    issue_datetime = invoice.issue_date.strftime("%Y-%m-%dT%H:%M:%S")
    date_str = invoice.issue_date.strftime("%Y-%m-%d")
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<dte version="1.0">',
        '  <DatosGenerales>',
        f'    <TipoDocumento>{invoice.type}</TipoDocumento>',
        f'    <NumeroDocumento>{invoice.number}</NumeroDocumento>',
        f'    {f"<DocumentoRelacionado>{invoice.related_invoice_id}</DocumentoRelacionado>" if invoice.related_invoice_id else ""}',
        f'    {f"<RazonDocumentoRelacionado>{invoice.reason}</RazonDocumentoRelacionado>" if invoice.reason else ""}',
        f'    <FechaEmision>{date_str}</FechaEmision>',
        f'    <HoraEmision>{invoice.issue_time}</HoraEmision>',
        f'    <TipoOperacion>1</TipoOperacion>',
        f'    <Moneda>{invoice.currency}</Moneda>',
        f'    <TipoCambio>{format_decimal(invoice.exchange_rate)}</TipoCambio>',
        f'    <NumeroResolucion>201-2024</NumeroResolucion>',
        '  </DatosGenerales>',
        '  <Emisor>',
        f'    <RUCEmisor>{invoice.sender_ruc}</RUCEmisor>',
        f'    <DVEmisor>{invoice.sender_dv or ""}</DVEmisor>',
        f'    <RazonSocialEmisor>{invoice.sender_razon_social}</RazonSocialEmisor>',
        f'    <NombreComercialEmisor>{invoice.sender_razon_social}</NombreComercialEmisor>',
        f'    <DireccionEmisor>{invoice.sender_address or ""}</DireccionEmisor>',
        f'    <TelefonoEmisor>{invoice.sender_phone or ""}</TelefonoEmisor>',
        f'    <CorreoEmisor>{invoice.sender_email or ""}</CorreoEmisor>',
        '  </Emisor>',
        '  <Receptor>',
        f'    <RUCReceptor>{invoice.receiver_ruc}</RUCReceptor>',
        f'    <DVReceptor>{invoice.receiver_dv or ""}</DVReceptor>',
        f'    <RazonSocialReceptor>{invoice.receiver_razon_social}</RazonSocialReceptor>',
        f'    <DireccionReceptor>{invoice.receiver_address or ""}</DireccionReceptor>',
        f'    <CorreoReceptor>{invoice.receiver_email or ""}</CorreoReceptor>',
        f'    <TipoIdentificacionReceptor>{invoice.receiver_tipo}</TipoIdentificacionReceptor>',
        '  </Receptor>',
    ]
    
    for detail in details:
        xml_lines.extend([
            '  <Items>',
            '    <Item>',
            f'      <NumeroLinea>{detail.line_number}</NumeroLinea>',
            f'      <Codigo>{detail.code or ""}</Codigo>',
            f'      <Descripcion>{detail.description}</Descripcion>',
            f'      <Cantidad>{format_decimal(detail.quantity)}</Cantidad>',
            f'      <UnidadMedida>{detail.unit_code}</UnidadMedida>',
            f'      <PrecioUnitario>{format_decimal(detail.unit_price)}</PrecioUnitario>',
            f'      <MontoDescuento>{format_decimal(detail.discount_amount)}</MontoDescuento>',
            f'      <PorcentajeDescuento>{format_decimal(detail.discount_percent)}</PorcentajeDescuento>',
            f'      <MontoTotal>{format_decimal(detail.subtotal)}</MontoTotal>',
            '      <Impuestos>',
            '        <Impuesto>',
            f'          <Codigo>01</Codigo>',
            f'          <Tarifa>{format_decimal(detail.itbms_rate * 100)}</Tarifa>',
            f'          <Monto>{format_decimal(detail.itbms_amount)}</Monto>',
            '        </Impuesto>',
            '      </Impuestos>',
            f'      <MonteroItem>{format_decimal(detail.total)}</MonteroItem>',
            '    </Item>',
            '  </Items>',
        ])
    
    xml_lines.extend([
        '  <Totales>',
        f'    <TotalSinImpuestos>{format_decimal(invoice.subtotal)}</TotalSinImpuestos>',
        f'    <MontoDescuento>{format_decimal(invoice.descuento)}</MontoDescuento>',
        f'    <TotalImpuesto>{format_decimal(invoice.total_itbms)}</TotalImpuesto>',
        f'    <TotalFinal>{format_decimal(invoice.total)}</TotalFinal>',
        '  </Totales>',
    ])
    
    if invoice.cufe:
        xml_lines.append(f'  <CodigoGeneracion>{invoice.cufe}</CodigoGeneracion>')
    
    xml_lines.append('</dte>')
    
    return '\n'.join(xml_lines)

def create_invoice_from_data(
    invoice_data: InvoiceCreate,
    tenant_id: int,
    sender_ruc: str,
    sender_razon_social: str,
    sender_dv: str = None,
    sender_address: str = None,
    sender_phone: str = None,
    sender_email: str = None
) -> tuple[Invoice, List[InvoiceDetail]]:
    
    invoice_number = generate_invoice_number(tenant_id, invoice_data.type)
    
    subtotal_total = 0
    descuento_total = 0
    itbms_total = 0
    total_final = 0
    
    details = []
    for idx, detail_data in enumerate(invoice_data.details):
        line_totals = calculate_line_totals(detail_data)
        
        detail = InvoiceDetail(
            line_number=idx + 1,
            code=detail_data.code,
            description=detail_data.description,
            quantity=detail_data.quantity,
            unit_code=detail_data.unit_code,
            unit_price=detail_data.unit_price,
            discount_percent=detail_data.discount_percent,
            discount_amount=line_totals["discount_amount"],
            subtotal=line_totals["subtotal"],
            itbms_rate=detail_data.itbms_rate,
            itbms_amount=line_totals["itbms_amount"],
            total=line_totals["total"]
        )
        
        subtotal_total += line_totals["subtotal"]
        descuento_total += line_totals["discount_amount"]
        itbms_total += line_totals["itbms_amount"]
        total_final += line_totals["total"]
        
        details.append(detail)
    
    invoice = Invoice(
        tenant_id=tenant_id,
        number=invoice_number,
        type=invoice_data.type,
        status="draft",
        issue_date=invoice_data.issue_date,
        issue_time=invoice_data.issue_time,
        sender_ruc=sender_ruc,
        sender_razon_social=sender_razon_social,
        sender_dv=sender_dv,
        sender_address=sender_address,
        sender_phone=sender_phone,
        sender_email=sender_email,
        receiver_ruc=invoice_data.receiver.ruc,
        receiver_razon_social=invoice_data.receiver.razon_social,
        receiver_dv=invoice_data.receiver.dv,
        receiver_address=invoice_data.receiver.address,
        receiver_email=invoice_data.receiver.email,
        receiver_tipo=invoice_data.receiver.tipo,
        subtotal=subtotal_total,
        descuento=descuento_total,
        itbms=itbms_total,
        total=total_final,
        total_itbms=itbms_total,
        currency=invoice_data.currency,
        exchange_rate=invoice_data.exchange_rate,
        related_invoice_id=invoice_data.related_invoice_id,
        reason=invoice_data.reason
    )
    
    return invoice, details
