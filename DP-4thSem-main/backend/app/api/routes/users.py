"""User routes — profile and user complaint endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, Dict, Any
from datetime import datetime
import logging
import math

from app.api.deps import get_current_user
from app.database import users_collection, complaints_collection, timeline_collection
from app.schemas.complaint import CreateComplaintRequest, EscalateRequest, PaginatedResponse, PaginationInfo
from app.utils.helpers import (
    generate_complaint_id, generate_uuid, datetime_to_str,
    format_complaint_for_response, format_timeline_for_response,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profile")
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user's profile."""
    user = current_user.copy()
    user["id"] = str(user.pop("_id"))
    user.pop("password_hash", None)
    if isinstance(user.get("created_at"), datetime):
        user["created_at"] = datetime_to_str(user["created_at"])
    if isinstance(user.get("updated_at"), datetime):
        user["updated_at"] = datetime_to_str(user["updated_at"])
    return user


@router.put("/profile")
async def update_profile(
    updates: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Update current user's profile."""
    allowed_fields = {"name", "email", "address"}
    update_data = {k: v for k, v in updates.items() if k in allowed_fields}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    update_data["updated_at"] = datetime.utcnow()

    await users_collection().update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data},
    )

    return {"message": "Profile updated successfully"}


@router.get("/complaints")
async def get_user_complaints(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Get all complaints for the current user."""
    query = {"user_id": str(current_user["_id"])}

    if status:
        query["status"] = status
    if priority:
        query["priority_level"] = priority

    total = await complaints_collection().count_documents(query)
    total_pages = math.ceil(total / limit) if total > 0 else 1

    cursor = complaints_collection().find(query).sort("created_at", -1).skip((page - 1) * limit).limit(limit)
    complaints = []
    async for doc in cursor:
        complaints.append(format_complaint_for_response(doc))

    return PaginatedResponse(
        data=complaints,
        pagination=PaginationInfo(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.post("/complaints", status_code=201)
async def create_complaint(
    request: CreateComplaintRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Register a new complaint — runs full AI pipeline for analysis, prioritization, and assignment."""
    now = datetime.utcnow()
    complaint_id_str = generate_complaint_id()
    doc_id = generate_uuid()

    # Build user info for denormalized storage
    user_info = {
        "name": current_user.get("name", ""),
        "phone": current_user.get("phone", ""),
        "address": current_user.get("address", {}),
    }

    # Run the full AI pipeline (NLU → Prioritization → Assignment)
    pipeline_result = None
    try:
        from app.agents.pipeline import run_complaint_pipeline
        pipeline_result = await run_complaint_pipeline(
            description=request.description,
            location=request.location or "",
            user_info=user_info,
            category_override=request.category,
            skip_assignment=False,
        )
    except Exception as e:
        logger.warning(f"AI pipeline failed, using defaults: {e}")

    # Extract enriched fields from the pipeline, or use defaults
    if pipeline_result:
        enriched = pipeline_result.get("enriched_fields", {})
        priority_data = pipeline_result.get("priority", {})
        priority_level = enriched.get("priority_level", "medium")
        priority_score = enriched.get("priority_score", 50.0)
        priority_reasoning = enriched.get("priority_reasoning", "")
        ai_analysis = enriched.get("ai_analysis")
        ai_category = enriched.get("category", request.category)
        ai_subcategory = enriched.get("subcategory", request.subcategory or "")
        assigned_provider_id = enriched.get("assigned_provider_id")
        estimated_resolution_time = enriched.get("estimated_resolution_time")
    else:
        priority_level = "medium"
        priority_score = 50.0
        priority_reasoning = "Default priority (pipeline unavailable)"
        ai_analysis = None
        ai_category = request.category
        ai_subcategory = request.subcategory or ""
        assigned_provider_id = None
        estimated_resolution_time = None
        priority_data = {}

    complaint_doc = {
        "_id": doc_id,
        "complaint_id": complaint_id_str,
        "user_id": str(current_user["_id"]),
        "user": user_info,
        "category": ai_category,
        "subcategory": ai_subcategory,
        "description": request.description,
        "location": request.location or "",
        "priority_level": priority_level,
        "priority_score": priority_score,
        "priority_reasoning": priority_reasoning,
        "status": "open",
        "ai_analysis": ai_analysis,
        "media_urls": request.media_urls or [],
        "assigned_provider_id": assigned_provider_id,
        "assigned_admin_id": None,
        "estimated_resolution_time": estimated_resolution_time,
        "actual_resolution_time": None,
        "user_satisfaction": None,
        "created_at": now,
        "updated_at": now,
    }

    await complaints_collection().insert_one(complaint_doc)

    # Create timeline event
    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": complaint_id_str,
        "event_type": "created",
        "event_data": {},
        "performed_by": None,
        "created_at": now,
    })

    # Create prioritization timeline event
    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": complaint_id_str,
        "event_type": "prioritized",
        "event_data": {
            "priority_level": priority_level,
            "priority_score": priority_score,
            "reasoning": priority_reasoning,
            "source": pipeline_result.get("nlu_analysis", {}).get("source", "unknown") if pipeline_result else "fallback",
        },
        "performed_by": None,
        "created_at": now,
    })

    # If provider was auto-assigned by the pipeline, log it
    if pipeline_result and assigned_provider_id:
        assignment = pipeline_result.get("assignment", {})
        await timeline_collection().insert_one({
            "_id": generate_uuid(),
            "complaint_id": complaint_id_str,
            "event_type": "assigned",
            "event_data": {
                "provider_id": assigned_provider_id,
                "provider_name": assignment.get("recommended_provider_name", ""),
                "platform": assignment.get("recommended_provider_platform", ""),
                "confidence": assignment.get("confidence", 0),
                "source": "ai_auto_assign",
            },
            "performed_by": None,
            "created_at": now,
        })

    response_time = priority_data.get("response_time", "24 hours") if priority_data else "24 hours"

    logger.info(f"Complaint created: {complaint_id_str} (priority: {priority_level}, pipeline: {'ok' if pipeline_result else 'fallback'})")

    return {
        "id": doc_id,
        "complaint_id": complaint_id_str,
        "category": ai_category,
        "priority_level": priority_level,
        "priority_score": priority_score,
        "priority_reasoning": priority_reasoning,
        "status": "open",
        "created_at": datetime_to_str(now),
        "message": f"Complaint registered successfully. Expected response time: {response_time}",
    }


