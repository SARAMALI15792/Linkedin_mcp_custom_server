import json
import httpx
from ..utils import get_headers, handle_api_error
from ..config import settings
from urllib.parse import quote

async def search_jobs(keywords: str, location: Optional[str] = None) -> str:
    """
    Search for jobs on LinkedIn.
    """
    try:
        headers = await get_headers()
        url = f"{settings.api_base}/jobSearch?q=search&keywords={quote(keywords)}"
        if location:
            url += f"&location={quote(location)}"
            
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return json.dumps(resp.json(), indent=2)
            
    except Exception as e:
        return handle_api_error(e)

async def get_job_details(job_urn: str) -> str:
    """
    Fetch details for a specific job posting.
    """
    try:
        headers = await get_headers()
        encoded_urn = quote(job_urn)
        url = f"{settings.api_base}/jobs/{encoded_urn}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return json.dumps(resp.json(), indent=2)
            
    except Exception as e:
        return handle_api_error(e)

from typing import Optional
