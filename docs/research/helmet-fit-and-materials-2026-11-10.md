# Helmet/head registration and surface finish — 2026-11-10

## Request and source-first investigation

Sir reported that the new serious portrait was not centered under the helmet and their scales no longer matched, then requested investigating and improving the helmet's realism against https://landonorris.com/ . This change continues the existing local uncommitted work.

Read the live hero HTML/DOM first: `[data-gl-track="head"]`, `[data-gl="head"]`, `[data-gl-helmet="hover"]`. Followed its script URL to https://lando.itsoffbrand.io/dev-js/lando-by-OFF+BRAND.05.js and compared F9, W9 and O9 with retained reference/lando-engine.js. Viewed reference and local face/full-helmet at the same 1440×900 viewport, then the live reference at 390×844.

The source uses a displaced photographic head plane and a separate real helmet with independent shell/glass/plastic materials. Responsive camera Z is 3 desktop and 3.75 mobile; helmet Y is .05 desktop and 0 mobile. Its head pointer amplitude is .075, and the helmet uses head rotation /1.5 plus a fixed .06π pitch. Shared camera and matched spatial registration are essential. The helmet's realism also relies on real surface geometry, independent material channels and studio HDR reflections.

## Registration correction

The new photograph had been registered by an approximate eye midpoint while retaining the old portrait's vertical anchor. Its silhouette was displaced relative to the helmet; stronger local pointer rotation increased the difference during reveals.

The one shared RGB/alpha/depth transform now uses:

- Head center fraction X .514 (previously .506).
- Eye anchor (1024,940), previously (1024,1000), in 2048px texture space.
- Uniform portrait scale 1.09, previously 1.12; base square width remains 3072.
- Head pointer amplitude restored to the source .075 from the local .095.

The helmet model, its scale [7.2,6.6,7.1], camera, responsive offsets, and wireframe geometry remain shared and unchanged. Visual fitting follows the reference crown/chin clearance and head-to-helmet relationship, rather than stretching the person's facial proportions.

## Why the material looked different

The reference shell uses a dedicated normal map, metalness 1, roughness .05 and environment intensity 3; its glass uses distinct color/roughness/normal/metalness maps and environment intensity 1.5. Those values work with its authored chrome artwork and UVs, and cannot simply be copied onto the Max white/red photographic livery.

Local inspection showed a different input: the original Max shell material in assets/source/max-helmet/base.glb already has no connected normal map. Its glass and plastic do have authored normal maps. The export script also clears shell normal links when assigning the reconstructed livery, but inspection does not support claiming that it deleted an available native shell normal. The reconstructed color atlas retains photographed highlights/shadows, which is a continuing limit compared with clean independently authored material channels.

Previous local shell: roughness .3, environment .8, clearcoat .9 / clearcoat roughness .14. Previous visor: bright #eab65d, roughness .22, normal strength .12, environment .8, environment yaw 1.7. Together these produced broad, flat golden reflection bands and soft shell highlights.

## Implemented material improvements

- `scripts/bake_helmet_surface_normals.py` uses a short background Blender/Cycles bake of the existing shell into its current UVs. A .00012 bevel shader radius / 4 bevel samples produces a 2048×2048 tangent normal texture, `public/max/materials/shell-surface-normal.png`. It derives edge finish from existing geometry; it does not transfer Norris UVs, invent sponsor relief, rebuild geometry or rebake the livery. Blender exits automatically.
- Shell: metalness .04, roughness .22, environment 1.25, specular intensity .85, clearcoat 1, clearcoat roughness .065; bevel normal strength .55. White paint remains dielectric rather than imitating the source's chrome material.
- Visor: darker gold #9f7a46 for 2023, roughness .085, environment 1.15, existing authored normal strength .35, environment yaw 0. Clearcoat .65 / .055 and reduced 2023 iridescence .12 sharpen the curved reflected studio lights without retaining a uniformly bright gold sheet. 2024 retains an independently tinted rose visor.
- Plastic: preserved authored UV/detail maps; roughness .24 and environment 1.05.
- The homepage's offscreen materials apply a filmic highlight-compression curve before final compositing, limiting blown-out white paint. Independent edition pages retain their existing renderer ACES path, without double applying this curve.
- Both independent edition pages load the same correctly mapped shell normal. The separate source-fit comparison keeps its own geometry/normal UVs.

Normal attribution, method and hash are recorded in assets-manifest.json and helmet-surface-normal.json. Source Maubian / CC BY 4.0 credit remains. Ordinary build and preview need no Blender.

## Verification and limits

Build, six JS syntax checks, new Python script parsing, and whitespace checks passed. Actual screenshots were viewed; state values alone were not used as visual acceptance.

- Desktop 1440×900 at DPR 2: default face, left/right pointer positions, real hover full reveal; portrait shifted upward/centered with a slightly smaller uniform scale. Helmet covers the head while neck, shoulders and upper body remain. Errors empty. Runtime confirms normal texture width 2048, source pointer .075, and identical solid/wire position, scale and rotation.
- Mobile 390×844 at DPR 2: default portrait and full helmet framing; no horizontal overflow, errors empty. Full reveal was invoked through the existing hero animation method for camera/geometry inspection, not claimed as a physical touch-device interaction test. Transient fluid-cursor reveal patches are expected when moving the test pointer.
- Both 2023 and 2024 independent pages: ready, errors empty, 2048px shell normal loaded; actual material screenshots inspected, including the separate rose visor on 2024.
- Evidence: /tmp/mv33-fit-norris-face.png, /tmp/mv33-fit-norris-helmet.png, /tmp/mv33-fit-norris-mobile.png, /tmp/mv33-fit-desktop-final.png, /tmp/mv33-fit-left.png, /tmp/mv33-fit-right.png, /tmp/mv33-fit-mobile-helmet-final.png, /tmp/mv33-material-edition.png.

The Max model and reconstructed photo atlas differ from Norris's authored asset, with remaining decal seams and baked lighting. This improves the current material response; it is not a claim of equal geometry/detail quality, an official scan or source-identical rendering. No source commit/push, knowledge-base update or public deployment.
