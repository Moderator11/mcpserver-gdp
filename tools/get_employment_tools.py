# tools/get_employment_extended.py

import asyncio
import httpx
from typing import Any, Dict, List
from server import mcp

# World Bank employment indicators
indicators = {
    # Employment ratios
    "employment_to_population_ratio": "SL.EMP.TOTL.SP.ZS",  

    # Sector shares
    "agriculture": "SL.AGR.EMPL.ZS",
    "industry": "SL.IND.EMPL.ZS",
    "services": "SL.SRV.EMPL.ZS",

    # Unemployment
    "unemployment_total": "SL.UEM.TOTL.ZS",
    "unemployment_youth": "SL.UEM.1524.ZS",

    # Labor Force Participation
    "lf_participation_total": "SL.TLF.CACT.ZS",
    "lf_participation_female": "SL.TLF.CACT.FE.ZS",
    "lf_participation_male": "SL.TLF.CACT.MA.ZS",

    # Vulnerable / Employment types
    "vulnerable_employment": "SL.EMP.VULN.ZS",
    "wage_employment": "SL.EMP.WORK.ZS",
    "self_employment": "SL.EMP.SELF.ZS",

    # Absolute values
    "labor_force_total": "SL.TLF.TOTL.IN"
}


async def fetch_indicator(client: httpx.AsyncClient, country: str, indicator: str, year: int) -> Dict[str, Any]:
    """Fetch a single indicator from World Bank API."""
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={year}:{year}&format=json"
    try:
        resp = await client.get(url, timeout=20.0)
        resp.raise_for_status()
        data = resp.json()
        records = data[1] if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list) else []
        entry = records[0] if records else None
        if not entry or entry.get("value") is None:
            return {"indicator": indicator, "value": None, "message": f"No data found for {country} in {year}", "api": url}
        entry["api"] = url
        return entry
    except Exception as e:
        return {"indicator": indicator, "value": None, "error": str(e), "api": url}


@mcp.tool()
async def get_employment_extended(country: str, year: int) -> Dict[str, Any]:
    """
    Fetch extended employment and labor indicators from World Bank API for a given country/year.

    Returns a dict with:
        - employment_to_population_ratio: %
        - employment_percent: sector shares (%)
        - unemployment: total & youth (%)
        - labor_force_participation: total/male/female (%)
        - employment_type: vulnerable/wage/self (%)
        - labor_force_total: absolute number
        - raw: list of raw API entries
    """
    country = country.strip().upper()
    if not (2 <= len(country) <= 3):
        return {"error": "country must be ISO-2 or ISO-3 code (e.g., 'US' or 'USA')."}
    if not (1960 <= year <= 2100):
        return {"error": "year must be between 1960 and 2100."}

    async with httpx.AsyncClient(headers={"User-Agent": "mcp-worldbank-employment/1.0"}) as client:
        tasks: List[asyncio.Task] = [
            fetch_indicator(client, country, ind, year) for ind in indicators.values()
        ]
        results = await asyncio.gather(*tasks)

    # Map results back to keys
    keys = list(indicators.keys())
    mapped_results = {key: res for key, res in zip(keys, results)}

    return {
        "employment_to_population_ratio": mapped_results["employment_to_population_ratio"].get("value"),
        "employment_percent": {
            "agriculture": mapped_results["agriculture"].get("value"),
            "industry": mapped_results["industry"].get("value"),
            "services": mapped_results["services"].get("value")
        },
        "unemployment": {
            "total": mapped_results["unemployment_total"].get("value"),
            "youth": mapped_results["unemployment_youth"].get("value")
        },
        "labor_force_participation": {
            "total": mapped_results["lf_participation_total"].get("value"),
            "female": mapped_results["lf_participation_female"].get("value"),
            "male": mapped_results["lf_participation_male"].get("value")
        },
        "employment_type": {
            "vulnerable": mapped_results["vulnerable_employment"].get("value"),
            "wage": mapped_results["wage_employment"].get("value"),
            "self": mapped_results["self_employment"].get("value")
        },
        "labor_force_total": mapped_results["labor_force_total"].get("value"),
        "raw": results  # keep raw API entries for debugging
    }


# For local testing
# if __name__ == "__main__":
#     import asyncio, json
#     result = asyncio.run(get_employment_extended("US", 2023))
#     print(json.dumps(result, indent=2))
