# Hero depth, portrait and Retina finish — 2026-11-09

## What the source actually implements

`reference/lando-engine.js`, class W9, builds a 1×1 plane with 128×128 subdivisions, displacementScale .25, head depth/alpha/normal/roughness maps and pointer rotation. It is a photo-textured displaced surface rather than a complete face/head/body scan. The supplied reference scene has a real 3D helmet in a separate render target. This distinction matters: the implementation can show local facial relief during restrained pointer motion, not unseen side/back anatomy.

## Portrait asset and preparation

New native RGB: `/Users/louis/Suep/Project/MV33/public/max/portrait-studio-source.jpg` (1200×801), downloaded from the linked Motorsport studio portrait. It has a cleaner close-up presentation than the previous full-body F1 photograph. It is not described as a 4K source.

Opacity extraction: `/Users/louis/Suep/Project/MV33/public/max/portrait-studio-alpha.png`, created with the built-in image_gen tool; runtime reads only its alpha, while photographic RGB stays sourced from the JPEG. Generated facial color is not consumed. Original generated output is preserved outside the repository under Codex generated_images.

Final image-generation prompt:

> Use case: background-extraction. Edit target: the provided frontal studio photograph of Max Verstappen. Remove only the pure white background to actual transparency. Keep the exact original framing, head position, facial identity and expression, hair silhouette, shoulders, racing suit and printed marks. Keep the landscape 1200:801 aspect ratio and do not zoom, recompose, beautify, retouch or invent details. Deliver a clean anti-aliased transparent cutout. This cutout will primarily provide an opacity mask, so accurate registration to the input image is essential.

Relative depth: `/Users/louis/Suep/Project/MV33/public/max/portrait-studio-depth.png`, produced offline with the Apache-2.0 ONNX Depth Anything V2 Small model, with source/model/hash recorded in `portrait-depth.json`. It is an inference, not a measured scan. Foreground depth is extended beyond the alpha edge before smoothing to avoid displacement tearing at shoulders/hair.

The hero uses a 256×256 grid and 4096px color texture packing. Surface normals are derived from the depth with a 24-pixel sampling interval, avoiding visible 8-bit derivative quantization. Pointer tilt is .095 rad maximum instead of .075. Runtime requires no ML weights or inference libraries.

## Helmet and entry finish

The 2023 bake now uses four native 2250×3000 product photographs rather than 900×1200 transformed copies. The atlas remains 4096px and the Maubian model/UV system is preserved. The helmet render target uses 4x MSAA; texture anisotropy is capped at 8. Clearcoat and visor remain separate materials. The source-fit comparison and 2024 edition are retained; no claim of official scan fidelity is added.

The global desktop DPR cap changes from 1.25 to 2, matching the verified Retina display. The entry is midnight navy #101823 with orange #ef6b19 rather than olive #282c20. Fly-through lifecycle remains.

## Verification

- Source, generated assets and required module syntax checked; build and whitespace checks passed.
- Desktop: 2x DPR, 4096px color texture, 256×256 head subdivisions, matching model/wire transforms; no recorded runtime errors.
- Pointer left/right produced head y rotations about -.082 / +.071 radians, with inspected portrait frames.
- A short foreground RAF sample produced 67 frames in approximately 1.1 seconds (about 17ms/frame). This is a local sample, not a device-performance guarantee.
- Entry navy/orange, default portrait, full helmet and 390×844 mobile portrait/helmet were visually inspected. Mobile had no recorded error or horizontal overflow.
- No public deployment, physical-phone or cross-browser certification is claimed.

## Portrait-to-helmet proportion correction — 2026-11-09

After comparing the live Lando Norris homepage's portrait and complete helmet reveal, the Max portrait was enlarged by 12% around texture-space eye anchor (1024, 1000). The same registration is applied to photographic RGB, opacity and inferred depth before normals are derived. Helmet geometry, fit and shared wireframe transforms are unchanged.

The enlarged portrait and complete helmet reveal were visually inspected in ego lite on desktop and at 390×844. The head remains covered during the reveal, with shoulders and torso retained; no runtime errors or horizontal overflow were recorded. Build, six-module syntax and whitespace checks passed. This is a local composition correction, not a new source photograph, physical-device test or deployment.
