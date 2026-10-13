# Feature Ticket List
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 2.0
**Status:** Draft
**Date:** August 28, 2026
**Related Docs:** PRD v1.0, Technical Architecture Doc v1.0, Frontend Specification Doc **v3.0**, Security & Access Doc v1.0

---

## Changelog vs v1.0

The frontend spec was replaced with `Frontend_New.md` (v3.0). That version changes the Landing Page and Sign Up/Login pages significantly and also clarifies that navigation uses the `Dock` component, not a Navbar/Sidebar. This version updates the ticket list to match:

- **EPIC 8 rewritten.** Old tickets (two-beat Framer Motion text sequence, generic "customers drifting" background shared across Landing/auth pages, GradientWaves on Sign Up/Login) are replaced. New tickets cover `AnimatedHandsBackground`, `useCursorGlow`, `GlowText`, three-beat `ScrollFloat` sequence, `CustomerLossAnimation`, hand-anchored `SpecularButton`, and the `BackgroundVideo` component now used on Sign Up/Login.
- **EPIC 9 rewritten.** Removed `Navbar`/`Sidebar` tickets (901/902) — neither frontend spec ever specified them; both use `Dock`. Replaced with Dock integration, Authenticated Layout, and a floating logout/profile menu (since Dock is capped at 4 primary items).
- **New EPIC 12 added** — Design System & Shared Visual Components. Neither v1.0 nor v2.0 of the ticket list had explicit tickets for `GlassCard`, `GradientWaves`, or layout scaffolding, even though every page depends on them. Adding these makes the build order actually buildable in sequence.
- Epics 1–7, 10, 11 are unchanged from v1.0 — they don't depend on the frontend's visual system.
- Ticket IDs are renumbered within the affected epics; cross-references elsewhere are unaffected since no other epic pointed at 8xx/9xx IDs.

---

## How to Use This Document

Tickets are grouped by **Epic**, ordered in a recommended build sequence. Each ticket includes a suggested ID, description, and acceptance criteria. Use these directly in a tracker (Jira/Trello/Linear/GitHub Projects).

**Priority Key:** 🔴 Must-have (MVP) | 🟡 Should-have | 🟢 Nice-to-have

---

## EPIC 1: ML Model & Data Pipeline
*(unchanged from v1.0)*

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
*(unchanged from v1.0)*

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
*(unchanged from v1.0)*

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
*(unchanged from v1.0)*

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
- Drag-and-drop + file picker component (`UploadCard`, wrapped in `GlassCard`), `.csv` validation client-side.
- **AC:** Non-CSV files rejected before upload attempt.

### TICKET-407 🔴 — Upload Success Toast
- Show toast on successful upload ("File uploaded successfully").
- **AC:** Toast appears and auto-dismisses; error toast shown on failure.

### TICKET-408 🔴 — Calculate Button & Loading State
- Button triggers `/predict/upload` call; shows loading state during processing.
- **AC:** Button disabled during request; loading indicator visible.

### TICKET-409 🔴 — Results Tables (At Risk / Saved)
- Render `RiskTable` components (in `GlassCard`) below upload section using response data.
- Show "No customers saved yet." when applicable.
- **AC:** Tables populate correctly from API response; empty-state message displays correctly.

---

## EPIC 5: Dashboard
*(unchanged from v1.0)*

### TICKET-501 🔴 — Dashboard Summary Endpoint
- `GET /dashboard/summary` — return total customers, at-risk count, saved count, avg score.
- **AC:** Values match actual DB counts for the authenticated business.

### TICKET-502 🟡 — Dashboard Trend Endpoint
- `GET /dashboard/trend` — return time-series data for charting.
- **AC:** Returns data grouped by date/upload session.

### TICKET-503 🔴 — Summary Cards (Frontend)
- Build `SummaryCard` component (`GlassCard`-based); display 4 key metrics.
- **AC:** Cards render live data from `/dashboard/summary`.

### TICKET-504 🔴 — Risk Distribution Chart
- Recharts bar/pie chart showing At Risk vs Saved distribution, inside `GlassCard`.
- **AC:** Chart renders correctly with real data; handles empty state gracefully.

### TICKET-505 🟡 — Trend Line Chart
- Recharts line chart showing avg risk score over time.
- **AC:** Chart updates as new uploads add data points.

---

## EPIC 6: Customer Detail & Search
*(unchanged from v1.0)*

