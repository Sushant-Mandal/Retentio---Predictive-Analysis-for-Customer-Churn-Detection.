# Frontend Specification Document
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 3.0
**Status:** Draft
**Date:** August 28, 2026
**Related Docs:** Retentio PRD v1.0, Technical Architecture Document v1.0
**Changelog:**
- v2.0 — Integrated React Bits components (Dock, GradientWaves, SpecularButton, ScrollFloat, GradientText) and defined glassmorphism visual system.
- v3.0 — Landing Page redesigned around an animated "reaching hands" visual with cursor-reactive glow (replaces GradientWaves on this page only); scroll sequence expanded to 3 text beats; Get Started button repositioned between the hands. Sign Up/Login background changed from GradientWaves to a looping ambient background video (the source video originally planned for Landing's frame-sequence). Dashboard/Predict/Customers/Settings are unchanged from v2.0.

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
| WebGL Effects | ogl (via GradientWaves, SpecularButton, and the Landing hands visual) |
| Routing | React Router |
| State Management | React Context API (Auth) + local component state |

### 2.1 Dependencies (React Bits + supporting)
| Package | Used By |
|---|---|
| `motion` | Dock |
| `ogl` | GradientWaves, SpecularButton, `AnimatedHandsBackground` (Landing) |
| `gsap` | ScrollFloat, Landing scroll sequencing |

Install once:
```bash
npm i motion ogl gsap
```

---

## 3. Visual System

### 3.1 Design Language
Retentio's UI is built on a **dark glassmorphism system** everywhere except the Landing Page, which has its own distinct visual identity (the reaching-hands / glowing-space concept). Post-landing, a single animated `GradientWaves` background sits behind Dashboard/Predict/Customers/Settings, and all content floats above it as translucent, blurred "glass" surfaces. Sign Up and Login sit in between: they use a looping ambient background video rather than GradientWaves or the hands visual.

### 3.2 Global Background Rule

| Page | Background |
|---|---|
| Landing (`/`) | `AnimatedHandsBackground` — dark space, glowing wireframe reaching-hands visual, cursor-reactive glow |
| Sign Up, Login | Looping ambient background video (`BackgroundVideo` component) |
| Dashboard, Predict, Customers, Settings | `GradientWaves` (single shared instance, mounted once in the Authenticated Layout) |

**`GradientWaves` config is unchanged from v2.0** (see Section 3.2.1 of the prior spec / Technical Architecture Doc) and continues to apply only to the four authenticated pages.

### 3.3 Glassmorphism Card Style

Unchanged from v2.0 — applies to Sign Up, Login, Dashboard, Predict, Customers, Settings. **Does not apply to the Landing Page**, which uses its own distinct card treatment for the Sign Up/Login option reveal (see Section 6.5).

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}
```

```jsx
// components/GlassCard.jsx
export default function GlassCard({ children, className = '' }) {
  return <div className={`glass-panel p-6 ${className}`}>{children}</div>;
}
```

### 3.4 Design Tokens

| Token | Value |
|---|---|
| Page background (app-wide base) | Black/near-black base (`#0a0a0f`) |
| Glass fill | `rgba(255,255,255,0.06)` |
| Glass border | `rgba(255,255,255,0.12)` |
| Primary text (app) | `#f5f5f5` |
| Muted text | `#a1a1aa` (`zinc-400`) |
| Danger/At Risk | Red (`red-400`/`red-500`) |
| Success/Saved | Green (`green-400`/`green-500`) |
| Accent gradient (headings, highlights) | `GradientText` colors: `#40ffaa → #4079ff → #40ffaa → #4079ff → #40ffaa` |
| **Landing headline text** | Black fill (`#000000`), glowing white outline, black drop shadow (see Section 6.4) |
| Font | Inter or similar sans-serif |
| Border radius | `rounded-2xl` (16px) for cards, `rounded-lg` for inputs/buttons |

Status badges keep solid (non-glass) fills for legibility:
- **At Risk** → `bg-red-500/20 text-red-300 border border-red-500/30`
- **Saved** → `bg-green-500/20 text-green-300 border border-green-500/30`

