"""Helper utilities for the application."""

from datetime import datetime
import uuid


def generate_complaint_id() -> str:
    """Generate a unique complaint ID in format CM-YYYYMMDD-XXXX."""
    now = datetime.utcnow()
    date_part = now.strftime("%Y%m%d")
    # Use last 4 chars of a UUID for uniqueness
    unique_part = uuid.uuid4().hex[:4].upper()
    return f"CM-{date_part}-{unique_part}"


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def datetime_to_str(dt: datetime) -> str:
    """Convert datetime to ISO string."""
    if dt is None:
        return ""
    return dt.isoformat() + "Z" if not str(dt).endswith("Z") else str(dt)


def format_complaint_for_response(doc: dict) -> dict:
    """Format a MongoDB complaint document for API response."""
    if doc is None:
        return {}

    return {
        "id": str(doc.get("_id", "")),
        "complaint_id": doc.get("complaint_id", ""),
        "user_id": doc.get("user_id", ""),
        "user": doc.get("user", None),
        "category": doc.get("category", ""),
        "subcategory": doc.get("subcategory", ""),
        "description": doc.get("description", ""),
        "location": doc.get("location", ""),
        "priority_level": doc.get("priority_level", "medium"),
        "priority_score": doc.get("priority_score", 0),
        "priority_reasoning": doc.get("priority_reasoning", None),
        "status": doc.get("status", "open"),
        "ai_analysis": doc.get("ai_analysis", None),
        "media_urls": doc.get("media_urls", []),
        "assigned_provider_id": doc.get("assigned_provider_id", None),
        "assigned_provider": doc.get("assigned_provider", None),
        "estimated_resolution_time": doc.get("estimated_resolution_time", None),
        "actual_resolution_time": doc.get("actual_resolution_time", None),
        "user_satisfaction": doc.get("user_satisfaction", None),
        "created_at": datetime_to_str(doc.get("created_at", datetime.utcnow())),
        "updated_at": datetime_to_str(doc.get("updated_at", datetime.utcnow())),
    }


def format_provider_for_response(doc: dict) -> dict:
    """Format a MongoDB provider document for API response."""
    if doc is None:
        return {}

    return {
        "id": str(doc.get("_id", "")),
        "platform": doc.get("platform", ""),
        "name": doc.get("name", ""),
        "service_types": doc.get("service_types", []),
        "rating": doc.get("rating", 0),
        "reviews_count": doc.get("reviews_count", 0),
        "price_range": doc.get("price_range", "$$"),
        "service_areas": doc.get("service_areas", []),
        "availability_status": doc.get("availability_status", "available"),
        "avg_response_time": doc.get("avg_response_time", None),
        "deep_link_template": doc.get("deep_link_template", None),
        "is_active": doc.get("is_active", True),
    }


def format_timeline_for_response(doc: dict) -> dict:
    """Format a MongoDB timeline document for API response."""
    if doc is None:
        return {}

    return {
        "id": str(doc.get("_id", "")),
        "complaint_id": doc.get("complaint_id", ""),
        "event_type": doc.get("event_type", ""),
        "event_data": doc.get("event_data", {}),
        "performed_by": doc.get("performed_by", None),
        "performed_by_name": doc.get("performed_by_name", None),
        "created_at": datetime_to_str(doc.get("created_at", datetime.utcnow())),
    }
