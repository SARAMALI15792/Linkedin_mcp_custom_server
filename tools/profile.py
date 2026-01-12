import json
import httpx
from utils import get_headers, handle_api_error
from config import settings

async def get_my_profile(params=None) -> str:
    """
    Fetch the authenticated user's profile information.
    Uses OIDC UserInfo endpoint for reliable access to Name, Email, and Photo.
    """
    try:
        headers = await get_headers()
        async with httpx.AsyncClient() as client:
            # Use OpenID Connect userinfo endpoint
            response = await client.get(f"{settings.api_base}/userinfo", headers=headers, timeout=30.0)
            response.raise_for_status()
            user_info = response.json()
            
            # Map standard OIDC fields to a friendly format
            profile = {
                "id": user_info.get("sub"),
                "name": user_info.get("name"),
                "given_name": user_info.get("given_name"),
                "family_name": user_info.get("family_name"),
                "email": user_info.get("email"),
                "email_verified": user_info.get("email_verified"),
                "picture": user_info.get("picture"),
                "locale": user_info.get("locale")
            }
            return json.dumps(profile, indent=2)
            
    except Exception as e:
        return handle_api_error(e)
