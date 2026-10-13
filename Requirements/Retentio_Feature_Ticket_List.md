# Feature Ticket List
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 1.0
**Status:** Draft
**Date:** August 19, 2026
**Related Docs:** PRD v1.0, Technical Architecture Doc v1.0, Frontend Specification Doc v1.0, Security & Access Doc v1.0

---

## How to Use This Document

Tickets are grouped by **Epic**, ordered in a recommended build sequence. Each ticket includes a suggested ID, description, and acceptance criteria. Use these directly in a tracker (Jira/Trello/Linear/GitHub Projects).

**Priority Key:** 🔴 Must-have (MVP) | 🟡 Should-have | 🟢 Nice-to-have

---

## EPIC 1: ML Model & Data Pipeline

### TICKET-101 🔴 — Acquire & Explore Dataset
- Download Telco Customer Churn dataset (Kaggle).
- Perform basic EDA (nulls, distributions, class balance).
- **AC:** Dataset loaded, summary stats documented.

### TICKET-102 🔴 — Data Preprocessing Pipeline
- Handle missing values.
- Encode categorical columns (Label/One-Hot Encoding).
- Scale numeric columns (StandardScaler).
- Train/test split.
- **AC:** Reusable `preprocess.py` function that transforms raw CSV into model-ready format.

### TICKET-103 🔴 — Train Baseline Models
- Train Logistic Regression and Random Forest as baselines.
- Evaluate with Accuracy, F1, ROC-AUC.
- **AC:** Baseline metrics logged/documented for comparison.

### TICKET-104 🔴 — Train XGBoost Model
- Train XGBoost Classifier.
- Compare against baselines; select best performer.
- **AC:** Final model outperforms or matches baselines on ROC-AUC/F1.

### TICKET-105 🔴 — Convert Predictions to Risk Score
- Implement `predict_proba()` → × 100 → `risk_score` logic.
- Apply benchmark threshold → `risk_label`.
- **AC:** Given sample input, function returns correct score + label.

### TICKET-106 🔴 — Persist Trained Model
- Save `churn_model.pkl` and `preprocessor.pkl` via joblib.
- **AC:** Model and preprocessor load correctly in a fresh Python session.

---

## EPIC 2: Backend Foundation

### TICKET-201 🔴 — FastAPI Project Setup
- Initialize FastAPI app, folder structure per Technical Architecture Doc.
- Configure environment variables (.env, .gitignore).
- **AC:** `GET /health` returns 200 OK.

### TICKET-202 🔴 — MongoDB Connection Setup
- Set up MongoDB Atlas cluster.
- Implement `mongo_client.py` connection module.
- **AC:** Backend successfully connects and can read/write a test document.

### TICKET-203 🔴 — Define Schemas
- Create Pydantic schemas: `UserSchema`, `CustomerSchema`, upload request/response models.
- **AC:** Schemas validate correct/incorrect payloads as expected.

### TICKET-204 🔴 — CORS Configuration
- Restrict origins per Security & Access Doc (localhost dev + production domain).
- **AC:** Requests from allowed origin succeed; others blocked.

---

## EPIC 3: Authentication & Authorization

### TICKET-301 🔴 — Sign Up Endpoint
- `POST /auth/signup` — create business account, hash password (bcrypt), issue JWT.
- **AC:** New user created in DB; valid JWT returned; duplicate email rejected.

### TICKET-302 🔴 — Login Endpoint
- `POST /auth/login` — verify credentials, issue JWT.
- **AC:** Correct credentials return JWT; incorrect return generic error (no user enumeration).

### TICKET-303 🔴 — Get Current User Endpoint
- `GET /auth/me` — return current user info from valid JWT.
- **AC:** Valid token returns user data; invalid/missing token returns 401.

### TICKET-304 🔴 — Auth Dependency (Route Protection)
- Implement `get_current_user` FastAPI dependency for protected routes.
- **AC:** Protected endpoints reject requests without valid JWT.

### TICKET-305 🔴 — Frontend AuthContext
- Build React Context for `user`, `token`, `login()`, `signup()`, `logout()`.
- Store JWT in memory only.
- **AC:** Auth state persists across page navigation (not across refresh, per Security Doc).

