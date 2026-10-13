"""
api/routes/settings.py
======================
Settings endpoints: profile update and benchmark configuration.
"""

from __future__ import annotations

from bson import ObjectId
from fastapi import APIRouter, Depends

from db import get_db
from schemas import BenchmarkUpdate, ProfileUpdate, UserResponse
from services.auth_service import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    body: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update the user's name and/or business name."""
    db = get_db()
    update_fields: dict = {}
    if body.business_name is not None:
        update_fields["business_name"] = body.business_name
    if body.name is not None:
        update_fields["name"] = body.name

    if update_fields:
        await db.users.update_one(
            {"_id": ObjectId(current_user["_id"])},
            {"$set": update_fields},
        )

    # Re-fetch the user to return the updated state
    user = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    return UserResponse(
        name=user["name"],
        business_name=user["business_name"],
        email=user["email"],
        benchmark=user.get("benchmark", 78),
        created_at=user.get("created_at"),
    )


@router.patch("/benchmark", response_model=UserResponse)
async def update_benchmark(
    body: BenchmarkUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update the risk benchmark threshold."""
    db = get_db()
    await db.users.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": {"benchmark": body.benchmark}},
    )

    user = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    return UserResponse(
        name=user["name"],
        business_name=user["business_name"],
        email=user["email"],
        benchmark=user.get("benchmark", 78),
        created_at=user.get("created_at"),
    )
