# Retentio — Code Review & Viva Preparation Guide (`review2.md`)

> **Scope & Purpose:** Comprehensive architectural review, code-level inspection, and viva defense guide for **Retentio** (Customer Churn Prediction Platform).  
> All claims, line references, and snippets are verified against the actual repository files under `F:\Retentio`. Unverified items and recommended improvements are explicitly labeled.

---

## 1. Model Training Pipeline

**Location:** [`backend/train/train_model.py`](file:///F:/Retentio/backend/train/train_model.py)

* **Pipeline Flow:**
  1. **Dataset Ingestion & EDA:** `load_and_split()` loads raw data and calls `run_eda()` ([`train_model.py:67-171`](file:///F:/Retentio/backend/train/train_model.py#L67-L171)), generating [`backend/train/eda_summary.md`](file:///F:/Retentio/backend/train/eda_summary.md).
  2. **Preprocessing:** Calls `preprocess_training_data(df)` ([`backend/utils/preprocess.py:154-203`](file:///F:/Retentio/backend/utils/preprocess.py#L154-L203)).
  3. **Train/Test Splitting:** Stratified split using Scikit-Learn `train_test_split()`.
  4. **Model Training:** Trains Logistic Regression, Random Forest, and XGBoost.
  5. **Evaluation & Gating:** Compares models on hold-out test set; selects highest ROC-AUC model.
  6. **Artifact Serialization:** Saves trained artifacts using `joblib.dump()`.
* **Dataset:** Local CSV copy of IBM/Kaggle Telco Customer Churn dataset at [`backend/train/data/WA_Fn-UseC_-Telco-Customer-Churn.csv`](file:///F:/Retentio/backend/train/data/WA_Fn-UseC_-Telco-Customer-Churn.csv) (7,043 rows, 21 columns).
* **Target Variable:** `Churn` column. Mapped to binary integers in `_encode_target()` ([`preprocess.py:103-105`](file:///F:/Retentio/backend/utils/preprocess.py#L103-L105)): `Yes` $\rightarrow 1$, `No` $\rightarrow 0$. Dataset has 1,869 positive (26.5%) and 5,174 negative (73.5%) samples.
* **Train/Test Split:** 80% train (5,634 rows) / 20% test (1,409 rows), stratified on target `y`, seeded with `random_state=42` ([`train_model.py:207-212`](file:///F:/Retentio/backend/train/train_model.py#L207-L212)).
* **Saved Artifacts:**
  * [`backend/model/churn_model.pkl`](file:///F:/Retentio/backend/model/churn_model.pkl): Fitted Scikit-Learn `LogisticRegression` object (~1,231 bytes).
  * [`backend/model/preprocessor.pkl`](file:///F:/Retentio/backend/model/preprocessor.pkl): Fitted Scikit-Learn `ColumnTransformer` object (~7,412 bytes).
  * Markdown reports: [`backend/train/baseline_results.md`](file:///F:/Retentio/backend/train/baseline_results.md) and [`backend/train/eda_summary.md`](file:///F:/Retentio/backend/train/eda_summary.md).

```python
# From backend/train/train_model.py:207-212
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,     # 0.20
    stratify=y,
    random_state=RANDOM_STATE # 42
)
```

---

## 2. Machine Learning Algorithms Implemented

Three classifiers were implemented and compared in [`backend/train/train_model.py`](file:///F:/Retentio/backend/train/train_model.py):

| Algorithm | Implementation & Hyperparameters | Role & Why Implemented |
|---|---|---|
| **Logistic Regression** | `LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42, solver="lbfgs")` ([`train_model.py:223-233`](file:///F:/Retentio/backend/train/train_model.py#L223-L233)) | **Selected Production Model**. Telco churn indicators (contract type, tenure, monthly charges) exhibit strong linear and monotonic relationships. It achieved the highest ROC-AUC (0.8414) and produces well-calibrated, continuous probabilities for risk scoring. |
| **Random Forest** | `RandomForestClassifier(class_weight="balanced", n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)` ([`train_model.py:235-245`](file:///F:/Retentio/backend/train/train_model.py#L235-L245)) | **Non-linear Ensemble Baseline**. Evaluated to test whether feature interactions improved predictive discrimination. Lower ROC-AUC (0.8193) led to rejection. |
| **XGBoost** | `XGBClassifier(scale_pos_weight=n_neg/n_pos, n_estimators=300, max_depth=5, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, eval_metric="logloss", random_state=42, n_jobs=-1)` ([`train_model.py:248-264`](file:///F:/Retentio/backend/train/train_model.py#L248-L264)) | **Gradient Boosting Challenger**. Tested with `scale_pos_weight ≈ 2.77` to penalize minority false negatives. Narrowly fell below Logistic Regression on ROC-AUC (0.8369 vs 0.8414); retained in logs as a reference benchmark. |

---

## 3. Evaluation Metrics & Missing Evaluation Code

### Implemented Metrics & Genuine Test Scores
Verified directly from the hold-out test set run recorded in [`backend/train/baseline_results.md`](file:///F:/Retentio/backend/train/baseline_results.md#L11-L15) (evaluated via `evaluate()` at [`train_model.py:270-280`](file:///F:/Retentio/backend/train/train_model.py#L270-L280)):

| Model | Test Accuracy | Test F1 (Weighted) | Test ROC-AUC | Production Status |
|---|---|---|---|---|
| **Logistic Regression** | **0.7381 (73.81%)** | **0.7519** | **0.8414** | **Selected Winner** |
| Random Forest | 0.7637 (76.37%) | 0.7685 | 0.8193 | Baseline only |
| XGBoost | 0.7580 (75.80%) | 0.7688 | 0.8369 | Challenger only |

### Missing Evaluation Code
* **Missing in existing training pipeline:**
  1. Binary / Positive-class Precision (`precision_score`).
  2. Binary / Positive-class Recall (`recall_score`) — vital for churn, as false negatives lose customers.
  3. Binary F1-score (the code only computes `f1_score(..., average="weighted")`, which is inflated by the 73.5% negative class).
  4. Confusion Matrix (`confusion_matrix`).
* **Evaluation Code to Demonstrate Genuine Scores on Test Set:**
  Run this standalone evaluation against the hold-out test split (never use the unlabeled template CSV):

```python
import joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from utils.preprocess import preprocess_training_data

df = pd.read_csv("backend/train/data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
X, y, _ = preprocess_training_data(df)
_, X_test, _, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

model = joblib.load("backend/model/churn_model.pkl")
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("Binary F1:", f1_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_proba))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
```

---

## 4. End-to-End Prediction Trace

Tracing an uploaded CSV prediction:

1. **User Action:** In [`retentio/client/src/pages/Pages.tsx:108-119`](file:///F:/Retentio/retentio/client/src/pages/Pages.tsx#L108-L119), user drops a CSV into `<UploadDropzone />`. `handleUpload(file)` is invoked.
2. **Frontend Client:** [`retentio/client/src/lib/api.ts:78-86`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L78-L86) creates `FormData`, appends `file`, and makes an Axios `POST /api/v1/predict/upload`. The request interceptor adds header `Authorization: Bearer <token>` from `localStorage.getItem("retentio_token")`.
3. **Vite Reverse Proxy:** In dev mode, Vite proxies `/api` to `http://localhost:8000` ([`retentio/vite.config.ts:232-234`](file:///F:/Retentio/retentio/vite.config.ts#L232-L234)).
4. **FastAPI Routing & Auth:** Request enters `upload_csv()` at [`backend/api/routes/predict.py:34-42`](file:///F:/Retentio/backend/api/routes/predict.py#L34-L42). Dependency `get_current_user` ([`backend/services/auth_service.py:69-90`](file:///F:/Retentio/backend/services/auth_service.py#L69-L90)) decodes JWT and loads user document from MongoDB.
5. **Validation:** `upload_csv` validates `.csv` file extension, checks size ($\le 10\text{ MB}$), and parses contents with `pd.read_csv(io.BytesIO(contents))`.
6. **ML Service Invocation:** Calls `predict(df, benchmark)` ([`backend/services/ml_service.py:55-99`](file:///F:/Retentio/backend/services/ml_service.py#L55-L99)).
7. **Preprocessing:** Calls `preprocess_inference_data(df, _preprocessor)` ([`backend/utils/preprocess.py:210-243`](file:///F:/Retentio/backend/utils/preprocess.py#L210-L243)). It coerces `TotalCharges` strings to numeric, drops identifiers, and runs the pre-fitted `ColumnTransformer` (median/most-frequent imputation, `StandardScaler`, and `OneHotEncoder`).
8. **Inference & Scoring:** `_model.predict_proba(X)[:, 1]` outputs churn probabilities; `probabilities_to_risk_scores()` scales them to $[0.0, 100.0]$ ([`preprocess.py:249-264`](file:///F:/Retentio/backend/utils/preprocess.py#L249-L264)). Rows are tagged `"At Risk"` if $\text{score} \ge \text{benchmark}$, else `"Healthy"`.
9. **MongoDB Persistence:** `upsert_customers(user_id, all_scores, benchmark)` ([`backend/services/customer_service.py:21-114`](file:///F:/Retentio/backend/services/customer_service.py#L21-L114)) updates or inserts documents in `db.customers`, appends to the `history` array, and marks recovered accounts as `"Saved"`.
10. **Response & React UI:** FastAPI returns `PredictResponse` ([`backend/schemas/customer_schema.py:39-44`](file:///F:/Retentio/backend/schemas/customer_schema.py#L39-L44)). Axios returns response data; `setResult(res)` triggers React re-render displaying summary counts and tables.

---

## 5. Roles of Core ML & API Files

* **[`backend/utils/preprocess.py`](file:///F:/Retentio/backend/utils/preprocess.py):**
  Defines `CONFIG` (schema dictionary), data type coercion (`_coerce_types`), missing value handling (median for numeric, mode for categorical), and builds the `ColumnTransformer`. Provides two distinct APIs: `preprocess_training_data()` (fits preprocessor) and `preprocess_inference_data()` (transforms only, no fitting). Also exports `probabilities_to_risk_scores()`.
* **[`backend/services/ml_service.py`](file:///F:/Retentio/backend/services/ml_service.py):**
  Singleton container managing in-memory ML model state. Holds module globals `_model` and `_preprocessor`. Exposes `load_model()` for startup initialization and `predict()` to convert raw uploaded DataFrames into customer risk scores.
* **[`backend/api/routes/predict.py`](file:///F:/Retentio/backend/api/routes/predict.py):**
  API presentation layer. Exposes `POST /predict/upload` (file validation, authentication, calling `ml_service`, triggering `upsert_customers`) and `GET /predict/template` (streaming downloadable CSV headers).
* **`backend/model/*.pkl` files:**
  * `churn_model.pkl`: Serialized production `LogisticRegression` model with learned weights and intercept.
  * `preprocessor.pkl`: Serialized fitted `ColumnTransformer` preserving exact scaling statistics (mean, variance) and one-hot categorical feature mappings learned during training.

---

## 6. FastAPI Route Registration & Startup Architecture

* **Application Startup:**
  Defined in [`backend/main.py:24-48`](file:///F:/Retentio/backend/main.py#L24-L48) using FastAPI's `lifespan` async context manager:
  1. Calls `await connect_db()` ([`backend/db/__init__.py:26`](file:///F:/Retentio/backend/db/__init__.py#L26)): opens Motor client and pings MongoDB Atlas.
  2. Calls `load_model()` ([`backend/services/ml_service.py:36`](file:///F:/Retentio/backend/services/ml_service.py#L36)): loads `.pkl` files into memory once before handling requests.
  3. Yields to accept incoming HTTP traffic.
  4. On server termination, calls `await close_db()`.
* **Route Imports & Registration:**
  In [`backend/main.py:64-75`](file:///F:/Retentio/backend/main.py#L64-L75), individual `router` instances are directly imported from their respective module files and mounted with prefix `/api/v1`:
  ```python
  from api.routes.auth import router as auth_router
  from api.routes.customers import router as customers_router
  from api.routes.dashboard import router as dashboard_router
  from api.routes.predict import router as predict_router
  from api.routes.settings import router as settings_router

  app.include_router(auth_router, prefix="/api/v1")
  app.include_router(predict_router, prefix="/api/v1")
  app.include_router(customers_router, prefix="/api/v1")
  app.include_router(dashboard_router, prefix="/api/v1")
  app.include_router(settings_router, prefix="/api/v1")
  ```
* **Role of `__init__.py` files:**
  * [`backend/api/routes/__init__.py`](file:///F:/Retentio/backend/api/routes/__init__.py) & [`backend/api/__init__.py`](file:///F:/Retentio/backend/api/__init__.py): Empty package indicators (2 bytes); routers are imported explicitly from module files.
  * [`backend/schemas/__init__.py`](file:///F:/Retentio/backend/schemas/__init__.py): Exports auth and user Pydantic models (`UserCreate`, `UserLogin`, `UserResponse`, `TokenResponse`, etc.).
  * [`backend/db/__init__.py`](file:///F:/Retentio/backend/db/__init__.py): Acts as the database client module containing `connect_db()`, `close_db()`, and `get_db()`.

---

## 7. MongoDB Initialization & Data Operations

* **Initialization:**
  Located in [`backend/db/__init__.py:26-52`](file:///F:/Retentio/backend/db/__init__.py#L26-L52). Initialized via `AsyncIOMotorClient(MONGODB_URI, ...)` and assigns `db = _client[DATABASE_NAME]` (default database name is `retentio`). Verified via `await _client.admin.command("ping")`.
* **Collections Used:**
  1. `users` collection:
     * **Writes:**
       * `POST /auth/signup`: `db.users.insert_one(user_doc)` ([`auth.py:52`](file:///F:/Retentio/backend/api/routes/auth.py#L52)).
       * `PATCH /settings/profile`: `db.users.update_one({"_id": ObjectId(...)})` ([`settings.py:33`](file:///F:/Retentio/backend/api/routes/settings.py#L33)).
       * `PATCH /settings/benchmark`: `db.users.update_one({"_id": ObjectId(...)})` ([`settings.py:56`](file:///F:/Retentio/backend/api/routes/settings.py#L56)).
     * **Reads:**
       * `POST /auth/signup`: checks duplicate email `db.users.find_one({"email": body.email})` ([`auth.py:37`](file:///F:/Retentio/backend/api/routes/auth.py#L37)).
       * `POST /auth/login`: verifies user `db.users.find_one({"email": body.email})` ([`auth.py:73`](file:///F:/Retentio/backend/api/routes/auth.py#L73)).
       * `get_current_user`: extracts token subject and calls `db.users.find_one({"_id": ObjectId(user_id)})` ([`auth_service.py:84`](file:///F:/Retentio/backend/services/auth_service.py#L84)).
  2. `customers` collection:
     * **Writes (Upsert & Score Ingestion):**
       * Handled in `upsert_customers()` ([`customer_service.py:21-114`](file:///F:/Retentio/backend/services/customer_service.py#L21-L114)).
       * Existing customer: `db.customers.update_one({"_id": existing["_id"]}, {"$set": {"current_score": score, "status": new_status, ...}, "$push": {"history": {"date": today, "score": score}}})`.
       * New customer: `db.customers.insert_one({"customer_id": cid, "user_id": user_id, "current_score": score, "status": new_status, "history": [...]})`.
     * **Reads:**
       * `GET /customers/at-risk`: `db.customers.find({"user_id": user_id, "status": "At Risk"})` ([`customer_service.py:137-142`](file:///F:/Retentio/backend/services/customer_service.py#L137-L142)).
       * `GET /customers/saved`: `db.customers.find({"user_id": user_id, "status": "Saved"})` ([`customer_service.py:145-150`](file:///F:/Retentio/backend/services/customer_service.py#L145-L150)).
       * `GET /customers/search`: `db.customers.find({"user_id": user_id, "$or": [{"name": regex}, {"customer_id": regex}]})` ([`customer_service.py:153-162`](file:///F:/Retentio/backend/services/customer_service.py#L153-L162)).
       * `GET /customers/{customer_id}`: `db.customers.find_one({"user_id": user_id, "customer_id": customer_id})` ([`customer_service.py:165-179`](file:///F:/Retentio/backend/services/customer_service.py#L165-L179)).
       * `GET /dashboard/summary`: `db.customers.count_documents(...)` and aggregate `{"$avg": "$current_score"}` ([`customer_service.py:181-203`](file:///F:/Retentio/backend/services/customer_service.py#L181-L203)).
       * `GET /dashboard/trend`: MongoDB aggregation unwinding `$history` to group average score by date ([`customer_service.py:206-237`](file:///F:/Retentio/backend/services/customer_service.py#L206-L237)).
* **Prediction Data Note:** Predictions are not stored in a separate table; each inference run updates the customer's `current_score` and appends to the embedded `history` array in `customers`.

---

## 8. Real React `useState` & Props Code Traces

### `useState` Example
* **File:** [`retentio/client/src/pages/Pages.tsx:208-264`](file:///F:/Retentio/retentio/client/src/pages/Pages.tsx#L208-L264) (`Settings` component)
* **Code Snippet:**
  ```tsx
  const [benchmark, setBenchmark] = useState(user?.benchmark || 78);
  ...
  <div className="benchmark-value"><strong>{benchmark}</strong><span>/ 100</span></div>
  <input
    className="range"
    type="range"
    min="70"
    max="90"
    value={benchmark}
    onChange={e => setBenchmark(Number(e.target.value))}
  />
  ```
* **UI Trace:** When the user moves the slider, `onChange` triggers `setBenchmark`. React schedules a re-render; the DOM node `<strong>{benchmark}</strong>` immediately reflects the new threshold number. Clicking "Save benchmark" then sends this state value to `settingsApi.updateBenchmark(benchmark)`.

### Props Example
* **Component Definition:** [`retentio/client/src/components/AppUI.tsx:55-57`](file:///F:/Retentio/retentio/client/src/components/AppUI.tsx#L55-L57)
  ```tsx
  export function DataTable({ rows, saved=false }: { rows: CustomerRow[]; saved?: boolean }) {
    return (
      <GlassCard className="table-card">
        <div className="table-heading">
          <p className="eyebrow">{saved ? 'Recovered signal' : 'Priority queue'}</p>
          <h2>{saved ? 'Saved customers' : 'At-risk customers'}</h2>
        </div>
        <div className="data-table">
          {rows.map(row => (
            <div className="table-row" key={row.customer_id}>
              <span><b>{row.name}</b><small>{row.customer_id}</small></span>
              <span className="score-value">{row.score.toFixed(1)}</span>
              <StatusBadge status={row.status}/>
            </div>
          ))}
        </div>
      </GlassCard>
    );
  }
  ```
* **Props Passed In:** [`retentio/client/src/pages/Pages.tsx:129-130`](file:///F:/Retentio/retentio/client/src/pages/Pages.tsx#L129-L130) (`Predict` page)
  ```tsx
  <DataTable rows={result.at_risk} />
  <DataTable rows={result.saved} saved />
  ```
* **UI Trace:** `Predict` passes the array `result.at_risk` as prop `rows` with default `saved=false` (rendering the heading "At-risk customers"). For recovered users, it passes `rows={result.saved}` and boolean prop `saved={true}`, switching the card header to "Saved customers" and rendering rows with a green status badge.

---

## 9. Scope Analysis: `var`, `let`, and `const`

* **`var` Status:** **Completely absent** across all TypeScript/React source files (`client/src`). Modern ES6+ / TypeScript standards disallow `var` due to function scoping and hoisting hazards.
* **`let` Examples & Scope:**
  * Used for reassignable, block-scoped variables.
  * *Example 1:* [`retentio/client/src/pages/Pages.tsx:36`](file:///F:/Retentio/retentio/client/src/pages/Pages.tsx#L36) (in `SignUp` typewriter effect):
    ```ts
    let index = 0;
    let timeout: number | undefined;
    // index is incremented (index += 1), timeout is reassigned window.setTimeout IDs
    ```
  * *Example 2:* [`retentio/client/src/components/BackgroundSystems.tsx:66`](file:///F:/Retentio/retentio/client/src/components/BackgroundSystems.tsx#L66):
    ```ts
    for (let i = 0; i < 240; i++) { ... } // Block-scoped loop counter
    ```
* **`const` Examples & Scope:**
  * Used for immutable identifiers (block-scoped; cannot be reassigned).
  * *Example 1:* Module tokens: [`retentio/client/src/lib/api.ts:26`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L26) `export const TOKEN_KEY = 'retentio_token';`.
  * *Example 2:* Client instances: [`retentio/client/src/lib/api.ts:30`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L30) `const client = axios.create({ ... });`.
  * *Example 3:* Context instances: [`retentio/client/src/contexts/AuthContext.tsx:17`](file:///F:/Retentio/retentio/client/src/contexts/AuthContext.tsx#L17) `const AuthContext = createContext<AuthContextValue | null>(null);`.

---

## 10. Technology Stack & Dependencies Audit

| Layer | Technologies & Dependencies | Purpose & Usage in Code |
|---|---|---|
| **Frontend Framework** | React 19 (`react: ^19.2.1`, `react-dom: ^19.2.1`) | Functional components, hooks (`useState`, `useEffect`, `useMemo`, `useRef`). |
| **Language & Typings** | TypeScript 5.6.3 (`typescript: 5.6.3`) | Strict compile-time typing across routes, APIs, and data models (`lib/types.ts`). |
| **Bundler & Build** | Vite 7.1.7 (`vite: ^7.1.7`), Tailwind CSS v4 (`@tailwindcss/vite`) | Fast HMR dev server and production asset compilation. |
| **Client Routing** | `wouter: ^3.3.5` | Route shell (`Route`, `Switch`, `Redirect`, `Link`, `useLocation`) in [`App.tsx`](file:///F:/Retentio/retentio/client/src/App.tsx). Lightweight alternative to React Router. |
| **API Client** | Axios (`axios: ^1.12.0`) | Centralized HTTP client in [`lib/api.ts`](file:///F:/Retentio/retentio/client/src/lib/api.ts); attaches JWT bearer token, unwraps error messages. |
| **State Management** | React Context API | `AuthContext` in [`AuthContext.tsx`](file:///F:/Retentio/retentio/client/src/contexts/AuthContext.tsx) for session token persistence; local state via `useState`. (No Redux/Zustand). |
| **UI, Animation & 3D** | `framer-motion: ^12.23.22`, `three: ^0.185.1`, `lucide-react: ^0.453.0` | Micro-interactions, background canvas shader/vortex in `BackgroundSystems.tsx`, iconography. |
| **Backend Framework** | FastAPI (`fastapi>=0.115.0`), Uvicorn (`uvicorn[standard]>=0.30.0`) | Async web server, dependency injection, automatic OpenAPI docs. |
| **Database Driver** | Motor (`motor>=3.5.0`), PyMongo (`pymongo>=4.8.0`) | Non-blocking async driver for MongoDB Atlas. |
| **Validation** | Pydantic v2 | Strict request/response payload validation schemas in [`backend/schemas`](file:///F:/Retentio/backend/schemas). |
| **Auth & Security** | `passlib[bcrypt]>=1.7.4`, `bcrypt==4.0.1`, `python-jose>=3.3.0` | Bcrypt password hashing and HMAC-SHA256 JWT tokens. |
| **Machine Learning** | `scikit-learn>=1.5.0`, `xgboost>=2.1.0`, `pandas>=2.2.0`, `numpy>=1.26.0`, `joblib>=1.4.0` | Offline training pipeline and online inference. |

---

## 11. Security Audit

* **Password Hashing:**
  * *Implementation:* [`backend/services/auth_service.py:29-40`](file:///F:/Retentio/backend/services/auth_service.py#L29-L40). Uses `CryptContext(schemes=["bcrypt"], deprecated="auto")`.
  * *Verification:* `bcrypt` is explicitly pinned to `4.0.1` in [`backend/requirements.txt:7`](file:///F:/Retentio/backend/requirements.txt#L7) to resolve compatibility issues with `passlib 1.7.4`.
* **Authentication & JWT:**
  * *Implementation:* [`backend/services/auth_service.py:45-65`](file:///F:/Retentio/backend/services/auth_service.py#L45-L65). Signs token with `sub` (`user_id`), `email`, and 24-hour expiration (`exp`). Algorithm: `HS256`.
  * *Frontend Handling:* Token stored in browser `localStorage` under `retentio_token` ([`lib/api.ts:26`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L26)).
* **Authorization & Tenant Isolation:**
  * Verified in [`backend/services/customer_service.py`](file:///F:/Retentio/backend/services/customer_service.py). All queries enforce `{"user_id": user_id}`. Users cannot view or modify another workspace's customer data.
* **Input Validation:**
  * Pydantic models validate email format (`EmailStr`) and enforce string length boundaries (`password` min 8, max 128 chars).
  * CSV file upload validates extension and limits file buffer to 10 MB ([`predict.py:44-50`](file:///F:/Retentio/backend/api/routes/predict.py#L44-L50)).
* **CORS:**
  * Configured in [`backend/main.py:52-60`](file:///F:/Retentio/backend/main.py#L52-L60). Parses `ALLOWED_ORIGINS` from environment variables, defaulting to `http://localhost:3000`.
* **Identified Vulnerabilities & Risks:**
  1. **Hardcoded Fallback JWT Secret:** [`backend/services/auth_service.py:25`](file:///F:/Retentio/backend/services/auth_service.py#L25) falls back to `"changeme_replace_before_production"` if `JWT_SECRET` is unset, risking token forgery.
  2. **Raw Exception Leakage:** [`backend/api/routes/predict.py:68`](file:///F:/Retentio/backend/api/routes/predict.py#L68) returns internal stack/exception messages directly to the client (`detail=f"Prediction error: {exc}"`).
  3. **XSS Exposure:** Storing JWT in `localStorage` makes tokens readable by malicious client-side scripts. (HttpOnly cookies recommended).

---

## 12. SQL vs. NoSQL Injection Analysis

* **Relevance of SQL Injection:**
  SQL injection is **not relevant** to Retentio. The backend does not use a relational SQL engine or execute SQL string queries (`SELECT`, `INSERT`). It connects exclusively to MongoDB via Motor.
* **NoSQL Injection Risks:**
  NoSQL injection occurs when user-supplied JSON structures containing MongoDB operators (e.g., `{"$gt": ""}`, `{"$ne": null}`) are passed into database query selectors.
* **Audit of Query Handling:**
  * **Protected by Pydantic:** In `login` and `signup` ([`auth.py:37, 73`](file:///F:/Retentio/backend/api/routes/auth.py#L37)), queries use `{"email": body.email}`. Because `body` is strictly validated by Pydantic as a string (`EmailStr`), an object payload like `{"email": {"$ne": null}}` is rejected with HTTP 422 before touching the database.
  * **Protected by Type Casting:** `get_current_user` ([`auth_service.py:84`](file:///F:/Retentio/backend/services/auth_service.py#L84)) wraps the ID with `ObjectId(user_id)`. Non-hex structures trigger `bson.errors.InvalidId`.
  * **Real Vulnerability (Regex Injection / ReDoS):**
    In [`backend/services/customer_service.py:155-160`](file:///F:/Retentio/backend/services/customer_service.py#L155-L160):
    ```python
    regex = {"$regex": query, "$options": "i"}
    cursor = db.customers.find({
        "user_id": user_id,
        "$or": [{"name": regex}, {"customer_id": regex}],
    }).limit(limit)
    ```
    The query parameter `q` is passed directly into `$regex` without `re.escape(query)`. An attacker can supply regex catastrophic backtracking payloads (e.g. `(a+)+$`) to cause CPU exhaustion (ReDoS) on the MongoDB Atlas cluster.

---

## 13. API Endpoints Directory

| Endpoint | Method | Auth Required | Request Schema / Params | Response Schema | Purpose |
|---|---|---|---|---|---|
| `/api/health` | `GET` | No | None | `dict` (`{"status": "ok"}`) | Backend service health check ([`main.py:77`](file:///F:/Retentio/backend/main.py#L77)). |
| `/api/v1/auth/signup` | `POST` | No | `UserCreate` (name, business, email, password) | `TokenResponse` (201) | User registration & token issue ([`auth.py:31`](file:///F:/Retentio/backend/api/routes/auth.py#L31)). |
| `/api/v1/auth/login` | `POST` | No | `UserLogin` (email, password) | `TokenResponse` (200) | User authentication & token issue ([`auth.py:68`](file:///F:/Retentio/backend/api/routes/auth.py#L68)). |
| `/api/v1/auth/me` | `GET` | Yes (Bearer) | None | `UserResponse` | Fetch current user profile ([`auth.py:95`](file:///F:/Retentio/backend/api/routes/auth.py#L95)). |
| `/api/v1/predict/upload` | `POST` | Yes (Bearer) | `UploadFile` (multipart CSV) | `PredictResponse` | Ingest CSV, run ML inference, upsert DB ([`predict.py:34`](file:///F:/Retentio/backend/api/routes/predict.py#L34)). |
| `/api/v1/predict/template`| `GET` | No | None | `StreamingResponse` (`.csv`) | Download sample CSV headers ([`predict.py:85`](file:///F:/Retentio/backend/api/routes/predict.py#L85)). |
| `/api/v1/customers/at-risk`| `GET` | Yes (Bearer) | None | `{"customers": List[CustomerRow]}` | List customers with score $\ge$ benchmark ([`customers.py:22`](file:///F:/Retentio/backend/api/routes/customers.py#L22)). |
| `/api/v1/customers/saved` | `GET` | Yes (Bearer) | None | `{"customers": List[CustomerRow]}` | List recovered customers ([`customers.py:30`](file:///F:/Retentio/backend/api/routes/customers.py#L30)). |
| `/api/v1/customers/search`| `GET` | Yes (Bearer) | `q: str = Query("")` | `{"customers": List[CustomerRow]}` | Search customers by name or ID ([`customers.py:38`](file:///F:/Retentio/backend/api/routes/customers.py#L38)). |
| `/api/v1/customers/{id}` | `GET` | Yes (Bearer) | `customer_id: str` (path) | `CustomerDetail` | Get customer details & history ([`customers.py:53`](file:///F:/Retentio/backend/api/routes/customers.py#L53)). |
| `/api/v1/dashboard/summary`| `GET` | Yes (Bearer) | None | `DashboardSummary` | Metrics for overview cards ([`dashboard.py:18`](file:///F:/Retentio/backend/api/routes/dashboard.py#L18)). |
| `/api/v1/dashboard/trend` | `GET` | Yes (Bearer) | None | `DashboardTrend` | Chronological risk trend points ([`dashboard.py:25`](file:///F:/Retentio/backend/api/routes/dashboard.py#L25)). |
| `/api/v1/settings/profile` | `PATCH`| Yes (Bearer) | `ProfileUpdate` | `UserResponse` | Update name / business name ([`settings.py:19`](file:///F:/Retentio/backend/api/routes/settings.py#L19)). |
| `/api/v1/settings/benchmark`|`PATCH`| Yes (Bearer) | `BenchmarkUpdate` (0-100) | `UserResponse` | Update risk score threshold ([`settings.py:49`](file:///F:/Retentio/backend/api/routes/settings.py#L49)). |

---

## 14. Validation, Encoding, and Scaling of the 19 Features

Defined in [`backend/utils/preprocess.py:40-75`](file:///F:/Retentio/backend/utils/preprocess.py#L40-L75):

1. **4 Numeric Features:** `tenure`, `MonthlyCharges`, `TotalCharges`, `SeniorCitizen`.
   * *Type Coercion:* `_coerce_types()` converts `TotalCharges` strings to float (`pd.to_numeric(..., errors="coerce")`). Blank strings (`" "`) become `NaN`. Note: `SeniorCitizen` is binary 0/1, scaled as numeric.
   * *Imputation:* `SimpleImputer(strategy="median")` replaces missing values with the training median.
   * *Scaling:* `StandardScaler()` standardizes features: $z = \frac{x - \mu}{\sigma}$.
2. **15 Categorical Features:** `gender`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`.
   * *Imputation:* `SimpleImputer(strategy="most_frequent")` fills missing entries with the training mode.
   * *Encoding:* `OneHotEncoder(handle_unknown="ignore", sparse_output=False)` produces binary dummy columns. `handle_unknown="ignore"` ensures novel string categories in uploaded CSVs encode as all-zeros rather than throwing an exception.
3. **Execution Pipeline:**
   Combined via Scikit-Learn `ColumnTransformer(transformers=[("num", numeric_pipeline, numeric_cols), ("cat", categorical_pipeline, categorical_cols)], remainder="drop")`. `remainder="drop"` automatically discards identifiers like `customerID`. If any of the 19 columns is missing from the CSV header, `ColumnTransformer.transform()` raises a `ValueError`.

---

## 15. Prioritized Gaps, Weaknesses, and Improvements

| Priority | Issue / Risk | Location | Impact & Recommended Improvement |
|---|---|---|---|
| **High** | **Zero Automated Tests** | Repository-wide | No `pytest` or `vitest` test suites exist. Only manual verification script [`verify_model.py`](file:///F:/Retentio/backend/verify_model.py) is present. Add unit tests for API routes, preprocessing edge cases, and JWT authentication. |
| **High** | **ReDoS Vulnerability in Search** | [`customer_service.py:155`](file:///F:/Retentio/backend/services/customer_service.py#L155) | Unescaped user query passed directly to MongoDB `$regex`. Escape query string with `re.escape(query)` before compiling query selector. |
| **Medium** | **Insecure Fallback JWT Secret** | [`auth_service.py:25`](file:///F:/Retentio/backend/services/auth_service.py#L25) | Defaults to `"changeme_replace_before_production"`. Raise a `RuntimeError` at application startup if `JWT_SECRET` is unset or blank. |
| **Medium** | **N+1 Sequential Upsert Loop** | [`customer_service.py:41-113`](file:///F:/Retentio/backend/services/customer_service.py#L41-L113) | `upsert_customers` issues individual `find_one()` + `update_one()` calls per row. A 5,000-row CSV triggers ~10,000 round-trips. Replace with `collection.bulk_write([UpdateOne(...)])`. |
| **Medium** | **Unhandled Header Exceptions** | [`predict.py:65-69`](file:///F:/Retentio/backend/api/routes/predict.py#L65-L69) | Missing CSV columns trigger an internal `ValueError`, returning HTTP 500. Catch column mismatch errors explicitly and return HTTP 400 with a list of missing columns. |
| **Low** | **Token Stored in LocalStorage** | [`retentio/client/src/lib/api.ts:26`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L26) | Tokens in `localStorage` can be accessed by XSS exploits. Transition to `HttpOnly`, `SameSite=Lax` cookies. |
| **Low** | **No Rate Limiting** | [`backend/api/routes/auth.py`](file:///F:/Retentio/backend/api/routes/auth.py) | Login/Signup endpoints are vulnerable to credential stuffing. Implement `slowapi` rate limiting. |

---

## 16. Viva: Difference Between Frontend, Backend, API, and Database

* **Frontend (`retentio/client`):** The React 19 Single Page Application rendered in the user's browser. Responsible for presentation, accepting user input (forms, drag-and-drop CSV), rendering charts, and managing client-side navigation.
* **Backend (`backend`):** The Python server environment running FastAPI and Uvicorn. Implements business logic, password hashing, JWT creation, ML inference execution, and database orchestration.
* **API (`backend/api` & `/api/v1/*`):** The HTTP interface connecting frontend and backend. Defines REST endpoints, validates incoming JSON/multipart payloads via Pydantic, and returns JSON response contracts.
* **Database (MongoDB Atlas):** The persistent document store. Stores user credentials (`users` collection) and customer risk records with historical scores (`customers` collection).

---

## 17. Viva: Lifecycle of a Login Request

1. **User Action:** User inputs email/password in [`retentio/client/src/pages/Pages.tsx:48`](file:///F:/Retentio/retentio/client/src/pages/Pages.tsx#L48) and submits the form.
2. **Client Request:** `authApi.login(email, password)` ([`lib/api.ts:68`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L68)) sends an HTTP `POST /api/v1/auth/login`.
3. **Route Handling & Validation:** FastAPI routes to `login()` in [`backend/api/routes/auth.py:68`](file:///F:/Retentio/backend/api/routes/auth.py#L68). Request body is validated against `UserLogin` schema.
4. **Database Query:** Backend queries `db.users.find_one({"email": body.email})`. If not found, raises HTTP 401.
5. **Password Verification:** Calls `verify_password(body.password, user["password_hash"])` ([`auth_service.py:39`](file:///F:/Retentio/backend/services/auth_service.py#L39)) using bcrypt. If hashes mismatch, raises HTTP 401.
6. **Token Issuance:** Backend signs a JWT with user ID, email, and 24-hour expiration ([`auth_service.py:45`](file:///F:/Retentio/backend/services/auth_service.py#L45)) and returns HTTP 200 with `TokenResponse`.
7. **Frontend Storage & State:** Frontend stores token in `localStorage.setItem("retentio_token", res.token)`, sets `user` in `AuthContext`, and redirects to `/dashboard`.

---

## 18. Viva: Error & Invalid Input Handling

* **Backend:**
  * Pydantic schemas validate payload data types, constraints, and string lengths, returning structured `422 Unprocessable Entity` responses on failure.
  * Route endpoints raise `fastapi.HTTPException` with explicit status codes: `400` (invalid file type, empty CSV), `401` (invalid credentials, expired token), `404` (customer not found), `409` (duplicate email), and `413` (file exceeds 10 MB).
* **Frontend:**
  * Axios response interceptor ([`retentio/client/src/lib/api.ts:46-55`](file:///F:/Retentio/retentio/client/src/lib/api.ts#L46-L55)) unwraps `err.response?.data?.detail` and rejects with a readable error message.
  * React components catch the rejected promise and update state (e.g., `setError(err.message)` in `Login` / `SignUp`), rendering an error banner above the form.

---

## 19. Viva: Runtime Model Loading & Failure Handling

* **How Model is Loaded:**
  At application startup, FastAPI's `lifespan` hook ([`backend/main.py:33`](file:///F:/Retentio/backend/main.py#L33)) calls `load_model()` in [`backend/services/ml_service.py:36-53`](file:///F:/Retentio/backend/services/ml_service.py#L36-L53). This reads `churn_model.pkl` and `preprocessor.pkl` into module-level globals `_model` and `_preprocessor`.
* **What Happens if Loading Fails:**
  If either `.pkl` file is missing, `load_model()` raises `FileNotFoundError`. Because this happens inside the `lifespan` startup hook, **FastAPI fails to start and Uvicorn aborts process launch**.
* If `predict()` is called before `load_model()` (e.g. during an unhandled import), it raises `RuntimeError("ML model not loaded. Call load_model() first.")` ([`ml_service.py:70`](file:///F:/Retentio/backend/services/ml_service.py#L70)).

---

## 20. Viva: Model Training vs Preprocessing vs Prediction

* **Model Training:** Offline learning process ([`train_model.py`](file:///F:/Retentio/backend/train/train_model.py)). Fits mathematical parameters (weights $w$ and bias $b$ in Logistic Regression) by minimizing log loss over labeled training data (`X_train`, `y_train`).
* **Model Preprocessing:** Data transformation pipeline ([`preprocess.py`](file:///F:/Retentio/backend/utils/preprocess.py)). Imputes missing values, scales continuous variables to standard normal distributions, and one-hot encodes categoricals. The transformer parameters ($\mu, \sigma$, category sets) are fitted once during training and stored in `preprocessor.pkl`.
* **Model Prediction:** Online inference process ([`ml_service.py`](file:///F:/Retentio/backend/services/ml_service.py)). Takes new customer data, transforms it using the *pre-fitted* transformer (`transform()`, no fitting), and executes $P(\text{churn}) = \sigma(w \cdot X + b)$ to calculate risk scores.

---

## 21. Viva: Why Accuracy is Misleading for Churn

* In the Telco dataset, only **26.5% of customers churn** (1,869 vs 5,174 non-churners).
* A naive dummy classifier that predicts "No Churn" for every customer would achieve **73.5% Accuracy**, despite having **0% Recall** and failing to identify any at-risk accounts.
* In customer retention, the business cost of a **False Negative** (failing to detect an at-risk customer who then churns) is far higher than a False Positive (offering retention outreach to a satisfied customer).
* Therefore, **ROC-AUC** (discrimination ability across all thresholds) and **Recall / F1-score** are the decisive metrics, not Accuracy.

---

## 22. Viva: Python Environment & Dependency Management

* **Virtual Environment:** Uses standard Python virtual environments (`backend/venv`). VS Code settings in [`.vscode/settings.json`](file:///F:/Retentio/.vscode/settings.json) point `python.defaultInterpreterPath` to `backend/venv/Scripts/python.exe`.
* **Dependency Manifest:** Dependencies are specified in [`backend/requirements.txt`](file:///F:/Retentio/backend/requirements.txt).
* **Package Conflicts:** A known conflict between `passlib 1.7.4` and `bcrypt 5.0.0` (removal of `__about__` attribute) was resolved by explicitly pinning `bcrypt==4.0.1`.
* **Frontend Packages:** Managed via `pnpm` (lockfile [`retentio/pnpm-lock.yaml`](file:///F:/Retentio/retentio/pnpm-lock.yaml)).

---

## 23. Viva: Environment Variables & Secret Protection

* **Values Belonging in `.env`:**
  * `MONGODB_URI`: Database connection string containing credentials.
  * `DATABASE_NAME`: Database name (e.g. `retentio`).
  * `JWT_SECRET`: Cryptographic key used to sign and verify HMAC-SHA256 JWTs.
  * `ALLOWED_ORIGINS`: Permitted frontend origins for CORS.
* **How Secrets Must Be Protected:**
  1. Add `.env` to `.gitignore` so secrets are never pushed to version control (verified in [`backend/.gitignore:2`](file:///F:/Retentio/backend/.gitignore#L2)).
  2. Commit only sanitized templates like [`backend/.env.example`](file:///F:/Retentio/backend/.env.example).
  3. Fail startup immediately if `JWT_SECRET` is missing or uses default placeholder strings.
  4. Use secure secret management vaults (e.g., AWS Secrets Manager, Doppler, Azure Key Vault) in production deployments.

---

## 24. Viva: Automated Tests Status & Missing Tests

* **Existing Automated Tests:**
  * **None.** There is no automated test runner configured (`pytest` or `vitest`).
  * Only one manual verification script exists: [`backend/verify_model.py`](file:///F:/Retentio/backend/verify_model.py), which checks that `churn_model.pkl` and `preprocessor.pkl` can be unpickled and run on a single sample row.
* **Critical Missing Tests:**
  1. **Authentication Tests:** Signup duplicate email conflict (409), password length validation (422), valid login (200), bad credentials (401), and token expiry.
  2. **Preprocessing Edge Cases:** Handling empty rows, corrupted numeric strings in `TotalCharges`, unseen categorical strings, and missing required columns.
  3. **Inference & Scoring Tests:** Verifying probabilities correctly map to $[0, 100]$ and boundary threshold evaluations.
  4. **Multi-tenant Isolation Tests:** Ensuring User A cannot read or mutate User B's customer records.

---

## 25. Viva: Project Limitations & Top 3 Next Improvements

* **Current Limitations:**
  1. **Batch Upsert Performance:** Iterative `update_one` / `insert_one` calls in `upsert_customers()` scale poorly on large CSV uploads.
  2. **Static Risk Thresholding:** Binary risk classification based on an arbitrary global cutoff (e.g., 78) ignores customer lifetime value (LTV).
  3. **No Model Monitoring or Retraining:** The model does not learn from customer outcomes or detect data drift over time.
* **Top 3 Recommended Improvements:**
  1. **Batch MongoDB Upserts:** Refactor [`customer_service.py:upsert_customers`](file:///F:/Retentio/backend/services/customer_service.py#L21) to use `collection.bulk_write()` with `UpdateOne(..., upsert=True)` to process thousands of records in a single database round-trip.
  2. **Automated Testing & CI Pipeline:** Implement `pytest` test suites covering authentication, schema validation, and inference, automated via GitHub Actions.
  3. **SHAP Feature Explanations:** Integrate SHAP (SHapley Additive exPlanations) into `ml_service.py` so the UI explains *why* a customer is at risk (e.g., "Month-to-month contract (+18 pts)", "High monthly charges (+12 pts)").

---

## Quick Viva Revision

```text
Q: What is Retentio?
A: A B2B customer churn prediction platform that ingests customer CSV exports,
   scores churn risk using machine learning, and prioritizes at-risk accounts.

Q: Which ML model runs in production?
A: Logistic Regression (class_weight="balanced", max_iter=1000). Selected because
   its ROC-AUC (0.8414) surpassed Random Forest (0.8193) and XGBoost (0.8369).

Q: How is the risk score calculated?
A: predict_proba() extracts churn probability (0.0 - 1.0); multiplied by 100
   and rounded to two decimals to produce a 0 - 100 score.

Q: How is class imbalance handled?
A: class_weight="balanced" in Logistic Regression and Random Forest;
   scale_pos_weight (ratio of negative to positive classes ≈ 2.77) in XGBoost.

Q: How many ML features are required?
A: 19 features (4 numeric: tenure, MonthlyCharges, TotalCharges, SeniorCitizen;
   15 categorical: Contract, InternetService, PaymentMethod, etc.).
   customerID is dropped; Churn is the binary target.

Q: What database is used?
A: MongoDB Atlas, connected asynchronously via Motor.
   Two collections: users (auth & settings) and customers (scores & history).

Q: How does the frontend talk to the backend?
A: Axios client in lib/api.ts sends requests to /api/v1/* with Bearer JWT tokens.
   In development, Vite proxies /api to http://localhost:8000.

Q: What are the biggest security/code weaknesses?
A: 1. No automated test suite (pytest/vitest).
   2. Unescaped regex query in customer search (ReDoS risk).
   3. Hardcoded default fallback for JWT_SECRET.
   4. N+1 sequential database upserts on CSV uploads.
```
