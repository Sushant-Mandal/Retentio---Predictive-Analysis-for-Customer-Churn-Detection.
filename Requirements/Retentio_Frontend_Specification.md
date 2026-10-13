# Frontend Specification Document
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 2.0
**Status:** Draft
**Date:** August 20, 2026
**Related Docs:** Retentio PRD v1.0, Technical Architecture Document v1.0
**Changelog:** v2.0 — Integrated React Bits components (Dock, GradientWaves, SpecularButton, ScrollFloat, GradientText) and defined glassmorphism visual system.

---

## 1. Purpose

This document defines the frontend structure, page-by-page specifications, components, visual system, state management, and API integration points for Retentio's React application.

---

## 2. Tech Stack

| Category | Technology |
|---|---|
| Framework | React.js (Vite) |
| Styling | Tailwind CSS + glassmorphism utility classes |
| UI Components | shadcn/ui (forms, tables, sliders, toasts) |
| Icons | lucide-react + react-icons (`Vsc*` set, used by Dock) |
| Charts | Recharts |
| HTTP Client | Axios |
| Animation | Framer Motion, GSAP (`ScrollTrigger`) |
| WebGL Effects | ogl (via GradientWaves, SpecularButton) |
| Routing | React Router |
| State Management | React Context API (Auth) + local component state |

### 2.1 New Dependencies (React Bits)
| Package | Used By |
|---|---|
| `motion` | Dock |
| `ogl` | GradientWaves, SpecularButton |
| `gsap` | ScrollFloat |

Install once:
```bash
npm i motion ogl gsap
```

---

## 3. Visual System

### 3.1 Design Language
Retentio's post-landing UI is built on a **dark glassmorphism system**: a single animated `GradientWaves` background sits behind every authenticated page, and all content — cards, tables, forms, panels — floats above it as translucent, blurred "glass" surfaces. The Landing Page is the one exception: it uses its own frame-sequence scroll animation as the background instead of GradientWaves.

### 3.2 Global Background Rule

| Page | Background |
|---|---|
| Landing (`/`) | Custom 300-frame scroll-scrubbed video sequence (canvas-based, per earlier scroll-animation plan) |
| Sign Up, Login | `GradientWaves` |
| Dashboard, Predict, Customers, Settings | `GradientWaves` (single shared instance, mounted once in the Authenticated Layout, not remounted per page) |

**`GradientWaves` config (shared default):**
```jsx
<GradientWaves
  horizonColor="#5227FF"
  waveColor="#FF9FFC"
  crestColor="#FFFFFF"
  speed={0.4}
  amplitude={2.5}
  waveScale={0.6}
  waveRatio={0.9}
  swell={35}
  turbulence={20}
  tilt={1.11}
  zoom={1.0}
  height={5.5}
  fogDepth={15}
  detail="medium"
  brightness={1.0}
  opacity={1.0}
  mouseInteraction={true}
  parallaxStrength={0.5}
  grain={true}
  grainIntensity={0.05}
/>
```

- Rendered as a fixed, full-viewport layer (`position: fixed; inset: 0; z-index: 0`) behind all page content.
- **Important:** Mount `GradientWaves` once in `AuthLayout.jsx` (and once in a shared `PublicLayout.jsx` for Sign Up/Login) rather than inside every page — remounting a WebGL canvas per route change causes flicker and wastes GPU cycles.

### 3.3 Glassmorphism Card Style

All content surfaces (cards, tables, modals, form panels, side panels) use a shared `.glass-panel` utility:

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 1rem; /* rounded-2xl */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}
```

Applied via a reusable `GlassCard` wrapper component so every card in the app (SummaryCard, RiskTable container, UploadCard, forms, RotatingFactPanel, Customer Detail panel) is visually consistent without repeating Tailwind classes everywhere.

```jsx
// components/GlassCard.jsx
export default function GlassCard({ children, className = '' }) {
  return <div className={`glass-panel p-6 ${className}`}>{children}</div>;
}
```

### 3.4 Design Tokens

| Token | Value |
|---|---|
| Page background | Black/near-black base (`#0a0a0f`), with `GradientWaves` layered on top |
| Glass fill | `rgba(255,255,255,0.06)` |
| Glass border | `rgba(255,255,255,0.12)` |
| Primary text | `#f5f5f5` |
| Muted text | `#a1a1aa` (`zinc-400`) |
| Danger/At Risk | Red (`red-400`/`red-500`, tuned for dark glass backgrounds) |
| Success/Saved | Green (`green-400`/`green-500`) |
| Accent gradient (headings, highlights) | `GradientText` colors: `#40ffaa → #4079ff → #40ffaa → #4079ff → #40ffaa` |
| Font | Inter or similar sans-serif |
| Border radius | `rounded-2xl` (16px) for cards, `rounded-lg` for inputs/buttons |

