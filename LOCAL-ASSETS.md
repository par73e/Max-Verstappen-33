# Local asset inventory - 2026-11-08

Preview all imagery at http://127.0.0.1:4173/assets.html .

| Path | Content and current use |
| --- | --- |
| `public/max/portrait-front-source.png` | Original F1 front portrait, preserved from yesterday's `/private/tmp/max-2024.png` |
| `public/max/portrait-front-cutout.png` | Background extraction left by the interrupted session, now used in the hero |
| `public/max/portrait.webp` | Previous angled portrait, kept as a source |
| `public/max/helmet-04-00.jpg` through `helmet-04-03.jpg` | Original 2023 season product photos; `02` is the frontal view |
| `public/max/helmet-2023-front-cutout.png` | Historical Imagegen-assisted extraction; current hero uses the GLB |
| `public/max/mv.svg`, `favicon.svg` | Official MV mark and tab-icon layout |
| `public/max/helmet-00-*`, `helmet-03-*` | Other helmet designs and angles in the gallery |
| `public/max/photo-*`, `signature.png` | Editorial photos and signature; provenance is in the manifest |
| `public/gl/models/helmet-21.glb` | Reference-site geometry, not a Max-specific model |
| `assets-manifest.json`, `max-assets.json` | Source URLs, hashes, derivation and selected assets |

Downloads is currently empty except system files. The RB19/RB16B models recorded yesterday are no longer there. AERO's research records point to `/Users/louis/Suep/Project/AERO/assets/source/rb19/source/Sketchfab_2024_02_21_19_13_35.blend` and that project's `assets/working/` directory. These are car assets, not helmets. This task did not move or modify AERO files.

## Model supplied and integrated (2026-11-09)

The user supplied `helmet_redbull_-_max_verstappen.glb` from Downloads. The 4k original is retained in `assets/source/max-helmet/original.glb` (local only); the normalized mesh is `assets/source/max-helmet/base.glb`. Author/license: Maubian, CC BY 4.0, https://skfb.ly/pEDBZ . Complete credit and adaptation details are in `assets/source/max-helmet/ATTRIBUTION.md`.

Public runtime models: `public/gl/models/season-2023.glb` and `zandvoort-2024.glb`. Both use real geometry and reconstructed photographic UV materials, not the previous hero cutout. They are approximations, not official scans. The hero's solid model and wireframe share this geometry.

Official Orange Tribute photography is in `public/max/orange-2024-00.jpg` through `08.jpg`; sources and hashes are in `assets-manifest.json`. Blender-baked material maps are in `public/max/materials/`. Earlier AI background extractions remain as historical assets and are not the current 3D hero.

The earlier Downloads/AERO inventory above is a snapshot from before the user supplied the helmet.

Final material pipeline: only `*-helmet.jpg` is baked (4096px). Glass/plastic use authored UVs and source details; older `*-glass.jpg` and `*-plastic.jpg` files are retained as historical outputs and are not loaded.
