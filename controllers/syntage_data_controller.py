import os
from fastapi import APIRouter, HTTPException, Body, Form
import httpx
from .cacheController import cache

# Crear el enrutador para las rutas de la API
router = APIRouter()


@router.get("/invoicing-annual-comparison/{entity_id}")
async def get_invoicing_annual_comparison(entity_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        url = f"https://api.sandbox.syntage.com/entities/{entity_id}/insights/metrics/invoicing-annual-comparison"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


# Endpoint para obtener financial ratios
@router.get("/financial-ratios/{business_id}")
async def get_financial_ratios(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        url = f"https://api.sandbox.syntage.com/insights/{business_id}/financial-ratios"
        headers = {"X-API-Key": api_key}
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/vendor-network-insight/{entity_id}")
async def get_vendor_network_insight(entity_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        url = f"https://api.sandbox.syntage.com/entities/{entity_id}/insights/metrics/vendor-network"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/customer-network-insight/{entity_id}")
async def get_customer_network_insight(entity_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        url = f"https://api.sandbox.syntage.com/entities/{entity_id}/insights/metrics/customer-network"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/customer-invoice-concentration/{entity_id}")
async def get_customer_invoice_concentration(entity_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        url = f"https://api.sandbox.syntage.com/insights/{entity_id}/customer-concentration"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


# Nuevo endpoint para obtener instituciones financieras
@router.get("/financial-institutions/{business_id}")
async def get_financial_institutions(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.syntage.com/insights/{business_id}/financial-institutions"
        headers = {"X-API-Key": api_key}

        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/supplier-invoice-concentration/{business_id}")
async def get_supplier_invoice_concentration(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.sandbox.syntage.com/insights/{business_id}/supplier-concentration"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/employees/{business_id}")
async def get_employees(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.sandbox.syntage.com/insights/{business_id}/employees"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/expenditures/{business_id}")
async def get_expenditures(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        url = f"https://api.sandbox.syntage.com/insights/{business_id}/expenditures"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


@router.get("/government-customers/{business_id}")
async def get_government_customers(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.sandbox.syntage.com/insights/{business_id}/government-customers"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    
@router.get("/invoicing-blacklist/{business_id}")
async def get_invoicing_blacklist(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.sandbox.syntage.com/insights/{business_id}/invoicing-blacklist"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    
@router.get("/risk-calculations/{business_id}")
async def get_risks(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.sandbox.syntage.com/insights/{business_id}/risks"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    
@router.get("/sales-revenue/{business_id}")
async def get_sales_revenue(business_id: str):
    try:
        api_key = os.getenv("SYNTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = f"https://api.sandbox.syntage.com/insights/{business_id}/sales-revenue"
        headers = {"X-API-Key": api_key}
        
        # Verificar cache
        cached_data = cache.get(url)
        if cached_data is not None:
            return cached_data
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Cachear la respuesta
            cache.set(url, data)
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from external API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")