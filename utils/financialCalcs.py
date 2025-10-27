from typing import Dict, Any, Optional, List
from datetime import datetime


def map_to_evaluate_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mapea datos financieros complejos a un formato estructurado para evaluación.
    
    Args:
        data: Diccionario con summaryData, financialRatiosData, 
              riskIndicatorsData, annualComparisonData y buroReportData
    
    Returns:
        Diccionario con estructuras fin, ch, comp y geo
    """
    
    # Extraer datos principales
    summary = data.get('summaryData') or {}
    ratios = data.get('financialRatiosData') or {}
    risks = data.get('riskIndicatorsData', {}).get('data') or {}
    annual = data.get('annualComparisonData', {}).get('items') or []
    buro_report = data.get('buroReportData') or {}
    
    # ===== FIN - Datos Financieros =====
    fin_data = _map_financial_data(summary, ratios, annual)
    
    # ===== CH - Historial Crediticio =====
    ch_data = _map_credit_history_data(buro_report)
    
    # ===== COMP - Cumplimiento =====
    comp_data = _map_compliance_data(risks)
    
    # ===== GEO - Datos Geográficos =====
    geo_data = _map_geographic_data(summary)
    
    return {
        "fin": fin_data,
        "ch": ch_data,
        "comp": comp_data,
        "geo": geo_data
    }


def _map_financial_data(summary: Dict, ratios: Dict, annual: List) -> Dict[str, Any]:
    """Mapea datos financieros (fin)"""
    
    # Utilidad neta anual (del último año disponible)
    utilidad_neta = summary.get('lastYearNetIncome', 0.0)
    
    # Razón circulante (del año más reciente disponible)
    razon_circulante = _get_most_recent_ratio(
        ratios.get('liquidity', {}).get('current_ratio', {})
    )
    
    # Apalancamiento en porcentaje (debt ratio * 100)
    debt_ratio = _get_most_recent_ratio(
        ratios.get('leverage', {}).get('total_debt_ratio', {})
    )
    apalancamiento_pct = debt_ratio * 100 if debt_ratio is not None else 0.0
    
    # Rentabilidad (ROA)
    rentabilidad = _get_most_recent_ratio(
        ratios.get('profitability', {}).get('return_on_assets', {})
    )
    
    # Años de historial de ventas
    anios_historial = len(annual) if annual else 0
    # Si hay datos acumulados, restar 1
    if anios_historial > 0 and any(
        item.get('period') == 'Acumulado' for item in annual
    ):
        anios_historial -= 1
    
    # Gran empresa (ingresos > 1M)
    total_ingresos = summary.get('lastYearTotalIncome', 0.0)
    gran_empresa = total_ingresos > 1_000_000
    
    # Crecimiento de ventas último año
    crecimiento_positivo = _calculate_sales_growth(annual)
    
    return {
        "utilidad_neta_anual": utilidad_neta,
        "razon_circulante": razon_circulante if razon_circulante is not None else 0.0,
        "apalancamiento_pct": apalancamiento_pct,
        "rentabilidad": rentabilidad if rentabilidad is not None else 0.0,
        "anios_historial_ventas": anios_historial,
        "gran_empresa": gran_empresa,
        "crecimiento_ventas_ultimo_anio_pos": crecimiento_positivo
    }


def _map_credit_history_data(buro_report: Dict) -> Dict[str, Any]:
    """
    Mapea datos del historial crediticio desde el reporte de buró (ch)
    
    Args:
        buro_report: Diccionario con la estructura BuroReportData
    
    Returns:
        Diccionario con métricas de historial crediticio
    """
    # Inicializar valores por defecto
    ch_data = {
        "dias_atraso": 0,
        "num_open_performing_loan": 0,
        "saldo_vencido_maxic_udis": 0.0,
        "creditos_abiertos": 0,
        "pct_open_12m": 0.0,
        "claves_observacion": [],
        "maximo_credito_aprobado_historico": 0.0
    }
    
    # Si no hay datos de buró, retornar valores por defecto
    if not buro_report or not buro_report.get('Buro'):
        return ch_data
    
    # Obtener el primer reporte de buró (normalmente solo hay uno)
    buro_members = buro_report.get('Buro', [])
    if not buro_members or len(buro_members) == 0:
        return ch_data
    
    buro_data = buro_members[0].get('data', {})
    if not buro_data:
        return ch_data
    
    # Extraer créditos financieros
    creditos_financieros = buro_data.get('creditoFinanciero', []) or []
    creditos_comerciales = buro_data.get('creditoComercial', []) or []
    
    # Calcular días de atraso máximo
    dias_atraso = _calculate_max_days_overdue(creditos_financieros)
    ch_data['dias_atraso'] = dias_atraso
    
    # Contar créditos abiertos con buen desempeño (performing loans)
    num_performing = _count_open_performing_loans(creditos_financieros)
    ch_data['num_open_performing_loan'] = num_performing
    
    # Calcular saldo vencido máximo
    saldo_vencido = _calculate_max_overdue_balance(creditos_financieros, creditos_comerciales)
    ch_data['saldo_vencido_maxic_udis'] = saldo_vencido
    
    # Contar créditos abiertos totales
    creditos_abiertos = _count_open_credits(creditos_financieros)
    ch_data['creditos_abiertos'] = creditos_abiertos
    
    # Calcular porcentaje de créditos abiertos en últimos 12 meses
    pct_open_12m = _calculate_pct_open_12m(creditos_financieros)
    ch_data['pct_open_12m'] = pct_open_12m
    
    # Extraer claves de observación
    claves_observacion = _extract_observation_keys(creditos_financieros)
    ch_data['claves_observacion'] = claves_observacion
    
    # Calcular máximo crédito aprobado histórico
    maximo_credito = _calculate_max_approved_credit(creditos_financieros)
    ch_data['maximo_credito_aprobado_historico'] = maximo_credito
    
    return ch_data


def _map_compliance_data(risks: Dict) -> Dict[str, bool]:
    """Mapea datos de cumplimiento (comp)"""
    
    # Legal OK (basado en taxCompliance)
    tax_compliance = risks.get('taxCompliance', {})
    legal_ok = (
        not tax_compliance.get('risky', True) 
        if tax_compliance else False
    )
    
    # PLD OK (basado en contrapartes en lista negra)
    blacklisted = risks.get('blacklistedCounterparties', {})
    pld_ok = (
        blacklisted.get('value', 0) == 0 
        if blacklisted.get('value') is not None else False
    )
    
    # Fiscal OK (basado en facturas canceladas)
    canceled_invoices = risks.get('canceledIssuedInvoices', {})
    fiscal_ok = (
        not canceled_invoices.get('risky', True)
        if canceled_invoices else False
    )
    
    return {
        "legal_ok": legal_ok,
        "pld_ok": pld_ok,
        "fiscal_ok": fiscal_ok,
        "peps_ok": False,  # No disponible, devuelve false
        "profeco_ok": False  # No disponible, devuelve false
    }


def _map_geographic_data(summary: Dict) -> Dict[str, Any]:
    """Mapea datos geográficos (geo)"""
    
    # Extraer estado de la dirección fiscal
    fiscal_address = summary.get('fiscalAddress', '')
    estado = _extract_state_from_address(fiscal_address)
    
    # Validación de domicilio
    address_status = summary.get('fiscalAddressStatusRaw')
    domicilio_validado = address_status is not None
    
    # Presencia física (asumimos true si hay dirección)
    presencia_fisica = bool(fiscal_address)
    
    # Código SCIAN (del primer activity económico)
    activities = summary.get('economicActivities', [])
    scian = None
    if activities and len(activities) > 0:
        # Extraer código SCIAN si está en el nombre
        activity_name = activities[0].get('name', '')
        # En este caso, necesitaríamos un mapeo real de actividades a SCIAN
        # Por ahora, generamos un código basado en la actividad principal
        scian = _get_scian_from_activity(activities[0])
    
    return {
        "estado": estado,
        "domicilio_validado": domicilio_validado,
        "presencia_fisica": presencia_fisica,
        "scian": scian
    }


def _get_most_recent_ratio(ratio_dict: Dict[str, Any]) -> Optional[float]:
    """Obtiene el ratio más reciente de un diccionario de ratios por año"""
    if not ratio_dict:
        return None
    
    # Filtrar años válidos (no "Acumulado")
    valid_years = {
        year: value for year, value in ratio_dict.items()
        if year.isdigit()
    }
    
    if not valid_years:
        return None
    
    # Obtener el año más reciente
    most_recent_year = max(valid_years.keys())
    value = valid_years[most_recent_year]
    
    # Convertir a float si es string
    if value is None:
        return None
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _calculate_sales_growth(annual: List[Dict]) -> bool:
    """Calcula si hubo crecimiento positivo en ventas el último año"""
    if len(annual) < 2:
        return False
    
    # Filtrar años válidos (excluir "Acumulado")
    valid_years = [
        item for item in annual 
        if item.get('period', '').isdigit()
    ]
    
    if len(valid_years) < 2:
        return False
    
    # Ordenar por año
    sorted_years = sorted(valid_years, key=lambda x: int(x['period']))
    
    # Comparar últimos dos años
    last_year = sorted_years[-1]
    prev_year = sorted_years[-2]
    
    try:
        last_income = float(last_year.get('netIncome', 0))
        prev_income = float(prev_year.get('netIncome', 0))
        
        return last_income > prev_income
    except (ValueError, TypeError):
        return False


def _extract_state_from_address(address: str) -> str:
    """Extrae el estado de una dirección fiscal"""
    if not address:
        return ""
    
    # Diccionario de estados comunes en México
    estados_mexico = [
        "AGUASCALIENTES", "BAJA CALIFORNIA", "BAJA CALIFORNIA SUR",
        "CAMPECHE", "CHIAPAS", "CHIHUAHUA", "COAHUILA", "COLIMA",
        "DURANGO", "GUANAJUATO", "GUERRERO", "HIDALGO", "JALISCO",
        "MEXICO", "MICHOACAN", "MORELOS", "NAYARIT", "NUEVO LEON",
        "OAXACA", "PUEBLA", "QUERETARO", "QUINTANA ROO", "SAN LUIS POTOSI",
        "SINALOA", "SONORA", "TABASCO", "TAMAULIPAS", "TLAXCALA",
        "VERACRUZ", "YUCATAN", "ZACATECAS", "CDMX", "CIUDAD DE MEXICO"
    ]
    
    address_upper = address.upper()
    
    # Buscar estado en la dirección
    for estado in estados_mexico:
        if estado in address_upper:
            if estado == "CIUDAD DE MEXICO":
                return "CDMX"
            return estado
    
    return ""


def _get_scian_from_activity(activity: Dict) -> Optional[str]:
    """
    Obtiene el código SCIAN de una actividad económica.
    Nota: Esta es una función simplificada. En producción, 
    necesitarías un catálogo completo de actividades -> SCIAN
    """
    activity_name = activity.get('name', '').lower()
    
    # Mapeo simplificado de algunas actividades comunes
    scian_mapping = {
        'comercio al por mayor': '43',
        'comercializadora': '434',
        'impresión': '323',
        'reparación': '811',
        'cómputo': '517',
    }
    
    for keyword, code in scian_mapping.items():
        if keyword in activity_name:
            # Extender a 6 dígitos con ceros
            return code.ljust(6, '0')
    
    # Por defecto, usar código genérico de servicios financieros
    return '522190'


# ===== Funciones auxiliares para procesamiento de datos de Buró =====

def _safe_float(value: Any, default: float = 0.0) -> float:
    """Convierte un valor a float de manera segura"""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    """Convierte un valor a int de manera segura"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def _calculate_max_days_overdue(creditos: List[Dict]) -> int:
    """
    Calcula el número máximo de días de atraso entre todos los créditos
    """
    max_days = 0
    
    for credito in creditos:
        # Obtener el atraso mayor del crédito
        atraso_str = credito.get('atrasoMayor', '0')
        atraso = _safe_int(atraso_str, 0)
        
        if atraso > max_days:
            max_days = atraso
        
        # También revisar el mayor número de días vencido en la historia
        historia_pagos = credito.get('historicoPagos', '')
        if historia_pagos:
            # El historicoPagos puede tener formato como "00000001112" donde cada dígito
            # representa el estado en un mes (0=al corriente, 1=1-29 días, etc.)
            max_from_history = _extract_max_days_from_history(historia_pagos)
            if max_from_history > max_days:
                max_days = max_from_history
    
    return max_days


