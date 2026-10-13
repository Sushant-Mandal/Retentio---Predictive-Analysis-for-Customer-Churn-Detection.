"""
schemas/customer_schema.py
==========================
Pydantic models for customer, prediction, and dashboard responses.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


# ── Customer models ─────────────────────────────────────────────────────────

class ScoreHistoryEntry(BaseModel):
    date: str
    score: float


class CustomerRow(BaseModel):
    customer_id: str
    name: str
    score: float
    meta: Optional[str] = None
    status: str = "At Risk"


class CustomerDetail(BaseModel):
    customer_id: str
    name: str
    current_score: float
    status: str
    history: List[ScoreHistoryEntry] = []


# ── Predict response ────────────────────────────────────────────────────────

class PredictResponse(BaseModel):
    total_rows: int
    at_risk: List[CustomerRow]
    saved: List[CustomerRow]
    saved_message: Optional[str] = None


# ── Dashboard response ──────────────────────────────────────────────────────

class DashboardSummary(BaseModel):
    total_customers: int
    at_risk_count: int
    saved_count: int
    avg_score: float


class TrendPoint(BaseModel):
    date: str
    avg_score: float
    at_risk_count: int


class DashboardTrend(BaseModel):
    points: List[TrendPoint]