---

## 4. Global Layout Structure

```
App
 ├── Landing Layout (own layout, unique to /)
 │     └── Landing Page (/)              — AnimatedHandsBackground + cursor glow
 │
 ├── Public Layout (Sign Up / Login only)
 │     ├── Sign Up Page (/signup)        — BackgroundVideo
 │     └── Login Page (/login)           — BackgroundVideo
 │
 └── Authenticated Layout (GradientWaves + Dock navigation)
       ├── Dashboard (/dashboard)
       ├── Predict (/predict)
       ├── Customers (/customers)
       └── Settings (/settings)
```

- **Landing Layout** is now its own top-level layout (not grouped with Sign Up/Login) since its background system, cursor-glow behavior, and card styling are all unique to that one page.
- **Public Layout** wraps Sign Up and Login, mounting `BackgroundVideo` once so it isn't restarted when navigating between the two.
- **Authenticated Layout** is unchanged from v2.0.
- Route protection: unauthenticated users attempting to access `/dashboard`, `/predict`, `/customers`, `/settings` are redirected to `/login`.

---

## 5. Navigation — Dock Component

Unchanged from v2.0. See Technical Architecture Doc / prior spec for the full `Dock` implementation — it continues to render on all four authenticated pages only (Dashboard, Predict, Customers, Settings). Landing, Sign Up, and Login have no persistent nav (Landing has no nav at all; Sign Up/Login only link to each other).

---

## 6. Landing Page — Detailed Spec (Redesigned in v3.0)

### 6.1 Concept

The Landing Page reference art depicts two hands reaching toward each other (Michelangelo "Creation of Adam" pose) rendered in a glowing, wireframe/mesh style against a dark space background — not a photographic or static image. As the user scrolls, three text beats appear in sequence, and once the third beat completes, a **Get Started** button materializes in the gap between the hands' near-touching fingers, visually completing the "handing you the button" composition.

### 6.2 Background — `AnimatedHandsBackground`

**Requirements from the reference material:**
- Dark, space-like backdrop (near-black, subtle depth/stars optional).
- The two reaching hands rendered as a **glowing wireframe/mesh** treatment (the wireframe-hand reference image is a style guide for this look — a lit, faceted mesh surface rather than flat line art).
- Must be a true **animation**, not a static image and not a "dynamic image" (e.g., not a GIF/video loop of a fixed clip) — the brief calls for a genuinely animated, presumably code-driven visual (subtle idle motion: slow rotation, breathing/pulsing glow, faint particle drift).
- **Cursor-reactive glow:** a soft light source follows the cursor across the whole page, illuminating the mesh/space near the pointer.
- **5-second idle rule:** if the cursor stops moving for 5+ seconds, the glow-follow behavior stops updating (freezes in place) until the cursor moves again.

**Recommended technical approach:**
Given the existing `ogl` dependency (already used for `GradientWaves` and `SpecularButton`), build `AnimatedHandsBackground` as a custom `ogl`-based WebGL scene:
- Two hand meshes (or a pre-baked wireframe/point-cloud representation of the reference art) rendered with an emissive/fresnel-style shader so edges glow.
- A point-light/uniform (`uMouse`) drives a glow falloff shader term, following cursor position — reuse the same mouse-lerp pattern already implemented in `GradientWaves` (`currentMouse`/`targetMouse` lerp toward pointer position each frame).
- Idle-freeze behavior: track `lastMouseMoveTime`; if `now - lastMouseMoveTime > 5000ms`, stop updating `targetMouse` (glow stays at its last position) — resume updating on the next `pointermove` event.

**Scope/timeline note:** building an original 3D hand mesh from scratch is a significant asset-creation task on top of the shader work. If full 3D modeling isn't feasible in the project timeline, a **fallback approach** is to commission or trace an SVG line-art version of the two hands, animate the stroke draw-in with Framer Motion/GSAP, and apply an SVG `feGaussianBlur` + `feColorMatrix` glow filter, with the cursor-glow implemented as a separate radial-gradient overlay (Section 6.3) rather than baked into a 3D shader. This trades some visual fidelity to the wireframe reference for a much smaller build effort — flag this trade-off with the person who provided the reference art before committing to one path.

