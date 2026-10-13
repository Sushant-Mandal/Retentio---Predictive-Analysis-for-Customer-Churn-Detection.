# Technical Architecture Document
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 1.0
**Status:** Draft
**Date:** August 19, 2026
**Related Doc:** Retentio PRD v1.0

---

## 1. Architecture Overview

Retentio follows a **client-server architecture** with a decoupled frontend and backend:

```
┌─────────────────┐        HTTPS/REST (Axios)        ┌──────────────────┐
│   React Frontend │ ───────────────────────────────► │  FastAPI Backend  │
│  (Tailwind, ShadCN,                                  │  (Python)         │
│  Recharts, Lucide) │ ◄─────────────────────────────  │                   │
└─────────────────┘         JSON responses            └────────┬──────────┘
                                                                  │
                                                     ┌────────────┼────────────┐
                                                     │                         │
                                            ┌────────▼────────┐      ┌─────────▼────────┐
                                            │  ML Layer         │      │  MongoDB Atlas    │
                                            │  (XGBoost model,  │      │  (customers,       │
                                            │  preprocessor)    │      │  users collections)│
                                            └───────────────────┘      └───────────────────┘
```

- **Frontend:** React SPA — handles UI, animations, auth forms, file upload, and data visualization.
- **Backend:** FastAPI — handles auth, file processing, ML inference, and DB read/write.
- **ML Layer:** Pre-trained XGBoost model + preprocessor loaded into memory by the backend (not a separate service in v1).
- **Database:** MongoDB Atlas — stores user accounts and customer risk records/history.

---

## 2. Tech Stack Summary

| Layer | Technology |
|---|---|
| Frontend Framework | React.js |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Icons | lucide-react |
| Charts | Recharts |
| HTTP Client | Axios |
| Animations | Framer Motion |
| Backend Framework | FastAPI (Python) |
| ML Libraries | scikit-learn, XGBoost |
| Data Handling | pandas, numpy |
| Model Persistence | joblib |
| Database | MongoDB (Atlas) |
| DB Driver | PyMongo / Motor |
| Auth | JWT (JSON Web Tokens) |

---

## 3. System Components

### 3.1 Frontend (React SPA)
- Single-page application with client-side routing (React Router).
- Pages: Landing, Sign Up, Login, Dashboard, Predict, Customers, Settings.
- Communicates with backend exclusively via REST API calls (Axios).
- Stores JWT token (post-login/signup) for authenticated requests — kept in memory/context (not localStorage, to reduce token exposure risk — detailed in Security doc).

### 3.2 Backend (FastAPI)
Organized into logical modules:
- **Auth module** — signup/login, JWT issuance, password hashing.
- **Predict module** — CSV ingestion, preprocessing, ML inference, risk classification.
- **Customers module** — retrieval of at-risk/saved customers, search, history.
- **Settings module** — user profile updates, benchmark configuration.

### 3.3 ML Layer
- Model trained offline (Step 1–5 of build plan) and saved as `.pkl` files.
- Loaded once at backend startup (not reloaded per request) for performance.
- Inference logic isolated in a `services/ml_service.py` module — swappable without touching API routes.

### 3.4 Database (MongoDB)
Two primary collections:

**`users` collection**
```json
{
  "_id": "ObjectId",
  "business_name": "Acme Corp",
  "name": "John Doe",
  "email": "john@acme.com",
  "password_hash": "...",
  "benchmark": 78,
  "created_at": "2026-08-19"
}
```

**`customers` collection**
```json
{
  "_id": "C1023",
  "user_id": "ObjectId (owning business)",
  "name": "Jane Smith",
  "current_score": 82,
  "status": "At Risk",
  "history": [
    {"date": "2026-07-01", "score": 65},
    {"date": "2026-08-01", "score": 82}
  ]
}
```

> Note: `user_id` field scopes each customer record to the business that uploaded it, since Retentio is multi-tenant (multiple businesses use the same platform).

---

## 4. API Design

Base URL: `/api/v1`

### Auth Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Create business account, return JWT |
| POST | `/auth/login` | Authenticate, return JWT |
| GET | `/auth/me` | Get current logged-in user info |

### Predict Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict/upload` | Upload CSV, run ML model, update DB, return results |
| GET | `/predict/template` | Download sample CSV template |

**Response shape for `/predict/upload`:**
```json
{
  "at_risk": [
    {"customer_id": "C1023", "name": "Jane Smith", "score": 82}
  ],
  "saved": [
    {"customer_id": "C1010", "name": "Mike Lee", "previous_score": 81, "current_score": 60}
  ],
  "saved_message": null
}
```
*(If `saved` array is empty → `saved_message: "No customers saved yet."`)*

