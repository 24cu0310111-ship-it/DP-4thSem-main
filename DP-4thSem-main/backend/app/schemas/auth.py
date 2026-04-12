"""Authentication request/response schemas."""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class RegisterRequest(BaseModel):
    phone: str
    email: Optional[str] = None
    name: str
    password: str
    address: Optional[Dict[str, Any]] = None


class LoginRequest(BaseModel):
    phone: str  # Can be phone number or "admin" for admin login
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class LoginUserInfo(BaseModel):
    id: str
    name: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 86400
    user: LoginUserInfo


class RegisterResponse(BaseModel):
    id: str
    phone: str
    email: Optional[str] = None
    name: str
    role: str
    created_at: str