```jsx
// components/AnimatedHandsBackground.jsx — conceptual shape, ogl-based
// Mirrors GradientWaves' lifecycle (Renderer, Program, Mesh, mouse lerp,
// IntersectionObserver + visibilitychange pause/resume) but with:
//  - hand geometry/mesh instead of a plasma raymarch
//  - an idle-timeout on the mouse-follow glow uniform
```

### 6.3 Cursor Glow Layer

Whether implemented inside the WebGL shader or as a separate overlay, the glow behavior is a shared concern worth isolating into its own hook for reuse/testing:

```jsx
// hooks/useCursorGlow.js
function useCursorGlow({ idleTimeoutMs = 5000 } = {}) {
  const position = useRef({ x: 0.5, y: 0.5 });
  const lastMoveRef = useRef(Date.now());

  useEffect(() => {
    const onMove = (e) => {
      lastMoveRef.current = Date.now();
      position.current = { x: e.clientX / window.innerWidth, y: e.clientY / window.innerHeight };
    };
    window.addEventListener('pointermove', onMove);
    return () => window.removeEventListener('pointermove', onMove);
  }, []);

  const isIdle = () => Date.now() - lastMoveRef.current > idleTimeoutMs;

  return { position, isIdle };
}
```

Consumed by `AnimatedHandsBackground` (feeding the shader's mouse uniform, skipping updates while `isIdle()` is true).

### 6.4 Text Sequence — Three Beats

The scroll sequence now has **three** beats (expanded from the two-beat version in v2.0), each built with `ScrollFloat` for scroll-driven character reveal:

```jsx
import ScrollFloat from '@/components/ScrollFloat';

// Beat 1
<ScrollFloat animationDuration={1} ease="back.inOut(2)" stagger={0.03}>
  Welcome to Retentio
</ScrollFloat>

// Beat 2
<ScrollFloat animationDuration={1} ease="back.inOut(2)" stagger={0.03}>
  Losing Customers?
</ScrollFloat>
{/* Small accompanying animation: customer icons/dots drifting apart —
    a lightweight Framer Motion loop, positioned near Beat 2's text */}
<CustomerLossAnimation />

// Beat 3
<ScrollFloat animationDuration={1} ease="back.inOut(2)" stagger={0.03}>
  Start Your Customer Retention Today
</ScrollFloat>
```

All three beats share the same `scrollContainerRef` as the pinned hands-background section, so text and background progress together as the user scrolls.

**`CustomerLossAnimation`** — a small supporting visual next to "Losing Customers?" depicting customers scattering/drifting away (a handful of dot/icon elements animating outward with fading opacity via Framer Motion), matching the sketch's note: *"a design of customer losing (an animation)."*

### 6.5 Text Styling — `GlowText`

Per the brief, all Landing Page headline text uses a distinct style so it reads clearly over the dark, glowing hands background:

```css
.glow-text {
  color: #000000;
  text-shadow:
    0 0 4px #ffffff,
    0 0 8px #ffffff,
    0 0 16px #ffffff,
    2px 2px 6px rgba(0, 0, 0, 0.8); /* black drop shadow */
}
```

```jsx
// components/GlowText.jsx
export default function GlowText({ children, className = '' }) {
  return <span className={`glow-text ${className}`}>{children}</span>;
}
```

Wrap each `ScrollFloat` heading's text in `GlowText` styling (either by passing `textClassName="glow-text"` into `ScrollFloat`, or wrapping the rendered characters — confirm `ScrollFloat`'s `textClassName` prop applies to the outer `<span>` wrapping all characters, which it does per its component source, so this is a direct prop pass-through).

### 6.6 CTA — SpecularButton, Positioned Between the Hands

After Beat 3 completes, the **Get Started** button appears, absolutely positioned to sit in the gap between the two hands' nearest fingers (per the reference image, roughly the upper-middle area where the reaching fingers almost touch):

