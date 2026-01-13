import json
import httpx
from ..utils import get_headers, handle_api_error
from ..config import settings
from urllib.parse import quote

async def search_people(keywords: str) -> str:
    """
    Search for people on LinkedIn by keywords.
    Note: Requires specific LinkedIn API permissions (e.g., r_basicprofile).
    """
    try:
        headers = await get_headers()
        # V2 people search is often restricted, but this is the standard endpoint
        url = f"{settings.api_base}/peopleSearch?q=keywords&keywords={quote(keywords)}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return json.dumps(resp.json(), indent=2)
            
    except Exception as e:
        return handle_api_error(e)

async def get_member_profile(member_urn: str) -> str:
    """
    Fetch a specific member's profile by their URN.
    Requires permission to view the member's profile.
    """
    try:
        headers = await get_headers()
        encoded_urn = quote(member_urn)
        url = f"{settings.api_base}/people/{encoded_urn}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return json.dumps(resp.json(), indent=2)
            
    except Exception as e:
        return handle_api_error(e)
