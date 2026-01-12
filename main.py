from fastmcp import FastMCP
from config import settings
from tools import auth, profile, post, company, search, job

# Initialize MCP Server
mcp = FastMCP("linkedin_custom_mcp")

# --- Authentication Tools ---

@mcp.tool(name="linkedin_get_oauth_url", annotations={"title": "Get LinkedIn Auth URL"})
async def linkedin_get_oauth_url() -> str:
    """Generate the LinkedIn OAuth 2.0 authorization URL for browser login."""
    return await auth.get_oauth_url()

@mcp.tool(name="linkedin_exchange_code", annotations={"title": "Exchange Auth Code"})
async def linkedin_exchange_code(code: str) -> str:
    """Exchange the browser-provided authorization code for a persistent access token."""
    return await auth.exchange_code(code)

# --- Profile Tools ---

@mcp.tool(name="linkedin_get_my_profile", annotations={"title": "Get My Profile"})
async def linkedin_get_my_profile() -> str:
    """Fetch the authenticated user's profile information (Name, Email, Picture)."""
    return await profile.get_my_profile()

@mcp.tool(name="linkedin_get_member_profile", annotations={"title": "Get Member Profile"})
async def linkedin_get_member_profile(member_urn: str) -> str:
    """Fetch a specific member's profile by their URN (e.g., 'urn:li:person:123')."""
    return await search.get_member_profile(member_urn)

# --- Post Tools ---

@mcp.tool(name="linkedin_create_post", annotations={"title": "Create Feed Post"})
async def linkedin_create_post(text: str, visibility: str = "PUBLIC") -> str:
    """
    Create a new text-based update on the user LinkedIn feed.
    Args:
        text: The content of the post.
        visibility: 'PUBLIC' or 'CONNECTIONS'.
    """
    params = post.PostParams(text=text, visibility=visibility)
    return await post.create_post(params)

@mcp.tool(name="linkedin_create_image_post", annotations={"title": "Create Image Post"})
async def linkedin_create_image_post(text: str, image_source: str, visibility: str = "PUBLIC") -> str:
    """
    Create a post with an image.
    Args:
        text: Post caption.
        image_source: Local file path or public URL of the image.
        visibility: 'PUBLIC' or 'CONNECTIONS'.
    """
    params = post.ImagePostParams(text=text, image_source=image_source, visibility=visibility)
    return await post.create_image_post(params)

@mcp.tool(name="linkedin_update_post", annotations={"title": "Update Post"})
async def linkedin_update_post(post_urn: str, text: str, visibility: str = "PUBLIC") -> str:
    """
    Update a post's text.
    ⚠️ Warning: This deletes the old post and creates a new one with a new ID,
    as LinkedIn does not support editing published posts via API.
    """
    params = post.UpdatePostParams(post_urn=post_urn, text=text, visibility=visibility)
    return await post.update_post(params)

@mcp.tool(name="linkedin_delete_post", annotations={"title": "Delete Post"})
async def linkedin_delete_post(post_urn: str) -> str:
    """Delete a LinkedIn post by its URN (e.g., 'urn:li:share:123')."""
    return await post.delete_post(post_urn)

@mcp.tool(name="linkedin_get_recent_posts", annotations={"title": "Get Recent Posts"})
async def linkedin_get_recent_posts() -> str:
    """List the user's recent posts (Requires 'r_member_social' permission)."""
    return await post.get_recent_posts()

@mcp.tool(name="linkedin_create_comment", annotations={"title": "Create Comment"})
async def linkedin_create_comment(object_urn: str, text: str) -> str:
    """
    Create a comment on a LinkedIn share, article, or video.
    Args:
        object_urn: The URN of the content to comment on (e.g., 'urn:li:share:123').
        text: The text of the comment.
    """
    params = post.CommentParams(object_urn=object_urn, text=text)
    return await post.create_comment(params)

@mcp.tool(name="linkedin_get_post_comments", annotations={"title": "Get Comments"})
async def linkedin_get_post_comments(object_urn: str) -> str:
    """Get comments for a specific post/share."""
    return await post.get_post_comments(object_urn)

@mcp.tool(name="linkedin_delete_comment", annotations={"title": "Delete Comment"})
async def linkedin_delete_comment(comment_urn: str, object_urn: str) -> str:
    """
    Delete a specific comment.
    Args:
        comment_urn: The URN of the comment to delete.
        object_urn: The URN of the parent post/object.
    """
    return await post.delete_comment(comment_urn, object_urn)

# --- Company Tools ---

@mcp.tool(name="linkedin_get_company_profile", annotations={"title": "Get Company Profile"})
async def linkedin_get_company_profile(company_urn: str) -> str:
    """Fetch a company's profile information by its URN (e.g., 'urn:li:organization:123')."""
    return await company.get_company_profile(company_urn)

@mcp.tool(name="linkedin_search_companies", annotations={"title": "Search Companies"})
async def linkedin_search_companies(keywords: str) -> str:
    """Search for companies on LinkedIn by keywords."""
    return await company.search_companies(keywords)

# --- Job Tools ---

@mcp.tool(name="linkedin_search_jobs", annotations={"title": "Search Jobs"})
async def linkedin_search_jobs(keywords: str, location: str = None) -> str:
    """Search for jobs on LinkedIn by keywords and optional location."""
    return await job.search_jobs(keywords, location)

@mcp.tool(name="linkedin_get_job_details", annotations={"title": "Get Job Details"})
async def linkedin_get_job_details(job_urn: str) -> str:
    """Fetch details for a specific job posting by its URN."""
    return await job.get_job_details(job_urn)

# --- Search Tools ---

@mcp.tool(name="linkedin_search_people", annotations={"title": "Search People"})
async def linkedin_search_people(keywords: str) -> str:
    """Search for people on LinkedIn by keywords."""
    return await search.search_people(keywords)

# --- Main Entry Point ---

def main():
    print(f"LinkedIn MCP Server | {settings.server_host}:{settings.server_port}")
    mcp.run(transport="sse", host=settings.server_host, port=settings.server_port)

if __name__ == "__main__":
    main()