def _extract_max_days_from_history(historia: str) -> int:
    """
    Extrae el máximo de días de atraso del historial de pagos
    Formato típico: "00000001112" donde:
    0 = al corriente
    1 = 1-29 días
    2 = 30-59 días
    3 = 60-89 días
    4 = 90-119 días
    5 = 120-149 días
    """
    if not historia:
        return 0
    
    # Mapeo de códigos a días aproximados
    code_to_days = {
        '0': 0, '1': 15, '2': 45, '3': 75, 
        '4': 105, '5': 135, '6': 165, '7': 195
    }
    
    max_code = max(historia) if historia else '0'
    return code_to_days.get(max_code, 0)


def _count_open_performing_loans(creditos: List[Dict]) -> int:
    """
    Cuenta los créditos abiertos con buen desempeño (sin atrasos significativos)
    """
    count = 0
    
    for credito in creditos:
        # Verificar si el crédito está cerrado
        fecha_cierre = credito.get('fechaCierre')
        if fecha_cierre:
            continue  # Crédito cerrado, no contar
        
        # Verificar atraso
        atraso = _safe_int(credito.get('atrasoMayor', '0'), 0)
        
        # Considerar "performing" si tiene menos de 30 días de atraso
        if atraso < 30:
            count += 1
    
    return count


