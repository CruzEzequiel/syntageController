from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional, List
from utils.financialCalcs import map_to_evaluate_request
from pydantic import BaseModel, Field

# Crear el enrutador para las rutas del mapping financiero
router = APIRouter()

# ===== Modelos Pydantic para Buró de Crédito =====

class BuroScoreItem(BaseModel):
    errorScore: Optional[str] = None
    valorScore: Optional[str] = None
    codigoScore: Optional[str] = None
    codigoRazon1: Optional[str] = None
    codigoRazon2: Optional[str] = None
    codigoRazon3: Optional[str] = None
    codigoRazon4: Optional[str] = None

class BuroHawkHr(BaseModel):
    codigoHawk: Optional[str] = None
    fechaMensajeHawk: Optional[str] = None
    descripcionPrevencionHawk: Optional[str] = None

class BuroCalifica(BaseModel):
    clave: Optional[str] = None
    nombre: Optional[str] = None
    valorCaracteristica: Optional[str] = None

class BuroHistoria(BaseModel):
    rfc: Optional[str] = None
    periodo: Optional[str] = None
    saldoVigente: Optional[str] = None
    maximoSaldoVencido: Optional[str] = None
    saldoVencidoA90Dias: Optional[str] = None
    saldoVencido1A29Dias: Optional[str] = None
    saldoVencido30A59Dias: Optional[str] = None
    saldoVencido60A89Dias: Optional[str] = None
    mayorNumeroDiasVencido: Optional[str] = None

class BuroEncabezado(BaseModel):
    claveRetorno: Optional[str] = None
    fechaConsulta: Optional[str] = None
    identificadorTransaccion: Optional[str] = None

class BuroDatosGenerales(BaseModel):
    pais: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    nombre: Optional[str] = None
    direccion1: Optional[str] = None
    rfcCliente: Optional[str] = None
    tipoCliente: Optional[str] = None
    codigoPostal: Optional[str] = None
    coloniaPoblacion: Optional[str] = None
    actividadEconomica1: Optional[str] = None
    delegacionMunicipio: Optional[str] = None
    consultaEmpresaComercialMas24Meses: Optional[str] = None
    consultaEntidadFinancieraMas24Meses: Optional[str] = None
    consultaEmpresaComercialUltimos3Meses: Optional[str] = None
    consultaEmpresaComercialUltimos12Meses: Optional[str] = None
    consultaEmpresaComercialUltimos24Meses: Optional[str] = None
    consultaEntidadFinancieraUltimos3Meses: Optional[str] = None
    consultaEntidadFinancieraUltimos12Meses: Optional[str] = None
    consultaEntidadFinancieraUltimos24Meses: Optional[str] = None

class BuroCreditoComercial(BaseModel):
    rfcCliente: Optional[str] = None
    saldoTotal: Optional[str] = None
    saldoVencido: Optional[str] = None
    saldoVigente: Optional[str] = None
    historicoPagos: Optional[str] = None
    identificadorUsuario: Optional[str] = None
    saldoVencidoDe1a29Dias: Optional[str] = None
    saldoVencidoDe30a59Dias: Optional[str] = None
    saldoVencidoDe60a89Dias: Optional[str] = None
    saldoVencidoDe90a119Dias: Optional[str] = None
    ultimoPeriodoActualizado: Optional[str] = None
    saldoVencidoDe120a179Dias: Optional[str] = None
    saldoVencidoDe180DiasOMas: Optional[str] = None

class BuroCreditoFinanciero(BaseModel):
    plazo: Optional[str] = None
    moneda: Optional[str] = None
    apertura: Optional[str] = None
    montoPago: Optional[str] = None
    rfcCliente: Optional[str] = None
    tipoCambio: Optional[str] = None
    atrasoMayor: Optional[str] = None
    numeroPagos: Optional[str] = None
    tipoCredito: Optional[str] = None
    tipoUsuario: Optional[str] = None
    numeroCuenta: Optional[str] = None
    saldoInicial: Optional[str] = None
    saldoVigente: Optional[str] = None
    saldoInsoluto: Optional[str] = None
    fechaUltimoPago: Optional[str] = None
    frecuenciaPagos: Optional[str] = None
    historicoPagos: Optional[str] = None
    creditoMaximoUtilizado: Optional[str] = None
    saldoVencidoDe1a29Dias: Optional[str] = None
    saldoVencidoDe30a59Dias: Optional[str] = None
    saldoVencidoDe60a89Dias: Optional[str] = None
    saldoVencidoDe90a119Dias: Optional[str] = None
    ultimoPeriodoActualizado: Optional[str] = None
    saldoVencidoDe120a179Dias: Optional[str] = None
    saldoVencidoDe180DiasOMas: Optional[str] = None
    quita: Optional[str] = None
    dacion: Optional[str] = None
    quebranto: Optional[str] = None
    pagoCierre: Optional[str] = None
    fechaCierre: Optional[str] = None
    claveObservacion: Optional[str] = None
    tipoResponsabilidad: Optional[str] = None
    fechaPrimerIncumplimiento: Optional[str] = None
    fechaIngresoCarteraVencida: Optional[str] = None

