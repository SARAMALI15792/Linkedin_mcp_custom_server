import json
import httpx
import os
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict
from utils import get_headers, handle_api_error
from config import settings
from urllib.parse import quote

# --- Models ---

class PostParams(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    text: str = Field(..., description="The commentary/text content of the post.")
    visibility: str = Field(default="PUBLIC", description="Post visibility: PUBLIC or CONNECTIONS.")

class ImagePostParams(BaseModel):
    text: str = Field(..., description="The text content.")
    image_source: str = Field(..., description="Local file path or public URL of the image.")
    visibility: str = Field(default="PUBLIC")

class CommentParams(BaseModel):
    object_urn: str = Field(..., description="The URN of the post/share to comment on (e.g., urn:li:share:123)")
    text: str = Field(..., description="The text content of the comment.")

class UpdatePostParams(BaseModel):
    post_urn: str = Field(..., description="The URN of the post to update.")
    text: str = Field(..., description="The new text content.")
    visibility: str = Field(default="PUBLIC", description="Visibility for the new post: PUBLIC or CONNECTIONS.")

# --- Helper: Image Upload ---

async def upload_image(client: httpx.AsyncClient, headers: dict, person_urn: str, image_source: str) -> str:
    """
    Handles the 3-step image upload process:
    1. Register Upload -> Get upload URL and Asset URN.
    2. Upload Image Binary.
    3. Return Asset URN.
    """
    # Step 1: Register
    reg_url = f"{settings.api_base}/assets?action=registerUpload"
    reg_body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
        }
    }
    
    reg_resp = await client.post(reg_url, headers=headers, json=reg_body)
    reg_resp.raise_for_status()
    reg_data = reg_resp.json()
    
    upload_url = reg_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_urn = reg_data['value']['asset']
    
    # Step 2: Get Image Data
    if image_source.startswith("http"):
        # Download from URL
        img_resp = await client.get(image_source)
        img_resp.raise_for_status()
        image_data = img_resp.content
    else:
        # Read from local file
        if not os.path.exists(image_source):
            raise FileNotFoundError(f"Image file not found: {image_source}")
        with open(image_source, "rb") as f:
            image_data = f.read()
            
    # Step 3: Upload Binary
    # Use the same token for upload if required, though typically it's a signed URL
    upload_headers = {"Authorization": headers["Authorization"]}
    upload_resp = await client.put(upload_url, headers=upload_headers, content=image_data)
    upload_resp.raise_for_status()
    
    return asset_urn

# --- Post Implementation ---

async def create_image_post(params: ImagePostParams) -> str:
    """Create a post with an image."""
    try:
        headers = await get_headers()
        async with httpx.AsyncClient() as client:
            # 1. Get User ID
            user_resp = await client.get(f"{settings.api_base}/userinfo", headers=headers)
            user_resp.raise_for_status()
            person_id = user_resp.json().get("sub")
            author_urn = f"urn:li:person:{person_id}"
            
            # 2. Upload Image
            asset_urn = await upload_image(client, headers, author_urn, params.image_source)
            
            # 3. Create Post
            payload = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {"com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": params.text},
                    "shareMediaCategory": "IMAGE",
                    "media": [{
                        "status": "READY",
                        "description": {"text": "Image"},
                        "media": asset_urn,
                        "title": {"text": "Image Post"}
                    }]
                }},
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": params.visibility}
            }
            
            resp = await client.post(f"{settings.api_base}/ugcPosts", headers=headers, json=payload)
            resp.raise_for_status()
            
            post_id = resp.json().get("id")
            return f"✅ Image Post created successfully.\nID: {post_id}"

    except Exception as e:
        return handle_api_error(e)

async def create_post(params: PostParams) -> str:
    """Create a new text-based update on the user LinkedIn feed."""
    try:
        headers = await get_headers()
        async with httpx.AsyncClient() as client:
            # 1. Get User ID (sub) to construct Author URN
            user_resp = await client.get(f"{settings.api_base}/userinfo", headers=headers)
            user_resp.raise_for_status()
            person_id = user_resp.json().get("sub")
            author = f"urn:li:person:{person_id}"

            # 2. Construct Payload
            payload = {
                "author": author, 
                "lifecycleState": "PUBLISHED",
                "specificContent": {"com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": params.text}, 
                    "shareMediaCategory": "NONE"
                }},
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": params.visibility}
            }
            
            # 3. Send Request
            resp = await client.post(f"{settings.api_base}/ugcPosts", headers=headers, json=payload)
            resp.raise_for_status()
            
            post_id = resp.json().get("id")
            return f"✅ Post created successfully.\nID: {post_id}"
            
    except Exception as e:
        return handle_api_error(e)

