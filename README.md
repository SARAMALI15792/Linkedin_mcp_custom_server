# LinkedIn Custom MCP Server

**Empower your AI agents with professional networking capabilities.**

This project implements a **Model Context Protocol (MCP)** server that acts as a bridge between Large Language Models (LLMs) like Claude or Gemini and the LinkedIn platform. It allows your AI assistants to autonomously manage your professional presence, interact with your feed, search for opportunities, and analyze profiles—all through a secure and authenticated interface.

Built with performance and modularity in mind using [FastMCP](https://github.com/jlowin/fastmcp) and Python.

---

## 🌟 Key Features

*   **📈 Feed Management**: Create text posts, upload images, and manage comments seamlessly.
*   **👤 Profile Intelligence**: Retrieve and analyze your own profile or public member profiles.
*   **🤝 Network Interaction**: Engage with content by commenting on posts and shares.
*   **🏢 Company Insights**: Search for companies and retrieve detailed organizational data.
*   **💼 Job Search**: Find relevant job postings based on keywords and location.
*   **🔐 Secure Auth**: Robust OAuth 2.0 implementation with token persistence.

---

## 📂 Project Structure

```text
LinkedIn_mcp_custom_server/
├── main.py              # Server entry point & tool registration
├── config.py            # Environment & settings management
├── utils.py             # Shared API & error handling helpers
├── requirements.txt     # Python dependencies
├── .env                 # Local secrets (not committed)
├── .gitignore           # Git exclusion rules
├── LICENSE              # MIT License details
└── tools/               # Modular tool implementations
    ├── auth.py          # OAuth 2.0 flow logic
    ├── profile.py       # Profile data extraction
    ├── post.py          # Posts, Comments, and Image uploads
    ├── company.py       # Company search and profiles
    ├── job.py           # Job search and details
    └── search.py        # People search and member profiles
```

---

## 🚀 Installation & Setup

### Prerequisites
*   **Python 3.12+** installed on your system.
*   A **LinkedIn Developer App** (See configuration below).

### Step 1: Clone the Repository
```bash
git clone https://github.com/SARAMALI15792/LinkedIn_mcp_custom_server.git
cd LinkedIn_mcp_custom_server
```

### Step 2: Install Dependencies
We recommend using a virtual environment.

```bash
# Create and activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure Environment
1.  Go to the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps).
2.  Create a new app and request access to the **"Sign In with LinkedIn using OpenID Connect"** and **"Share on LinkedIn"** products.
3.  In the **Auth** tab, add `http://localhost:8000` to the **Authorized redirect URLs**.
4.  Create a `.env` file in the project root:

```ini
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000
# Access token will be added automatically after login
```

---

## 🏃‍♂️ Usage

### Starting the Server
Run the server locally using Python:

```bash
python main.py
```
The server will start listening on `http://127.0.0.1:8000` using the SSE (Server-Sent Events) transport.

### Connecting to an MCP Client
To use this with **Claude Desktop**, add the following to your config file (`%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "C:/path/to/project/.venv/Scripts/python.exe",
      "args": ["C:/path/to/project/main.py"]
    }
  }
}
```

### First-Time Authentication
1.  Ask your Agent: **"Generate a LinkedIn login URL."**
2.  Open the provided link and authorize the app.
3.  You will be redirected to a page. **Copy the `code` parameter** from the URL bar.
4.  Ask your Agent: **"Exchange this code for a token: [PASTE_CODE]"**
5.  You are now connected!

---

## 💡 Usage Examples

Once connected, you can ask your AI agent to perform various tasks:

**📝 Posting Content**
> "Create a LinkedIn post with the text 'Excited to launch my new MCP server!' and set visibility to CONNECTIONS."
> "Post this image 'C:/photos/launch.jpg' with the caption 'Project Launch Day!'"

**🔎 Job Hunting**
> "Search for 'Senior Python Developer' jobs in 'San Francisco' and show me the top 3 details."

**📊 Profile & Network**
> "Get my profile summary."
> "Who is the user with the username 'stickerdaniel'?"

**💬 Engagement**
> "Show me the comments on my latest post."
> "Reply to the first comment saying 'Thanks for the support!'"

---

## 🛠️ Available Tools

| Category | Tool Name | Description |
| :--- | :--- | :--- |
| **Auth** | `linkedin_get_oauth_url` | Generate the OAuth 2.0 authorization URL for LinkedIn login. |
| | `linkedin_exchange_code` | Exchange an authorization code for a persistent access token. |
| **Profile** | `linkedin_get_my_profile` | Retrieve your own profile information (Name, Email, Picture). |
| | `linkedin_get_member_profile` | Fetch public profile details for a specific member using their URN. |
| **Search** | `linkedin_search_people` | Search for LinkedIn members based on keywords and filters. |
| **Post** | `linkedin_create_post` | Publish a text-only update to your professional LinkedIn feed. |
| | `linkedin_create_image_post` | Upload an image and publish a media post to your feed. |
| | `linkedin_update_post` | Update a post's content (via the Delete & Re-create method). |
| | `linkedin_delete_post` | Permanently remove a post from your feed using its URN. |
| | `linkedin_get_recent_posts` | Retrieve a list of your most recent activity and publications. |
| **Comment** | `linkedin_create_comment` | Post a new comment on a share, article, or video. |
| | `linkedin_get_post_comments` | List all comments and reactions for a specific post. |
| | `linkedin_delete_comment` | Remove a comment you previously published. |
| **Company** | `linkedin_search_companies` | Find organizational profiles using keywords or industries. |
| | `linkedin_get_company_profile` | Retrieve detailed information about a specific company. |
| **Job** | `linkedin_search_jobs` | Find open career opportunities by keywords and location. |
| | `linkedin_get_job_details` | Get the full description and application details for a job. |

---

## 🤝 Contribution Guidelines

We welcome contributions to make this server even better!

1.  **Fork the Repository**: Click the "Fork" button on GitHub.
2.  **Create a Branch**: `git checkout -b feature/amazing-feature`.
3.  **Commit Changes**: `git commit -m 'Add amazing feature'`.
4.  **Push to Branch**: `git push origin feature/amazing-feature`.
5.  **Open a Pull Request**: Submit your changes for review.

Please ensure your code follows the existing modular structure in the `tools/` directory.

---

## 📄 License

This project is open-source and available under the **MIT License**. See the [LICENSE](LICENSE) file for full details.
