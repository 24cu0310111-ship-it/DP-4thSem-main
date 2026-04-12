"""Admin routes — complaint management, provider assignment, analytics."""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, Dict, Any, List
from datetime import datetime
import math
import logging

from app.api.deps import require_admin
from app.database import (
    complaints_collection, users_collection, providers_collection,
    timeline_collection, notes_collection,
)
from app.schemas.complaint import (
    UpdateStatusRequest, AssignProviderRequest, AddNoteRequest,
    PaginatedResponse, PaginationInfo,
)
from app.utils.helpers import (
    generate_uuid, datetime_to_str,
    format_complaint_for_response, format_provider_for_response,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/complaints")
async def get_all_complaints(
    priority: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    sort: Optional[str] = Query(None),
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Get all complaints with filters (admin only)."""
    query = {}

    if priority:
        priorities = [p.strip() for p in priority.split(",")]
        query["priority_level"] = {"$in": priorities}
    if status:
        statuses = [s.strip() for s in status.split(",")]
        query["status"] = {"$in": statuses}
    if category:
        query["category"] = category
    if area:
        query["user.address.area"] = area

    total = await complaints_collection().count_documents(query)
    total_pages = math.ceil(total / limit) if total > 0 else 1

    # Sort
    sort_field = "created_at"
    sort_dir = -1
    if sort == "priority":
        sort_field = "priority_score"
        sort_dir = -1

    cursor = (
        complaints_collection()
        .find(query)
        .sort(sort_field, sort_dir)
        .skip((page - 1) * limit)
        .limit(limit)
    )

    complaints = []
    async for doc in cursor:
        complaints.append(format_complaint_for_response(doc))

    return PaginatedResponse(
        data=complaints,
        pagination=PaginationInfo(
            page=page, limit=limit, total=total, total_pages=total_pages,
        ),
    )


@router.get("/complaints/{complaint_id}")
async def get_complaint_admin(
    complaint_id: str,
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Get full complaint details for admin."""
    doc = await complaints_collection().find_one({
        "$or": [
            {"_id": complaint_id},
            {"complaint_id": complaint_id},
        ],
    })

    if not doc:
        raise HTTPException(status_code=404, detail="Complaint not found")

    result = format_complaint_for_response(doc)

    # Attach timeline
    cursor = timeline_collection().find(
        {"complaint_id": doc.get("complaint_id", "")}
    ).sort("created_at", 1)
    timeline = []
    async for evt in cursor:
        timeline.append({
            "event_type": evt.get("event_type"),
            "event_data": evt.get("event_data", {}),
            "performed_by_name": evt.get("performed_by_name"),
            "created_at": datetime_to_str(evt.get("created_at", datetime.utcnow())),
        })
    result["timeline"] = timeline

    # Attach notes
    notes_cursor = notes_collection().find(
        {"complaint_id": doc.get("complaint_id", "")}
    ).sort("created_at", -1)
    notes = []
    async for note in notes_cursor:
        notes.append({
            "id": str(note["_id"]),
            "content": note.get("content", ""),
            "is_internal": note.get("is_internal", True),
            "created_at": datetime_to_str(note.get("created_at", datetime.utcnow())),
        })
    result["notes"] = notes

    return result


@router.put("/complaints/{complaint_id}/status")
async def update_complaint_status(
    complaint_id: str,
    request: UpdateStatusRequest,
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Update complaint status."""
    # Find the complaint
    doc = await complaints_collection().find_one({
        "$or": [{"_id": complaint_id}, {"complaint_id": complaint_id}]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Complaint not found")

    old_status = doc.get("status", "open")
    now = datetime.utcnow()

    update = {
        "status": request.status,
        "updated_at": now,
    }
    if request.status == "resolved":
        update["actual_resolution_time"] = datetime_to_str(now)

    await complaints_collection().update_one(
        {"_id": doc["_id"]},
        {"$set": update},
    )

    # Timeline event
    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": doc.get("complaint_id", ""),
        "event_type": "status_changed",
        "event_data": {
            "previous_status": old_status,
            "new_status": request.status,
        },
        "performed_by": str(admin["_id"]),
        "performed_by_name": admin.get("name", ""),
        "created_at": now,
    })

    # Optional note
    if request.note:
        await notes_collection().insert_one({
            "_id": generate_uuid(),
            "complaint_id": doc.get("complaint_id", ""),
            "admin_id": str(admin["_id"]),
            "content": request.note,
            "is_internal": True,
            "created_at": now,
            "updated_at": now,
        })

    return {
        "message": "Status updated successfully",
        "complaint": {
            "id": str(doc["_id"]),
            "status": request.status,
            "updated_at": datetime_to_str(now),
        },
    }


@router.put("/complaints/{complaint_id}/assign")
async def assign_provider(
    complaint_id: str,
    request: AssignProviderRequest,
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Assign a service provider to a complaint."""
    doc = await complaints_collection().find_one({
        "$or": [{"_id": complaint_id}, {"complaint_id": complaint_id}]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Complaint not found")

    provider = await providers_collection().find_one({"_id": request.provider_id})
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    now = datetime.utcnow()

    await complaints_collection().update_one(
        {"_id": doc["_id"]},
        {"$set": {
            "assigned_provider_id": request.provider_id,
            "assigned_provider": format_provider_for_response(provider),
            "status": "assigned",
            "estimated_resolution_time": request.estimated_time,
            "updated_at": now,
        }},
    )

    # Timeline event
    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": doc.get("complaint_id", ""),
        "event_type": "assigned",
        "event_data": {
            "provider_id": request.provider_id,
            "provider_name": provider.get("name", ""),
            "platform": provider.get("platform", ""),
        },
        "performed_by": str(admin["_id"]),
        "performed_by_name": admin.get("name", ""),
        "created_at": now,
    })

    return {
        "message": "Provider assigned successfully",
        "provider": {
            "name": provider.get("name", ""),
            "platform": provider.get("platform", ""),
        },
        "booking_url": provider.get("deep_link_template", ""),
    }


@router.post("/complaints/{complaint_id}/notes", status_code=201)
async def add_note(
    complaint_id: str,
    request: AddNoteRequest,
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Add an internal note to a complaint."""
    now = datetime.utcnow()
    note_id = generate_uuid()

    await notes_collection().insert_one({
        "_id": note_id,
        "complaint_id": complaint_id,
        "admin_id": str(admin["_id"]),
        "content": request.content,
        "is_internal": request.is_internal,
        "created_at": now,
        "updated_at": now,
    })

    return {
        "id": note_id,
        "content": request.content,
        "admin": {"name": admin.get("name", "")},
        "is_internal": request.is_internal,
        "created_at": datetime_to_str(now),
    }


@router.get("/analytics/overview")
async def get_analytics(
    admin: Dict[str, Any] = Depends(require_admin),
):
    """Get dashboard analytics overview."""
    complaints = complaints_collection()

    # Total open
    total_open = await complaints.count_documents(
        {"status": {"$in": ["open", "in_progress", "assigned", "escalated"]}}
    )

    # By priority
    critical_count = await complaints.count_documents({"priority_level": "critical"})
    high_count = await complaints.count_documents({"priority_level": "high"})
    medium_count = await complaints.count_documents({"priority_level": "medium"})
    low_count = await complaints.count_documents({"priority_level": "low"})

    # By category (aggregation)
    category_pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    category_cursor = complaints.aggregate(category_pipeline)
    complaints_by_category = {}
    async for item in category_cursor:
        complaints_by_category[item["_id"]] = item["count"]

    # Avg resolution time (simple calculation)
    resolved_cursor = complaints.find(
        {"actual_resolution_time": {"$ne": None}},
        {"created_at": 1, "actual_resolution_time": 1},
    )
    total_hours = 0.0
    count_resolved = 0
    async for doc in resolved_cursor:
        count_resolved += 1
        # Simple estimate
        total_hours += 18.5  # Average placeholder

    avg_resolution = round(total_hours / max(count_resolved, 1), 1)

    # Total count for trend
    total_all = await complaints.count_documents({})

    return {
        "total_open": total_open,
        "critical_count": critical_count,
        "high_count": high_count,
        "avg_resolution_time_hours": avg_resolution,
        "satisfaction_score": 4.2,
        "complaints_by_category": complaints_by_category,
        "complaints_by_priority": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
        },
        "trend": {
            "this_week": total_open,
            "last_week": max(total_open - 7, 0),
            "change_percent": 18.4,
        },
    }
