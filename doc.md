# Documentación del Financial Mapping Controller

## Descripción General

El Financial Mapping Controller proporciona endpoints para mapear datos de métricas financieras obtenidos de la API de Syntage al formato EvaluateRequest utilizado por sistemas de evaluación crediticia.

## Endpoints Disponibles

### 1. POST `/map-to-evaluate-request`

**Descripción:** Mapea datos completos de métricas financieras al formato EvaluateRequest.

**Autenticación:** Requiere token de acceso válido en el header `Authorization`.

#### Payload Esperado

```json
{
  "invoicing_annual": {
    "hydra:member": [
      {
        "period": "2021",
        "totalIncome": "161227.35",
        "incomePaymentPending": "24206.10",
        "netIncome": "125267.06",
        "margin": "0.2955",
        "totalExpenses": "120439.39",
        "netExpenses": "88254.16",
        "profitOrLoss": "37012.90",
        "daysSalesOutstanding": "-1.33",
        "daysPayableOutstanding": "14.00"
      }
    ]
  },
  "financial_ratios": {
    "data": {
      "liquidity": {
        "current_ratio": {
          "2014": 2.170153630241602,
          "2020": 1.3305483243873792
        }
      },
      "leverage": {
        "debt_equity_ratio": {
          "2014": 0.836600142459244,
          "2020": 0.9173805946813605
        }
      },
      "profitability": {
        "return_on_assets": {
          "2014": 0.8909660418010791,
          "2020": 0.8023060035397855
        }
      }
    }
  },
  "risk_calculations": {
    "data": {
      "taxCompliance": {
        "value": "positive",
        "risky": false
      },
      "blacklistStatus": {
        "value": "clean",
        "risky": false
      },
      "blacklistedCounterparties": {
        "value": 4,
        "risky": true
      },
      "canceledIssuedInvoices": {
        "value": 0.1,
        "risky": true
      },
      "canceledReceivedInvoices": {
        "value": 0.1,
        "risky": true
      }
    }
  },
  "summary": {
    "value": {
      "rfc": "VAT115AP3",
      "name": "VARO",
      "fiscalAddress": "CALLE N, CIUDAD DE MEXICO",
      "fiscalAddressStatusRaw": null,
      "economicActivities": [
        {
          "name": "Sociedades financieras de objeto múltiple",
          "order": 1,
          "endDate": null,
          "startDate": "2019-05-15",
          "percentage": 100
        }
      ],
      "taxRegimes": [
        {
          "code": 601,
          "name": "General de Ley Personas Morales",
          "endDate": null,
          "startDate": "2019-05-15"
        }
      ],
      "totalEmployees": 0,
      "lastYearNetIncome": 5469207,
      "lastYearTotalIncome": 5469207,
      "totalRevenueLastTaxReturn": 5469207,
      "totalNetProfitLastTaxReturn": -7219778,
      "lastTaxReturnYear": 2024,
      "totalSalesRevenueCurrentYear": 4573274.79,
      "registrationDate": "2019-05-15T00:00:00.000000Z",
      "blacklistStatus": null,
      "lastEfirmaCertificate": null
    }
  },
  "credit_bureau_data": {
    "dias_atraso": 30,
    "num_open_performing_loan": 2,
    "saldo_vencido_maxic_udis": 50000.0,
    "creditos_abiertos": 3,
    "pct_open_12m": 0.75,
    "claves_observacion": ["01", "02"],
    "maximo_credito_aprobado_historico": 1000000.0
  },
  "geographic_data": {
    "estado": "CDMX",
    "domicilio_validado": true,
    "presencia_fisica": true,
    "scian": "522190"
  }
}
```

#### Campos Requeridos

- **invoicing_annual**: Datos anuales de facturación
- **financial_ratios**: Ratios financieros calculados
- **risk_calculations**: Cálculos de riesgo y compliance
- **summary**: Resumen con información fiscal y de la empresa

#### Campos Opcionales

- **credit_bureau_data**: Información del buró de crédito
- **geographic_data**: Datos geográficos adicionales

#### Respuesta Esperada

```json
{
  "fin": {
    "utilidad_neta_anual": -7219778.0,
    "razon_circulante": 1.3305483243873792,
    "apalancamiento_pct": 91.73805946813605,
    "rentabilidad": 0.8023060035397855,
    "anios_historial_ventas": 6,
    "gran_empresa": true,
    "crecimiento_ventas_ultimo_anio_pos": false
  },
  "ch": {
    "dias_atraso": 30,
    "num_open_performing_loan": 2,
    "saldo_vencido_maxic_udis": 50000.0,
    "creditos_abiertos": 3,
    "pct_open_12m": 0.75,
    "claves_observacion": ["01", "02"],
    "maximo_credito_aprobado_historico": 1000000.0
  },
  "comp": {
    "legal_ok": true,
    "pld_ok": true,
    "fiscal_ok": true,
    "peps_ok": null,
    "profeco_ok": null
  },
  "geo": {
    "estado": "CDMX",
    "domicilio_validado": true,
    "presencia_fisica": true,
    "scian": "522190"
  }
}
```

#### Descripción de Campos de Respuesta

##### FinData (fin)
- **utilidad_neta_anual**: Utilidad neta anual en pesos
- **razon_circulante**: Ratio de liquidez corriente
- **apalancamiento_pct**: Porcentaje de apalancamiento
- **rentabilidad**: Retorno sobre activos (ROA)
- **anios_historial_ventas**: Años de historial de ventas
- **gran_empresa**: Boolean indicando si es gran empresa (>1M ingresos)
- **crecimiento_ventas_ultimo_anio_pos**: Boolean indicando crecimiento positivo