Status badges keep solid (non-glass) fills for legibility against blurred backgrounds:
- **At Risk** → `bg-red-500/20 text-red-300 border border-red-500/30`
- **Saved** → `bg-green-500/20 text-green-300 border border-green-500/30`

---

## 4. Global Layout Structure

```
App
 ├── Public Layout (own layout, no Dock)
 │     ├── Landing Page (/)          — custom scroll-video background
 │     ├── Sign Up Page (/signup)    — GradientWaves background
 │     └── Login Page (/login)       — GradientWaves background
 │
 └── Authenticated Layout (GradientWaves background + Dock navigation)
       ├── Dashboard (/dashboard)
       ├── Predict (/predict)
       ├── Customers (/customers)
       └── Settings (/settings)
```

- **Authenticated Layout** mounts `GradientWaves` once and renders the `Dock` navbar fixed at the bottom of the viewport, giving equal access to all 4 pages regardless of entry point (Sign Up → Predict, Login → Dashboard).
- Route protection: unauthenticated users attempting to access `/dashboard`, `/predict`, `/customers`, `/settings` are redirected to `/login`.

---

## 5. Navigation — Dock Component

Retentio's primary navigation is the **Dock** component (React Bits), replacing a traditional top navbar/sidebar. It sits fixed at the bottom-center of the viewport on all authenticated pages.

```jsx
import Dock from '@/components/Dock';
import { VscDashboard, VscGraph, VscAccount, VscSettingsGear } from 'react-icons/vsc';
import { useNavigate } from 'react-router-dom';

function AppDock() {
  const navigate = useNavigate();

  const items = [
    { icon: <VscDashboard size={18} />, label: 'Dashboard', onClick: () => navigate('/dashboard') },
    { icon: <VscGraph size={18} />, label: 'Predict', onClick: () => navigate('/predict') },
    { icon: <VscAccount size={18} />, label: 'Customers', onClick: () => navigate('/customers') },
    { icon: <VscSettingsGear size={18} />, label: 'Settings', onClick: () => navigate('/settings') },
  ];

  return <Dock items={items} panelHeight={68} baseItemSize={50} magnification={70} />;
}
```

**Notes:**
- The Dock's own CSS already gives it a dark glass-adjacent look (`#120F17` panel, subtle border) — this pairs well with the GradientWaves background without extra styling.
- Active-route highlighting: extend `DockItem`'s `className` prop conditionally (e.g., `isActive ? 'dock-item-active' : ''`) using `useLocation()` from React Router, with a small CSS addition (outline or brighter background) for the current page — not in the base component, add as a thin wrapper.
- A **Logout** action and **user avatar/menu** are not part of the Dock's 4 core items — place a small floating `GlassCard` menu in the top-right corner instead (separate from the Dock) for logout/profile-quick-view, since the Dock is capped at a focused set of primary nav items.
- On mobile (`< md`), the Dock's built-in magnification/hover behavior is less meaningful (no cursor) — fall back to fixed equal-sized items (pass `magnification={baseItemSize}` on small screens, or conditionally render a simpler bottom bar).

---

## 6. Landing Page — Detailed Spec

### 6.1 Background
Custom 300-frame canvas scroll-scrubbing sequence (per the earlier scroll-animation build plan: preload frames → draw to canvas → GSAP `ScrollTrigger` with `scrub` + `pin` maps scroll position to frame index). This is the **only** page using this background — everywhere else uses `GradientWaves`.

### 6.2 Text Sequence — ScrollFloat + GradientText

The two headline moments use `ScrollFloat` for the character-by-character scroll-driven reveal, with `GradientText` used for a colored accent word/phrase within them for visual punch.

```jsx
import ScrollFloat from '@/components/ScrollFloat';
import GradientText from '@/components/GradientText';

// Beat 1
<ScrollFloat
  animationDuration={1}
  ease="back.inOut(2)"
  scrollStart="center bottom+=50%"
  scrollEnd="bottom bottom-=40%"
  stagger={0.03}
>
  Losing Customers?
</ScrollFloat>

// Beat 2
<ScrollFloat
  animationDuration={1}
  ease="back.inOut(2)"
  scrollStart="center bottom+=50%"
  scrollEnd="bottom bottom-=40%"
  stagger={0.03}
>
  Predict Customer Churn Before It Happens
</ScrollFloat>
```

