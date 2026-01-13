"""CLI entry point for LinkedIn MCP Server."""

from .server import mcp


def main():
    """Run the LinkedIn MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
