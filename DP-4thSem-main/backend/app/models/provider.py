"""Service provider models for MongoDB."""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class ProviderPlatform(str, Enum):
    urban_company = "urban_company"
    taskrabbit = "taskrabbit"
    handy = "handy"
    local = "local"


class ProviderAvailability(str, Enum):
    available = "available"
    busy = "busy"
    unavailable = "unavailable"


class PriceRange(str, Enum):
    budget = "$"
    moderate = "$$"
    premium = "$$$"


class ServiceProviderInDB(BaseModel):
    """Full service provider document stored in MongoDB."""
    id: str = Field(alias="_id", default="")
    platform: ProviderPlatform
    platform_provider_id: str = ""
    name: str
    service_types: List[str] = []
    rating: float = 0.0
    reviews_count: int = 0
    price_range: str = "$$"
    service_areas: List[str] = []
    availability_status: ProviderAvailability = ProviderAvailability.available
    avg_response_time: Optional[int] = None  # minutes
    deep_link_template: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class ProviderResponse(BaseModel):
    """Provider data returned to the client."""
    id: str
    platform: str
    name: str
    service_types: List[str] = []
    rating: float = 0.0
    reviews_count: int = 0
    price_range: str = "$$"
    service_areas: List[str] = []
    availability_status: str = "available"
    avg_response_time: Optional[int] = None
    deep_link_template: Optional[str] = None
    is_active: bool = True
