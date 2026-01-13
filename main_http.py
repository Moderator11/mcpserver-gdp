# mcp_http_ok.py
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn, random
from typing import Literal

mcp = FastMCP("demo_weather")

@mcp.tool()
def get_rain_forecast(location: str, day: Literal["today","tomorrow"]="today")->str:
    return f"There is a {random.randint(0,100)}% chance of rain in {location} {day}."

@mcp.tool()
def get_temperature(location: str, unit: Literal["C","F"]="C")->str:
    t = random.uniform(-10,35)
    if unit.upper()=="F": t = t*9/5+32; u="°F"
    else: u="°C"
    return f"The temperature in {location} is {t:.1f}{u}."

async def ping(_): return JSONResponse({"ok": True})

app = Starlette(routes=[Route("/ping", ping)])
# Expose MCP at /mcp  (final URL will be http://127.0.0.1:1230/mcp  — no trailing slash)
app.mount("/mcp", mcp.streamable_http_app())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1230, log_level="debug")