```jsx
import SpecularButton from '@/components/SpecularButton';

<div className="hands-cta-anchor"> {/* positioned via CSS to align with the fingertip gap in AnimatedHandsBackground's coordinate space */}
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
</div>
```

**Positioning note:** since the hands are rendered in a WebGL canvas (not a static image with fixed pixel coordinates), the button's anchor position needs to be expressed as a percentage/viewport-relative offset tuned to match wherever the fingertip gap lands in the final rendered scene — this will need visual tuning once `AnimatedHandsBackground` is built, rather than a single hardcoded pixel value up front.

**On click (`handleGetStarted`):** zooms out and reveals the Sign Up / Login option card (Section 6.7).

### 6.7 Sign Up / Login Option Card

Unlike the rest of the app, this card sits on the Landing Page's unique background, not a `GlassCard`-over-`GradientWaves` context. Use a variant with slightly stronger opacity/blur so it reads clearly against the busier hands visual:

```css
.landing-auth-card {
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 1.25rem;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}
```

### 6.8 Landing Page Flow Summary
1. `AnimatedHandsBackground` renders — dark space, glowing wireframe hands, cursor-reactive glow (freezes after 5s idle).
2. `ScrollFloat` Beat 1 — "Welcome to Retentio" (glow-text styled), scroll-tied reveal.
3. `ScrollFloat` Beat 2 — "Losing Customers?" + `CustomerLossAnimation` (customers scattering).
4. `ScrollFloat` Beat 3 — "Start Your Customer Retention Today."
5. `SpecularButton` "Get Started" appears, positioned in the gap between the hands' fingers.
6. On click → `.landing-auth-card`-styled Sign Up/Login options appear.
7. Choosing Sign Up → `/signup`; choosing Login → `/login` (both leave the hands background behind and enter `BackgroundVideo`-backed pages).

---

## 7. Sign Up / Login — Background Video

### 7.1 Source

The video that was originally planned for the Landing Page (previously broken into ~300 frames for scroll-scrubbing) is **repurposed** here as a simple looping ambient background — no scroll-scrubbing, no GSAP `ScrollTrigger` frame math. This substantially simplifies its implementation versus the original Landing Page plan.

### 7.2 `BackgroundVideo` Component

```jsx
// components/BackgroundVideo.jsx
export default function BackgroundVideo({ src, className = '' }) {
  return (
    <video
      className={`background-video ${className}`}
      src={src}
      autoPlay
      muted
      loop
      playsInline
      preload="auto"
    />
  );
}
```

```css
.background-video {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}
```

**Notes:**
- `muted` is required for `autoPlay` to work reliably across browsers.
- Mount once in the Public Layout wrapping both Sign Up and Login so the video doesn't restart when the user toggles between the two pages.
- Encode as compressed `.mp4` (H.264) with a reasonable bitrate/resolution target — this is a background element, not the focal point, so it doesn't need source-quality resolution. A `.webm` fallback is a reasonable enhancement if browser support becomes a concern.
- Provide a static `poster` frame (first frame of the video) so there's no flash-of-empty-background before the video loads.

---

## 8. Page-by-Page Specification

### 8.1 Landing Page (`/`)
Covered fully in Section 6.

---

### 8.2 Sign Up Page (`/signup`)

**Background:** `BackgroundVideo` (shared instance from Public Layout).

**Elements (all wrapped in `GlassCard`):**
- Short intro blurb about Retentio (what it does, why it matters).
- Form fields: Business Name, Full Name, Email, Password, Confirm Password.
- Submit button — shadcn `Button` (glass-themed).
- Inline validation messages (email format, password match, required fields).

**On Success:** Store JWT in `AuthContext` → redirect to `/predict`.

**API:** `POST /api/v1/auth/signup`

---

### 8.3 Login Page (`/login`)

**Background:** `BackgroundVideo` (shared instance).

**Elements (wrapped in `GlassCard`):**
- Entrance animation (fade/slide in via Framer Motion).
- Form fields: Email, Password.
- Submit button (shadcn `Button`, glass-themed, loading state while request is in-flight).
- **Side panel** (separate `GlassCard`): `RotatingFactPanel` — rotating "Did you know?" business/churn facts, auto-changing every 7 seconds.

