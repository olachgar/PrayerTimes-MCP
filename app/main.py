from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.client import PrayerTimesClient
from app.config import settings
from app.schemas import MCPToolRequest, PrayerTimesRequest, PrayerTimesResponse

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Local FastAPI service that fetches prayer times from Aladhan and exposes them through a lightweight MCP-style endpoint.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = PrayerTimesClient()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/prayer-times", response_model=PrayerTimesResponse)
async def get_prayer_times(
    city: str = Query(..., description="City to search."),
    country: str = Query(..., description="Country to search."),
    method: int | None = Query(default=None, description="Optional prayer calculation method."),
    date: str | None = Query(default=None, description="Optional date in YYYY-MM-DD format."),
) -> PrayerTimesResponse:
    try:
        payload = await client.get_prayer_times(city=city, country=country, method=method, date=date)
    except Exception as exc:  # pragma: no cover - defensive layer for external API issues
        raise HTTPException(status_code=502, detail=f"Prayer times provider request failed: {exc}") from exc

    return PrayerTimesResponse(**payload)


@app.post("/mcp")
async def local_mcp_tool_call(request: MCPToolRequest) -> Dict[str, Any]:
    if request.tool != "get_prayer_times":
        raise HTTPException(status_code=400, detail=f"Unsupported MCP tool: {request.tool}")

    args = request.arguments or {}
    city = args.get("city")
    country = args.get("country")
    if not city or not country:
        raise HTTPException(status_code=400, detail="Both 'city' and 'country' arguments are required.")

    method = args.get("method")
    date = args.get("date")

    try:
        payload = await client.get_prayer_times(city=city, country=country, method=method, date=date)
    except Exception as exc:  # pragma: no cover - defensive layer for external API issues
        raise HTTPException(status_code=502, detail=f"Prayer times provider request failed: {exc}") from exc

    return {
        "tool": request.tool,
        "status": "ok",
        "result": payload,
    }


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "PrayerTimes MCP is running. Visit /docs for the OpenAPI specification."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)
