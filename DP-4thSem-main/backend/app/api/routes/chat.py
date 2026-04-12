"""Chat routes — AI-powered complaint intake assistant."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from app.api.deps import get_current_user
from app.database import chat_collection, complaints_collection, timeline_collection
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatMetadata,
    FileComplaintFromChatRequest,
    FileComplaintFromChatResponse,
)
from app.agents.sarvam_llm import sarvam_chat
from app.agents.pipeline import run_complaint_pipeline, analyze_for_chat
from app.utils.helpers import generate_uuid, generate_complaint_id, datetime_to_str

logger = logging.getLogger(__name__)
router = APIRouter()

# System prompt for the conversational AI assistant
CHAT_SYSTEM_PROMPT = """You are the AI assistant for SCMS (Smart Complaint Management System).
Your role is to help users file complaints about urban infrastructure issues like
plumbing, electricity, water, HVAC, sanitation, maintenance, and security.

Guidelines:
- Be friendly, professional, and empathetic.
- Ask clarifying questions to understand the issue fully (what, where, when, severity).
- Once you have enough information, summarize the issue and ask the user to confirm filing.
- Support multilingual input (English, Hindi, Tamil, etc.) — respond in the user's language.
- Keep responses concise (2-4 sentences max).
- If the user says "yes", "file it", "proceed", "confirm", indicate you're ready to file.
- Do NOT use markdown headers or long paragraphs. Be conversational.

You should detect and mention:
- The category of the issue (electricity, water, plumbing, sanitation, hvac, maintenance, security)
- How urgent it seems
- If there's a safety risk

When you have enough detail, end with:
"Would you like me to file this complaint now?"
"""


@router.post("/chat", response_model=ChatMessageResponse)
async def chat_message(
    request: ChatMessageRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Send a message to the AI complaint assistant.
    Returns the AI response with NLU metadata (detected category, priority, confidence).
    """
    user_id = str(current_user["_id"])
    now = datetime.utcnow()

    # Get or create session
    session_id = request.session_id or generate_uuid()

    # Store user message
    user_msg_doc = {
        "_id": generate_uuid(),
        "session_id": session_id,
        "user_id": user_id,
        "role": "user",
        "content": request.message,
        "metadata": None,
        "created_at": now,
    }
    await chat_collection().insert_one(user_msg_doc)

    # Fetch conversation history for context
    history_cursor = chat_collection().find(
        {"session_id": session_id}
    ).sort("created_at", 1)

    messages_for_llm = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
    async for doc in history_cursor:
        role = "assistant" if doc["role"] == "ai" else "user"
        messages_for_llm.append({"role": role, "content": doc["content"]})

    # Generate AI response via Sarvam
    ai_content = await sarvam_chat(
        messages=messages_for_llm,
        temperature=0.3,
        max_tokens=512,
    )

    # Fallback response if AI is unavailable
    if not ai_content:
        ai_content = _generate_fallback_response(request.message)

    # Run NLU analysis on the user's message for metadata
    analysis = await analyze_for_chat(request.message)

    # Build metadata
    metadata = None
    if analysis.get("detected_category") and analysis["detected_category"] != "other":
        metadata = ChatMetadata(
            detected_category=analysis.get("detected_category"),
            detected_subcategory=analysis.get("detected_subcategory"),
            detected_priority=analysis.get("detected_priority"),
            priority_score=analysis.get("priority_score"),
            confidence=analysis.get("confidence"),
            safety_risk=analysis.get("safety_risk"),
            urgency=analysis.get("urgency"),
            detected_language=analysis.get("detected_language"),
            key_issues=analysis.get("key_issues"),
        )

    # Store AI response
    ai_msg_doc = {
        "_id": generate_uuid(),
        "session_id": session_id,
        "user_id": user_id,
        "role": "ai",
        "content": ai_content,
        "metadata": metadata.model_dump() if metadata else None,
        "created_at": datetime.utcnow(),
    }
    await chat_collection().insert_one(ai_msg_doc)

    return ChatMessageResponse(
        session_id=session_id,
        role="ai",
        content=ai_content,
        metadata=metadata,
        timestamp=datetime_to_str(datetime.utcnow()),
    )


