"""Database models for the application."""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Text,
    ForeignKey,
    Integer,
    Numeric,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, INET
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()


# --- Enums ---

class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"


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


class TimelineEventType(str, Enum):
    created = "created"
    prioritized = "prioritized"
    assigned = "assigned"
    status_changed = "status_changed"
    provider_booked = "provider_booked"
    resolved = "resolved"
    escalated = "escalated"
    commented = "commented"


# --- Models ---

class User(Base):
    """User model for residents and admins."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.user)
    address = Column(JSONB, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id")
    assigned_complaints = relationship("Complaint", back_populates="assigned_admin", foreign_keys="Complaint.assigned_admin_id")
    timeline_events = relationship("ComplaintTimeline", back_populates="performed_by")
    notes = relationship("AdminNote", back_populates="admin")

    __table_args__ = (
        Index("idx_users_role", "role"),
    )

    def __repr__(self):
        return f"<User {self.name} ({self.phone})>"


class Complaint(Base):
    """Complaint model for tracking user issues."""

    __tablename__ = "complaints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(String(20), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category = Column(SQLEnum(ComplaintCategory), nullable=False)
    subcategory = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    priority_level = Column(SQLEnum(PriorityLevel), nullable=False)
    priority_score = Column(Numeric(5, 2), default=0)
    priority_reasoning = Column(Text, nullable=True)
    status = Column(SQLEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.open)
    ai_analysis = Column(JSONB, nullable=True)
    media_urls = Column(ARRAY(String), nullable=True)
    assigned_provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.id"), nullable=True)
    assigned_admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    estimated_resolution_time = Column(DateTime(timezone=True), nullable=True)
    actual_resolution_time = Column(DateTime(timezone=True), nullable=True)
    user_satisfaction = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])
    assigned_admin = relationship("User", back_populates="assigned_complaints", foreign_keys=[assigned_admin_id])
    assigned_provider = relationship("ServiceProvider", back_populates="complaints")
    timeline = relationship("ComplaintTimeline", back_populates="complaint", order_by="ComplaintTimeline.created_at")
    notes = relationship("AdminNote", back_populates="complaint")

    __table_args__ = (
        Index("idx_complaints_status", "status"),
        Index("idx_complaints_priority", "priority_level"),
        Index("idx_complaints_category", "category"),
        Index("idx_complaints_created", "created_at", postgresql_using="btree", postgresql_ops={"created_at": "DESC"}),
    )

    def __repr__(self):
        return f"<Complaint {self.complaint_id} - {self.status}>"


class ServiceProvider(Base):
    """Service provider from external platforms."""

    __tablename__ = "service_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(SQLEnum(ProviderPlatform), nullable=False, index=True)
    platform_provider_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    service_types = Column(ARRAY(String), nullable=False)
    rating = Column(Numeric(3, 2), nullable=False, default=0)
    reviews_count = Column(Integer, default=0)
    price_range = Column(SQLEnum(PriceRange), nullable=False)
    service_areas = Column(ARRAY(String), nullable=False)
    availability_status = Column(SQLEnum(ProviderAvailability), default=ProviderAvailability.available)
    avg_response_time = Column(Integer, nullable=True)
    deep_link_template = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    complaints = relationship("Complaint", back_populates="assigned_provider")

    __table_args__ = (
        Index("idx_providers_availability", "availability_status"),
    )

    def __repr__(self):
        return f"<ServiceProvider {self.name} ({self.platform})>"


class ComplaintTimeline(Base):
    """Timeline events for complaints."""

    __tablename__ = "complaint_timeline"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), nullable=False, index=True)
    event_type = Column(SQLEnum(TimelineEventType), nullable=False, index=True)
    event_data = Column(JSONB, nullable=False)
    performed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    # Relationships
    complaint = relationship("Complaint", back_populates="timeline")
    performed_by = relationship("User", back_populates="timeline_events")

    def __repr__(self):
        return f"<TimelineEvent {self.event_type} for {self.complaint_id}>"


class AdminNote(Base):
    """Internal notes for complaints."""

    __tablename__ = "admin_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), nullable=False, index=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    complaint = relationship("Complaint", back_populates="notes")
    admin = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<AdminNote for {self.complaint_id}>"


class AuditLog(Base):
    """Audit log for tracking actions."""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    details = Column(JSONB, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AuditLog {self.action} by {self.user_id}>"
