from __future__ import annotations

from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("prayer_times_local")


async def fetch_prayer_times(
    city: str,
    country: str,
    method: Optional[int] = None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"city": city, "country": country}
    if method is not None:
        params["method"] = method
    if date:
        params["date"] = date

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        response = await client.get("https://api.aladhan.com/v1/timingsByCity", params=params)
        response.raise_for_status()
        payload = response.json()

    data = payload.get("data", {})
    timings = data.get("timings", {})
    meta = data.get("meta", {})
    return {
        "city": city,
        "country": country,
        "date": data.get("date", {}).get("readable") or date or "today",
        "timezone": meta.get("timezone"),
        "timings": timings,
        "metadata": {
            "latitude": meta.get("latitude"),
            "longitude": meta.get("longitude"),
            "method": method,
            "source": payload.get("status") or "aladhan",
        },
    }


@mcp.tool()
async def get_prayer_times_local(
    city: str,
    country: str,
    method: Optional[int] = None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch prayer times for a city and country from the public Aladhan API. This tool is for the local machine instance."""
    return await fetch_prayer_times(city=city, country=country, method=method, date=date)


@mcp.tool()
async def get_prayer_times(
    city: str,
    country: str,
    method: Optional[int] = None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Backward-compatible alias for the local machine instance."""
    return await fetch_prayer_times(city=city, country=country, method=method, date=date)


if __name__ == "__main__":
    mcp.run(transport="stdio")
