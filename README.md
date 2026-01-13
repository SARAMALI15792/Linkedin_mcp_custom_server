# LinkedIn MCP Server

[![PyPI version](https://badge.fury.io/py/linkedin-mcp-server.svg)](https://badge.fury.io/py/linkedin-mcp-server)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Model Context Protocol (MCP) server that enables AI agents like Claude to interact seamlessly with LinkedIn's professional network. Built with [FastMCP](https://github.com/jlowin/fastmcp) for high performance and reliability.

## What is This?

This MCP server bridges the gap between AI assistants and LinkedIn, allowing them to:
- Create and manage LinkedIn posts with text and images
- Comment on posts and engage with content
- Access profile information
- Search for companies, jobs, and people
- Automate LinkedIn interactions through natural language

Perfect for professionals who want to leverage AI to manage their LinkedIn presence efficiently.

## Features

### Core Capabilities
- **Secure Authentication** - OAuth 2.0 flow with access token management
- **Content Creation** - Publish text posts and image posts
- **Content Management** - Update and delete posts
- **Engagement** - Comment on posts and manage comments
- **Profile Access** - Retrieve authenticated user profile information
- **Company Intelligence** - Search and view company profiles
- **Job Discovery** - Search job postings and view details
- **People Search** - Find professionals on LinkedIn

### Built With
- **FastMCP** - Modern Python MCP framework
- **httpx** - Async HTTP client for API calls
- **Pydantic** - Data validation and settings management
- **OAuth 2.0** - Industry-standard authentication

## Installation

### Option 1: Using uvx (Recommended)

The fastest way to get started:

```bash
uvx linkedin-mcp-server
```

### Option 2: Using pip

Install from PyPI:

```bash
pip install linkedin-mcp-server
```

### Option 3: From Source

For development or customization:

```bash
git clone https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server.git
cd LinkedIn_mcp_custom_server
pip install -e .
```

## Quick Start Guide

### Step 1: Create LinkedIn App

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Click "Create app"
3. Fill in required information:
   - App name: Choose a descriptive name
   - LinkedIn Page: Associate with your page or create one
   - App logo: Upload a logo (optional but recommended)
4. Request access to these products:
   - **Sign In with LinkedIn using OpenID Connect** (instant approval)
   - **Share on LinkedIn** (instant approval)
5. In the "Auth" tab:
   - Add Redirect URL: `http://localhost:8000`
   - Copy your **Client ID**
   - Copy your **Client Secret**

### Step 2: Configure Environment

Create a `.env` file in your working directory:

```ini
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000
```

**Security Note:** Never commit the `.env` file to version control. It's already in `.gitignore`.

### Step 3: Configure Claude Desktop

Edit your Claude Desktop configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

Add the LinkedIn MCP server:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["linkedin-mcp-server"]
    }
  }
}
```

**If installed via pip:**

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp-server"
    }
  }
}
```

**For local development:**

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "python",
      "args": ["-m", "linkedin_mcp_server"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_client_secret",
        "LINKEDIN_REDIRECT_URI": "http://localhost:8000"
      }
    }
  }
}
```

### Step 4: Authenticate with LinkedIn

1. Restart Claude Desktop
2. In Claude, type: **"Generate LinkedIn login URL"**
3. Copy and open the URL in your browser
4. Sign in to LinkedIn and authorize the application
5. You'll be redirected to `http://localhost:8000/?code=...`
6. Copy the `code` parameter value from the URL
7. In Claude, type: **"Exchange this code: [paste the code]"**
8. Done! You're now authenticated.

**Your access token is automatically saved to `.env` and will be used for all future requests.**

## Usage Examples

### Authentication

```
User: "Generate LinkedIn login URL"
Claude: [Provides OAuth URL with instructions]

User: "Exchange this code: AQTvqXXXXXXXXXXX"
Claude: "Success! Access Token saved. Expires in 5183999 seconds."
```

### Creating Posts

**Text Post:**
```
User: "Post to LinkedIn: Excited to announce the launch of our new AI-powered LinkedIn MCP server! Check it out on GitHub."
Claude: [Creates post and returns post URN]
```

**Post with Image:**
```
User: "Post this image to LinkedIn with caption 'Team celebration': C:/Users/photos/team.jpg"
Claude: [Uploads image and creates post with caption]
```

### Managing Content

**Update a Post:**
```
User: "Update post urn:li:share:7289123456789 to say: Updated announcement..."
Claude: [Deletes old post and creates new one with updated text]
```

**Delete a Post:**
```
User: "Delete my post urn:li:share:7289123456789"
Claude: [Deletes the post permanently]
```

### Engagement

