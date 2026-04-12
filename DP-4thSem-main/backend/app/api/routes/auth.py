"""Authentication routes — register, login, refresh."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging

from app.database import users_collection
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenRefreshRequest,
    LoginResponse, LoginUserInfo, RegisterResponse,
)
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from app.utils.helpers import generate_uuid

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(request: RegisterRequest):
    """Register a new user account."""
    users = users_collection()

    # Check if phone already exists
    existing = await users.find_one({"phone": request.phone})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    # Check if email already exists
    if request.email:
        existing_email = await users.find_one({"email": request.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    now = datetime.utcnow()
    user_id = generate_uuid()

    user_doc = {
        "_id": user_id,
        "phone": request.phone,
        "email": request.email,
        "name": request.name,
        "password_hash": hash_password(request.password),
        "role": "user",
        "address": request.address or {},
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }

    await users.insert_one(user_doc)
    logger.info(f"User registered: {request.phone}")

    return RegisterResponse(
        id=user_id,
        phone=request.phone,
        email=request.email,
        name=request.name,
        role="user",
        created_at=now.isoformat() + "Z",
    )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login with phone/admin-id and password."""
    users = users_collection()

    # Support "admin" as a special login identifier
    if request.phone == "admin":
        user = await users.find_one({"role": "admin"})
    else:
        user = await users.find_one({"phone": request.phone})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(request.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    # Create tokens
    token_data = {"sub": str(user["_id"]), "role": user["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    logger.info(f"User logged in: {user['phone']} (role: {user['role']})")

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=86400,
        user=LoginUserInfo(
            id=str(user["_id"]),
            name=user["name"],
            role=user["role"],
        ),
    )


@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest):
    """Refresh an access token using a refresh token."""
    payload = decode_token(request.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    token_data = {"sub": payload["sub"], "role": payload.get("role", "user")}
    new_access_token = create_access_token(token_data)

    return {
        "access_token": new_access_token,
        "expires_in": 86400,
    }
