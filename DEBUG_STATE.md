# RETENTIO — Debug State

## All Tasks Complete

---

## Task 1 — Login Failure: PASS

**Root cause:** User `maya@northstar.co` does not exist in the database — login correctly returns 401.
Login route itself works: valid user → 200 + JWT; invalid creds → 401.
Shared root cause with Task 2 (no users could be registered due to bcrypt crash).

**Verification:**
- `POST /api/v1/auth/login` with valid user → 200 ✅
- `POST /api/v1/auth/login` with wrong password → 401 ✅
- `GET /api/v1/auth/me` with Bearer token → 200 ✅

---

## Task 2 — Signup HTTP 500: PASS

**Root cause:** `bcrypt 5.0.0` installed; incompatible with `passlib 1.7.4`.
- `bcrypt >= 4.1.0` removed `__about__` attribute used by passlib to detect version.
- Crash occurs at `pwd_context.hash(password)` during signup.
- The exception propagates as an unhandled 500 with no detail body.

**Fix:** Downgraded `bcrypt` to `4.0.1` in the active `venv`. Pinned `bcrypt==4.0.1` in `requirements.txt`.

**Files changed:**
- `backend/requirements.txt` — added `bcrypt==4.0.1` pin
- `backend/venv` — `bcrypt` downgraded from 5.0.0 to 4.0.1 (live, no restart needed)

**Verification:**
- `POST /api/v1/auth/signup` → 201 + JWT ✅
- `POST /api/v1/auth/login` with registered email → 200 ✅
- `POST /api/v1/auth/login` with wrong password → 401 ✅
- `GET /api/v1/auth/me` with JWT → 200 ✅
- Duplicate email handling: 409 (code path verified, not re-tested)

---

## Task 3 — Editor Import Warnings: PASS

**Root cause:** Editor was using `.venv` (11MB, near-empty — only pip/setuptools installed).
`dotenv` and `motor` are only in `venv` (402MB, full dependency set).

**Fix:** Created `F:\Retentio\.vscode\settings.json` pointing `python.defaultInterpreterPath` to `backend/venv/Scripts/python.exe`.

Also fixed stale filename in `backend/db/__init__.py` docstring (`mongo_client.py` → `__init__.py`).

**Action required:** Reload the VS Code window (Ctrl+Shift+P → "Developer: Reload Window") for the new interpreter setting to take effect. The red underlines will clear once Pylance reindexes against `venv`.

---

## Task 4 — Duplicate Virtual Environments: AWAITING APPROVAL

| | `backend/venv` | `backend/.venv` |
|-|----------------|-----------------|
| **Used by** | Uvicorn process (PID 8460) | Nothing (editor was selecting it by default) |
| **Size** | ~402 MB | ~11 MB |
| **Packages** | Full: fastapi, uvicorn, motor, passlib, bcrypt, pandas, scikit-learn, xgboost, etc. | Near-empty: only pip + setuptools |
| **Python** | 3.13.14 | 3.13.14 |

**Recommendation:** Delete `backend/.venv`. It is an empty orphan environment with no packages and nothing depends on it. The `.vscode/settings.json` now explicitly points the editor to `backend/venv`, so `.venv` serves no purpose.

**⚠️ Awaiting your approval before deletion.**
To delete after approval: `Remove-Item -Recurse -Force F:\Retentio\backend\.venv`

---

## No Remaining Blockers

---

## ML Model & Prediction CSV Schema Specification

### 1. Required Column Names, Data Types, and Example Values
Total 19 required feature columns (plus 1 optional identifier column `customerID`):

