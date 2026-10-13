"""
services/ml_service.py
======================
ML model loading and inference.

Loads churn_model.pkl + preprocessor.pkl once (at import / startup) and
exposes a predict() function that accepts a raw pandas DataFrame from a
user-uploaded CSV and returns per-row risk scores.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ── Paths ───────────────────────────────────────────────────────────────────

BACKEND_DIR = Path(__file__).resolve().parent.parent  # backend/
MODEL_DIR = BACKEND_DIR / "model"
MODEL_PATH = MODEL_DIR / "churn_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"

# ── Module-level singletons (loaded once) ───────────────────────────────────

_model = None
_preprocessor = None


def load_model() -> None:
    """Load the trained model and preprocessor from disk. Call once at startup."""
    global _model, _preprocessor

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(f"Preprocessor file not found: {PREPROCESSOR_PATH}")

    _model = joblib.load(MODEL_PATH)
    _preprocessor = joblib.load(PREPROCESSOR_PATH)

    logger.info(
        "ML model loaded — model=%s, preprocessor=%s",
        type(_model).__name__,
        type(_preprocessor).__name__,
    )


def predict(df: pd.DataFrame, benchmark: int = 78) -> Tuple[List[dict], List[dict]]:
    """
    Run churn prediction on a raw customer DataFrame.

    Parameters
    ----------
    df        : Raw DataFrame from the uploaded CSV.
    benchmark : Risk score threshold. Customers at or above this are "At Risk".

    Returns
    -------
    (at_risk, all_scores) where each entry is a dict with
    customer_id, name (if available), score, status.
    """
    if _model is None or _preprocessor is None:
        raise RuntimeError("ML model not loaded. Call load_model() first.")

    # Import the preprocessing pipeline from utils
    import sys
    sys.path.insert(0, str(BACKEND_DIR))
    from utils.preprocess import preprocess_inference_data, probabilities_to_risk_scores

    # Keep a copy of IDs / names before preprocessing drops them
    ids = df["customerID"].tolist() if "customerID" in df.columns else [f"C-{i}" for i in range(len(df))]
    # Some datasets may have a 'name' column; fall back to ID
    names = df["name"].tolist() if "name" in df.columns else ids

    # Preprocess and predict
    X = preprocess_inference_data(df, _preprocessor)
    proba = _model.predict_proba(X)[:, 1]
    scores = probabilities_to_risk_scores(proba)

    # Build result rows
    all_scores: List[dict] = []
    for i, (cid, name, score) in enumerate(zip(ids, names, scores)):
        row = {
            "customer_id": str(cid),
            "name": str(name),
            "score": round(float(score), 2),
            "status": "At Risk" if score >= benchmark else "Healthy",
        }
        all_scores.append(row)

    at_risk = [r for r in all_scores if r["status"] == "At Risk"]
    return at_risk, all_scores
