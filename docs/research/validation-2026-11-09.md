# Validation - 2026-11-09

- `npm run build`: generated homepage and both helmet routes.
- `npm run check`: engine, texture bridge, homepage adapter and edition module syntax passed.
- Python syntax checks passed for the build and Blender scripts.
- `git diff --check`: passed.
- ego lite desktop: both edition pages reached ready state; no recorded runtime errors, broken loaded images or horizontal overflow. Side-view button and wireframe visibility toggles worked.
- ego lite 390x844: Orange Tribute page reached ready state without overflow or recorded errors; visual layout inspected.
- Theme emulation: icon href switched to `favicon-light.svg` and `favicon-dark.svg` on prefers-color-scheme changes.
- Homepage full reveal: native model and wireframe both had 19,807 vertices; position and scale matched, rotation delta was [0, 0, 0]. Screenshot inspected with shoulders and upper body preserved. No recorded runtime errors, broken loaded images or horizontal overflow.
- Homepage menu contained both edition links; clicking Season 2023 navigated to the correct route and loaded its model.

These are local Chromium previews, not a cross-browser or physical-device certification. Models are artist-mesh / photographic-livery reconstructions. Some side decals, UV transitions and shell details differ from the photographic references; do not describe the result as an official scan or complete source-site equivalence.

## Final material repair

- Rebuilt both GLBs with a 4096px shell bake, original hardware UVs/normal maps and a physical coated visor; each is approximately 3 MB. Removed unused embedded visor images.
- Fixed the transparent-to-opaque depth-write setting and duplicate ORACLE projection. Desktop runtime confirmed glass is opaque, writes depth, keeps its normal map and has no photo color map. Hardware has its authored map and normal map.
- Recalibrated forehead projection, narrowed multi-view blending, fixed crown confidence underflow and reversed top-view projection. Inspected front/side views and both Orange Tribute front/back views.
- Hero default outline, full hover, hover exit and 390x844 full reveal were inspected. Model/wire position, scale and rotation matched; shoulders and torso remain visible. Top signature opacity was zero after entry; runtime error list was empty.
- Orange Tribute wireframe toggle hid the solid model and showed matching wire geometry. Its mobile route loaded without overflow, broken loaded images or recorded errors.
- Final `npm run build`, `npm run check`, Python AST parsing and `git diff --check` passed. Blender work used separate background processes, all of which exited; no open interactive scene was changed.