Since `ScrollFloat` splits its `children` into characters itself (it expects a plain string), the `GradientText` accent is layered as a **separate inline element placed adjacent to or beneath** the ScrollFloat heading rather than nested inside it — e.g., the word "Retentio" rendered via `GradientText` directly beneath the second ScrollFloat line as a highlighted sub-label:

```jsx
<div className="text-center">
  <ScrollFloat animationDuration={1} ease="back.inOut(2)" stagger={0.03}>
    Predict Customer Churn Before It Happens
  </ScrollFloat>
  <GradientText
    colors={["#40ffaa", "#4079ff", "#40ffaa", "#4079ff", "#40ffaa"]}
    animationSpeed={3}
    showBorder={false}
    className="mt-2 text-lg"
  >
    Retentio
  </GradientText>
</div>
```

Both `ScrollFloat` blocks are tied to the same scroll container as the frame-sequence canvas (`scrollContainerRef` pointed at the pinned section) so text beats and frame scrubbing progress together.

### 6.3 CTA — SpecularButton

After the second text beat ("Predict Customer Churn Before It Happens"), the **Get Started** button appears using `SpecularButton`:

```jsx
import SpecularButton from '@/components/SpecularButton';

<SpecularButton
  size="lg"
  radius={18}
  tint="#ffffff"
  tintOpacity={0}
  blur={0}
  textColor="#f5f5f5"
  lineColor="#ffffff"
  baseColor="#525252"
  intensity={1}
  shineSize={10}
  shineFade={40}
  thickness={1}
  speed={0.35}
  followMouse
  proximity={250}
  autoAnimate={false}
  onClick={handleGetStarted}
>
  Get Started
</SpecularButton>
```

**On click (`handleGetStarted`):** triggers the existing "zoom out → reveal Sign Up / Login card" behavior. The Sign Up/Login card itself should adopt the `GlassCard` style (Section 3.3) even though it's on the Landing Page's custom background, for visual consistency with the rest of the app.

### 6.4 Landing Page Flow Summary
1. Frame-sequence background scrubs via scroll (GSAP ScrollTrigger, pinned section).
2. `ScrollFloat` — "Losing Customers?" reveals character-by-character, scroll-tied.
3. `ScrollFloat` — "Predict Customer Churn Before It Happens" reveals; `GradientText` "Retentio" accent beneath it.
4. `SpecularButton` "Get Started" appears/zooms in.
5. On click → `GlassCard`-styled Sign Up/Login options appear in place.

---

## 7. Page-by-Page Specification

### 7.1 Landing Page (`/`)
Covered fully in Section 6.

---

### 7.2 Sign Up Page (`/signup`)

**Background:** `GradientWaves` (shared instance from Public Layout).

**Elements (all wrapped in `GlassCard`):**
- Short intro blurb about Retentio (what it does, why it matters).
- Form fields: Business Name, Full Name, Email, Password, Confirm Password.
- Submit button — recommendation: use shadcn `Button` (glass-themed) for form submits, reserving `SpecularButton` for the one hero CTA on Landing so it keeps feeling special rather than repeated everywhere.
- Inline validation messages (email format, password match, required fields).

**On Success:** Store JWT in `AuthContext` → redirect to `/predict`.

**API:** `POST /api/v1/auth/signup`

---

### 7.3 Login Page (`/login`)

**Background:** `GradientWaves` (shared instance).

**Elements (wrapped in `GlassCard`):**
- Entrance animation consistent with Landing Page style (fade/slide in via Framer Motion).
- Form fields: Email, Password.
- Submit button (shadcn `Button`, glass-themed, loading state while request is in-flight).
- **Side panel** (separate `GlassCard`): `RotatingFactPanel` — rotating "Did you know?" business/churn facts, auto-changing every 7 seconds.

**On Success:** Store JWT in `AuthContext` → redirect to `/dashboard`.

**API:** `POST /api/v1/auth/login`

**Component:** `RotatingFactPanel` — accepts an array of fact strings, cycles index every 7s via `setInterval` or Framer Motion `AnimatePresence` with a timed key change.

---

### 7.4 Dashboard Page (`/dashboard`)