def _calculate_max_overdue_balance(creditos_financieros: List[Dict], 
                                   creditos_comerciales: List[Dict]) -> float:
    """
    Calcula el saldo vencido máximo en UDIs
    Nota: Asumimos que los saldos vienen en pesos y aplicamos una conversión aproximada
    """
    max_saldo_vencido = 0.0
    
    # Procesar créditos financieros
    for credito in creditos_financieros:
        # Sumar todos los saldos vencidos
        saldo_vencido_total = 0.0
        
        saldo_vencido_total += _safe_float(credito.get('saldoVencidoDe1a29Dias', '0'))
        saldo_vencido_total += _safe_float(credito.get('saldoVencidoDe30a59Dias', '0'))
        saldo_vencido_total += _safe_float(credito.get('saldoVencidoDe60a89Dias', '0'))
        saldo_vencido_total += _safe_float(credito.get('saldoVencidoDe90a119Dias', '0'))
        saldo_vencido_total += _safe_float(credito.get('saldoVencidoDe120a179Dias', '0'))
        saldo_vencido_total += _safe_float(credito.get('saldoVencidoDe180DiasOMas', '0'))
        
        if saldo_vencido_total > max_saldo_vencido:
            max_saldo_vencido = saldo_vencido_total
    
    # Procesar créditos comerciales
    for credito in creditos_comerciales:
        saldo_vencido = _safe_float(credito.get('saldoVencido', '0'))
        if saldo_vencido > max_saldo_vencido:
            max_saldo_vencido = saldo_vencido
    
    # Conversión aproximada a UDIs (1 UDI ≈ 7.5 MXN, puede variar)
    # En producción, deberías usar el valor real de UDI del día
    UDIS_PER_MXN = 1 / 7.5
    return max_saldo_vencido * UDIS_PER_MXN


