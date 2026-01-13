# server.py
import asyncio
import httpx
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
# This is the shared MCP server instance
mcp = FastMCP("mix_server-fileops")