**On Success:** Store JWT in `AuthContext` → redirect to `/dashboard`.

**API:** `POST /api/v1/auth/login`

---

### 8.4 Dashboard Page (`/dashboard`)
Unchanged from v2.0. Background: `GradientWaves`. Summary Cards, Recharts risk distribution + trend charts, all in `GlassCard`s.

**API:** `GET /api/v1/dashboard/summary`, `GET /api/v1/dashboard/trend`

---

### 8.5 Predict Page (`/predict`)
Unchanged from v2.0. Background: `GradientWaves`. Upload → Calculate → At Risk / Saved tables, all in `GlassCard`s.

**API:** `POST /api/v1/predict/upload`, `GET /api/v1/predict/template`

---

### 8.6 Customers Page (`/customers`)
Unchanged from v2.0. Background: `GradientWaves`. Search + Customer Detail panel in `GlassCard`s.

**API:** `GET /api/v1/customers/search?q=`, `GET /api/v1/customers/{id}`

---

### 8.7 Settings Page (`/settings`)
Unchanged from v2.0. Background: `GradientWaves`. Profile + benchmark form in `GlassCard`.

**API:** `PATCH /api/v1/settings/profile`, `PATCH /api/v1/settings/benchmark`

---

## 9. Shared/Reusable Components

| Component | Source | Used In | Description |
|---|---|---|---|
| `AnimatedHandsBackground` | Custom (ogl) | Landing only | Glowing wireframe reaching-hands scene, cursor-reactive glow with 5s idle freeze |
| `useCursorGlow` | Custom hook | Landing only | Tracks pointer position + idle state, feeds the hands shader |
| `CustomerLossAnimation` | Custom (Framer Motion) | Landing, Beat 2 | Small "customers scattering" supporting animation |
| `GlowText` | Custom | Landing headings | Black fill, white glow outline, black drop shadow |
| `BackgroundVideo` | Custom | Sign Up, Login | Looping ambient background video |
| `Dock` | React Bits | All authenticated pages | Bottom-fixed navigation |
| `GradientWaves` | React Bits | Dashboard, Predict, Customers, Settings | Shared animated WebGL background |
| `SpecularButton` | React Bits | Landing (CTA, positioned between hands) | Glowing specular-highlight button |
| `ScrollFloat` | React Bits | Landing (3 beats) | Scroll-driven character reveal |
| `GradientText` | React Bits | Optional accent use | Animated gradient-colored text |
| `GlassCard` | Custom wrapper | Sign Up, Login, Dashboard, Predict, Customers, Settings | Standardized glassmorphism container |
| `RotatingFactPanel` | Custom, uses `GlassCard` | Login | Cycles business facts every 7s |
| `UploadCard` | Custom, uses `GlassCard` | Predict | Drag-and-drop CSV upload |
| `RiskTable` | Custom, uses `GlassCard` | Predict, Dashboard | Table with status badges |
| `SummaryCard` | Custom, uses `GlassCard` | Dashboard | Stat display card |
| `ScoreChart` | Custom | Dashboard, Customers | Recharts wrapper |
| `Toast` | shadcn/Sonner | Global | Success/error notifications |
| `StatusBadge` | Custom | RiskTable, Customer Detail | Red/Green badge |
| `LoadingSpinner`/`Skeleton` | shadcn | Global | Loading states |

---

## 10. State Management

Unchanged from v2.0.
- **AuthContext:** `user`, `token`, `isAuthenticated`, `login()`, `signup()`, `logout()`. JWT kept in memory, not `localStorage`.
- **Per-page local state:** forms, upload state, search queries.
- **Landing-specific local state:** scroll progress (via GSAP `ScrollTrigger`/`useScroll`), cursor position + idle flag (`useCursorGlow`).

---

## 11. API Integration Layer

Unchanged from v2.0 — centralized Axios instance in `services/api.js` with JWT interceptor and 401 → logout handling.

---

## 12. Routing Table

