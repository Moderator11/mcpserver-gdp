# tools/get_gdp_tools.py

import asyncio
import httpx
from typing import Any, Dict, Optional
from server import mcp   

FRED_API_KEY = "5d9fe2b4df17d182b64bd807fe549a3f"
FRED_SERIES_ID = "FPCPITOTLZGUSA"
FRED_OBS_URL = "https://api.stlouisfed.org/fred/series/observations"

@mcp.tool()
async def get_us_inflation(year: Optional[int] = None) -> Dict[str, Any]:
    """
    Return the FRED series 'Inflation, consumer prices for the United States' (FPCPITOTLZGUSA)
    for a given year, or the latest available if year is omitted.

    Args:
        year: Four-digit year (e.g., 2021). If None, returns latest available observation.

    Returns:
        JSON dict with series metadata and the observation (year, date, value).
    """
    if not FRED_API_KEY:
        return {"error": "FRED_API_KEY environment variable is not set."}

    params = {
        "series_id": FRED_SERIES_ID,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "asc",
        "observation_start": "1960-01-01",
        "observation_end": "2100-12-31",
    }
    if year is not None:
        if not (1960 <= int(year) <= 2100):
            return {"error": "year must be between 1960 and 2100 or omitted for latest."}
        params["observation_start"] = f"{year}-01-01"
        params["observation_end"] = f"{year}-12-31"

    async with httpx.AsyncClient(headers={"User-Agent": "mcp-fred-us-inflation/1.0"}) as client:
        resp = await client.get(FRED_OBS_URL, params=params, timeout=20.0)

    if resp.status_code != 200:
        return {"error": f"FRED request failed: HTTP {resp.status_code}", "api": {"endpoint": FRED_OBS_URL, "params": params}}

    data = resp.json()
    observations = data.get("observations", [])
    if not observations:
        return {"message": f"No observations found for year {year}." if year else "No observations available."}

    # Pick matching year if specified; else latest non-missing value
    selected = None
    if year is not None:
        for obs in observations:
            try:
                if str(year) in obs.get("date", ""):
                    selected = obs
                    break
            except Exception:
                continue
    else:
        for obs in reversed(observations):
            v = obs.get("value")
            if v not in (None, "", "."):
                selected = obs
                break

    if not selected:
        return {"message": f"No observation found for year {year}." if year else "No non-empty latest observation found."}

    value_str = selected.get("value", "")
    if value_str in ("", "."):
        return {"message": f"No value reported for {year}." if year else "Latest observation has no value."}

    try:
        value = float(value_str)
    except Exception:
        return {"error": f"Unable to parse value '{value_str}' from FRED."}

    result = {
        "seriesId": FRED_SERIES_ID,
        "title": "Inflation, consumer prices for the United States",
        "units": "Percent (annual % change)",
        "date": selected.get("date"),
        "year": int(selected.get("date", "0000-01-01")[:4]),
        "value": value,
        "source": "St. Louis Fed (FRED)",
        "api": {"endpoint": FRED_OBS_URL, "params": params},
    }
    return result
