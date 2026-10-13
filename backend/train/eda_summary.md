# EDA Summary
**Generated:** 2026-08-20 16:34:07

## Dataset Overview
| Metric | Value |
|---|---|
| Rows | 7,043 |
| Columns | 21 |
| Source | Telco Customer Churn (Kaggle / IBM) |

## Class Balance (Target: `Churn`)

| Class | Count | Percentage |
|---|---|---|
| No | 5,174 | 73.5% |
| Yes | 1,869 | 26.5% |

> [!WARNING]
> **Class imbalance detected**: Churn=Yes is only 26.5% of the dataset.
> Strategy chosen: `class_weight='balanced'` on Logistic Regression & Random Forest;
> `scale_pos_weight` on XGBoost (ratio = n_no_churn / n_churn).

## Missing Values

- `TotalCharges`: 11 rows with whitespace-only string (read as blank, not NaN by pandas).
  → Coerced to `float`; blank rows become `NaN` and are filled with **median** during preprocessing.

| Column | Null Count |
|---|---|
| TotalCharges | 11 |

## Key Numeric Distributions

| Statistic | tenure | MonthlyCharges | TotalCharges |
|---|---|---|---|
| mean | 32.37 | 64.76 | 2283.30 |
| std | 24.56 | 30.09 | 2266.77 |
| min | 0.00 | 18.25 | 18.80 |
| 25% | 9.00 | 35.50 | 401.45 |
| 50% | 29.00 | 70.35 | 1397.47 |
| 75% | 55.00 | 89.85 | 3794.74 |
| max | 72.00 | 118.75 | 8684.80 |

## Data Types

| Column | dtype |
|---|---|
| customerID | str |
| gender | str |
| SeniorCitizen | int64 |
| Partner | str |
| Dependents | str |
| tenure | int64 |
| PhoneService | str |
| MultipleLines | str |
| InternetService | str |
| OnlineSecurity | str |
| OnlineBackup | str |
| DeviceProtection | str |
| TechSupport | str |
| StreamingTV | str |
| StreamingMovies | str |
| Contract | str |
| PaperlessBilling | str |
| PaymentMethod | str |
| MonthlyCharges | float64 |
| TotalCharges | str |
| Churn | str |

## Preprocessing Notes
- `TotalCharges` coerced from `object` -> `float64`.
- `SeniorCitizen` is already binary (0/1) -- treated as numeric, scaled but not one-hot-encoded.
- `customerID` dropped (non-predictive identifier).
- `Churn` encoded: `Yes` -> 1, `No` -> 0.