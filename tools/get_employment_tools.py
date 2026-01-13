# get_employment_tools.py

import asyncio
import httpx
from typing import Any, Dict  
from server import mcp  

sectors = [
        "SL.EMP.TOTL.SP.ZS", # employment‑to‑population ratio
        "SL.AGR.EMPL.ZS", # Agriculture
        "SL.IND.EMPL.ZS", # Industry
        "SL.SRV.EMPL.ZS"  # Service
    ]

@mcp.tool()
async def get_employment(country: str, year: int) -> Dict[str, Any]:
    """
    Fetch employment share by major economic sector (Agriculture, Industry, Services)
    from the World Bank API for a given country and year.

    Indicators used (World Bank WDI):
        - SL.AGR.EMPL.ZS : Employment in agriculture (% of total employment)
        - SL.IND.EMPL.ZS : Employment in industry (% of total employment)
        - SL.SRV.EMPL.ZS : Employment in services (% of total employment)

    Args:
        country: ISO 2- or 3-letter country code (e.g., 'US', 'USA', 'KR', 'KOR').
        year: Four-digit year (>= 1960).

    Returns:
        A list of raw World Bank indicator entries, one per sector, each containing:
            - country metadata
            - indicator metadata
            - year
            - employment share value (%)
            - source URL

        If data is missing or the API request fails, an error/message dict is returned.
    """

    if not (2 <= len(country.strip()) <= 3):
        return {"error": "country must be ISO-2 or ISO-3 code (e.g., 'US' or 'USA')."}
    if not (1960 <= int(year) <= 2100):
        return {"error": "year must be between 1960 and 2100."}

    code = country.strip()
    payload = []

    for sector in sectors:
        url = (
            f"https://api.worldbank.org/v2/country/{code}/indicator/{sector}?date={year}:{year}&format=json"
        )

        async with httpx.AsyncClient(headers={"User-Agent": "mcp-worldbank-employment/1.0"}) as client:
            resp = await client.get(url, timeout=20.0)

        if resp.status_code != 200:
            return {"error": f"World Bank request failed: HTTP {resp.status_code}", "api": url}

        data = resp.json()
        records = data[1] if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list) else []
        entry = records[0] if records else None

        if not entry or entry.get("value") in (None,):
            return {
                "message": f"No employment value found for {code.upper()} in {year}.",
                "countryCode": code.upper(),
                "year": year,
                "indicator": sector,
                "api": url,
            }
        
        payload.append(entry)

    return {
        "employment‑to-population-ratio": payload[0],
        "employment": {
            "agriculture": payload[1],
            "industry": payload[2],
            "services": payload[3]
        }
    }

# For Testing
# if __name__ == "__main__":
#     import asyncio
#     result = asyncio.run(get_employment("US", 2023))
#     print(result)