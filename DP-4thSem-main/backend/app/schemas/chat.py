"""Chat request/response schemas."""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatMessageRequest(BaseModel):
    """User sends a chat message to the AI assistant."""
    message: str
    session_id: Optional[str] = None  # Re-use to continue a conversation


class ChatMetadata(BaseModel):
    """AI analysis metadata attached to chat responses."""
    detected_category: Optional[str] = None
    detected_subcategory: Optional[str] = None
    detected_priority: Optional[str] = None
    priority_score: Optional[float] = None
    confidence: Optional[float] = None
    safety_risk: Optional[bool] = None
    urgency: Optional[str] = None
    detected_language: Optional[str] = None
    key_issues: Optional[List[str]] = None


class ChatMessageResponse(BaseModel):
    """AI response returned to the frontend."""
    session_id: str
    role: str = "ai"
    content: str
    metadata: Optional[ChatMetadata] = None
    timestamp: str


class FileComplaintFromChatRequest(BaseModel):
    """User confirms filing a complaint from the chat context."""
    session_id: str
    category: Optional[str] = None       # Override AI-detected category
    subcategory: Optional[str] = None
    location: Optional[str] = ""
    description: Optional[str] = None     # If empty, we reconstruct from chat history
    media_urls: Optional[List[str]] = []


class FileComplaintFromChatResponse(BaseModel):
    """Response after filing a complaint from chat."""
    complaint_id: str
    id: str
    category: str
    priority_level: str
    priority_score: float
    status: str = "open"
    message: str
    created_at: str


class ChatSession(BaseModel):
    """A chat session summary."""
    session_id: str
    started_at: str
    last_message_at: str
    message_count: int
    filed_complaint_id: Optional[str] = None
