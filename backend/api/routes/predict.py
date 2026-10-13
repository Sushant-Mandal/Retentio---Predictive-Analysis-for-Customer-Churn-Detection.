"""
api/routes/predict.py
=====================
Prediction endpoints: CSV upload + ML inference, and CSV template download.
"""

from __future__ import annotations

import io
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from schemas.customer_schema import PredictResponse
from services.auth_service import get_current_user
from services.customer_service import upsert_customers
from services.ml_service import predict

router = APIRouter(prefix="/predict", tags=["predict"])

# ── CSV template columns (Telco schema) ─────────────────────────────────────

TEMPLATE_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges",
]


@router.post("/upload", response_model=PredictResponse)
async def upload_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Upload a customer CSV, run the ML model, upsert results into MongoDB,
    and return at-risk / saved customer lists.
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    # Read CSV
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=413, detail="File too large. Maximum 10 MB.")

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}")

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV is empty.")

    # Get user benchmark
    benchmark = current_user.get("benchmark", 78)
    user_id = current_user["_id"]

    # Run ML prediction
    try:
        _at_risk, all_scores = predict(df, benchmark=benchmark)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction error: {exc}")

    # Upsert into MongoDB and get final at-risk / saved lists
    result = await upsert_customers(user_id, all_scores, benchmark=benchmark)

    at_risk = result["at_risk"]
    saved = result["saved"]
    saved_message: Optional[str] = None if saved else "No customers saved yet."

    return PredictResponse(
        total_rows=len(df),
        at_risk=at_risk,
        saved=saved,
        saved_message=saved_message,
    )


@router.get("/template")
async def download_template():
    """Download a sample CSV template with the expected column headers."""
    df = pd.DataFrame(columns=TEMPLATE_COLUMNS)
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=retentio_template.csv"},
    )
