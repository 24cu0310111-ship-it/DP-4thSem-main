"""Provider routes — list and filter service providers."""

from fastapi import APIRouter, Depends, Query
from typing import Optional, Dict, Any, List
import logging

from app.api.deps import require_admin
from app.database import providers_collection
from app.utils.helpers import format_provider_for_response

logger = logging.getLogger(__name__)
router = APIRouter()


# Category-to-service-type mapping
CATEGORY_SERVICE_MAP = {
    "electricity": ["electrical", "electrician", "wiring"],
    "water": ["plumbing", "water_heater", "water"],
    "plumbing": ["plumbing", "pipe_repair", "leak", "drain_cleaning"],
    "sanitation": ["cleaning", "sanitation", "drain_cleaning"],
    "hvac": ["hvac", "ac_repair", "heating", "cooling"],
    "maintenance": ["maintenance", "handyman", "repairs", "general"],
    "security": ["security", "locksmith", "cctv"],
}


@router.get("")
async def get_providers(
    platform: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    availability: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None),
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Get all service providers with filters."""
    query = {"is_active": True}

    if platform:
        query["platform"] = platform

    if category:
        service_types = CATEGORY_SERVICE_MAP.get(category.lower(), [])
        if service_types:
            query["service_types"] = {"$in": service_types}

    if area:
        query["service_areas"] = area

    if availability:
        query["availability_status"] = availability

    if min_rating:
        query["rating"] = {"$gte": min_rating}

    cursor = providers_collection().find(query).sort("rating", -1)

    providers = []
    async for doc in cursor:
        providers.append(format_provider_for_response(doc))

    return {"data": providers}
