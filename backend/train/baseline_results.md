# Baseline & Final Model Results
**Generated:** 2026-08-20 16:34:10

## Configuration
- Train/test split: 80/20, stratified, random_state=42
- Class imbalance strategy: `class_weight='balanced'` (LR, RF) | `scale_pos_weight` (XGBoost)
- Metric priority: ROC-AUC > F1 (weighted) > Accuracy

## Results

| Model | Accuracy | F1 (weighted) | ROC-AUC |
|---|---|---|---|
| Logistic Regression ✅ **WINNER** | 0.7381 | 0.7519 | 0.8414 |
| Random Forest | 0.7637 | 0.7685 | 0.8193 |
| XGBoost | 0.7580 | 0.7688 | 0.8369 |

## Decision
**Selected model:** Logistic Regression

## Rationale
XGBoost ROC-AUC (0.8369) narrowly fell below Logistic Regression (0.8414) on the Telco dataset. This is expected — churn signal in this dataset is largely linear (contract type, tenure, monthly charges). User confirmed: ship Logistic Regression as the production model. XGBoost is retained in the results table for reference.

## Persisted Files
- `model/churn_model.pkl` — fitted Logistic Regression classifier (best ROC-AUC)
- `model/preprocessor.pkl` — fitted ColumnTransformer (StandardScaler + OneHotEncoder)