**Background:** `GradientWaves` (from Authenticated Layout, shared).

**Elements (each in its own `GlassCard`):**
- **Summary Cards row:** Total Customers, At Risk Count, Saved Count, Average Risk Score.
- **Charts (Recharts, inside `GlassCard`):**
  - Bar or pie chart — risk distribution.
  - Trend line — average risk score over time.
- **Expandable section:** placeholder `GlassCard` for future widgets (recent activity, top risk factors).

**API:** `GET /api/v1/dashboard/summary`, `GET /api/v1/dashboard/trend`

**Loading state:** Skeleton loaders (shadcn `Skeleton`, styled semi-transparent to match glass theme) while data fetches.

---

### 7.5 Predict Page (`/predict`)

**Background:** `GradientWaves` (shared).

**Flow & Elements (upload section + results, each in `GlassCard`):**
1. **Upload section** (`GlassCard` containing `UploadCard`):
   - Drag-and-drop zone + file picker.
   - Accepts `.csv` only; client-side validation.
2. **On successful upload:** Toast/popup: "File uploaded successfully."
3. **Calculate button** (shadcn `Button`, or optionally `SpecularButton` since this is the app's key action — use sparingly per Section 12) appears, enabled only after successful upload.
4. **On Calculate click:** Loading state (spinner) while backend processes. `POST /api/v1/predict/upload`.
5. **Results render below upload section, in their own `GlassCard`s:**
   - **At Risk table** (`RiskTable`, red status badges).
   - **Saved table** (`RiskTable`, green status badges); shows *"No customers saved yet."* when `saved` array is empty.

**State:** `uploadedFile`, `uploadStatus`, `results` (at_risk, saved, saved_message), `isCalculating`.

**API:** `POST /api/v1/predict/upload`, `GET /api/v1/predict/template`.

---

### 7.6 Customers Page (`/customers`)

**Background:** `GradientWaves` (shared).

**Elements (`GlassCard` wrapping search + detail panel):**
- Search bar (`Input` + `Search` icon from lucide-react) — search by Customer Name or ID, debounced (~300ms).
- Results list/dropdown (glass-styled) as user types.
- On selecting a customer → detail panel (`GlassCard`) shows:
  - Score history line chart (Recharts).
  - Current status badge.
  - Status change timeline.

**API:** `GET /api/v1/customers/search?q=`, `GET /api/v1/customers/{id}`

**State:** `searchQuery`, `searchResults`, `selectedCustomer`.

---

### 7.7 Settings Page (`/settings`)

**Background:** `GradientWaves` (shared).

**Elements (`GlassCard`):**
- Editable fields: User Name, Business Name.
- Benchmark slider (shadcn `Slider`, range 70–90, default 78) with live numeric display.
- "Save Changes" button → confirmation toast on success.

**API:** `PATCH /api/v1/settings/profile`, `PATCH /api/v1/settings/benchmark`

**State:** Form state via `useState`/`react-hook-form`; dirty-check to enable/disable Save button.

---

## 8. Shared/Reusable Components

| Component | Source | Used In | Description |
|---|---|---|---|
| `Dock` | React Bits | All authenticated pages | Bottom-fixed navigation: Dashboard, Predict, Customers, Settings |
| `GradientWaves` | React Bits | All pages except Landing | Shared animated WebGL background |
| `SpecularButton` | React Bits | Landing (CTA), optionally Predict's Calculate button | Glowing specular-highlight button |
| `ScrollFloat` | React Bits | Landing | Scroll-driven character reveal for headline text |
| `GradientText` | React Bits | Landing (accent), optionally page headings | Animated gradient-colored text accent |
| `GlassCard` | Custom wrapper | Everywhere post-landing | Standardized glassmorphism container |
| `AuthCard` | Custom, uses `GlassCard` | Landing | Sign Up / Login option card |
| `RotatingFactPanel` | Custom, uses `GlassCard` | Login | Cycles business facts every 7s |
| `UploadCard` | Custom, uses `GlassCard` | Predict | Drag-and-drop CSV upload |
| `RiskTable` | Custom, uses `GlassCard` | Predict, Dashboard | Reusable table with status badges, sortable columns |
| `SummaryCard` | Custom, uses `GlassCard` | Dashboard | Stat display card (icon + number + label) |
| `ScoreChart` | Custom | Dashboard, Customers | Recharts wrapper for line/bar/pie charts |
| `Toast` | shadcn/Sonner | Global | Success/error notifications |
| `StatusBadge` | Custom | RiskTable, Customer Detail | Red/Green badge, solid fill (not glass) for legibility |
| `LoadingSpinner`/`Skeleton` | shadcn | Global | Loading states, semi-transparent to match glass theme |

---

## 9. State Management

- **AuthContext (React Context API):**
  - Holds: `user`, `token`, `isAuthenticated`, `login()`, `signup()`, `logout()`.
  - JWT kept in memory (React state), not `localStorage`, to reduce XSS token theft risk (finalized in Security & Access Doc).
- **Per-page local state:** Forms, upload state, search queries — handled via `useState`/`useReducer` within each page.

---

## 10. API Integration Layer

Centralized Axios instance (`services/api.js`):
```js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
  const token = getTokenFromContext();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```
All page-level API calls go through this instance. A response interceptor catches 401 → triggers logout + redirect to `/login`.

---

## 11. Routing Table

| Path | Page | Access | Background |
|---|---|---|---|
| `/` | Landing | Public | Scroll-video frame sequence |
| `/signup` | Sign Up | Public | GradientWaves |
| `/login` | Login | Public | GradientWaves |
| `/dashboard` | Dashboard | Protected | GradientWaves |
| `/predict` | Predict | Protected | GradientWaves |
| `/customers` | Customers | Protected | GradientWaves |
| `/settings` | Settings | Protected | GradientWaves |

Protected routes wrapped in `<ProtectedRoute>`, checking `isAuthenticated` from `AuthContext`.

---

## 12. Performance Considerations (WebGL-Specific)

Since this build now uses **three WebGL-driven components** (`GradientWaves`, `SpecularButton`, plus the custom canvas frame-sequence on Landing), performance discipline matters more than a typical CRUD frontend:

- **Never mount more than one `GradientWaves` instance at a time** — one shared instance per layout (Public Layout, Authenticated Layout), not one per page.
- `GradientWaves` already pauses its render loop when off-screen (`IntersectionObserver`) or when the tab is hidden (`visibilitychange`) — don't fight this by wrapping it in logic that force-remounts it on every route change.
- Limit `SpecularButton` usage to 1–2 buttons per page max (each spins up its own tiny `ogl` renderer) — it's a hero-moment component, not a default button replacement.
- On lower-end devices/mobile, consider passing `detail="low"` to `GradientWaves` via a `matchMedia`/viewport-width check.
- The Landing Page's 300-frame canvas sequence and `GradientWaves` should never run simultaneously — Landing uses only the frame sequence; the moment the user navigates to Sign Up/Login/etc., the frame-sequence canvas unmounts entirely.

---

## 13. Responsive Behavior

- Mobile-first Tailwind breakpoints (`sm`, `md`, `lg`).
- **Dock:** on screens `< md`, reduce/disable magnification (see Section 5) since hover-based magnification doesn't translate to touch.
- Glass cards stack vertically on mobile; `backdrop-filter: blur()` remains but blur radius can be reduced slightly on low-power devices for performance.
- Tables (`RiskTable`) scroll horizontally on small screens rather than breaking layout.
- Charts resize responsively via Recharts' `ResponsiveContainer`.
- `ScrollFloat` font sizing already uses `clamp()` in its default CSS — confirm it reads well at narrow viewports without further overrides needed.

---

## 14. Animation Guidelines

- **Landing page:** GSAP `ScrollTrigger` (frame scrubbing) + `ScrollFloat`'s own GSAP-driven character reveal — both scroll-tied, no manual timers.
- **SpecularButton / Dock:** self-contained animation (pointer-driven), no extra wrapping needed.
- **Page transitions:** subtle Framer Motion fade between routes (optional polish).
- **Toasts:** slide-in/fade per shadcn/Sonner defaults.
- Keep non-hero animation durations short (200–400ms); reserve the longer, more elaborate timing (600–900ms+) for Landing Page storytelling moments only.

---

## 15. Out of Scope (v1)

- Light mode (the entire glassmorphism system is designed dark-first; a light variant would need a separate token set).
- Internationalization (i18n).
- Offline support / PWA capabilities.
- Advanced accessibility audit beyond basic semantic HTML + ARIA labels (note: glass-on-glass contrast should be spot-checked for WCAG AA on text-heavy areas like tables).

---

## 16. Related Documents
- Product Requirements Document (PRD) v1.0
- Technical Architecture Document v1.0
- Security & Access Document v1.0
- Feature Ticket List v1.0