@router.get("/complaints/{complaint_id}")
async def get_complaint_detail(
    complaint_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Get specific complaint details."""
    doc = await complaints_collection().find_one({
        "$or": [
            {"_id": complaint_id},
            {"complaint_id": complaint_id},
        ],
        "user_id": str(current_user["_id"]),
    })

    if not doc:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return format_complaint_for_response(doc)


@router.get("/complaints/{complaint_id}/timeline")
async def get_complaint_timeline(
    complaint_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Get timeline events for a complaint."""
    cursor = timeline_collection().find(
        {"complaint_id": complaint_id}
    ).sort("created_at", 1)

    timeline = []
    async for doc in cursor:
        timeline.append(format_timeline_for_response(doc))

    return {"complaint_id": complaint_id, "timeline": timeline}


@router.post("/complaints/{complaint_id}/escalate")
async def escalate_complaint(
    complaint_id: str,
    request: EscalateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Escalate a complaint."""
    result = await complaints_collection().update_one(
        {"complaint_id": complaint_id, "user_id": str(current_user["_id"])},
        {"$set": {
            "status": "escalated",
            "priority_level": "critical",
            "updated_at": datetime.utcnow(),
        }},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Timeline event
    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": complaint_id,
        "event_type": "escalated",
        "event_data": {"reason": request.reason},
        "performed_by": str(current_user["_id"]),
        "performed_by_name": current_user.get("name", ""),
        "created_at": datetime.utcnow(),
    })

    return {
        "message": "Complaint escalated successfully",
        "new_priority": "critical",
    }
