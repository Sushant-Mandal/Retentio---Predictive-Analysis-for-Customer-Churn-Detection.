# Security & Access Document
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 1.0
**Status:** Draft
**Date:** August 19, 2026
**Related Docs:** Retentio PRD v1.0, Technical Architecture Document v1.0, Frontend Specification Document v1.0

---

## 1. Purpose

This document defines authentication, authorization, data isolation, and general security practices for Retentio. It covers how user accounts and business customer data are protected across the frontend, backend, and database layers.

---

## 2. Authentication

### 2.1 Method
- **JWT (JSON Web Tokens)** issued on successful Sign Up or Login.
- Token contains: `user_id`, `email`, `exp` (expiration) — no sensitive data embedded.
- Signed using a secret key (`HS256`) stored as an environment variable on the backend (never hardcoded, never committed to source control).

### 2.2 Password Handling
- Passwords hashed using **bcrypt** (via `passlib`) before storage — plaintext passwords are never stored or logged.
- Minimum password requirements enforced at signup: 8+ characters, at least 1 number (basic baseline; can be strengthened later).

### 2.3 Token Storage (Frontend)
- JWT stored **in memory** (React Context state), not `localStorage` or `sessionStorage`.
- **Rationale:** `localStorage` is accessible via JavaScript, making tokens vulnerable to XSS-based theft. In-memory storage limits exposure but requires re-login on full page refresh.
- **Trade-off accepted for v1:** No persistent "remember me" session across browser refreshes. This can be revisited in a future version using **httpOnly, Secure cookies** for refresh tokens if persistent sessions become a priority.

### 2.4 Token Expiration
- Access token expiry: **24 hours** (adjustable).
- No refresh token flow in v1 — user re-authenticates after expiry (simple, low-complexity approach appropriate for MVP scope).

---

## 3. Authorization & Access Control

### 3.1 Route Protection (Backend)
- All endpoints except `/auth/signup` and `/auth/login` require a valid JWT in the `Authorization: Bearer <token>` header.
- FastAPI dependency (`get_current_user`) validates token on every protected request and extracts `user_id` for scoping data access.

### 3.2 Route Protection (Frontend)
- `<ProtectedRoute>` wrapper checks `isAuthenticated` before rendering Dashboard, Predict, Customers, or Settings pages.
- Unauthenticated access attempts redirect to `/login`.

### 3.3 Data Isolation (Multi-Tenancy)
- Retentio is multi-tenant — multiple businesses use the same platform, so **no business may ever see another business's customer data.**
- Every `customers` document includes a `user_id` field tying it to the owning business account.
- **All backend queries must filter by `user_id`** (extracted from the JWT, never trusted from the frontend request body/params) — this is a hard rule, not optional:
  ```python
  # Correct — user_id from token, not from client input
  db.customers.find({"user_id": current_user.id})
  ```
- No endpoint should accept a client-supplied `user_id` to determine whose data to return.

---

## 4. API Security

### 4.1 Input Validation
- All request bodies validated via **Pydantic schemas** (FastAPI's built-in validation) — rejects malformed or unexpected data before it reaches business logic.
- CSV uploads validated for:
  - Correct file extension (`.csv`) and MIME type.
  - Required columns present (reject with clear error if missing).
  - Reasonable file size limit (e.g., max 5–10MB for v1) to prevent abuse/overload.

### 4.2 File Upload Safety
- Uploaded CSVs are parsed directly into memory via pandas — **never executed, never saved as executable files, never used to construct file system paths from user input.**
- No user-supplied filenames used directly for storage paths (prevents path traversal).

### 4.3 CORS Policy
- FastAPI CORS middleware restricts allowed origins to:
  - Local dev: `http://localhost:5173`
  - Production: the deployed frontend domain only (no wildcard `*` origins in production).

### 4.4 Rate Limiting (Recommended for v1)
- Basic rate limiting on `/auth/login` and `/predict/upload` endpoints to reduce brute-force and abuse risk (e.g., via `slowapi` or a reverse-proxy-level limit).

### 4.5 HTTPS
- All production traffic served over **HTTPS only** (enforced by hosting platform — Render/Railway/Vercel provide this by default).

---

## 5. Database Security

- MongoDB Atlas cluster access restricted via **IP allowlisting** (or VPC peering if scaled later) and database-user credentials with least-privilege access (read/write only to the specific database, not admin-level).
- Connection string stored as an environment variable, never committed to source control.
- No direct client-side database access — all reads/writes go through the FastAPI backend.

---

## 6. Secrets Management

| Secret | Storage |
|---|---|
| JWT signing key | Environment variable (backend host) |
| MongoDB connection string | Environment variable (backend host) |
| Frontend API base URL | Environment variable (`VITE_API_URL`, build-time) |

- `.env` files excluded from version control via `.gitignore`.
- No secrets logged, printed, or exposed in error messages returned to the client.

---

## 7. Error Handling & Information Disclosure

- Generic error messages returned to the client (e.g., "Invalid email or password") — avoid revealing whether an email exists in the system (prevents user enumeration).
- Detailed stack traces/internal errors logged server-side only, never returned in API responses.

---

## 8. Session/Account Security

- Logout clears in-memory token and redirects to Landing/Login page.
- No account lockout mechanism in v1 (acceptable for MVP); can be added later alongside rate limiting for repeated failed logins.

---

## 9. Out of Scope (Deferred to Future Versions)

- Multi-factor authentication (MFA).
- Role-based access control within a single business account (e.g., admin vs. team member permissions).
- Refresh token rotation / persistent "remember me" sessions via httpOnly cookies.
- Full audit logging of data access/changes.
- Penetration testing / formal security audit.
- GDPR/CCPA-specific data handling workflows (data export, right to deletion) — should be addressed before any real customer PII is processed in production.

---

## 10. Summary Checklist (MVP Security Baseline)

- [x] Passwords hashed with bcrypt
- [x] JWT-based auth, in-memory token storage
- [x] All customer data scoped by `user_id` from token (never client input)
- [x] Pydantic input validation on all endpoints
- [x] CSV upload type/size/column validation
- [x] CORS restricted to known origins
- [x] HTTPS enforced in production
- [x] Secrets in environment variables only
- [x] Generic auth error messages (no user enumeration)

---

## 11. Related Documents
- Product Requirements Document (PRD) v1.0
- Technical Architecture Document v1.0
- Frontend Specification Document v1.0
- Feature Ticket List *(separate)*
