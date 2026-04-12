"""Timeline and notes models for MongoDB."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class TimelineEventType(str, Enum):
    created = "created"
    prioritized = "prioritized"
    assigned = "assigned"
    status_changed = "status_changed"
    provider_booked = "provider_booked"
    resolved = "resolved"
    escalated = "escalated"
    commented = "commented"


class TimelineEventInDB(BaseModel):
    """Timeline event document stored in MongoDB."""
    id: str = Field(alias="_id", default="")
    complaint_id: str
    event_type: TimelineEventType
    event_data: Dict[str, Any] = {}
    performed_by: Optional[str] = None
    performed_by_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class TimelineEventResponse(BaseModel):
    """Timeline event returned to the client."""
    id: str
    complaint_id: str
    event_type: str
    event_data: Dict[str, Any] = {}
    performed_by: Optional[str] = None
    performed_by_name: Optional[str] = None
    created_at: str = ""


class AdminNoteInDB(BaseModel):
    """Admin note document stored in MongoDB."""
    id: str = Field(alias="_id", default="")
    complaint_id: str
    admin_id: str
    content: str
    is_internal: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
