# Retentio Reimagination — Space / Neural Dimension

## Three Directions

### Theme Name: Neural Portal
**Very Brief Intro:** A deep-space landing where an organic blue-cyan ribbon acts as a living cursor portal into a luminous neural brain. Glass UI stays minimal so the interaction is the brand moment.
**Probability:** 0.04

### Theme Name: Quiet Observatory
**Very Brief Intro:** A restrained editorial observatory with cool blue data traces, calm star drift, and more static product clarity than spectacle. The brain appears as a precise instrument rather than a portal.
**Probability:** 0.07

### Theme Name: Chromatic Current
**Very Brief Intro:** A more expressive dimension made of flowing cyan-violet waves, translucent cards, and kinetic gradients. The portal behaves like a current moving through the interface.
**Probability:** 0.03

## Chosen Approach: Neural Portal

### Design Movement
Contemporary digital surrealism fused with premium glassmorphism and neural-interface visualization. The cursor becomes an instrument that opens a second dimension rather than a decorative pointer effect.

### Core Principles
1. Keep the space field quiet and deep; motion belongs to the portal ribbon, brain nodes, and slow star drift.
2. Make the portal organic and asymmetric, never circular or generic.
3. Let glass panels hug their content, remain legible, and reveal the neural layer only where the portal overlaps them.
4. Make motion continuous, eased, accessible, and responsive without requiring landing-page scrolling.

### Color Philosophy
The base is near-black navy to create depth. Electric cyan and blue are reserved for the brain, ribbon edge, focus rings, and active controls so the neural layer feels alive without becoming cluttered. Violet appears only as a low-opacity transition tone in sign-up waves.

### Layout Paradigm
A one-screen asymmetric stage: brand mark in the upper-left, a content-hugging glass headline panel slightly above center, a compact glass CTA near the lower center, and the cursor portal free to roam across the viewport. Auth pages use a balanced two-card composition rather than a centered single form.

### Signature Elements
- An irregular, flowing ribbon portal with animated cyan edge trails and a transparent inner lens.
- A blue 3D brain with small pulsing synapse highlights revealed through the portal.
- Frosted glass cards whose local pixels can become transparent under the portal while their labels stay readable.

### Interaction Philosophy
The cursor behaves like a probe opening a dimensional window. It follows with slight lag, continues low-amplitude idle motion, and morphs its ribbon silhouette. Keyboard focus creates a visible cyan portal state so the experience is not mouse-only.

### Animation
Use GPU-friendly transforms and opacity for UI. The portal follows the pointer with spring-like easing, its edge trails undulate continuously, brain nodes pulse asynchronously, and star drift remains extremely slow. Reduced-motion mode freezes the portal in a readable centered state and removes non-essential pulses.

### Typography System
Use Space Grotesk for the brand and display system, with DM Sans for form labels and supporting copy. The landing headline is large but light-to-medium weight, generous in tracking, and never outlined with hard white text-shadow. Form headings are compact and bold enough to anchor glass cards.

### Brand Essence
Retentio is a neural retention observatory for small teams that need to see customer risk before it becomes churn. It is **perceptive, calm, alive**.

### Brand Voice
Headlines are direct and quietly confident. CTAs are action-oriented without hype. Microcopy is observant and specific.

Example lines:
- “Welcome to Retentio.”
- “Open the signal.”

### Wordmark & Logo
Keep the existing orbital R mark, but let it glow softly in cyan on dark surfaces and reduce wordmark tracking slightly on mobile.

### Signature Brand Color
**Portal Cyan — #5CF6FF.** A cool cyan that reads as light passing through a neural membrane rather than a generic SaaS accent.

## Reimagination Implementation Plan

The existing Wouter route structure, AuthContext, and API boundary remain intact. The landing route will be rebuilt as a single viewport with no required scrolling: a canvas star field, a browser-native neural brain scene, and an organic SVG/canvas ribbon mask that follows the pointer. The headline and CTA will become content-hugging glass panels with partial portal reveal while keeping the text readable. The current supplied hands and black-hole treatment will not be carried into the new landing because the attached brief establishes the neural portal as the new visual ground truth.

The login route will keep its form layout, facts card, and navigation behavior while receiving a subtler background exposure through an additional dark overlay. The sign-up route will replace the video/ambient background with a continuously animated blue-cyan-violet glow-flow field and use two glass cards: the existing form and a new companion information panel with a looping typewriter effect and blinking cursor.

The portal and brain should be implemented first as a meaningful landing checkpoint. The user review gate is whether the organic ribbon feels asymmetric and alive, whether the neural brain is visibly revealed under the portal, and whether the glass headline and CTA remain legible during overlap. Auth restyling follows only after this interaction is approved.

## Review Gates

**Gate 1 — Neural Portal Landing:** Review portal silhouette, brain reveal quality, star-field density, headline/CTA glass treatment, and one-screen composition.

**Gate 2 — Public Auth:** Review login dimming and sign-up glow-flow plus typewriter companion card.

**Gate 3 — Product Continuity:** Confirm the reimagined public surfaces still transition cleanly into the existing authenticated workspace without changing data or route contracts.

## Existing Product Constraints Preserved

Retentio remains a frontend-only static project with mock auth behavior until FastAPI contracts are available. The dashboard, predict, customers, settings, and Dock navigation remain outside the redesign scope unless a later review requests product-surface changes. All large media stays in managed webdev storage, and the redesign must retain keyboard focus, reduced-motion support, responsive layouts, and accessible contrast.

## Style Decisions

- The landing must show an idle Neural Portal state by default: an asymmetric cyan-edged ribbon/lens with a visible blue neural-brain layer, even before pointer movement.
- Portal Cyan is #5CF6FF and reads blue-cyan rather than mint; it is reserved for portal edges, neural highlights, focus states, and primary actions.
- The landing composition is asymmetric: the glass headline sits off-center while the portal occupies the counterweight space and the CTA stays compact near the lower center.
- Signup/auth copy uses observatory and signal language tied to retention risk, customer behavior, and churn detection; generic onboarding phrasing is avoided in new copy.
