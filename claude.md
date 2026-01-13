# LinkedIn MCP Server - Claude Integration Guide

## Overview

This is a Model Context Protocol (MCP) server that enables Claude to interact with LinkedIn's professional network through authenticated API calls. The server provides tools for content creation, profile management, job search, company research, and professional networking.

## Architecture

### Technology Stack
- **Framework**: FastMCP (Python-based MCP server framework)
- **HTTP Client**: httpx for async API calls
- **Authentication**: OAuth 2.0 with PKCE flow
- **Configuration**: pydantic-settings with environment variables
- **Python Version**: 3.10+

### Project Structure

```
linkedin_custom_mcp/
├── linkedin_mcp_server/         # Main package
│   ├── __init__.py              # Package exports and version
│   ├── __main__.py              # CLI entry point
│   ├── server.py                # MCP tool definitions (18 tools)
│   ├── config.py                # Configuration management
│   ├── utils.py                 # Shared utilities (HTTP client)
│   └── tools/                   # Tool implementation modules
│       ├── auth.py              # OAuth 2.0 authentication flow
│       ├── profile.py           # User profile operations
│       ├── post.py              # Post creation, updates, comments
│       ├── company.py           # Company search and profiles
│       ├── job.py               # Job search and details
│       └── search.py            # People search functionality
├── pyproject.toml               # Package configuration
├── README.md                    # User-facing documentation
├── claude.md                    # This file - Claude integration guide
├── LICENSE                      # MIT License
├── get_profile.py               # Example standalone script
└── requirements.txt             # Direct dependencies
```

## Core Components

### 1. Authentication System (tools/auth.py)

Implements OAuth 2.0 authorization code flow:
- **get_oauth_url()**: Generates authorization URL with required scopes
- **exchange_code(code)**: Exchanges auth code for access token, saves to .env

**Scopes Requested:**
- `openid`, `profile`, `email`: Basic profile access
- `w_member_social`: Create posts and comments

**Token Management:**
- Tokens stored in `.env` file as `LINKEDIN_ACCESS_TOKEN`
- Tokens expire (LinkedIn controls expiration time)
- No automatic refresh implemented (requires re-authentication)

### 2. Profile Operations (tools/profile.py)

- **get_my_profile()**: Retrieves authenticated user's profile (sub, name, email, picture)
- **get_member_profile(urn)**: Gets member profile by URN (restricted access)

**API Endpoints:**
- `/v2/userinfo` (OpenID Connect)
- `/v2/people/(id:...)` (restricted)

### 3. Content Management (tools/post.py)

**Posts:**
- **create_post(text)**: Create text-only post
- **create_image_post(text, image_path)**: Create post with image upload
- **update_post(urn, text)**: Delete old post, create new one (no native update API)
- **delete_post(urn)**: Permanently delete post
- **get_recent_posts(author, count)**: List posts (requires `r_member_social` - often unavailable)

**Comments:**
- **create_comment(parent_urn, text)**: Comment on posts
- **get_post_comments(urn)**: Get comments on post
- **delete_comment(urn)**: Delete comment

**Key Concepts:**
- URNs (Uniform Resource Names): LinkedIn's resource identifiers
- UGC (User Generated Content): API for post creation
- Image upload requires multi-step process: register upload → upload binary → create post

### 4. Company Operations (tools/company.py)

- **search_companies(keywords)**: Search for companies by name/keywords
- **get_company_profile(urn)**: Get detailed company information

**Note:** May require Marketing Developer Platform access

### 5. Job Search (tools/job.py)

- **search_jobs(keywords, location)**: Search job postings
- **get_job_details(urn)**: Get detailed job information

**Note:** May require Talent Solutions access

### 6. People Search (tools/search.py)

- **search_people(keywords)**: Search for professionals on LinkedIn

**Note:** May require Marketing Developer Platform access

## Tool Annotations

All tools use FastMCP annotations for better Claude integration:

```python
annotations = {
    "title": "Human-readable tool name",
    "readOnlyHint": True/False,          # Does it modify data?
    "destructiveHint": True/False,       # Can it delete data?
    "idempotentHint": True/False,        # Same result when called multiple times?
    "openWorldHint": True/False          # Makes external API calls?
}
```

## Configuration

### Environment Variables (.env)

```ini
LINKEDIN_CLIENT_ID=your_app_client_id
LINKEDIN_CLIENT_SECRET=your_app_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000
LINKEDIN_ACCESS_TOKEN=automatically_set_after_auth
```

### LinkedIn App Requirements

1. Create app at https://www.linkedin.com/developers/apps
2. Request products:
   - "Sign In with LinkedIn using OpenID Connect" (approved automatically)
   - "Share on LinkedIn" (approved automatically)
   - "Marketing Developer Platform" (restricted - requires approval)
   - "Talent Solutions" (restricted - requires approval)
3. Add redirect URL: `http://localhost:8000`

## API Limitations

