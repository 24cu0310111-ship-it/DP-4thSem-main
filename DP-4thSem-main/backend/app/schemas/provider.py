"""Provider request/response schemas."""

from pydantic import BaseModel
from typing import Optional


class ProviderFilterParams(BaseModel):
    platform: Optional[str] = None
    category: Optional[str] = None
    area: Optional[str] = None
    availability: Optional[str] = None
    min_rating: Optional[float] = None
