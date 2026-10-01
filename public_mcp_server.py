from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse

mcp = FastMCP("prayer_times_public", streamable_http_path="/mcp/")


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
async def get_prayer_times(
    city: str,
    country: str,
    method: Optional[int] = None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch prayer times for a city and country from the public Aladhan API."""
    return await fetch_prayer_times(city=city, country=country, method=method, date=date)


async def root(request):
    return JSONResponse(
        {
            "message": "PrayerTimes public MCP server is running.",
            "endpoints": {
                "mcp": "/mcp",
                "health": "/health",
            },
        }
    )


async def health(request):
    return JSONResponse({"status": "ok", "service": "PrayerTimes Public MCP"})


app = mcp.streamable_http_app()
app.add_route("/", root, methods=["GET"])
app.add_route("/health", health, methods=["GET"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("public_mcp_server:app", host="0.0.0.0", port=int(os.getenv("PORT", "8001")), reload=False)
