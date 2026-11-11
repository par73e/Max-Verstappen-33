# MV33 navy/orange identity and clean 2023 artwork · 2026-11-10

## User scope

Sir requested navy/orange throughout the scrolling experience, with role-specific judgment. Sir also authorized repairing the soft sponsor lettering and livery edges diagnosed earlier. Existing source-pinned layout, Mona/Brier typography, section rhythm and animation state machines remain the starting point.

## Implementation

- `theme/palette.json` records the source identity-color translation. `public/theme.css` defines semantic roles, including **body** overrides because the retained CSS redefines its palette on body at mobile breakpoints.
- Navy #101b30 and raised/slate blues replace olive scene grounds. Orange #ef6b19 carries actions and signature marks; soft orange #f2a268 accents navy; dark orange #b84310 supports smaller links on paper. Cool paper #f4f6fa and blue-grey neutrals replace pale green.
- The build translates HTML/engine color literals and makes derived SVG copies; original reference vectors remain intact. Photographs, authentic helmet paint, debug colors and HDR lighting are not blindly recolored. Menu photos receive a navy duotone. Rive files keep their original state machines; their discrete ink roles are translated at canvas compositing through a bounded color lookup.
- A source-derived SVG color separation was traced from each retained 2250×3000 2023 product photograph. Ink regions have clean spline edges and constant color rather than photographed highlights. Tight front-vent/latch patches retain actual clear-hardware photography. The original source files stay unchanged.
- Blender bakes these four views onto the existing unique UV atlas at 4096×4096 with a stronger front preference and narrower projection blending. Lossless PNG replaces only the shell image in a derived GLB; mesh geometry, UVs, accessory textures and source model remain intact.
- Clearcoat/specular strength is reduced to keep ink visible while preserving separate physical reflections. The visor still uses the prior reflective gold material. The 2024 fan edition retains its photographic colors and receives the shared material tuning.
- The helmet color target now has up to DPR2 / 5M pixels /2samples, replacing the earlier DPR1.25 /2M cap. A pose/camera/texture-revision key allows reusing a stationary PBR target. This is not a claim of zero redraws while the reference continues moving its camera.
- Mobile no-hover fluid trails no longer expose scraps of helmet on a resting portrait; explicit source touch exploration is preserved. The pointer-only mask is separate from the existing explicit helmet wipe.

## Reproduction

1. `scripts/vectorize_helmet_artwork.py` (Pillow, NumPy, VTracer0.6.15) writes editable source-coordinate SVG separations.
2. Rasterize those SVGs at original2250×3000 dimensions in a standards-compliant browser canvas, without resizing.
3. `Blender --background --python scripts/bake_helmet_editions.py -- --edition=season-2023 --clean`
4. `.venv/bin/python scripts/pack_clean_helmet.py`
5. `npm run build && npm run check`

## Limits and provenance

This is an approximate reconstruction from product photography on Maubian's CC BY4.0 mesh, not an official UV master or scan. Small lettering, projection seams, vent registration and silhouette can still differ. Vector separation cannot recreate detail absent from the photos. The goal is materially cleaner legible paint with reflections separated from color, rather than claiming that a 4K file alone supplies official source quality. Original photos and credited mesh provenance remain in `assets-manifest.json` and prior research notes.

## Final verification

- `npm run build`, `npm run check`, Python AST checks and `git diff --check` passed.
- Binary comparison confirmed unchanged meshes/accessors and byte-identical non-shell GLB buffer views.
- Desktop1440×900 and touch-emulated390×844: no recorded script/resource errors or horizontal overflow. Mobile tap lock sets aria-pressed=true and stops Lenis; unlocking restores scrolling. No old lime/olive computed text/background roles remained in the final mobile DOM sample.
- All10 light-gallery location captions compute to #344865. Actual sampled gallery fieldrgb193,196,203 gives5.32:1 contrast. Orange/navy primary pair5.56:1; darkorange/paper5.04:1.
- At a settled static full-helmet view, completed render-budget frames262→294 while PBR helmet draw count stayed26→26. This verifies target reuse in that settled state, not zero work in the full page.
- Independent2023 edition page reached state=ready with no reported errors and displayed the new clean material. This round did not include physical-phone, cross-browser or sustained GPU measurements.
- Finish reviewer requested gallery-caption contrast and design-sidecar updates. Both were scored resolved; final disposition `ship` applies to those scored fixes. DESIGN.md and .impeccable/design.json now describe the current palette and reconstruction limits.