class BuroHistorialConsultas(BaseModel):
    rfc: Optional[str] = None
    tipoUsuario: Optional[str] = None
    fechaConsulta: Optional[str] = None

class BuroData(BaseModel):
    score: Optional[List[BuroScoreItem]] = None
    hawkHr: Optional[List[BuroHawkHr]] = None
    califica: Optional[List[BuroCalifica]] = None
    historia: Optional[List[BuroHistoria]] = None
    encabezado: Optional[BuroEncabezado] = None
    datosGenerales: Optional[BuroDatosGenerales] = None
    creditoComercial: Optional[List[BuroCreditoComercial]] = None
    creditoFinanciero: Optional[List[BuroCreditoFinanciero]] = None
    historialConsultas: Optional[BuroHistorialConsultas] = None

class BuroFile(BaseModel):
    id: Optional[str] = None
    resource: Optional[str] = None
    mimeType: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[int] = None
    filename: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

class BuroMember(BaseModel):
    id: Optional[str] = None
    provider: Optional[str] = None
    productType: Optional[str] = None
    reportId: Optional[str] = None
    data: Optional[BuroData] = None
    score: Optional[str] = None
    files: Optional[List[BuroFile]] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

class BuroReportData(BaseModel):
    Buro: Optional[List[BuroMember]] = None

class EvaluateResponse(BaseModel):
    """Modelo de respuesta con el formato EvaluateRequest"""
    fin: Dict[str, Any] = Field(description="Datos financieros")
    ch: Dict[str, Any] = Field(description="Historial crediticio")
    comp: Dict[str, Any] = Field(description="Datos de cumplimiento")
    geo: Dict[str, Any] = Field(description="Datos geográficos")

@router.post(
    "/map-to-evaluate-request",
    response_model=EvaluateResponse,
    summary="Mapear datos financieros (formato flexible)",
    description="Versión alternativa que acepta cualquier estructura JSON sin validación estricta, incluyendo datos de buró de crédito"
)
async def map_to_evaluate_request_raw_endpoint(
    request_data: Dict[str, Any] = Body(
        ...,
        example={
            "summaryData": {
                "rfc": "CDV14100WEDA",
                "lastYearNetIncome": 19339633
            },
            "financialRatiosData": {},
            "riskIndicatorsData": {},
            "annualComparisonData": {},
            "buroReportData": {
                "Buro": [
                    {
                        "id": "example-id",
                        "provider": "Buro",
                        "data": {
                            "score": [{"valorScore": "750"}],
                            "creditoFinanciero": []
                        }
                    }
                ]
            }
        }
    )
):
    """
    Versión alternativa del endpoint que acepta Dict directamente.
    Útil para integraciones legacy o cuando no se conoce la estructura exacta.
    Ahora incluye soporte para datos de buró de crédito (buroReportData).
    """
    try:
        # Validación mínima
        if not isinstance(request_data, dict):
            raise HTTPException(
                status_code=400,
                detail="Request body must be a JSON object"
            )
        
        if not request_data.get("summaryData"):
            raise HTTPException(
                status_code=400,
                detail="summaryData is required"
            )
        
        # Llamar a la función de mapping (ahora incluye buroReportData)
        result = map_to_evaluate_request(request_data)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial mapping: {str(e)}"
        )

@router.post("/map-to-evaluate-request-by-ids")
async def map_to_evaluate_request_by_ids_endpoint(
    request_data: Dict[str, Any] = Body(...)
):
    """
    Endpoint alternativo que toma IDs de entidad/negocio y obtiene los datos automáticamente
    desde los otros endpoints, luego realiza el mapping.
    
    Espera un JSON con la siguiente estructura:
    {
        "entity_id": "string",
        "business_id": "string", 
        "credit_bureau_data": {...} (opcional),
        "geographic_data": {...} (opcional)
    }
    
    Retorna un objeto con formato EvaluateRequest: {fin, ch, comp, geo}
    """
    try:
        entity_id = request_data.get("entity_id")
        business_id = request_data.get("business_id")
        
        # Validar que los IDs estén presentes
        if not entity_id:
            raise HTTPException(status_code=400, detail="entity_id is required")
        if not business_id:
            raise HTTPException(status_code=400, detail="business_id is required")
        
        # TODO: Aquí se podrían hacer llamadas internas a los otros endpoints
        # para obtener los datos automáticamente. Por ahora, devolvemos un mensaje
        # indicando que esta funcionalidad requiere implementación adicional.
        
        return {
            "message": "Esta funcionalidad requiere integración con los endpoints existentes",
            "entity_id": entity_id,
            "business_id": business_id,
            "note": "Use el endpoint /map-to-evaluate-request con datos completos por ahora"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")