### TICKET-601 🔴 — Customer Search Endpoint
- `GET /customers/search?q=` — search by name or ID, scoped to business (`user_id`).
- **AC:** Returns matching customers only from the authenticated business's data.

### TICKET-602 🔴 — Customer Detail Endpoint
- `GET /customers/{id}` — return full customer record including `history[]`.
- **AC:** Returns 404 for non-existent or cross-tenant customer IDs.

### TICKET-603 🔴 — Search Bar Component (Frontend)
- Debounced search input, results list/dropdown, `GlassCard`-styled.
- **AC:** Typing triggers search after debounce delay; results display correctly.

### TICKET-604 🔴 — Customer Detail View (Frontend)
- Score history line chart, current status badge, status timeline, `GlassCard`-wrapped.
- **AC:** Selecting a search result renders correct customer data.

---

## EPIC 7: Settings
*(unchanged from v1.0)*

### TICKET-701 🔴 — Update Profile Endpoint
- `PATCH /settings/profile` — update name/business name.
- **AC:** Changes persist in DB; validation on empty fields.

### TICKET-702 🔴 — Update Benchmark Endpoint
- `PATCH /settings/benchmark` — update business's risk benchmark value.
- **AC:** New benchmark applied to subsequent uploads only (not retroactive).

### TICKET-703 🔴 — Settings Form (Frontend)
- Editable name/business name fields, benchmark slider (70–90), inside `GlassCard`.
- **AC:** Save button disabled until a field changes (dirty check); confirmation toast on success.

---

## EPIC 8: Landing Page — REWRITTEN for v3.0

> Replaces v1.0's TICKET-801/802 (two-beat text + generic drifting-icons background). The Landing Page is now its own top-level layout with a custom WebGL "reaching hands" scene, a 3-beat scroll sequence, and a hand-anchored CTA.

### TICKET-801 🔴 — Landing Layout Scaffold
- Create Landing as its own top-level layout (not grouped with Public Layout) — no Dock, no shared background with Sign Up/Login.
- **AC:** `/` renders independently of Public/Authenticated layouts; no other layout's background ever mounts alongside it.

### TICKET-802 🔴 — `AnimatedHandsBackground` — Core WebGL Scene
- Build custom `ogl`-based scene: dark space backdrop, two hand meshes/wireframe rendered with an emissive/fresnel-style glow shader.
- Idle motion (slow rotation, breathing glow, faint particle drift) independent of scroll, driven by `requestAnimationFrame`.
- **AC:** Background renders as a genuine animation (not a static image, GIF, or video loop); idle motion runs continuously without user input.
- **Note:** Per the spec's scope/timeline caveat, if a full 3D hand mesh isn't feasible in the timeline, fall back to an SVG line-art version (stroke draw-in via Framer Motion/GSAP + `feGaussianBlur`/`feColorMatrix` glow). Flag this trade-off with whoever supplied the reference art before committing to a path — this decision should happen before TICKET-803/807 are built on top of it.

### TICKET-803 🔴 — `useCursorGlow` Hook
- Track pointer position (normalized 0–1) and last-move timestamp.
- Expose `isIdle()` — true when 5+ seconds have passed since the last `pointermove`.
- **AC:** Hook correctly reports idle state after 5s of no movement; resumes tracking immediately on next `pointermove`.

### TICKET-804 🔴 — Cursor-Reactive Glow Integration
- Feed `useCursorGlow`'s position into `AnimatedHandsBackground`'s mouse uniform (or overlay, if SVG fallback path is used), lerping toward the pointer each frame — same pattern as `GradientWaves`' `currentMouse`/`targetMouse`.
- Freeze glow position (stop updating the uniform) while `isIdle()` is true.
- **AC:** Glow visibly follows the cursor across the full page; freezes in place after 5s idle; resumes on movement.

### TICKET-805 🔴 — `GlowText` Component
- Black fill text with white glow (`text-shadow` layers) + black drop shadow, per Section 6.5 design tokens.
- **AC:** Renders legibly over the hands background; visually matches spec (black fill, white outer glow, dark drop shadow).

### TICKET-806 🔴 — Three-Beat `ScrollFloat` Text Sequence
- Implement Beat 1 ("Welcome to Retentio"), Beat 2 ("Losing Customers?"), Beat 3 ("Start Your Customer Retention Today"), each `GlowText`-styled and tied to the same pinned `scrollContainerRef` as the hands background.
- **AC:** All three beats reveal character-by-character in scroll-tied sequence, in order; text and background scroll progress stay in sync.

