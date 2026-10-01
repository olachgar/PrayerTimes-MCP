from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PrayerTimesRequest(BaseModel):
    city: str = Field(..., description="City name to query.")
    country: str = Field(..., description="Country name to query.")
    method: Optional[int] = Field(default=None, description="Prayer calculation method (optional).")
    date: Optional[str] = Field(default=None, description="Optional date in YYYY-MM-DD format.")


class MCPToolRequest(BaseModel):
    tool: str = Field(..., description="MCP tool to call.")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments.")


class PrayerTimesResponse(BaseModel):
    service: str
    city: str
    country: str
    date: str
    timezone: Optional[str] = None
    timings: Dict[str, str]
    metadata: Dict[str, Any]
