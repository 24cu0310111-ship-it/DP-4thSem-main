"""Complaint request/response schemas."""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class CreateComplaintRequest(BaseModel):
    category: str
    subcategory: Optional[str] = ""
    description: str
    location: Optional[str] = ""
    media_urls: Optional[List[str]] = []


class UpdateStatusRequest(BaseModel):
    status: str
    note: Optional[str] = None


class AssignProviderRequest(BaseModel):
    provider_id: str
    estimated_time: Optional[str] = None
    notes: Optional[str] = None


class EscalateRequest(BaseModel):
    reason: str


class AddNoteRequest(BaseModel):
    content: str
    is_internal: bool = True


class PaginationInfo(BaseModel):
    page: int = 1
    limit: int = 20
    total: int = 0
    total_pages: int = 0


class PaginatedResponse(BaseModel):
    data: List[Dict[str, Any]] = []
    pagination: PaginationInfo = PaginationInfo()
