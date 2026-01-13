import json
import httpx
from ..utils import get_headers, handle_api_error
from ..config import settings
from urllib.parse import quote

async def get_company_profile(company_urn: str) -> str:
    """
    Fetch a company's profile information by its URN.
    Example URN: 'urn:li:organization:12345'
    """
    try:
        headers = await get_headers()
        # The URN must be URL encoded
        encoded_urn = quote(company_urn)
        url = f"{settings.api_base}/organizations/{encoded_urn}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return json.dumps(resp.json(), indent=2)
            
    except Exception as e:
        return handle_api_error(e)

async def search_companies(keywords: str) -> str:
    """
    Search for companies by keywords.
    Note: This often requires specialized LinkedIn Marketing permissions.
    """
    try:
        headers = await get_headers()
        # Standard search endpoint
        url = f"{settings.api_base}/companySearch?q=search&keywords={quote(keywords)}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return json.dumps(resp.json(), indent=2)
            
    except Exception as e:
        return handle_api_error(e)
