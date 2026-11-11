# Signature and center logo — 2026-11-10

## Requested changes and scope

Sir requested a serious high-resolution portrait, a smooth orange signature, and center-logo exit/re-entry matching the Norris homepage. This local change completes the signature and logo adapters. Sir subsequently authorized AI processing, and the serious portrait was installed as a 2048×2048 composition. Its original photograph is 1920×1920, not native 2K. See serious-portrait-2026-11-10.md for the final asset, processing limits and verification.

## Signature

The prior 300×212 CC0 Wikimedia PNG was enlarged across the viewport and tinted lime by a CSS filter. `scripts/vectorize_signature.py` now reproduces `public/max/signature-orange.svg` by fitting spline contours with VTracer 0.6.15. The SVG contains filled paths, no embedded raster image, and uses #ef6b19 directly. Runtime signature canvases and static signature images consume the SVG, with the lime filter and screen blend removed. Existing Rive input-driven opacity/cropping remains. This is traced artwork, not an original driver-provided vector or a new stroke-by-stroke writing animation. Attribution and derivation are recorded in assets-manifest.json. VTracer is optional offline tooling; the site adds no runtime dependency.

## Source audit and logo animation

Read the live homepage and its public bundle, `https://lando.itsoffbrand.io/dev-js/lando-by-OFF+BRAND.05.js`, and compared with retained `reference/lando-engine.js`. Function nR initializes the `logo` state machine, with boolean `logo-active`; pK writes it. The source navigation timeline creates an absolute `.top-marker` of height 10vh, sets the state false on desktop scroll entry and true on leave-back. Mobile uses scrollY <= 10. Navigation brand/button scale separately scrubs from 1.2 to 1.

The prior MV image hid the Rive canvas and never mirrored that input. The replacement inline SVG retains the original canvas/hooks and reads its live `logo-active` value. A single reversible CSS transition scales/folds the MV core and wings into the center and fades it; reversing the input expands it. Timing: transform .55s cubic-bezier(.65,0,.35,1), opacity .4s ease. Mid-transition reversal is supported. This adapts the source trigger/state behavior to MV geometry; it is not a claim that Norris's proprietary Rive keyframes have been reproduced exactly. Reduced motion removes the new transition.

## Local verification

- Build, six JS syntax checks, and git diff --check passed.
- Desktop visual inspection: smooth orange vector signature; centered orange MV.
- Live opacity/scale samples during exit moved 1 → 0 and scale 1 → .18; return moved 0 → 1 and scale .18 → 1, with corresponding false/true Rive states.
- 390×844 at DPR 2: no horizontal overflow or recorded runtime errors; logo state changed true → false on scroll.
- Existing local portrait and helmet pipeline remains; its earlier uncommitted changes were preserved.
- No commit, push, knowledge-base update, or deployment performed.
