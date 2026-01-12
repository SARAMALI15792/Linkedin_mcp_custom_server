# LinkedIn Custom MCP Server

A robust **Model Context Protocol (MCP)** server that connects LLMs (like Claude, Gemini, etc.) to LinkedIn. This server allows your AI agent to interact with LinkedIn on your behalf to manage posts, view profiles, search for jobs, and more.

Built with [FastMCP](https://github.com/jlowin/fastmcp), `httpx`, and Python.

## 🚀 Features

This server provides the following tools to your MCP Client:

### 🔐 Authentication
*   **`linkedin_get_oauth_url`**: Generates the login link to authorize the app.
*   **`linkedin_exchange_code`**: Exchanges the authorization code for a persistent Access Token.

### 👤 Profiles
*   **`linkedin_get_my_profile`**: Fetches your own profile details (Name, Photo, Email).
*   **`linkedin_get_member_profile`**: Fetches a public member's profile by URN (*Requires permissions*).

### 📝 Posts (Feed)
*   **`linkedin_create_post`**: Creates a text post on your feed.
    *   *Inputs:* `text` (content), `visibility` ("PUBLIC" or "CONNECTIONS").
*   **`linkedin_create_image_post`**: Creates a post with an image.
    *   *Inputs:* `text`, `image_source` (Public URL or local absolute file path).
*   **`linkedin_update_post`**: Updates a post's text.
    *   *Note:* Since LinkedIn's API does not support text edits, this tool **deletes** the old post and **creates** a new one (resulting in a new Post ID).
*   **`linkedin_delete_post`**: Deletes a post using its URN.
*   **`linkedin_get_recent_posts`**: Lists your recent posts (*Requires `r_member_social` permission*).

### 💬 Comments
*   **`linkedin_create_comment`**: Post a comment on an article, video, or share.
    *   *Inputs:* `object_urn` (the post ID, e.g., `urn:li:share:123`), `text`.
*   **`linkedin_get_post_comments`**: View comments on a specific post.
*   **`linkedin_delete_comment`**: Delete a comment you made.

### 🏢 Companies
*   **`linkedin_search_companies`**: Search for companies by name/keyword.
*   **`linkedin_get_company_profile`**: Get company details by URN.

### 💼 Jobs
*   **`linkedin_search_jobs`**: Search for job postings.
    *   *Inputs:* `keywords`, `location`.
*   **`linkedin_get_job_details`**: Get details of a specific job by URN.

### 🔍 Search
*   **`linkedin_search_people`**: Search for people on LinkedIn (*Requires permissions*).

---

## 🛠️ Prerequisites

1.  **Python 3.12+** installed.
2.  **LinkedIn Developer App**:
    *   Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps).
    *   Create an app.
    *   Request access to products: **"Sign In with LinkedIn using OpenID Connect"** and **"Share on LinkedIn"**.
    *   Note your **Client ID** and **Client Secret**.
    *   Add `http://localhost:8000` (or `http://127.0.0.1:8000` depending on your setup) to "Authorized redirect URLs".

---

## 📦 Installation

1.  **Clone/Download** this repository.
2.  **Install Dependencies**:
    We use `uv` for fast package management, but `pip` works too.

    ```powershell
    # Using pip
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:

    ```ini
    LINKEDIN_CLIENT_ID=your_client_id_here
    LINKEDIN_CLIENT_SECRET=your_client_secret_here
    LINKEDIN_REDIRECT_URI=http://localhost:8000
    # LINKEDIN_ACCESS_TOKEN=  <-- This will be added automatically after login
    ```

---

## 🚦 How to Run

### 1. Start the Server
Run the `main.py` file.

```powershell
# If using a virtual environment (recommended)
.venv\Scripts\python main.py

# Or directly
python main.py
```

The server will start on **http://127.0.0.1:8000** (SSE Transport).

### 2. Connect to an MCP Client (e.g., Claude Desktop)
Add the server configuration to your Claude Desktop config file (`%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "C:/path/to/python.exe",
      "args": ["C:/path/to/linkedin_custom_mcp/main.py"]
    }
  }
}
```
*Note: Use the absolute path to your python executable.*

---

## 🔑 Authentication Guide (First Run)

Since LinkedIn requires OAuth 2.0, you must authenticate once to generate an Access Token.

1.  **Ask your Agent:** "Generate a LinkedIn login URL."
2.  **Click the Link:** The agent will provide a URL. Open it in your browser.
3.  **Authorize:** Log in to LinkedIn and approve the app.
4.  **Copy the Code:** You will be redirected to a page (which might error out). Copy the `code` parameter from the URL bar (e.g., `?code=AQRe...`).
5.  **Exchange Code:** Ask your Agent: "Exchange this code for a token: [PASTE CODE HERE]".
6.  **Success:** The token is saved to your `.env` file automatically. You can now use all other tools!

---

## ⚠️ Troubleshooting & Limitations

*   **403 Forbidden Error:**
    *   This usually means your App lacks the specific permission for that tool.
    *   *Standard Access:* Allows `openid`, `profile`, `email`, and `w_member_social` (Post creation).
    *   *Restricted Access:* Reading posts, searching people, and detailed company data often require special "Marketing Developer Platform" or "Basic Profile" partner access from LinkedIn.
*   **Redirect URI Mismatch:**
    *   Ensure the `LINKEDIN_REDIRECT_URI` in `.env` matches the one in the LinkedIn Developer Portal **exactly**.
*   **Token Expiry:**
    *   LinkedIn tokens last for 60 days. If tools stop working, re-run the Auth flow.

## 📂 Project Structure

```text
linkedin_custom_mcp/
├── main.py              # Server entry point
├── config.py            # Settings management
├── utils.py             # Shared API helpers
├── .env                 # Secrets (Client ID, Token)
├── tools/               # Tool implementations
│   ├── auth.py          # OAuth logic
│   ├── profile.py       # Profile fetching
│   ├── post.py          # Posts, Comments, & Images
│   ├── company.py       # Company data
│   ├── job.py           # Job data
│   └── search.py        # People search
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
