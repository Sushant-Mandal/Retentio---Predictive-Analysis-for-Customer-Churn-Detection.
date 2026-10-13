"""
api/routes/dashboard.py
=======================
Dashboard endpoints: summary cards and trend data.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from schemas.customer_schema import DashboardSummary, DashboardTrend, TrendPoint
from services.auth_service import get_current_user
from services.customer_service import get_dashboard_summary, get_dashboard_trend

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def summary(current_user: dict = Depends(get_current_user)):
    """Aggregated totals for the dashboard summary cards."""
    user_id = current_user["_id"]
    return await get_dashboard_summary(user_id)


@router.get("/trend", response_model=DashboardTrend)
async def trend(current_user: dict = Depends(get_current_user)):
    """Risk score trend data for the dashboard chart."""
    user_id = current_user["_id"]
    points = await get_dashboard_trend(user_id)
    return DashboardTrend(
        points=[TrendPoint(**p) for p in points]
    )
