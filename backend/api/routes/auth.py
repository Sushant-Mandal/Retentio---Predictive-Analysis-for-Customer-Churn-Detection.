"""
api/routes/auth.py
==================
Authentication endpoints: signup, login, and current user info.
"""

from __future__ import annotations

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from db import get_db
from schemas import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from services.auth_service import (
    create_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(body: UserCreate):
    """Create a new business account and return a JWT."""
    db = get_db()

    # Check for existing email
    existing = await db.users.find_one({"email": body.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user_doc = {
        "business_name": body.business_name,
        "name": body.name,
        "email": body.email,
        "password_hash": hash_password(body.password),
        "benchmark": 78,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)

    token = create_token(user_id, body.email)
    return TokenResponse(
        token=token,
        user=UserResponse(
            name=body.name,
            business_name=body.business_name,
            email=body.email,
            benchmark=78,
            created_at=user_doc["created_at"],
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin):
    """Authenticate and return a JWT."""
    db = get_db()

    user = await db.users.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    user_id = str(user["_id"])
    token = create_token(user_id, body.email)

    return TokenResponse(
        token=token,
        user=UserResponse(
            name=user["name"],
            business_name=user["business_name"],
            email=user["email"],
            benchmark=user.get("benchmark", 78),
            created_at=user.get("created_at"),
        ),
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return UserResponse(
        name=current_user["name"],
        business_name=current_user["business_name"],
        email=current_user["email"],
        benchmark=current_user.get("benchmark", 78),
        created_at=current_user.get("created_at"),
    )
