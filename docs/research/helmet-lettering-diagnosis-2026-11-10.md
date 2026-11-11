# Helmet lettering/graphic edge diagnosis — 2026-11-10

Sir reported soft, faded graphic/lettering edges in a close-up screenshot. This round inspected the issue and made only temporary browser comparisons; no persistent runtime/material/texture changes were made.

## Evidence

- Read the current bake/export scripts, materials and offscreen-target configuration first.
- Inspected the retained 2250×3000 front product photograph: front lettering and painted outlines are visibly better defined than in the page.
- Inspected the 4096×4096 photographic shell atlas. Its many UV islands carry photographed illumination, and the bake blends front/side/back projections by spatial weights. Curvature/projection mismatch and view transitions can soften/double edges and carry lighting into the color map.
- Parsed the exported GLB: shell color really is 4096×4096 JPEG; plastic/decal color is 2048×2048 JPEG. A 4K atlas is shared among many islands, not a 4K resolution for each front logo.
- In one task-owned page, current viewport 1470×812 / device DPR 2 used a 1838×1015 helmet target and 2205×1218 main canvas, with anisotropy 8. The earlier GPU budget reduction adds a resampling stage that can soften close lettering.
- Temporarily replaced mapped shell/plastic materials with MeshBasicMaterial, preserving the same maps. Contrast and red/blue color separation improved visibly, while some lettering/view-transition defects remained. Thus surface reflections/highlights contribute to the washed-out appearance but are not the sole cause.
- Temporarily raised just the helmet target to 2940×1624 and waited for at least five actual completed scene frames before capturing. Sampling edges improved somewhat; the persistent washed-out/projected decal defects remained. Earlier trial captures taken immediately after resizing showed an empty helmet texture and were discarded as invalid comparisons.

## Assessment

Real printed/painted graphics should retain defined contours; lighting produces tonal/specular changes over them. The current image combines photographed highlights with another physically shaded coat, plus imperfect multi-view projection and limited per-island texel density. This explains the soft/gradient impression. It should not all be described as realistic reflections.

A durable repair should prioritize clean albedo/graphic boundaries, improved projection/UV registration, and reconstructing important logos/patterns as source-faithful vector artwork where possible. Then tune the coat/environment and render resolution together. Increasing reflections or enlarging an existing atlas alone cannot recover absent/blurred source detail.

Temporary evidence: /tmp/mv33-lettering-lit.png, /tmp/mv33-lettering-flat.png, /tmp/mv33-lettering-full-buffer-final.png. All temporary materials and target-size changes were restored, and the diagnostic Space was closed. No rebuild, source publication, knowledge-base update or deployment was performed in this diagnosis round.
