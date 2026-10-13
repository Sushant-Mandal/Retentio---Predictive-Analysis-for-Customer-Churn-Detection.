"""
utils/preprocess.py
===================
Schema-driven, reusable preprocessing pipeline for Retentio.

Design principles
-----------------
* All column definitions live in CONFIG — nothing is hardcoded to Telco-specific
  column names in the transformation logic. Swap CONFIG for a different dataset
  and the rest of the pipeline works unchanged.
* preprocess_training_data() — fits and returns the preprocessor (for training).
* preprocess_inference_data() — applies a *pre-fitted* preprocessor (for inference
  on live CSV uploads at backend runtime). This is the function ml_service.py will call.
* Missing value handling:
    - Numeric cols  -> median imputation (via SimpleImputer inside ColumnTransformer)
    - Categorical   -> most_frequent imputation
    - TotalCharges whitespace -> coerced to NaN before imputation picks it up
"""

from __future__ import annotations

import logging
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Schema configuration
# ---------------------------------------------------------------------------
# This is the single source of truth for column roles.
# Update only this dict if you swap to a different dataset.

CONFIG: dict = {
    # Columns to drop entirely (IDs, leak-prone, or uninformative)
    "DROP_COLS": ["customerID"],

    # Target column name and its positive-class label
    "TARGET_COL": "Churn",
    "POSITIVE_LABEL": "Yes",  # label that maps to churn=1

    # Numeric columns that get StandardScaler applied
    # SeniorCitizen is already 0/1 int -- treat as numeric (scale, don't one-hot)
    "NUMERIC_COLS": [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "SeniorCitizen",
    ],

    # Categorical columns that get OneHotEncoder applied
    "CATEGORICAL_COLS": [
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ],
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix known type issues before imputation/transformation.

    TotalCharges is stored as a string column in the Telco dataset.
    Rows where the customer just signed up (tenure=0) have a blank string ''.
    pandas.read_csv() reads this as ' ' (whitespace) -- not NaN. We coerce it
    to float and let the imputer fill the resulting NaN with the median.
    """
    df = df.copy()
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


def _drop_columns(df: pd.DataFrame, cols_to_drop: list) -> pd.DataFrame:
    """Drop columns that exist in both the config list and the DataFrame."""
    existing = [c for c in cols_to_drop if c in df.columns]
    return df.drop(columns=existing)


def _encode_target(series: pd.Series, positive_label: str) -> np.ndarray:
    """Convert the target column to binary (1 = churn, 0 = no churn)."""
    return (series == positive_label).astype(int).values


# ---------------------------------------------------------------------------
# Preprocessor builder
# ---------------------------------------------------------------------------

def build_preprocessor(
    numeric_cols: list,
    categorical_cols: list,
) -> ColumnTransformer:
    """
    Build (but do NOT fit) a ColumnTransformer that:
      - Imputes + scales numeric columns (median imputation + StandardScaler)
      - Imputes + encodes categorical columns (most_frequent + OneHotEncoder)

    Parameters
    ----------
    numeric_cols : list of column names to scale
    categorical_cols : list of column names to one-hot-encode

    Returns
    -------
    ColumnTransformer (unfitted)
    """
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols),
        ],
        remainder="drop",   # silently drop any columns not listed
    )
    return preprocessor


# ---------------------------------------------------------------------------
# Public API -- training time
# ---------------------------------------------------------------------------

def preprocess_training_data(
    df: pd.DataFrame,
    config: dict = CONFIG,
) -> Tuple[np.ndarray, np.ndarray, ColumnTransformer]:
    """
    Full preprocessing for TRAINING: coerce types, drop IDs, split X/y,
    fit the preprocessor, return transformed arrays.

    Parameters
    ----------
    df     : raw DataFrame read from the training CSV
    config : schema CONFIG dict (defaults to module-level CONFIG)

    Returns
    -------
    X      : np.ndarray -- transformed feature matrix
    y      : np.ndarray -- binary target vector (1 = churn)
    fitted_preprocessor : ColumnTransformer (fitted, ready to be pickled)
    """
    logger.info("Starting training preprocessing -- shape: %s", df.shape)

    df = _coerce_types(df)

    # Separate target before dropping anything else
    if config["TARGET_COL"] not in df.columns:
        raise ValueError(
            f"Target column '{config['TARGET_COL']}' not found in DataFrame. "
            f"Available columns: {list(df.columns)}"
        )
    y = _encode_target(df[config["TARGET_COL"]], config["POSITIVE_LABEL"])

    # Drop non-feature columns (IDs + target)
    cols_to_drop = config["DROP_COLS"] + [config["TARGET_COL"]]
    df = _drop_columns(df, cols_to_drop)

    # Resolve which numeric/categorical cols are actually present
    numeric_cols = [c for c in config["NUMERIC_COLS"] if c in df.columns]
    categorical_cols = [c for c in config["CATEGORICAL_COLS"] if c in df.columns]

    logger.info(
        "Feature split -- numeric: %d cols, categorical: %d cols",
        len(numeric_cols),
        len(categorical_cols),
    )

    preprocessor = build_preprocessor(numeric_cols, categorical_cols)
    X = preprocessor.fit_transform(df)

    logger.info("Training preprocessing done -- X shape: %s, y shape: %s", X.shape, y.shape)
    return X, y, preprocessor


# ---------------------------------------------------------------------------
# Public API -- inference time (called by ml_service.py on CSV uploads)
# ---------------------------------------------------------------------------

def preprocess_inference_data(
    df: pd.DataFrame,
    preprocessor: ColumnTransformer,
    config: dict = CONFIG,
) -> np.ndarray:
    """
    Preprocessing for INFERENCE: coerce types, drop IDs (no target expected),
    apply the pre-fitted preprocessor -- no fitting occurs.

    Parameters
    ----------
    df            : raw DataFrame from the user-uploaded CSV
    preprocessor  : fitted ColumnTransformer loaded from preprocessor.pkl
    config        : schema CONFIG dict (defaults to module-level CONFIG)

    Returns
    -------
    X : np.ndarray -- transformed feature matrix ready for model.predict_proba()
    """
    logger.info("Starting inference preprocessing -- shape: %s", df.shape)

    df = _coerce_types(df)

    # Drop ID cols if present (target col is not expected in inference CSVs)
    df = _drop_columns(df, config["DROP_COLS"])

    # Also drop target col if accidentally included in upload
    if config["TARGET_COL"] in df.columns:
        df = _drop_columns(df, [config["TARGET_COL"]])

    X = preprocessor.transform(df)
    logger.info("Inference preprocessing done -- X shape: %s", X.shape)
    return X


# ---------------------------------------------------------------------------
# Risk score helper (FR2 in PRD)
# ---------------------------------------------------------------------------

def probabilities_to_risk_scores(proba: np.ndarray) -> np.ndarray:
    """
    Convert churn probability array to risk scores (0-100).

    Implements FR2: predict_proba() * 100 = risk_score

    Parameters
    ----------
    proba : 1-D array of churn probabilities from model.predict_proba()[:, 1]

    Returns
    -------
    np.ndarray of float64, values in [0.0, 100.0], rounded to 2 decimal places
    """
    scores = np.round(proba * 100, 2)
    return scores