**Comment on Posts:**
```
User: "Comment on post urn:li:share:7289123456789: Great insights, thanks for sharing!"
Claude: [Posts comment and returns comment URN]
```

**View Comments:**
```
User: "Show comments on post urn:li:share:7289123456789"
Claude: [Retrieves and displays all comments]
```

### Profile Information

```
User: "What's my LinkedIn email address?"
Claude: [Retrieves profile and shows email]

User: "Show me my LinkedIn profile"
Claude: [Displays profile information: name, email, picture URL, etc.]
```

### Company Research

```
User: "Search for companies: Microsoft"
Claude: [Returns list of matching companies]

User: "Get details for company urn:li:organization:1035"
Claude: [Shows company profile information]
```

### Job Search

```
User: "Find remote Python developer jobs"
Claude: [Searches and displays matching job postings]

User: "Search for Machine Learning Engineer positions in San Francisco"
Claude: [Returns relevant job listings]

User: "Get details for job urn:li:job:123456789"
Claude: [Shows detailed job information]
```

### People Search

```
User: "Search for AI researchers at Stanford"
Claude: [Returns matching professionals]
```

## Available Tools

| Tool Name | Description | Read-Only | Destructive |
|-----------|-------------|-----------|-------------|
| `linkedin_get_oauth_url` | Generate OAuth 2.0 authorization URL | Yes | No |
| `linkedin_exchange_code` | Exchange auth code for access token | No | No |
| `linkedin_get_my_profile` | Get authenticated user's profile | Yes | No |
| `linkedin_get_member_profile` | Get member profile by URN | Yes | No |
| `linkedin_create_post` | Create text post | No | No |
| `linkedin_create_image_post` | Create post with image | No | No |
| `linkedin_update_post` | Update existing post (via delete + create) | No | Yes |
| `linkedin_delete_post` | Delete post permanently | No | Yes |
| `linkedin_get_recent_posts` | List recent posts | Yes | No |
| `linkedin_create_comment` | Comment on content | No | No |
| `linkedin_get_post_comments` | Get comments on post | Yes | No |
| `linkedin_delete_comment` | Delete comment permanently | No | Yes |
| `linkedin_get_company_profile` | Get company details by URN | Yes | No |
| `linkedin_search_companies` | Search for companies | Yes | No |
| `linkedin_search_jobs` | Search job postings | Yes | No |
| `linkedin_get_job_details` | Get job details by URN | Yes | No |
| `linkedin_search_people` | Search for people | Yes | No |

## Understanding LinkedIn URNs

LinkedIn uses URNs (Uniform Resource Names) to identify resources:

- **Person:** `urn:li:person:AbC123XyZ`
- **Post/Share:** `urn:li:share:7289123456789`
- **Comment:** `urn:li:comment:(ugcPost:7289123456789,7289987654321)`
- **Organization:** `urn:li:organization:1035`
- **Job:** `urn:li:job:123456789`

When Claude returns a URN, you can use it to reference that resource in other commands.

## API Permissions and Limitations

### Available Permissions

This server requests these OAuth scopes:
- `openid` - OpenID Connect authentication
- `profile` - Access to profile information
- `email` - Access to email address
- `w_member_social` - Create posts and comments

### Known Limitations

Some LinkedIn API features require additional permissions that are restricted to approved partners:

**Restricted Read Operations:**
- `r_member_social` - Read user's posts (rarely granted to third-party apps)
- Marketing Developer Platform - Advanced company/people search
- Talent Solutions - Advanced job search features

**What This Means:**
- Creating posts: Works perfectly
- Deleting posts: Works perfectly
- Reading your own posts: May not work (requires restricted permission)
- Advanced search: May require approval for Marketing/Talent APIs

**Why?** LinkedIn restricts these APIs to protect user privacy and control third-party access to their platform.

## Project Structure

```
linkedin-mcp-server/
├── linkedin_mcp_server/          # Main package
│   ├── __init__.py               # Package initialization
│   ├── __main__.py               # CLI entry point
│   ├── server.py                 # MCP server with 18 tool definitions
│   ├── config.py                 # Configuration with pydantic-settings
│   ├── utils.py                  # Shared HTTP client utilities
│   └── tools/                    # Tool implementations
│       ├── auth.py               # OAuth 2.0 authentication flow
│       ├── profile.py            # Profile retrieval operations
│       ├── post.py               # Post and comment operations
│       ├── company.py            # Company search and profiles
│       ├── job.py                # Job search operations
│       └── search.py             # People search functionality
├── pyproject.toml                # Package metadata and dependencies
├── requirements.txt              # Pinned dependencies
├── README.md                     # This file
├── claude.md                     # Claude integration guide
├── LICENSE                       # MIT License
└── get_profile.py                # Example standalone script
```

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server.git
cd LinkedIn_mcp_custom_server

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black linkedin_mcp_server/

