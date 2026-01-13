"""LinkedIn MCP Server - Model Context Protocol server for LinkedIn integration.

This package provides a FastMCP-based server that enables AI agents to interact
with LinkedIn's professional network through the Model Context Protocol.
"""

__version__ = "1.0.0"
__author__ = "SARAM ALI"
__email__ = "saramali15792@gmail.com"

from .server import mcp

__all__ = ["mcp", "__version__"]