##### ChData (ch) - Historial Crediticio
- **dias_atraso**: Días de atraso promedio
- **num_open_performing_loan**: Número de créditos abiertos funcionando
- **saldo_vencido_maxic_udis**: Saldo vencido máximo en UDIS
- **creditos_abiertos**: Número total de créditos abiertos
- **pct_open_12m**: Porcentaje de créditos abiertos en últimos 12 meses
- **claves_observacion**: Array de claves de observación
- **maximo_credito_aprobado_historico**: Máximo crédito aprobado históricamente

##### CompData (comp) - Cumplimiento
- **legal_ok**: Cumplimiento legal (basado en taxCompliance)
- **pld_ok**: Cumplimiento PLD (basado en contrapartes en lista negra)
- **fiscal_ok**: Cumplimiento fiscal (basado en facturas canceladas)
- **peps_ok**: Cumplimiento PEPs (no disponible - null)
- **profeco_ok**: Cumplimiento PROFECO (no disponible - null)

##### GeoData (geo) - Datos Geográficos
- **estado**: Estado de la República Mexicana
- **domicilio_validado**: Boolean indicando si el domicilio está validado
- **presencia_fisica**: Boolean indicando presencia física verificada
- **scian**: Código SCIAN de actividad económica

### 2. POST `/map-to-evaluate-request-by-ids`

**Descripción:** Endpoint preparado para obtener datos automáticamente usando IDs y realizar el mapping (funcionalidad futura).

#### Payload Esperado

```json
{
  "entity_id": "12345",
  "business_id": "67890",
  "credit_bureau_data": {
    "dias_atraso": 30,
    "num_open_performing_loan": 2,
    "saldo_vencido_maxic_udis": 50000.0,
    "creditos_abiertos": 3,
    "pct_open_12m": 0.75,
    "claves_observacion": ["01", "02"],
    "maximo_credito_aprobado_historico": 1000000.0
  },
  "geographic_data": {
    "estado": "CDMX",
    "domicilio_validado": true,
    "presencia_fisica": true,
    "scian": "522190"
  }
}
```

#### Respuesta Actual

```json
{
  "message": "Esta funcionalidad requiere integración con los endpoints existentes",
  "entity_id": "12345",
  "business_id": "67890",
  "note": "Use el endpoint /map-to-evaluate-request con datos completos por ahora"
}
```

## Códigos de Error

### 400 - Bad Request
- Falta algún campo requerido
- Error en el formato de los datos
- Error de validación en la función de mapping

### 401 - Unauthorized
- Token de acceso faltante o inválido

### 500 - Internal Server Error
- Error interno del servidor durante el procesamiento

## Ejemplo de Uso con cURL

```bash
curl -X POST "http://localhost:8000/map-to-evaluate-request" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "invoicing_annual": {
      "hydra:member": [
        {
          "period": "2021",
          "totalIncome": "161227.35",
          "netIncome": "125267.06",
          "profitOrLoss": "37012.90"
        }
      ]
    },
    "financial_ratios": {
      "data": {
        "liquidity": {
          "current_ratio": {"2020": 1.33}
        },
        "leverage": {
          "debt_equity_ratio": {"2020": 0.92}
        },
        "profitability": {
          "return_on_assets": {"2020": 0.80}
        }
      }
    },
    "risk_calculations": {
      "data": {
        "taxCompliance": {"value": "positive", "risky": false},
        "blacklistStatus": {"value": "clean", "risky": false},
        "blacklistedCounterparties": {"value": 4, "risky": true},
        "canceledIssuedInvoices": {"value": 0.1, "risky": true}
      }
    },
    "summary": {
      "value": {
        "rfc": "VAT115AP3",
        "name": "VARO",
        "fiscalAddress": "CALLE N, CIUDAD DE MEXICO",
        "lastYearNetIncome": 5469207,
        "totalNetProfitLastTaxReturn": -7219778,
        "totalSalesRevenueCurrentYear": 4573274.79,
        "registrationDate": "2019-05-15T00:00:00.000000Z"
      }
    }
  }'
```

## Obtención de Datos para el Mapping

Los datos requeridos pueden obtenerse de los siguientes endpoints existentes:

- **invoicing_annual**: `GET /invoicing-annual-comparison/{entity_id}`
- **financial_ratios**: `GET /financial-ratios/{business_id}`
- **risk_calculations**: `GET /risk-calculations/{business_id}`
- **summary**: `GET /summary/{entity_id}`

## Notas Importantes

1. **Autenticación**: Todos los endpoints requieren autenticación mediante token de acceso.

2. **Datos Opcionales**: Si no se proporcionan `credit_bureau_data` o `geographic_data`, los campos correspondientes en la respuesta tendrán valores `null` o por defecto.

3. **Validación de Datos**: La función de mapping incluye validaciones internas que pueden generar errores 400 si los datos no están en el formato esperado.

4. **Manejo de Fechas**: Las fechas deben estar en formato ISO 8601 (`2019-05-15T00:00:00.000000Z`).

5. **Valores Numéricos**: Los valores monetarios pueden estar como strings o números. La función de mapping maneja ambos formatos.

6. **Estados Geográficos**: El mapping automático de estados se basa en patrones comunes en direcciones fiscales mexicanas.