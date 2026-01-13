# tools/get_gdp_tools.py

import asyncio
import httpx
from typing import Any, Dict  
from server import mcp  
@mcp.tool()
async def get_gdp(country: str, year: int) -> Dict[str, Any]:
    """
    Return the World Bank GDP (current US$) for a given country and year.

    Args:
        country: ISO 2- or 3-letter code (e.g., 'US' or 'USA', 'IN' or 'IND').
        year: Four-digit year (>=1960).

    Returns:
        JSON dict with country name/code, year, indicator metadata, GDP value (USD), and source URL.
        If no value is found, returns a message dict.
    """
    if not (2 <= len(country.strip()) <= 3):
        return {"error": "country must be ISO-2 or ISO-3 code (e.g., 'US' or 'USA')."}
    if not (1960 <= int(year) <= 2100):
        return {"error": "year must be between 1960 and 2100."}

    code = country.strip()
    url = (
        f"https://api.worldbank.org/v2/country/{code}"
        f"/indicator/NY.GDP.MKTP.CD?date={year}:{year}&format=json"
    )

    async with httpx.AsyncClient(headers={"User-Agent": "mcp-worldbank-gdp/1.0"}) as client:
        resp = await client.get(url, timeout=20.0)

    if resp.status_code != 200:
        return {"error": f"World Bank request failed: HTTP {resp.status_code}", "api": url}

    data = resp.json()
    records = data[1] if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list) else []
    entry = records[0] if records else None

    if not entry or entry.get("value") in (None,):
        return {
            "message": f"No GDP value found for {code.upper()} in {year}.",
            "countryCode": code.upper(),
            "year": year,
            "indicator": "NY.GDP.MKTP.CD",
            "api": url,
        }

    payload = {
        "country": (entry.get("country") or {}).get("value", code.upper()),
        "countryCode": code.upper(),
        "year": int(year),
        "indicator": (entry.get("indicator") or {}).get("id", "NY.GDP.MKTP.CD"),
        "indicatorName": (entry.get("indicator") or {}).get(
            "value", "GDP (current US$) - NY.GDP.MKTP.CD"
        ),
        "valueUSD": entry.get("value"),
        "source": "World Bank Open Data",
        "api": url,
    }
    return payload



 