### Customers Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/customers/at-risk` | List all current at-risk customers |
| GET | `/customers/saved` | List all saved customers |
| GET | `/customers/search?q=` | Search by name or ID |
| GET | `/customers/{id}` | Get individual customer detail + history |

### Settings Endpoints
| Method | Endpoint | Description |
|---|---|---|
| PATCH | `/settings/profile` | Update name/business name |
| PATCH | `/settings/benchmark` | Update risk benchmark |

### Dashboard Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/dashboard/summary` | Total customers, at-risk count, saved count, avg score |
| GET | `/dashboard/trend` | Risk distribution / trend data for charts |

---

## 5. Request Flow — Predict Page (Core Flow)

```
1. User uploads CSV (frontend) 
      → Axios POST /predict/upload (multipart/form-data)

2. FastAPI receives file
      → pandas reads CSV
      → preprocessor.pkl transforms data
      → churn_model.pkl (XGBoost) generates probability
      → probability × 100 = risk_score

3. For each customer row:
      → Query MongoDB `customers` collection by customer_id + user_id
      → Apply status logic:
          - New & score ≥ benchmark → insert, status "At Risk"
          - Existing "At Risk" & score < benchmark → update, status "Saved"
          - Existing "At Risk" & score ≥ benchmark → remains "At Risk"
      → Append {date, score} to history[]

4. Backend returns JSON: { at_risk: [...], saved: [...], saved_message }

5. Frontend renders At Risk table + Saved table (or "No customers saved yet.")
```

---

## 6. Folder Structure

### Backend
```
backend/
  main.py
  api/
    routes/
      auth.py
      predict.py
      customers.py
      settings.py
      dashboard.py
  services/
    ml_service.py          # model loading + inference
    customer_service.py    # status comparison logic
    auth_service.py        # JWT + password hashing
  db/
    mongo_client.py
  model/
    churn_model.pkl
    preprocessor.pkl
  train/
    train_model.py
  utils/
    preprocess.py
    csv_validator.py
  schemas/
    user_schema.py
    customer_schema.py
  requirements.txt
```

### Frontend
```
frontend/
  src/
    pages/
      Landing.jsx
      SignUp.jsx
      Login.jsx
      Dashboard.jsx
      Predict.jsx
      Customers.jsx
      Settings.jsx
    components/
      Navbar.jsx
      Sidebar.jsx
      UploadCard.jsx
      RiskTable.jsx
      ScoreChart.jsx
      SummaryCard.jsx
      Toast.jsx
    context/
      AuthContext.jsx
    services/
      api.js               # Axios instance + interceptors
    routes/
      AppRoutes.jsx
    App.jsx
    main.jsx
  tailwind.config.js
  package.json
```

---

## 7. Data Flow Between Frontend & Backend

- All authenticated requests attach JWT via Axios interceptor (`Authorization: Bearer <token>`).
- `AuthContext` (React Context API) holds current user state, propagated across pages after login/signup.
- Axios `baseURL` configured via environment variable (`VITE_API_URL`) — differs between local dev and production.

---

## 8. Environments

| Environment | Frontend Host | Backend Host | Database |
|---|---|---|---|
| Local Dev | localhost:5173 (Vite) | localhost:8000 | MongoDB Atlas (dev cluster) or local MongoDB |
| Production | Vercel/Netlify | Render/Railway | MongoDB Atlas (production cluster) |

CORS must be configured on FastAPI to allow the frontend's deployed domain.

---

## 9. Scalability Considerations (v1 scope)

- MongoDB collections indexed on `user_id` and `customer_id` for fast lookups as customer base grows.
- ML model loaded once in memory at server startup — avoids reloading `.pkl` files per request.
- CSV processing is synchronous in v1 (acceptable for expected file sizes); can be moved to a background task queue (Celery) in a future version if files grow large.

---

## 10. Out of Scope (Deferred to Future Architecture)

- Real-time/streaming data ingestion (webhooks, scheduled syncs) — see Option 3 discussion.
- Horizontal scaling / load balancing setup.
- Model retraining pipeline automation (MLOps).
- Caching layer (Redis) for dashboard queries.

---

## 11. Related Documents
- Product Requirements Document (PRD) v1.0
- Security & Access Document *(separate)*
- Frontend Specification Document *(separate)*
- Feature Ticket List *(separate)*