### TICKET-306 🔴 — Protected Route Wrapper (Frontend)
- Build `<ProtectedRoute>` component; redirect unauthenticated users to `/login`.
- **AC:** Direct URL access to `/dashboard` etc. without auth redirects correctly.

---

## EPIC 4: Predict Feature (Core ML Flow)

### TICKET-401 🔴 — CSV Upload Endpoint
- `POST /predict/upload` — accept file, validate type/size/columns.
- **AC:** Valid CSV accepted; invalid file type/missing columns rejected with clear error.

### TICKET-402 🔴 — ML Inference Service
- `ml_service.py` — load model/preprocessor once at startup, run inference on uploaded data.
- **AC:** Given valid preprocessed data, returns risk scores for all rows.

### TICKET-403 🔴 — Status Comparison Logic
- Implement At Risk / Saved classification logic against MongoDB (per Technical Architecture Doc Section 5).
- **AC:** New customer ≥ benchmark → "At Risk"; existing "At Risk" customer whose new score < benchmark → "Saved"; correctly updates `history[]`.

### TICKET-404 🔴 — Predict Response Formatting
- Return `{ at_risk: [...], saved: [...], saved_message }` per API spec.
- **AC:** `saved_message` populated only when `saved` array is empty.

### TICKET-405 🔴 — CSV Template Endpoint
- `GET /predict/template` — return downloadable sample CSV.
- **AC:** Downloaded file matches required column structure.

### TICKET-406 🔴 — Frontend Upload Card
- Drag-and-drop + file picker component, `.csv` validation client-side.
- **AC:** Non-CSV files rejected before upload attempt.

### TICKET-407 🔴 — Upload Success Toast
- Show toast on successful upload ("File uploaded successfully").
- **AC:** Toast appears and auto-dismisses; error toast shown on failure.

### TICKET-408 🔴 — Calculate Button & Loading State
- Button triggers `/predict/upload` call; shows loading state during processing.
- **AC:** Button disabled during request; loading indicator visible.

### TICKET-409 🔴 — Results Tables (At Risk / Saved)
- Render `RiskTable` components below upload section using response data.
- Show "No customers saved yet." when applicable.
- **AC:** Tables populate correctly from API response; empty-state message displays correctly.

---

## EPIC 5: Dashboard

### TICKET-501 🔴 — Dashboard Summary Endpoint
- `GET /dashboard/summary` — return total customers, at-risk count, saved count, avg score.
- **AC:** Values match actual DB counts for the authenticated business.

### TICKET-502 🟡 — Dashboard Trend Endpoint
- `GET /dashboard/trend` — return time-series data for charting.
- **AC:** Returns data grouped by date/upload session.

### TICKET-503 🔴 — Summary Cards (Frontend)
- Build `SummaryCard` component; display 4 key metrics.
- **AC:** Cards render live data from `/dashboard/summary`.

### TICKET-504 🔴 — Risk Distribution Chart
- Recharts bar/pie chart showing At Risk vs Saved distribution.
- **AC:** Chart renders correctly with real data; handles empty state gracefully.

### TICKET-505 🟡 — Trend Line Chart
- Recharts line chart showing avg risk score over time.
- **AC:** Chart updates as new uploads add data points.

---

## EPIC 6: Customer Detail & Search

### TICKET-601 🔴 — Customer Search Endpoint
- `GET /customers/search?q=` — search by name or ID, scoped to business (`user_id`).
- **AC:** Returns matching customers only from the authenticated business's data.

### TICKET-602 🔴 — Customer Detail Endpoint
- `GET /customers/{id}` — return full customer record including `history[]`.
- **AC:** Returns 404 for non-existent or cross-tenant customer IDs.

### TICKET-603 🔴 — Search Bar Component (Frontend)
- Debounced search input, results list/dropdown.
- **AC:** Typing triggers search after debounce delay; results display correctly.

### TICKET-604 🔴 — Customer Detail View (Frontend)
- Score history line chart, current status badge, status timeline.
- **AC:** Selecting a search result renders correct customer data.

---

## EPIC 7: Settings

### TICKET-701 🔴 — Update Profile Endpoint
- `PATCH /settings/profile` — update name/business name.
- **AC:** Changes persist in DB; validation on empty fields.

### TICKET-702 🔴 — Update Benchmark Endpoint
- `PATCH /settings/benchmark` — update business's risk benchmark value.
- **AC:** New benchmark applied to subsequent uploads only (not retroactive).

