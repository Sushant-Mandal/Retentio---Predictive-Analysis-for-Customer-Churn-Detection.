# Retentio Visual Revision Tasks

- [x] Replace generic landing intro with the requested three-stage scroll sequence: “Welcome to Retentio.”, “Losing Customers?”, and “Your Retention Journey starts here”.
- [x] Remove the premature Get Started CTA from the initial landing viewport; reveal it only after the final scroll stage and hands transition.
- [x] Remove the helix/orbit and pixelated treatment from the landing background.
- [x] Rework the landing background toward a dark galaxy/star field with a cursor-follow glow.
- [x] Rework the hands toward solid dark-peach and black forms, each with a controlled glow, while keeping the visual system performant and accessible.
- [x] Preserve the auth reveal flow after the final CTA and route to Sign Up or Login.
- [x] Verify desktop/mobile layout, reduced-motion behavior, and production build before checkpointing.

## Supplied Hands Artwork Revision

- [x] Register `/home/ubuntu/upload/hands.jpg` as a webdev-managed visual asset without re-inspecting the image file.
- [x] Replace the landing’s generated mesh/helix background with the supplied portrait hands artwork.
- [x] Add subtle image breathing/parallax and a cursor-follow glow that freezes after five seconds of inactivity.
- [x] Keep the staged landing sequence and reveal Get Started only after the final scroll stage.
- [x] Verify the new landing background on desktop and mobile, then save a checkpoint.

## Final Offering-Hand Artwork

- [x] Register `/home/ubuntu/upload/hands2.jpg` as a webdev-managed visual asset without re-inspecting the uploaded image.
- [x] Transition from the first hands artwork to the second wireframe offering-hand artwork only at the final landing scroll stage.
- [x] Keep Get Started positioned over the second artwork and preserve the Sign Up/Login reveal after activation.
- [x] Verify the transition and CTA on desktop and mobile before checkpointing.

## Animated Landing Correction

- [x] Remove the two-artwork static background treatment from the landing hero.
- [x] Build animated solid hand silhouettes: dark peach hand on one side, black hand on the other, with distinct soft glows and subtle motion.
- [x] Keep the galaxy star field and cursor-follow glow, with no helix or pixel-grid decoration.
- [x] Make the scroll narrative exactly three copy beats followed by one offering stage: Welcome to Retentio; Losing Customers?; Your Retention Journey starts here; then animated hands with Get Started.
- [x] Remove duplicate “Your retention journey starts now”/extra landing text and unnecessary visual elements.
- [x] Verify all four states, delayed CTA behavior, dark theme, mobile layout, and production build before checkpointing.

## Reference-Aligned Restoration

- [x] Remove the crude generated canvas hand silhouettes from the landing.
- [x] Restore the supplied hand references as the visual ground truth while keeping the overall reference composition intact.
- [x] Animate the hand layers themselves with glow, pulse, and gentle parallax rather than showing them as inert background images.
- [x] Replace only the backdrop with a dark space/star field and retain cursor-follow light.
- [x] Keep the three copy beats and final delayed Get Started stage clean, with no duplicate text.
- [x] Verify reference fidelity and production build before checkpointing.

## Scroll Text Refinement

- [x] Replace fade-only copy transitions with visible upward travel and a readable settled state for every scroll beat.
- [x] Strengthen the landing headlines with bold display weight, tighter line breaks, and improved contrast over the hands/space composition.
- [x] Refine the three landing messages so they feel sharper and more intentional without adding extra copy.
- [x] Verify text remains visible during and after each transition on desktop and mobile, then checkpoint.

## Landing Pacing Correction

- [x] Give each of the three signal messages and the final hands stage a full viewport-sized dwell section.
- [x] Add wheel gesture throttling so one scroll gesture advances only one stage.
- [x] Keep the copy visible and settled long enough to read before the next upward transition.
- [x] Verify the paced sequence on desktop and mobile, then checkpoint.

## Editor Feedback Cleanup

- [x] Remove the two unnecessary landing helper paragraphs identified by the visual editor.
- [x] Remove the unnecessary progress UI elements identified by the editor.
- [x] Improve the final CTA color, hover, pulse, and press animation using the frontend motion guidance.
- [x] Move the final CTA upward so it sits in the center of the offering hand.
- [x] Change the cursor-follow effect to a soft faded white glow.
- [x] Verify the refined landing and save a checkpoint.

