# Serious portrait and 2K delivery — 2026-11-10

## Result and limits

Sir authorized AI enhancement and background extraction of the selected frontal, neutral-expression F1 photograph. The homepage now uses `public/max/portrait-serious-2k.png`, a 2048×2048 RGBA asset. The original photograph remains unchanged in `public/max/portrait-serious-source.png` (1920×1920).

Two built-in image_gen requests explicitly asked for 2048×2048 or larger transparent output, but both actually returned 1254×1254 PNGs. We did not label those as 2K generations. The retained second extraction is `public/max/portrait-serious-ai-cutout.png`. To preserve more real facial detail, the final asset uses original photographic RGB in the interior, AI-extracted alpha, and AI color only in a 24px silhouette band to remove the blue source-background fringe. `scripts/pack_serious_portrait.js` reproduces this browser-canvas composition. Final output dimensions are 2K; photographic detail is limited by the 1920px source. No claim of native 2K photography or AI-recovered true facial detail is made.

Source: https://media.formula1.com/image/upload/content/dam/fom-website/drivers/2024Drivers/verstappen.png
Source context: https://www.formula1.com/en/drivers/max-verstappen
Source and derivatives have individual hashes and methods in assets-manifest.json. Existing studio portraits and their depth maps were retained.

## Source-first integration

Inspected the existing homepage HTML/DOM: `.home-hero[data-gl-track="head"]`, `[data-gl="head"]`, `[data-gl-helmet="hover"]`. Followed these into retained `reference/lando-engine.js`: W9's displaced head surface and the hero's helmetHover/hoverAnimation lifecycle. Kept the source's renderer, camera, 256×256 adapted grid, helmet geometry/materials and shared wire transforms.

`public/texture-bridge.js` registers RGB, alpha and depth with one transform: eye anchor (1024,940), width 3072×1.09 in 2048px texture space, photograph head-center/eye fractions (.514,.207), recalibrated after Sir reported misalignment. Runtime color packing remains 4096px; source photo resolution and final asset resolution are exposed separately in mv33PortraitInfo.

The new `portrait-serious-depth.png` is inferred offline from the original photo and aligned extraction using the existing Depth Anything V2 Small ONNX weights. `scripts/estimate_portrait_depth.py` accepts optional source/alpha/output/record paths, retaining its previous defaults. The model hash and inference metadata are in portrait-serious-depth.json. This is relative depth rather than a complete 3D scan.

Reproduction after generating the extraction:

1. Serve public/ and run scripts/pack_serious_portrait.js in a same-origin browser evaluation. Save its returned base64 PNG as public/max/portrait-serious-2k.png.
2. Run `.venv/bin/python scripts/estimate_portrait_depth.py --model /path/to/model.onnx --source public/max/portrait-serious-source.png --alpha public/max/portrait-serious-ai-cutout.png --output public/max/portrait-serious-depth.png --record docs/research/portrait-serious-depth.json`.
3. Run `npm run build` and `npm run check`.

## Final image_gen prompt and tool

Built-in image_gen; input is the original 1920×1920 photograph; transparent_background=true. Retained generation: exec-61d54e3c-3e01-400a-8961-9d4c3650e7ec.png. This generated RGB is used only near the final silhouette, not across the photographic facial interior.

> Edit the supplied original Max Verstappen photograph. OUTPUT SIZE REQUIRED: 2048 x 2048 pixels minimum, square 2K image. Previous output at 1254x1254 was too small, so please use HIGH RESOLUTION 2048x2048 or 2560x2560. This is a resolution enhancement / background extraction production asset, not a small preview. Preserve original photo's exact serious neutral closed-mouth expression, identity, natural skin and all original framing and photographic lighting. No smile, no teeth, no stylization, no face reshaping or exaggerated sharpened skin. Remove blue background to genuine transparency, with clean alpha on hair and shoulders. Keep original suit marks as in supplied original photo. Keep complete original shoulders and visible upper body, centered with exactly original head/body proportions and position in the square. Improve fine detail gently to 2K without changing face or expression.

## Verification

- Actual output: PNG, 2048×2048, RGBA, alpha range 0–255.
- npm build/check, preparation-script syntax and git diff --check passed.
- Ego lite desktop at 1440×900 / DPR 2: inspected serious face and cleaned hair edges; full helmet covers head, with neck/shoulders/torso retained. Errors empty; html root remains transparent.
- Ego lite mobile at 390×844 / DPR 2: inspected default face and scrolling orange signature, logo state false after leaving top, errors empty, no horizontal overflow.
- Temporary visual evidence: /tmp/mv33-serious-desktop-final.png, /tmp/mv33-serious-helmet-final.png, /tmp/mv33-serious-mobile-final.png, /tmp/mv33-serious-mobile-scroll.png.
- Local preview on 4173; no commit, push, knowledge-base maintenance or public deployment. Physical phones and the user's Chrome tab were not tested.