| Path | Page | Access | Background |
|---|---|---|---|
| `/` | Landing | Public | `AnimatedHandsBackground` |
| `/signup` | Sign Up | Public | `BackgroundVideo` |
| `/login` | Login | Public | `BackgroundVideo` |
| `/dashboard` | Dashboard | Protected | GradientWaves |
| `/predict` | Predict | Protected | GradientWaves |
| `/customers` | Customers | Protected | GradientWaves |
| `/settings` | Settings | Protected | GradientWaves |

---

## 13. Performance Considerations

Retentio now runs **four** distinct animated-background systems across its pages (down from what would otherwise be a fifth, since the video approach is lighter than scroll-scrubbed canvas frames):

- `AnimatedHandsBackground` (Landing) — custom `ogl` WebGL scene; heaviest asset in the app if built as a full mesh/shader. Apply the same off-screen/hidden-tab pause pattern already used in `GradientWaves` (`IntersectionObserver` + `visibilitychange`) even though Landing is a single page — pausing when the tab isn't visible still matters (background tab, screen lock).
- `BackgroundVideo` (Sign Up/Login) — standard `<video>` element, much cheaper than canvas/WebGL. Compress well (target a reasonable file size for a looping background clip) and keep resolution modest since it's blurred/dimmed under a `GlassCard` overlay anyway.
- `GradientWaves` (Dashboard/Predict/Customers/Settings) — unchanged, one shared instance per layout.
- `SpecularButton` — unchanged guidance: 1–2 instances per page max.
- **Never run more than one WebGL-heavy background at a time** — since Landing, Public, and Authenticated are now three separate layouts that fully unmount each other's backgrounds on navigation, this should hold naturally as long as each layout only mounts its own background component.

---

## 14. Responsive Behavior

- Mobile-first Tailwind breakpoints (`sm`, `md`, `lg`).
- **`AnimatedHandsBackground`:** cursor-glow behavior has no equivalent on touch devices — on mobile, either substitute a fixed/ambient glow (no pointer-follow) or a subtle idle pulse animation instead of trying to simulate cursor movement from touch events.
- **`BackgroundVideo`:** `object-fit: cover` handles most aspect-ratio concerns; verify the source video's focal point remains reasonable when cropped to portrait mobile viewports.
- **Dock:** on screens `< md`, reduce/disable magnification (unchanged from v2.0).
- Glass cards, tables, and charts: unchanged responsive behavior from v2.0.

---

## 15. Animation Guidelines

- **Landing page:** GSAP `ScrollTrigger` drives the pinned scroll section; `ScrollFloat` handles each text beat's character reveal; `AnimatedHandsBackground`'s idle motion (rotation/pulse/particle drift) runs independently via `requestAnimationFrame`, decoupled from scroll position.
- **Cursor glow idle-freeze:** implemented via the `useCursorGlow` timeout check (Section 6.3) — not a CSS transition, since it needs to fully stop updating rather than just animate slowly.
- **SpecularButton / Dock:** self-contained, pointer-driven, no extra wrapping needed.
- **BackgroundVideo:** no JS-driven animation — native video loop only.
- **Page transitions:** subtle Framer Motion fade between routes (optional polish).
- Keep non-hero animation durations short (200–400ms); reserve longer timing (600–900ms+) for Landing Page storytelling moments.

---

## 16. Out of Scope (v1)

- Light mode.
- Internationalization (i18n).
- Offline support / PWA capabilities.
- Full accessibility audit (note: `GlowText`'s black-fill-on-dark-background approach relies entirely on the glow/shadow for contrast — this should get a manual legibility check across a few screen sizes/brightness settings, since text-shadow-based contrast doesn't get evaluated by standard automated contrast checkers the way solid text color does).
- Alternate/reduced-motion version of the Landing Page for users with `prefers-reduced-motion` set — worth a follow-up ticket given how animation-heavy this page now is, even though it's not in the initial build scope.

---

## 17. Related Documents
- Product Requirements Document (PRD) v1.0
- Technical Architecture Document v1.0
- Security & Access Document v1.0
- Feature Ticket List v2.0