## Natural Scroll Motion Refinement

- [x] Preserve the current reference composition, typography, CTA timing, and overall UI.
- [x] Make the first hands visibly glow with a stronger but restrained pulsing halo.
- [x] Enrich the dark space backdrop with brighter stars and a few subtle cosmic entities.
- [x] Sync the visual layer to the landing rail’s downward scroll so it feels like moving through a scene, not viewing a pinned painting.
- [x] Avoid upward-floating hand motion; use only gentle breathing and scroll-linked parallax.
- [x] Verify the non-degrading refinement and save a checkpoint.

## Continuous Artwork Scroll

- [x] Replace snap-stepped wheel progression with native continuous scrolling.
- [x] Let the first artwork reveal through three consecutive viewport thirds as the page scrolls down.
- [x] Bring the second artwork upward from below during the final viewport instead of crossfading it in.
- [x] Keep copy moving upward naturally with the page like a long-form document.
- [x] Change Get Started to black with bold white text, white glow, and black shadow.
- [x] Verify the continuous scroll composition and save a checkpoint.

## Scroll Scene Reliability Fix

- [x] Ensure the star field and hand scene respond continuously to the actual landing scroll position.
- [x] Make the first artwork occupy the opening three viewport sections without appearing pinned/static.
- [x] Make the second artwork physically follow below the first and reliably occupy the final offering section.
- [x] Verify “Reach them before they leave” and Get Started over the second hand at the final scroll position.
- [x] Preserve the current typography, CTA treatment, and overall visual quality while fixing the scene architecture.

## Cosmic Entity Refinement

- [x] Add a small rotating black hole with a luminous accretion ring and bent-light treatment in the opening section.
- [x] Add a small moving pulsar with rotating beams in the second section.
- [x] Make stars and cosmic entities continue moving while the landing scene scrolls.
- [x] Smooth the artwork/copy travel so it feels like natural document scrolling rather than a rough pull upward.
- [x] Reposition the final offering hand and Get Started control so the CTA is centered on the hand.
- [x] Verify the refined scene and save a checkpoint.

## High-Refinement Cosmic Scene

- [x] Replace the weak black-hole drawing with a small bright accretion ring, central shadow, and visibly bent-light arcs.
- [x] Replace the weak pulsar drawing with a compact fast-orbiting luminous object and strong rotating emission beams.
- [x] Make both entities follow the scroll scene and disappear cleanly as later content enters.
- [x] Simplify and recompose the final hands stage so the second artwork, headline, and CTA read as one polished scene.
- [x] Verify the full landing sequence and save a checkpoint.

## Supplied Black-Hole Model Integration

- [x] Inspect `black_hole.zip` contents safely without executing archive files.
- [x] Determine whether the archive contains a browser-loadable model, animation, texture, or rendered fallback.
- [x] Register the usable asset through the managed webdev asset path.
- [x] Replace the procedural black hole in the first landing section while preserving scroll-follow behavior and the pulsar.
- [x] Verify performance, fallback behavior, and production build before checkpointing.

## Stable Black-Hole Motion Refinement

- [x] Keep the supplied black-hole body fixed at its scene position.
- [x] Animate only the ring/material lighting so the ring revolves around the black hole.
- [x] Restore animated stars, shiny planets, and the cursor-follow white glow.
- [x] Make the black-hole scene move upward naturally with the content instead of staying pinned.
- [x] Verify the refined cosmic scene and save a checkpoint.

## Reimagination: Space / Neural Dimension

The attached redesign brief is the new visual ground truth for the next build pass.

- [x] Audit the existing landing, login, and sign-up routes against the new brief and preserve working auth behavior.
- [x] Define the new portal, glassmorphism, typography, color, and motion system in `ideas.md` before implementation.
- [x] Build a one-screen landing with a deep space field, organic blue-cyan ribbon portal, cursor-follow easing, and visible neural-brain reveal.
- [x] Keep the landing headline and Get Started button in content-hugging glass panels with partial portal reveal and persistent label contrast.
- [x] Dim the login background without changing login layout or behavior.
- [x] Replace sign-up background with animated cool-tone glow-flow waves, add glass form card, and add typewriter companion card.
- [x] Verify desktop/mobile, reduced-motion, keyboard focus, portal interaction, and auth navigation before delivery.
- [x] Ask for visual review at the first meaningful landing checkpoint before expanding the redesign further.

