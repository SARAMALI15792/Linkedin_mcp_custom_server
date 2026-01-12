import httpx
from config import settings

async def get_oauth_url() -> str:
    """Generate the LinkedIn OAuth 2.0 authorization URL."""
    if not settings.linkedin_client_id:
        return "Error: LINKEDIN_CLIENT_ID not configured in .env"
        
    # Extended scopes for maximum functionality
    # openid, profile, email: Standard OIDC
    # w_member_social: Create posts
    # r_member_social: Read posts (often restricted, but we request it just in case)
    scope = "openid profile email w_member_social"
    
    # URL Encode scopes
    scope_encoded = scope.replace(" ", "%20")
    
    url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={settings.linkedin_client_id}"
        f"&redirect_uri={settings.linkedin_redirect_uri}"
        f"&scope={scope_encoded}"
    )
    
    return (
        f"# LinkedIn Authorization\n\n"
        f"1. [Click here to authorize]({url})\n"
        f"2. After login, copy the `code` parameter from the redirect URL.\n"
        f"3. Use the `linkedin_exchange_code` tool with that code."
    )

async def exchange_code(code: str) -> str:
    """Exchange authorization code for an access token."""
    if not settings.linkedin_client_id or not settings.linkedin_client_secret:
        return "Error: Missing client credentials (ID or Secret)."
        
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post("https://www.linkedin.com/oauth/v2/accessToken", data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.linkedin_redirect_uri,
                "client_id": settings.linkedin_client_id,
                "client_secret": settings.linkedin_client_secret
            })
            
            if resp.status_code != 200:
                return f"Error exchanging code: {resp.text}"
                
            token = resp.json().get("access_token")
            expires = resp.json().get("expires_in")
            
            # Save to .env
            env_path = ".env"
            lines = []
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    lines = f.readlines()
            
            with open(env_path, "w") as f:
                found = False
                for line in lines:
                    if line.startswith("LINKEDIN_ACCESS_TOKEN"):
                        f.write(f"LINKEDIN_ACCESS_TOKEN={token}\n")
                        found = True
                    else:
                        f.write(line)
                if not found:
                    f.write(f"\nLINKEDIN_ACCESS_TOKEN={token}")
                    
            return f"✅ Success! Access Token saved. Expires in {expires} seconds."
            
        except Exception as e:
            return f"Error: {str(e)}"
            
import os
