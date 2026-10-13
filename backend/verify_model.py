"""
verify_model.py
===============
Retentio EPIC 1 -- Fresh-process end-to-end verification (TICKET-106 AC).

This script must be run as a STANDALONE process (not inside the training
session) to confirm that the .pkl files are fully self-contained and load
correctly without any training-time state.

Usage
-----
    python backend/verify_model.py

Expected output: a risk score in [0, 100] for one sample customer row.
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parent   # backend/
sys.path.insert(0, str(BACKEND_DIR))

MODEL_DIR = BACKEND_DIR / "model"
MODEL_PATH = MODEL_DIR / "churn_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"


def main():
    print("\n" + "=" * 60)
    print("  Retentio -- Model Verification (Fresh Process)")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 1: Load pkl files
    # ------------------------------------------------------------------
    print("\n[1] Loading model artifacts...")
    import joblib

    if not MODEL_PATH.exists():
        print(f"  ERROR: {MODEL_PATH} not found. Run train_model.py first.")
        sys.exit(1)
    if not PREPROCESSOR_PATH.exists():
        print(f"  ERROR: {PREPROCESSOR_PATH} not found. Run train_model.py first.")
        sys.exit(1)

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    print(f"  Loaded model       : {MODEL_PATH.name}  ({MODEL_PATH.stat().st_size:,} bytes)")
    print(f"  Loaded preprocessor: {PREPROCESSOR_PATH.name}  ({PREPROCESSOR_PATH.stat().st_size:,} bytes)")
    print(f"  Model type         : {type(model).__name__}")
    print(f"  Preprocessor type  : {type(preprocessor).__name__}")

    # ------------------------------------------------------------------
    # Step 2: Construct one sample raw customer row
    #         Columns match the Telco CSV schema exactly.
    #         This mimics what ml_service.py receives from an uploaded CSV.
    # ------------------------------------------------------------------
    print("\n[2] Constructing sample raw customer row (Telco schema)...")
    import pandas as pd

    sample = {
        # This row represents a high-risk customer profile:
        # month-to-month contract, no extra services, electronic check payment
        "customerID": "TEST-0001",       # will be dropped by preprocessor
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 1,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 70.35,
        "TotalCharges": 70.35,           # new customer -- tenure=1
        # Note: 'Churn' column intentionally omitted (inference scenario)
    }

    df_sample = pd.DataFrame([sample])
    print("  Sample row:")
    for col, val in sample.items():
        print(f"    {col:<20} = {val!r}")

    # ------------------------------------------------------------------
    # Step 3: Run preprocessing
    # ------------------------------------------------------------------
    print("\n[3] Running preprocess_inference_data()...")
    from utils.preprocess import preprocess_inference_data

    X = preprocess_inference_data(df_sample, preprocessor)
    print(f"  Output shape: {X.shape}")

    # ------------------------------------------------------------------
    # Step 4: Run predict_proba and compute risk score
    # ------------------------------------------------------------------
    print("\n[4] Running model.predict_proba() -> risk_score...")
    import numpy as np
    from utils.preprocess import probabilities_to_risk_scores

    proba = model.predict_proba(X)[:, 1]   # churn probability
    risk_score = probabilities_to_risk_scores(proba)

    print(f"\n{'='*60}")
    print("  END-TO-END PREDICTION RESULT")
    print(f"{'='*60}")
    print(f"  Customer ID  : {sample['customerID']}")
    print(f"  Churn proba  : {proba[0]:.6f}")
    print(f"  Risk Score   : {risk_score[0]:.2f}  (scale: 0-100)")

    # Validation
    assert 0.0 <= risk_score[0] <= 100.0, f"Risk score out of range: {risk_score[0]}"
    print("\n  [PASS] Risk score is within valid range [0, 100]")
    print("  [PASS] Both .pkl files loaded and ran successfully in a fresh process")
    print("=" * 60)


if __name__ == "__main__":
    main()