async def update_post(params: UpdatePostParams) -> str:
    """
    Update a post by deleting the old one and creating a new one.
    (LinkedIn API does not support direct text edits).
    """
    try:
        # 1. Delete the old post
        delete_result = await delete_post(params.post_urn)
        
        if "Error" in delete_result:
            return f"Update Failed during deletion step: {delete_result}"
            
        # 2. Create the new post
        create_params = PostParams(text=params.text, visibility=params.visibility)
        create_result = await create_post(create_params)
        
        if "Error" in create_result:
            return f"⚠️ Old post deleted, but creation failed: {create_result}"
            
        return f"✅ Post updated (Re-created).\nOld ID: {params.post_urn}\n{create_result}"

    except Exception as e:
        return handle_api_error(e)

async def delete_post(post_urn: str) -> str:
    """Delete a LinkedIn post by its URN."""
    try:
        headers = await get_headers()
        # Ensure URN is URL encoded for the path
        encoded_urn = quote(post_urn)
        
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{settings.api_base}/ugcPosts/{encoded_urn}", headers=headers)
            
            if resp.status_code == 404:
                return f"Error: Post {post_urn} not found."
                
            resp.raise_for_status()
            return f"✅ Post {post_urn} deleted successfully."
            
    except Exception as e:
        return handle_api_error(e)

async def get_recent_posts() -> str:
    """
    List the user's recent posts. 
    Note: Requires 'r_member_social' permission which is often restricted.
    """
    try:
        headers = await get_headers()
        async with httpx.AsyncClient() as client:
            # 1. Get Author URN
            user_resp = await client.get(f"{settings.api_base}/userinfo", headers=headers)
            user_resp.raise_for_status()
            person_id = user_resp.json().get("sub")
            author_urn = f"urn:li:person:{person_id}"
            
            # 2. Search
            encoded_author = quote(author_urn)
            url = f"{settings.api_base}/ugcPosts?q=authors&authors=List({encoded_author})"
            
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            
            data = resp.json()
            posts = []
            for item in data.get("elements", []):
                # Extract text
                content = item.get("specificContent", {}).get("com.linkedin.ugc.ShareContent", {})
                text = content.get("shareCommentary", {}).get("text", "")
                
                posts.append({
                    "id": item.get("id"),
                    "text": text,
                    "created": item.get("created", {}).get("time"),
                    "visibility": item.get("visibility", {}).get("com.linkedin.ugc.MemberNetworkVisibility")
                })
            
            return json.dumps(posts, indent=2)
            
    except Exception as e:
        return handle_api_error(e)

# --- Comment Implementation ---

async def create_comment(params: CommentParams) -> str:
    """Create a comment on a share, UGC post, or article."""
    try:
        headers = await get_headers()
        async with httpx.AsyncClient() as client:
            # 1. Get User ID
            user_resp = await client.get(f"{settings.api_base}/userinfo", headers=headers)
            user_resp.raise_for_status()
            person_id = user_resp.json().get("sub")
            actor_urn = f"urn:li:person:{person_id}"
            
            # 2. Payload
            # LinkedIn Social Actions API uses 'socialActions' endpoint
            # Path: /socialActions/{objectUrn}/comments
            encoded_object = quote(params.object_urn)
            url = f"{settings.api_base}/socialActions/{encoded_object}/comments"
            
            payload = {
                "actor": actor_urn,
                "message": {
                    "text": params.text
                }
            }
            
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            
            comment_id = resp.json().get("id")
            return f"✅ Comment created successfully.\nID: {comment_id}"
            
    except Exception as e:
        return handle_api_error(e)

async def get_post_comments(object_urn: str) -> str:
    """Get comments for a specific post/share."""
    try:
        headers = await get_headers()
        encoded_object = quote(object_urn)
        url = f"{settings.api_base}/socialActions/{encoded_object}/comments"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            
            data = resp.json()
            comments = []
            for item in data.get("elements", []):
                comments.append({
                    "id": item.get("id"),
                    "actor": item.get("actor"),
                    "text": item.get("message", {}).get("text"),
                    "created": item.get("created", {}).get("time")
                })
            return json.dumps(comments, indent=2)
            
    except Exception as e:
        return handle_api_error(e)

async def delete_comment(comment_urn: str, object_urn: str) -> str:
    """
    Delete a comment. 
    Note: Requires the parent object URN as well for the endpoint context in some versions, 
    or direct access via ID. The standard Social Actions API is:
    DELETE /socialActions/{objectUrn}/comments/{commentId}
    """
    try:
        headers = await get_headers()
        
        # We need to extract the ID from the Comment URN if passed fully
        # Comment URN format often: urn:li:comment:(urn:li:share:123, 456)
        # But the API expects the call on the Object.
        # User should provide Object URN and Comment ID ideally.
        # For simplicity, we ask for both or try to parse.
        
        encoded_object = quote(object_urn)
        # Extract numeric ID if a full URN is passed, or use as is
        comment_id = comment_urn.split(",")[-1].replace(")", "") if "(" in comment_urn else comment_urn
        encoded_comment_id = quote(comment_id)
        
        url = f"{settings.api_base}/socialActions/{encoded_object}/comments/{encoded_comment_id}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.delete(url, headers=headers)
            if resp.status_code == 404:
                return "Error: Comment or Object not found."
            resp.raise_for_status()
            return "✅ Comment deleted successfully."
            
    except Exception as e:
        return handle_api_error(e)