def _count_open_credits(creditos: List[Dict]) -> int:
    """
    Cuenta el número total de créditos abiertos
    """
    count = 0
    
    for credito in creditos:
        fecha_cierre = credito.get('fechaCierre')
        if not fecha_cierre:  # No tiene fecha de cierre = está abierto
            count += 1
    
    return count


def _calculate_pct_open_12m(creditos: List[Dict]) -> float:
    """
    Calcula el porcentaje de créditos abiertos en los últimos 12 meses
    """
    from datetime import datetime, timedelta
    
    if not creditos:
        return 0.0
    
    fecha_limite = datetime.now() - timedelta(days=365)
    creditos_recientes = 0
    total_creditos_abiertos = 0
    
    for credito in creditos:
        # Solo considerar créditos abiertos
        fecha_cierre = credito.get('fechaCierre')
        if fecha_cierre:
            continue
        
        total_creditos_abiertos += 1
        
        # Verificar fecha de apertura
        fecha_apertura_str = credito.get('apertura', '')
        if fecha_apertura_str:
            try:
                # Intentar parsear diferentes formatos de fecha
                fecha_apertura = _parse_date(fecha_apertura_str)
                if fecha_apertura and fecha_apertura >= fecha_limite:
                    creditos_recientes += 1
            except:
                pass
    
    if total_creditos_abiertos == 0:
        return 0.0
    
    return (creditos_recientes / total_creditos_abiertos) * 100