## Vortex Portal Refinement

- [x] Keep the space field visible everywhere as the default base layer.
- [x] Make the brain a fixed, hidden-under-space scene that does not follow the cursor.
- [x] Add fixed thought bubbles around the brain with the six churn-related phrases from the new brief.
- [x] Reveal brain and thought bubbles only through the organic cursor-following vortex window.
- [x] Animate only the vortex edge trails continuously; keep the inner portal transparent and the hidden scene static.
- [x] Preserve the one-screen layout, content-hugging glass headline/CTA, keyboard focus, reduced-motion fallback, and responsive behavior.
- [x] Verify pointer movement over different fixed brain regions and save a checkpoint.

## Vortex Reference Match

- [x] Change only the vortex to an irregular blue-cyan luminous ribbon with multiple flowing trails and a transparent center, matching the supplied reference.
- [x] Enlarge the fixed brain reveal and overall vortex scene to approximately 75% of the viewport.
- [x] Preserve the current brain animation, thought bubbles, space background, glass UI, copy, CTA, and interaction behavior.
- [x] Verify desktop/mobile sizing and save a checkpoint.

## Exact Vortex Correction

- [x] Return the vortex assembly to its original scale; enlarge only the fixed brain scene.
- [x] Replace the current loop with 3–4 separate overlapping asymmetric strands that weave across an irregular pentagon-like silhouette.
- [x] Add per-strand core, inner-glow, and outer-ambient passes with hue rotation from indigo/blue to cyan/teal.
- [x] Add uneven brightness, flowing dash motion, subtle organic wobble, and sparse strand sparkles without rigid spinning.
- [x] Preserve the current space background, hidden-scene masking, thought bubbles, glass UI, copy, CTA, and pointer easing.
- [x] Verify desktop/mobile and save a checkpoint.

## Responsive Vortex Refinement

- [x] Keep the vortex assembly at its original scale and enlarge only the hidden brain scene further.
- [x] Remove visible cursor lag while keeping the vortex movement smooth and premium.
- [x] Preserve the exact 3–4 strand woven loop, three glow passes, hue rotation, brightness variation, sparkles, and transparent center from the pasted specification.
- [x] Preserve the space base, hidden brain/thought layers, glass UI, copy, CTA, and pointer-only interaction model.
- [x] Verify desktop/mobile motion and save a checkpoint.

## Smaller Black-Hole Vortex

- [x] Replace the current vortex look with an animated inward-swirling blue-violet strand field inspired by the supplied reference, without using the image itself.
- [x] Add a dark circular central opening while preserving the portal reveal behavior beneath it.
- [x] Make the vortex smaller than the current portal ratio on desktop and mobile.
- [x] Preserve the enlarged brain, space field, thought bubbles, glass UI, copy, CTA, and cursor tracking.
- [x] Verify responsive scale and save a checkpoint.

## Vortex Layering Correction

- [x] Remove the black center fill so the vortex interior is transparent and reveals the fixed brain scene.
- [x] Remove the outer translucent vortex layer that makes the surrounding portal look see-through.
- [x] Keep the visible vortex strands and their local glow solid/opaque enough to read cleanly.
- [x] Increase the vortex size slightly, without returning to the previous oversized ratio.
- [x] Preserve the rest of the landing and verify desktop/mobile before checkpointing.

## External Vortex Halo and Brain Scale

- [x] Remove the remaining translucent halo outside the last visible vortex strand.
- [x] Keep the vortex strand edges crisp without adding a replacement outer wash.
- [x] Enlarge only the hidden neural brain scene slightly more.
- [x] Preserve the landing copy, CTA, space field, cursor reveal, and responsive behavior.
- [x] Verify desktop/mobile and save a checkpoint.

## Visual Editor Span Removal Verification

- [x] Inspect the editor-targeted spans in `client/src/pages/Pages.tsx` and determine whether the edits were already applied or selectors are stale.
- [x] Apply the intended removals manually if the targeted spans are still present.
- [x] Validate the affected routes and production build, then save a checkpoint.
