"""Complaint models for MongoDB."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class ComplaintCategory(str, Enum):
    electricity = "electricity"
    water = "water"
    sanitation = "sanitation"
    hvac = "hvac"
    plumbing = "plumbing"
    maintenance = "maintenance"
    security = "security"
    other = "other"


class PriorityLevel(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class ComplaintStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    assigned = "assigned"
    resolved = "resolved"
    closed = "closed"
    escalated = "escalated"


class ComplaintInDB(BaseModel):
    """Full complaint document stored in MongoDB."""
    id: str = Field(alias="_id", default="")
    complaint_id: str  # e.g., CM-20240115-0001
    user_id: str
    category: ComplaintCategory
    subcategory: str = ""
    description: str
    location: str = ""
    priority_level: PriorityLevel = PriorityLevel.medium
    priority_score: float = 0.0
    priority_reasoning: Optional[str] = None
    status: ComplaintStatus = ComplaintStatus.open
    ai_analysis: Optional[Dict[str, Any]] = None
    media_urls: List[str] = []
    assigned_provider_id: Optional[str] = None
    assigned_admin_id: Optional[str] = None
    estimated_resolution_time: Optional[str] = None
    actual_resolution_time: Optional[str] = None
    user_satisfaction: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class ComplaintResponse(BaseModel):
    """Complaint data returned to the client."""
    id: str
    complaint_id: str
    user_id: str
    user: Optional[Dict[str, Any]] = None
    category: str
    subcategory: str = ""
    description: str
    location: str = ""
    priority_level: str
    priority_score: float = 0.0
    priority_reasoning: Optional[str] = None
    status: str
    ai_analysis: Optional[Dict[str, Any]] = None
    media_urls: List[str] = []
    assigned_provider_id: Optional[str] = None
    assigned_provider: Optional[Dict[str, Any]] = None
    estimated_resolution_time: Optional[str] = None
    actual_resolution_time: Optional[str] = None
    user_satisfaction: Optional[int] = None
    created_at: str = ""
    updated_at: str = ""