def _parse_date(date_str: str) -> Optional[datetime]:
    """
    Intenta parsear una fecha en múltiples formatos comunes
    """
    if not date_str:
        return None
    
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%Y%m%d',
        '%d-%m-%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    return None


def _extract_observation_keys(creditos: List[Dict]) -> List[str]:
    """
    Extrae las claves de observación de los créditos
    """
    claves = []
    
    for credito in creditos:
        clave = credito.get('claveObservacion', '').strip()
        if clave and clave not in claves:
            claves.append(clave)
    
    return claves


def _calculate_max_approved_credit(creditos: List[Dict]) -> float:
    """
    Calcula el máximo crédito aprobado histórico
    """
    max_credito = 0.0
    
    for credito in creditos:
        # Revisar el crédito máximo utilizado
        credito_max = _safe_float(credito.get('creditoMaximoUtilizado', '0'))
        if credito_max > max_credito:
            max_credito = credito_max
        
        # También revisar el saldo inicial como posible monto aprobado
        saldo_inicial = _safe_float(credito.get('saldoInicial', '0'))
        if saldo_inicial > max_credito:
            max_credito = saldo_inicial
    
    return max_credito


# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo (estructura simplificada)
    example_data = {
        'summaryData': {
            'rfc': 'CDV14100WEDA',
            'lastYearNetIncome': -7219778.0,
            'lastYearTotalIncome': 19339633,
            'fiscalAddress': 'CALLE JOSE MARIA MORELOS 5, TLALNEPANTLA, MEXICO',
            'economicActivities': [
                {'name': 'Comercio al por mayor', 'percentage': 80}
            ]
        },
        'financialRatiosData': {
            'liquidity': {
                'current_ratio': {'2024': '1.3305483243873792'}
            },
            'leverage': {
                'total_debt_ratio': {'2024': '0.9173805946813605'}
            },
            'profitability': {
                'return_on_assets': {'2024': '0.8023060035397855'}
            }
        },
        'riskIndicatorsData': {
            'data': {
                'taxCompliance': {'risky': False},
                'blacklistedCounterparties': {'value': 0},
                'canceledIssuedInvoices': {'risky': False}
            }
        },
        'annualComparisonData': {
            'items': [
                {'period': '2019', 'netIncome': '1000000'},
                {'period': '2020', 'netIncome': '1100000'},
                {'period': '2021', 'netIncome': '1200000'},
                {'period': '2022', 'netIncome': '1300000'},
                {'period': '2023', 'netIncome': '1400000'},
                {'period': '2024', 'netIncome': '1350000'}
            ]
        },
        'buroReportData': {
            'Buro': [
                {
                    'id': 'buro-123',
                    'provider': 'Buro',
                    'score': '750',
                    'data': {
                        'score': [
                            {
                                'valorScore': '750',
                                'codigoScore': 'BC'
                            }
                        ],
                        'creditoFinanciero': [
                            {
                                'numeroCuenta': '1234567890',
                                'tipoCredito': 'SIMPLE',
                                'saldoInicial': '500000',
                                'saldoVigente': '350000',
                                'creditoMaximoUtilizado': '500000',
                                'atrasoMayor': '15',
                                'historicoPagos': '00000001110',
                                'apertura': '2023-01-15',
                                'saldoVencidoDe1a29Dias': '5000',
                                'saldoVencidoDe30a59Dias': '0',
                                'saldoVencidoDe60a89Dias': '0'
                            },
                            {
                                'numeroCuenta': '0987654321',
                                'tipoCredito': 'REVOLVENTE',
                                'saldoInicial': '200000',
                                'saldoVigente': '180000',
                                'creditoMaximoUtilizado': '200000',
                                'atrasoMayor': '0',
                                'historicoPagos': '000000000',
                                'apertura': '2024-06-01',
                                'fechaCierre': None
                            }
                        ],
                        'creditoComercial': [
                            {
                                'identificadorUsuario': 'PROVEEDOR-ABC',
                                'saldoTotal': '100000',
                                'saldoVencido': '2000',
                                'saldoVigente': '98000'
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    result = map_to_evaluate_request(example_data)
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))