# Lint
ruff check linkedin_mcp_server/

# Type checking
mypy linkedin_mcp_server/
```

### Running Locally

```bash
# Using module syntax
python -m linkedin_mcp_server

# Using installed command
linkedin-mcp-server
```

## Troubleshooting

### Authentication Issues

**Problem:** "Error: LINKEDIN_CLIENT_ID not configured"
**Solution:** Create `.env` file with your LinkedIn app credentials

**Problem:** "Unauthorized (401)" errors
**Solution:** Your access token expired. Re-authenticate using the OAuth flow

**Problem:** "Error exchanging code: invalid code"
**Solution:** Authorization codes expire quickly. Generate a new OAuth URL and try again

### API Errors

**Problem:** "Forbidden (403)" errors
**Solution:** Your LinkedIn app may lack required permissions. Check your app's products in the Developer Portal

**Problem:** "r_member_social permission required"
**Solution:** This permission is restricted. LinkedIn rarely grants it to third-party apps. Focus on write operations instead

**Problem:** Can't search companies/jobs/people
**Solution:** These APIs may require Marketing/Talent Solutions products which need LinkedIn approval

### Connection Issues

**Problem:** MCP server not connecting in Claude Desktop
**Solution:**
1. Verify `claude_desktop_config.json` syntax is valid JSON
2. Check that the command path is correct
3. Restart Claude Desktop
4. Check Claude Desktop logs for error messages

**Problem:** ".env file not found"
**Solution:** Create `.env` file in the same directory where Claude Desktop runs the server, or specify environment variables in the config

## Security Best Practices

1. **Never commit credentials** - `.env` is in `.gitignore` for a reason
2. **Rotate tokens regularly** - Re-authenticate periodically for security
3. **Use HTTPS in production** - Update redirect URI to HTTPS for production apps
4. **Minimum permissions** - Only request scopes you actually need
5. **Review app access** - Regularly check LinkedIn's "Apps" section in settings

## Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Format code: `black linkedin_mcp_server/`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Contribution Guidelines

- Follow existing code style (Black formatter, 100 char line length)
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic
- Write clear commit messages

## Roadmap

Future enhancements being considered:

- Token refresh flow implementation
- Webhook support for real-time notifications
- Enhanced error handling and retry logic
- Pagination support for search results
- Bulk operations for efficiency
- Analytics and insights (if API access granted)
- Connection management features
- Message sending (if Messaging API access granted)

## FAQ

**Q: Why can't I read my own posts?**
A: The `r_member_social` permission required to read posts is restricted by LinkedIn. Most third-party apps cannot access this feature.

**Q: How long do access tokens last?**
A: LinkedIn controls token expiration. Typically tokens last for 60 days, but this can vary. You'll need to re-authenticate when tokens expire.

**Q: Can I use this for multiple LinkedIn accounts?**
A: Currently, the server is designed for single-user authentication. Each `.env` file holds one access token.

**Q: Is this officially supported by LinkedIn?**
A: No, this is a community project. It uses LinkedIn's public APIs but is not officially endorsed by LinkedIn.

**Q: Can I use this commercially?**
A: Yes, the MIT license allows commercial use. However, check LinkedIn's terms of service and API usage policies.

**Q: Why do some searches return empty results?**
A: Search APIs may require additional LinkedIn products (Marketing/Talent) that need approval. Also, API access varies by account type.

## Support

- **Report bugs:** [GitHub Issues](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server/issues)
- **Documentation:** [GitHub README](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server#readme)
- **Integration Guide:** [claude.md](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server/blob/main/claude.md)
- **Discussions:** [GitHub Discussions](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server/discussions)

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [LinkedIn API Documentation](https://learn.microsoft.com/en-us/linkedin/)
- [OAuth 2.0 Specification](https://oauth.net/2/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- **FastMCP** - For the excellent MCP framework
- **Model Context Protocol** - For enabling AI-agent integrations
- **LinkedIn API** - For providing professional networking capabilities
- **Claude** - For inspiring and testing this integration

## Author

**SARAM ALI**

- Email: saramali15792@gmail.com
- GitHub: [@SARAMALI15792](https://github.com/SARAMALI15792)
- Project: [LinkedIn MCP Custom Server](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server)

---

**Built with care for the AI and LinkedIn communities** | [Report Issues](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server/issues) | [Contribute](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server/pulls) | [Star on GitHub](https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server)