### TICKET-703 🔴 — Settings Form (Frontend)
- Editable name/business name fields, benchmark slider (70–90).
- **AC:** Save button disabled until a field changes (dirty check); confirmation toast on success.

---

## EPIC 8: Landing Page & Public Auth Pages

### TICKET-801 🔴 — Landing Page Animation Sequence
- Framer Motion text sequence: "Losing Customers?" → "Predict Customer Churn Before It Happens" → "Let's Get Started!"
- **AC:** Text transitions play in correct order and timing; CTA reveals AuthCard on completion.

### TICKET-802 🔴 — Animated Background
- Subtle customer-leaving visual (icons/dots drifting).
- **AC:** Background animation loops smoothly, doesn't obstruct text readability.

### TICKET-803 🔴 — Sign Up Page (Frontend)
- Intro blurb + form (business name, name, email, password).
- **AC:** Successful signup redirects to `/predict`; validation errors shown inline.

### TICKET-804 🔴 — Login Page (Frontend)
- Entrance animation, login form, `RotatingFactPanel`.
- **AC:** Facts rotate every 7 seconds; successful login redirects to `/dashboard`.

### TICKET-805 🟡 — Rotating Fact Panel Content
- Compile list of business/churn facts for rotation.
- **AC:** At least 8–10 facts available to avoid quick repetition.

---

## EPIC 9: Navigation & Layout

### TICKET-901 🔴 — Navbar Component
- Logo, user menu, logout button.
- **AC:** Visible on all authenticated pages; logout clears session and redirects to Landing.

### TICKET-902 🔴 — Sidebar Component
- Links: Dashboard, Predict, Customers, Settings.
- **AC:** Active route highlighted; accessible from any authenticated page regardless of entry point (signup vs login).

### TICKET-903 🟡 — Responsive Sidebar/Nav
- Collapse to hamburger/bottom nav on mobile breakpoints.
- **AC:** Usable navigation on small screens (< `md` breakpoint).

---

## EPIC 10: Security Hardening

### TICKET-1001 🔴 — Input Validation Everywhere
- Ensure all endpoints use Pydantic schemas for validation.
- **AC:** Malformed requests return 422 with clear error messages.

### TICKET-1002 🔴 — Multi-Tenant Data Scoping Audit
- Verify every DB query filters by `user_id` from JWT, never client input.
- **AC:** Manual test confirms Business A cannot access Business B's customer data.

### TICKET-1003 🟡 — Rate Limiting on Auth & Upload
- Add basic rate limiting to `/auth/login` and `/predict/upload`.
- **AC:** Excessive requests from same IP throttled/blocked.

### TICKET-1004 🔴 — Secrets & Env Config Review
- Confirm no secrets committed to repo; `.env.example` provided for setup.
- **AC:** Repo scan shows no exposed credentials.

---

## EPIC 11: Deployment

### TICKET-1101 🔴 — Backend Deployment (Render/Railway)
- Deploy FastAPI app with environment variables configured.
- **AC:** Production API accessible over HTTPS.

### TICKET-1102 🔴 — Frontend Deployment (Vercel/Netlify)
- Deploy React app, configure `VITE_API_URL` for production backend.
- **AC:** Production frontend successfully communicates with production backend.

### TICKET-1103 🔴 — Production CORS & Env Verification
- Confirm CORS allows only deployed frontend domain.
- **AC:** Cross-origin requests from unauthorized domains blocked.

---

## Recommended Build Order

1. **EPIC 1** (ML Model) — can be done in parallel with EPIC 2.
2. **EPIC 2** (Backend Foundation)
3. **EPIC 3** (Auth)
4. **EPIC 4** (Predict — core feature)
5. **EPIC 8 & 9** (Landing, Auth Pages, Navigation) — frontend catches up here
6. **EPIC 5** (Dashboard)
7. **EPIC 6** (Customer Detail & Search)
8. **EPIC 7** (Settings)
9. **EPIC 10** (Security Hardening — ongoing, finalize before launch)
10. **EPIC 11** (Deployment)

---

## Related Documents
- Product Requirements Document (PRD) v1.0
- Technical Architecture Document v1.0
- Frontend Specification Document v1.0
- Security & Access Document v1.0