### TICKET-807 🔴 — `CustomerLossAnimation`
- Small Framer Motion loop next to Beat 2 depicting customer icons/dots scattering outward with fading opacity.
- **AC:** Animation loops smoothly next to "Losing Customers?" without obstructing text readability.

### TICKET-808 🔴 — Hand-Anchored `SpecularButton` CTA
- "Get Started" button appears after Beat 3 completes, positioned via a viewport-relative anchor tuned to the fingertip gap in the rendered hands scene.
- **AC:** Button appears only after Beat 3 finishes; visually sits in the gap between the hands' nearest fingers at common viewport sizes (requires manual visual tuning once TICKET-802 is built — flag as a follow-up tuning pass, not a one-shot pixel value).

### TICKET-809 🔴 — Landing Auth Reveal (`.landing-auth-card`)
- On CTA click: zoom-out transition, then reveal Sign Up/Login option card styled per `.landing-auth-card` (stronger opacity/blur than standard `GlassCard`, since it sits directly on the busier hands background).
- **AC:** Click reveals both Sign Up and Login options; selecting either navigates to `/signup` or `/login` respectively.

### TICKET-810 🔴 — Landing Background Performance Guard
- Apply the same off-screen/hidden-tab pause pattern used in `GradientWaves` (`IntersectionObserver` + `visibilitychange`) to `AnimatedHandsBackground`, even though Landing is a single page.
- **AC:** WebGL render loop pauses when tab is hidden or backgrounded; resumes on return.

### TICKET-811 🟡 — Mobile Cursor-Glow Fallback
- On touch devices, substitute a fixed/ambient glow or subtle idle pulse instead of simulating cursor-follow from touch events.
- **AC:** No broken/jumpy glow behavior on touch devices; a reasonable static or pulsing alternative is shown instead.

### TICKET-812 🟢 — Reduced-Motion Landing Variant
- Follow-up ticket (explicitly flagged as out-of-initial-scope in the spec, Section 16): build an alternate Landing experience respecting `prefers-reduced-motion` given how animation-heavy this page is.
- **AC:** With `prefers-reduced-motion` set, hands background idle motion, scroll-pinning intensity, and/or cursor-glow are reduced or disabled.

---

## EPIC 8B: Public Layout — Sign Up & Login (Background changed to Video)

> Sign Up/Login no longer use `GradientWaves`; they now share a `BackgroundVideo` mounted once in a dedicated Public Layout.

### TICKET-813 🔴 — Public Layout Scaffold
- Create `PublicLayout` wrapping `/signup` and `/login`, mounting `BackgroundVideo` once so it isn't restarted on navigation between the two.
- **AC:** Navigating between Sign Up and Login does not restart or flash the background video.

### TICKET-814 🔴 — `BackgroundVideo` Component
- `<video autoPlay muted loop playsInline preload="auto">`, `object-fit: cover`, fixed full-viewport layer.
- Source: repurposed video originally planned for Landing's frame sequence — encode as compressed `.mp4` (H.264), modest resolution/bitrate; provide a static `poster` frame to avoid flash-of-empty-background.
- **AC:** Video loops seamlessly, autoplays across major browsers (muted), no visible empty-background flash before load.

### TICKET-815 🔴 — Sign Up Page (Frontend)
- Intro blurb + form (business name, name, email, password, confirm password), wrapped in `GlassCard`, on `BackgroundVideo`.
- **AC:** Successful signup redirects to `/predict`; validation errors shown inline.

### TICKET-816 🔴 — Login Page (Frontend)
- Entrance animation, login form, `RotatingFactPanel` side panel — `GlassCard`-wrapped, on `BackgroundVideo`.
- **AC:** Facts rotate every 7 seconds; successful login redirects to `/dashboard`.

### TICKET-817 🟡 — Rotating Fact Panel Content
- Compile list of business/churn facts for rotation.
- **AC:** At least 8–10 facts available to avoid quick repetition.

---

## EPIC 9: Navigation & Layout — REWRITTEN (Dock, not Navbar/Sidebar)

> v1.0's TICKET-901/902 specified a `Navbar` and `Sidebar`, but **neither frontend spec (v2.0 or v3.0) uses those** — navigation is the `Dock` component on all four authenticated pages. Replacing with tickets that match what's actually specified.