| Column Name | Required By | Data Type | Example Value | Description |
|---|---|---|---|---|
| `customerID` | API / ID tracking | string | `7590-VHVEG` | Optional for model (defaults to `C-{i}`), but required by template |
| `gender` | Model (cat) | string | `Female` | Customer gender |
| `SeniorCitizen` | Model (num) | int (0/1) | `0` | Binary indicator (treated as numeric) |
| `Partner` | Model (cat) | string | `Yes` | Partner status |
| `Dependents` | Model (cat) | string | `No` | Dependents status |
| `tenure` | Model (num) | int/float | `1` | Months with company |
| `PhoneService` | Model (cat) | string | `No` | Phone service subscription |
| `MultipleLines` | Model (cat) | string | `No phone service` | Multiple phone lines |
| `InternetService` | Model (cat) | string | `DSL` | Internet provider type |
| `OnlineSecurity` | Model (cat) | string | `No` | Online security add-on |
| `OnlineBackup` | Model (cat) | string | `Yes` | Online backup add-on |
| `DeviceProtection` | Model (cat) | string | `No` | Device protection add-on |
| `TechSupport` | Model (cat) | string | `No` | Tech support add-on |
| `StreamingTV` | Model (cat) | string | `No` | Streaming TV add-on |
| `StreamingMovies` | Model (cat) | string | `No` | Streaming movies add-on |
| `Contract` | Model (cat) | string | `Month-to-month` | Contract terms |
| `PaperlessBilling` | Model (cat) | string | `Yes` | Paperless billing enrollment |
| `PaymentMethod` | Model (cat) | string | `Electronic check` | Payment method |
| `MonthlyCharges` | Model (num) | float | `29.85` | Monthly billing amount |
| `TotalCharges` | Model (num) | float / string | `29.85` | Total amount charged (blanks/whitespace handled) |

### 2. Expected Categorical Values and Missing-Value Rules
- **Expected Categorical Values:**
  - `gender`: `Female`, `Male`
  - `Partner`: `No`, `Yes`
  - `Dependents`: `No`, `Yes`
  - `PhoneService`: `No`, `Yes`
  - `MultipleLines`: `No`, `No phone service`, `Yes`
  - `InternetService`: `DSL`, `Fiber optic`, `No`
  - `OnlineSecurity`: `No`, `No internet service`, `Yes`
  - `OnlineBackup`: `No`, `No internet service`, `Yes`
  - `DeviceProtection`: `No`, `No internet service`, `Yes`
  - `TechSupport`: `No`, `No internet service`, `Yes`
  - `StreamingTV`: `No`, `No internet service`, `Yes`
  - `StreamingMovies`: `No`, `No internet service`, `Yes`
  - `Contract`: `Month-to-month`, `One year`, `Two year`
  - `PaperlessBilling`: `No`, `Yes`
  - `PaymentMethod`: `Bank transfer (automatic)`, `Credit card (automatic)`, `Electronic check`, `Mailed check`
  - *Note on Unseen Categories:* OneHotEncoder uses `handle_unknown="ignore"` (unseen strings encode as all-zeros).
- **Missing-Value Rules:**
  - `TotalCharges`: Whitespace strings (e.g. `" "`) are coerced to `NaN` via `pd.to_numeric(..., errors="coerce")`.
  - Numeric columns (`tenure`, `MonthlyCharges`, `TotalCharges`, `SeniorCitizen`): Missing values (`NaN`) are imputed with the median (`SimpleImputer(strategy="median")`).
  - Categorical columns (all 15): Missing values are imputed with the most frequent category (`SimpleImputer(strategy="most_frequent")`).
  - Missing column headers: All 19 feature columns must be present; if any column is missing from the CSV header, `ColumnTransformer` raises `ValueError: columns are missing: {...}`.

### 3. Inclusion of `churn` and `customer_id`
- `churn` / `Churn`: **Must NOT be included** for prediction. It is the target variable. If present in an uploaded CSV, `preprocess_inference_data` drops it automatically. It is excluded from the prediction template.
- `customer_id` / `customerID`: **NOT required for ML inference** (if omitted, `ml_service.py` assigns synthetic IDs `C-0`, `C-1`, ...), but **must be named `customerID` (exact casing)** if provided to associate predictions with specific customers. `customer_id` (snake_case) is not recognized and will be discarded by `remainder="drop"`.

### 4. Mismatches Between Training and Prediction Schemas
- **Target presence:** Training strictly requires `Churn` (raises `ValueError` if absent); prediction expects no target (drops it if present).
- **Header Casing:** Preprocessor column matching is strictly case-sensitive (`customerID`, `SeniorCitizen`, `gender`, `tenure`, etc.).
- **Extra columns:** Extra columns (e.g., `name`) are permitted during prediction as `ColumnTransformer` has `remainder="drop"`. `ml_service.py` explicitly extracts `name` if present.
- **Column count:** Training dataset has 21 columns (20 features/ID + `Churn`). Template CSV has 20 columns (19 features + `customerID`).

### 5. Valid Example CSV Header and Row
```csv
customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges
7590-VHVEG,Female,0,Yes,No,1,No,No phone service,DSL,No,Yes,No,No,No,No,Month-to-month,Yes,Electronic check,29.85,29.85
```

Last updated: 2026-10-12T21:56

