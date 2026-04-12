"""User models for MongoDB."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"


class Address(BaseModel):
    flat_no: str = ""
    building: str = ""
    street: Optional[str] = None
    area: str = ""
    city: str = ""
    state: Optional[str] = None
    pincode: str = ""
    coordinates: Optional[dict] = None


class UserInDB(BaseModel):
    """Full user document stored in MongoDB."""
    id: str = Field(alias="_id", default="")
    phone: str
    email: Optional[str] = None
    name: str
    password_hash: str = ""
    role: UserRole = UserRole.user
    address: Address = Address()
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class UserResponse(BaseModel):
    """User data returned to the client (no password)."""
    id: str
    phone: str
    email: Optional[str] = None
    name: str
    role: str
    address: Optional[Address] = None
    is_active: bool = True
    created_at: str = ""
    updated_at: str = ""