### TICKET-901 🔴 — Authenticated Layout Scaffold
- Mount `GradientWaves` once (not per-page) for Dashboard/Predict/Customers/Settings; render `Dock` fixed at bottom.
- **AC:** Navigating between the four authenticated pages does not remount or flicker the `GradientWaves` canvas.

### TICKET-902 🔴 — Dock Navigation Component
- Integrate React Bits `Dock` with 4 items (Dashboard, Predict, Customers, Settings) using `react-icons/vsc` icons.
- Active-route highlighting via `useLocation()` + conditional `DockItem` className.
- **AC:** Dock visible on all four authenticated pages; correct icon highlighted for current route; clicking navigates correctly.

### TICKET-903 🔴 — Floating Logout / Profile Menu
- Small floating `GlassCard` menu in the top-right corner (separate from Dock, since Dock is capped at 4 core items) for logout/profile quick-view.
- **AC:** Visible on all authenticated pages; logout clears session and redirects to Landing.

### TICKET-904 🟡 — Responsive Dock
- On screens `< md`, disable/reduce magnification (hover-based magnification doesn't translate to touch) — fixed equal-sized items or simpler bottom bar.
- **AC:** Dock remains usable and doesn't visually break on small screens.

---

## EPIC 10: Security Hardening
*(unchanged from v1.0)*

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
*(unchanged from v1.0)*

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

## EPIC 12: Design System & Shared Visual Components *(new)*

> Neither v1.0 nor v2.0 of this ticket list had explicit tickets for the components every page depends on. Adding them so the recommended build order (below) is actually followable — these should land before EPIC 4–9 frontend tickets, not after.

### TICKET-1201 🔴 — `GlassCard` Component
- Shared glassmorphism wrapper (`.glass-panel` utility: translucent fill, blur, border, shadow) used across Sign Up, Login, Dashboard, Predict, Customers, Settings.
- **AC:** Visually consistent across all consuming pages; single source of truth for the glass style (no duplicated Tailwind classes per page).

### TICKET-1202 🔴 — `GradientWaves` Shared Instance
- Integrate React Bits `GradientWaves` with the spec's default config; mount once in Authenticated Layout only (per TICKET-901) — never per-page.
- **AC:** Only one `GradientWaves` instance exists at a time across Dashboard/Predict/Customers/Settings; pauses via `IntersectionObserver`/`visibilitychange` when off-screen or tab hidden.

### TICKET-1203 🔴 — Design Tokens & Base Styles
- Set up Tailwind config / CSS variables for page background, glass fill/border, text colors, status colors, `GradientText` accent colors, border radii, font.
- **AC:** Tokens available app-wide; status badges (At Risk / Saved) use solid (non-glass) fills per spec for legibility.

### TICKET-1204 🟡 — `StatusBadge` Component
- Reusable red/green badge for At Risk / Saved states, used in `RiskTable` and Customer Detail.
- **AC:** Renders correct color/label per status; solid fill (not glass-blurred) for legibility.

### TICKET-1205 🟡 — Global Loading States
- Shared `LoadingSpinner`/`Skeleton` components (shadcn-based), styled semi-transparent to match the glass theme.
- **AC:** Used consistently across Dashboard, Predict, and Customers while data is loading.

---

## Recommended Build Order

1. **EPIC 1** (ML Model) — can be done in parallel with EPIC 2.
2. **EPIC 2** (Backend Foundation)
3. **EPIC 3** (Auth)
4. **EPIC 12** (Design System) — build shared visual components before any page that consumes them.
5. **EPIC 4** (Predict — core feature)
6. **EPIC 8 & 8B** (Landing, Public Auth Pages) and **EPIC 9** (Dock Navigation & Authenticated Layout) — frontend catches up here. Resolve the AnimatedHandsBackground scope decision (TICKET-802's build-vs-fallback note) early, since TICKET-804/808 depend on it.
7. **EPIC 5** (Dashboard)
8. **EPIC 6** (Customer Detail & Search)
9. **EPIC 7** (Settings)
10. **EPIC 10** (Security Hardening — ongoing, finalize before launch)
11. **EPIC 11** (Deployment)

---

## Related Documents
- Product Requirements Document (PRD) v1.0
- Technical Architecture Document v1.0
- Frontend Specification Document **v3.0**
- Security & Access Document v1.0
