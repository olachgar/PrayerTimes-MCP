from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from app.config import settings


class PrayerTimesClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.api_base_url).rstrip("/")

    async def get_prayer_times(
        self,
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

        async with httpx.AsyncClient(timeout=settings.request_timeout, follow_redirects=True) as client:
            response = await client.get(f"{self.base_url}/v1/timingsByCity", params=params)
            response.raise_for_status()
            payload = response.json()

        data = payload.get("data", {})
        timings = data.get("timings", {})
        meta = data.get("meta", {})
        return {
            "service": "prayer_times_mcp",
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