### Available Operations
- Create posts (text and images)
- Create comments
- Get own profile (OpenID Connect)
- Delete own posts and comments

### Restricted Operations (May Not Work)
- Read posts (requires `r_member_social` - rarely granted)
- Search people (requires Marketing API)
- Search companies (requires Marketing API)
- Search jobs (requires Talent API)
- Get other members' profiles (restricted)

**Why?** LinkedIn restricts most read APIs to protect user privacy and limit third-party access.

## Common Use Cases for Claude

### 1. Content Publishing
```
User: "Post to LinkedIn: Just launched our new feature!"
Claude: Uses linkedin_create_post(text="...")
```

### 2. Image Posts
```
User: "Post this screenshot to LinkedIn with caption: New UI design"
Claude: Uses linkedin_create_image_post(text="...", image_path="...")
```

### 3. Engagement
```
User: "Comment on this post: urn:li:share:123456"
Claude: Uses linkedin_create_comment(parent_urn="...", text="Great post!")
```

### 4. Profile Information
```
User: "What's my LinkedIn email?"
Claude: Uses linkedin_get_my_profile() → extracts email
```

### 5. Authentication Setup
```
User: "Help me connect to LinkedIn"
Claude:
  1. Uses linkedin_get_oauth_url() → provides URL
  2. Waits for user to authorize and paste code
  3. Uses linkedin_exchange_code(code="...") → saves token
```

## Error Handling

### Common Errors

1. **401 Unauthorized**
   - Cause: Token expired or invalid
   - Solution: Re-authenticate using OAuth flow

2. **403 Forbidden**
   - Cause: Missing required permission/product
   - Solution: Check LinkedIn app products and permissions

3. **404 Not Found**
   - Cause: Invalid URN or resource doesn't exist
   - Solution: Verify URN format and resource existence

4. **422 Unprocessable Entity**
   - Cause: Invalid request format or missing required fields
   - Solution: Check API documentation and required parameters

### Error Handling Strategy

All tools return user-friendly error messages:
```python
try:
    response = await client.get(...)
    return response.json()
except Exception as e:
    return f"Error: {str(e)}"
```

## Security Considerations

1. **Token Storage**: Access tokens stored in `.env` file (excluded from git)
2. **OAuth Flow**: Uses authorization code flow (more secure than implicit)
3. **Scope Limitation**: Only requests minimum required scopes
4. **No Token Refresh**: Tokens expire and require manual re-authentication

## Development and Testing

### Running Locally

```bash
# Install in development mode
pip install -e .

# Run server directly
python -m linkedin_mcp_server

# Or use entry point
linkedin-mcp-server
```

### Testing with Claude Desktop

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp-server"
    }
  }
}
```

### Debugging

1. **Check logs**: Claude Desktop logs show MCP communication
2. **Test tools individually**: Use `get_profile.py` as example
3. **Verify .env**: Ensure all credentials are set correctly
4. **Check LinkedIn API status**: https://www.linkedin-apistatus.com/

## Future Enhancements

### Potential Improvements
- Token refresh flow (requires refresh token support)
- Webhook support for real-time notifications
- Analytics and insights (if API access granted)
- Connection management (if API access granted)
- Message sending (requires Messaging API product)

### Current Limitations
- No pagination for search results
- No bulk operations
- Limited read access due to LinkedIn restrictions
- No real-time data updates

## Useful Resources

- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **LinkedIn API Docs**: https://learn.microsoft.com/en-us/linkedin/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **OAuth 2.0 Spec**: https://oauth.net/2/

## Troubleshooting Guide for Claude

### Issue: Authentication Fails
**Check:**
1. `.env` file exists with valid CLIENT_ID and CLIENT_SECRET
2. Redirect URI matches LinkedIn app configuration
3. User completed browser authorization
4. Authorization code not expired (use immediately)

### Issue: 403 Errors on Operations
**Check:**
1. LinkedIn app has required products enabled
2. User granted requested scopes during OAuth
3. Access token is still valid
4. Operation doesn't require restricted permission

### Issue: Search Tools Don't Work
**Explanation:** Search APIs require Marketing/Talent products which are restricted
**Solution:** Focus on available operations (posts, comments, profile)

### Issue: Can't Read User's Posts
**Explanation:** `r_member_social` permission rarely granted to third-party apps
**Solution:** Use write operations instead (create posts, comments)

## Version History

- **1.0.0**: Initial release with core functionality
  - OAuth 2.0 authentication
  - Post creation (text and images)
  - Comment management
  - Profile access
  - Company/job/people search (limited availability)

## Author Information

**SARAM ALI**
- Email: saramali15792@gmail.com
- GitHub: [@SARAMALI15792](https://github.com/SARAMALI15792)
- Project: https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server

---

**For Claude:** This server enables you to help users publish content to LinkedIn, engage with their network, and access their profile information. Always check token validity first, guide users through OAuth if needed, and provide clear feedback on API limitations when certain operations fail.
