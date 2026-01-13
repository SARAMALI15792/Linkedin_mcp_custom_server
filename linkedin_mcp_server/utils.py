import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from .config import settings

async def get_headers() -> Dict[str, str]:
    """Retrieve and format headers for LinkedIn API requests."""
    token = settings.linkedin_access_token
    # Reload .env if token is missing (in case it was just updated)
    if not token:
        load_dotenv()
        token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not token:
        raise ValueError("LinkedIn Access Token missing. Please use the auth tools to login first.")
        
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

def handle_api_error(e: Exception) -> str:
    """Standardized error handling for API calls."""
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        try:
            error_details = e.response.json()
            message = error_details.get("message", e.response.text)
        except:
            message = e.response.text
            
        if status == 401:
            return "Error: Unauthorized (401). Your access token might be invalid or expired. Please re-authenticate."
        if status == 403:
            return f"Error: Forbidden (403). You lack permissions for this action. Message: {message}"
        if status == 429:
            return "Error: Rate limit exceeded. Please wait a moment."
            
        return f"Error: API request failed ({status}): {message}"
        
    return f"Error: {str(e)}"