@router.post("/chat/file-complaint", response_model=FileComplaintFromChatResponse)
async def file_complaint_from_chat(
    request: FileComplaintFromChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    File a real complaint from a chat conversation.
    Pulls context from the chat history and runs the full AI pipeline.
    """
    user_id = str(current_user["_id"])
    now = datetime.utcnow()

    # Gather description from chat history if not provided
    description = request.description
    if not description:
        history_cursor = chat_collection().find(
            {"session_id": request.session_id, "role": "user"}
        ).sort("created_at", 1)

        user_messages = []
        async for doc in history_cursor:
            user_messages.append(doc["content"])

        if not user_messages:
            raise HTTPException(
                status_code=400,
                detail="No messages found in this chat session",
            )
        description = " | ".join(user_messages)

    # Build user info
    user_info = {
        "name": current_user.get("name", ""),
        "phone": current_user.get("phone", ""),
        "address": current_user.get("address", {}),
    }

    # Run the full AI pipeline
    pipeline_result = await run_complaint_pipeline(
        description=description,
        location=request.location or "",
        user_info=user_info,
        category_override=request.category,
        skip_assignment=False,
    )

    enriched = pipeline_result.get("enriched_fields", {})
    priority_data = pipeline_result.get("priority", {})

    complaint_id_str = generate_complaint_id()
    doc_id = generate_uuid()

    complaint_doc = {
        "_id": doc_id,
        "complaint_id": complaint_id_str,
        "user_id": user_id,
        "user": user_info,
        "category": enriched.get("category", request.category or "other"),
        "subcategory": enriched.get("subcategory", request.subcategory or ""),
        "description": description,
        "location": request.location or "",
        "priority_level": enriched.get("priority_level", "medium"),
        "priority_score": enriched.get("priority_score", 50.0),
        "priority_reasoning": enriched.get("priority_reasoning", ""),
        "status": "open",
        "ai_analysis": enriched.get("ai_analysis"),
        "media_urls": request.media_urls or [],
        "assigned_provider_id": enriched.get("assigned_provider_id"),
        "assigned_admin_id": None,
        "estimated_resolution_time": enriched.get("estimated_resolution_time"),
        "actual_resolution_time": None,
        "user_satisfaction": None,
        "chat_session_id": request.session_id,
        "created_at": now,
        "updated_at": now,
    }

    await complaints_collection().insert_one(complaint_doc)

    # Create timeline events
    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": complaint_id_str,
        "event_type": "created",
        "event_data": {"source": "ai_chat", "session_id": request.session_id},
        "performed_by": None,
        "created_at": now,
    })

    await timeline_collection().insert_one({
        "_id": generate_uuid(),
        "complaint_id": complaint_id_str,
        "event_type": "prioritized",
        "event_data": {
            "priority_level": enriched.get("priority_level", "medium"),
            "priority_score": enriched.get("priority_score", 50.0),
            "reasoning": enriched.get("priority_reasoning", ""),
            "source": pipeline_result.get("nlu_analysis", {}).get("source", "unknown"),
        },
        "performed_by": None,
        "created_at": now,
    })

    # If provider was auto-assigned, add timeline event
    assignment = pipeline_result.get("assignment")
    if assignment and assignment.get("recommended_provider_id"):
        await timeline_collection().insert_one({
            "_id": generate_uuid(),
            "complaint_id": complaint_id_str,
            "event_type": "assigned",
            "event_data": {
                "provider_id": assignment["recommended_provider_id"],
                "provider_name": assignment.get("recommended_provider_name", ""),
                "platform": assignment.get("recommended_provider_platform", ""),
                "confidence": assignment.get("confidence", 0),
                "reasoning": assignment.get("reasoning", ""),
                "source": "ai_auto_assign",
            },
            "performed_by": None,
            "created_at": now,
        })

    # Mark the chat session as having filed a complaint
    await chat_collection().insert_one({
        "_id": generate_uuid(),
        "session_id": request.session_id,
        "user_id": user_id,
        "role": "system",
        "content": f"Complaint filed: {complaint_id_str}",
        "metadata": {"complaint_id": complaint_id_str, "doc_id": doc_id},
        "created_at": datetime.utcnow(),
    })

    response_time = priority_data.get("response_time", "24 hours")

    return FileComplaintFromChatResponse(
        complaint_id=complaint_id_str,
        id=doc_id,
        category=enriched.get("category", "other"),
        priority_level=enriched.get("priority_level", "medium"),
        priority_score=enriched.get("priority_score", 50.0),
        status="open",
        message=(
            f"Complaint registered successfully. "
            f"Expected response time: {response_time}"
        ),
        created_at=datetime_to_str(now),
    )


@router.get("/chat/history")
async def get_chat_history(
    session_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get chat history — either a specific session or a list of all sessions.
    """
    user_id = str(current_user["_id"])

    if session_id:
        # Return messages for a specific session
        cursor = chat_collection().find(
            {"session_id": session_id, "user_id": user_id}
        ).sort("created_at", 1)

        messages = []
        async for doc in cursor:
            messages.append({
                "id": str(doc["_id"]),
                "role": doc["role"],
                "content": doc["content"],
                "metadata": doc.get("metadata"),
                "timestamp": datetime_to_str(doc.get("created_at", datetime.utcnow())),
            })

        return {"session_id": session_id, "messages": messages}

    # Return list of sessions
    pipeline = [
        {"$match": {"user_id": user_id, "role": {"$ne": "system"}}},
        {"$group": {
            "_id": "$session_id",
            "started_at": {"$min": "$created_at"},
            "last_message_at": {"$max": "$created_at"},
            "message_count": {"$sum": 1},
            "first_message": {"$first": "$content"},
        }},
        {"$sort": {"last_message_at": -1}},
        {"$limit": 20},
    ]

    cursor = chat_collection().aggregate(pipeline)
    sessions = []
    async for doc in cursor:
        sessions.append({
            "session_id": doc["_id"],
            "started_at": datetime_to_str(doc["started_at"]),
            "last_message_at": datetime_to_str(doc["last_message_at"]),
            "message_count": doc["message_count"],
            "preview": doc.get("first_message", "")[:100],
        })

    return {"sessions": sessions}


def _generate_fallback_response(user_message: str) -> str:
    """Generate a deterministic fallback when Sarvam AI is unavailable."""
    lower = user_message.lower()

    if any(w in lower for w in ["leak", "pipe", "plumb", "drain", "toilet", "sink"]):
        return (
            "I've detected this as a **plumbing issue**. "
            "This sounds like it could be urgent if there's active leaking. "
            "Can you tell me exactly where the problem is located?\n\n"
            "Would you like me to file this complaint now?"
        )
    elif any(w in lower for w in ["power", "electric", "light", "spark", "wire", "switch"]):
        return (
            "This appears to be an **electrical issue**. "
            "Electrical problems can be safety-critical. "
            "Can you confirm which area is affected?\n\n"
            "Would you like me to file this complaint now?"
        )
    elif any(w in lower for w in ["water", "tap", "supply", "tank", "pressure"]):
        return (
            "I've identified this as a **water supply issue**. "
            "Can you tell me more about the severity — is it a complete outage or low pressure?\n\n"
            "Would you like me to file this complaint now?"
        )
    elif any(w in lower for w in ["ac", "cool", "heat", "hvac", "temperature", "fan"]):
        return (
            "This seems to be an **HVAC issue**. "
            "Is this affecting a residential unit or a commercial space? "
            "That helps me set the right priority.\n\n"
            "Would you like me to file this complaint now?"
        )
    elif any(w in lower for w in ["garbage", "trash", "waste", "clean", "pest", "smell"]):
        return (
            "I've detected a **sanitation issue**. "
            "How long has this been going on? "
            "Is it affecting common areas or just your unit?\n\n"
            "Would you like me to file this complaint now?"
        )
    elif any(w in lower for w in ["lock", "security", "gate", "cctv", "camera", "theft"]):
        return (
            "This looks like a **security concern**. "
            "Security issues are treated with high priority. "
            "Can you describe the exact location?\n\n"
            "Would you like me to file this complaint now?"
        )
    elif any(w in lower for w in ["yes", "file", "proceed", "confirm", "go ahead"]):
        return (
            "✅ Great! I'll file this complaint for you now. "
            "Please click the **File Complaint** button to confirm the details."
        )
    elif any(w in lower for w in ["hi", "hello", "hey", "start"]):
        return (
            "Hello! I'm here to help you file a complaint. "
            "Please describe the issue you're facing — "
            "for example, a water leak, power outage, broken lock, etc."
        )
    else:
        return (
            "I understand. Could you provide more details about the issue? "
            "For example:\n"
            "- What type of problem is it? (plumbing, electrical, water, etc.)\n"
            "- Where exactly is it located?\n"
            "- How urgent is it?"
        )
