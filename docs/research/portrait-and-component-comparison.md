# Portrait and original-component comparison — 2026-11-09

## Source diagnosis and implemented correction

The preserved front photograph is 1920x1920; the earlier AI-assisted extraction is 1254x1254. The old runtime enlarged the latter 2.6x as its RGB source. It also multiplied a displacement depth field by the cutout alpha, introducing a depth cliff at the silhouette on the source 128x128-subdivision plane. The shoulder edge was therefore both resampled and geometrically deformed.

The runtime now draws original photographic RGB and uses the extraction only for opacity, retaining the original photo untouched. The depth field is smooth across the silhouette and localised around the head; shoulders stay nearly planar. The horizontal texture offset changes from -606 to -640, registering the face centre against the model rather than moving the whole helmet away from the camera axis. No invented facial detail or generated replacement portrait is used. Native photographic detail still limits close-up resolution.

The Max model fit changes from [7.2, 6.25, 6.9] to [7.2, 6.6, 7.1]. Its frontal width/height is now approximately .96, close to the source helmet's .95. The prior y compression made it unusually squat. Model and generated wireframe continue to share transforms. Edition page fit ratios follow the same correction.

## Original component feasibility

The retained Draco GLB was decoded by Blender. An alternate asset retains the original helmet/glass/plastic geometry, original UVs and source normal maps, repainting the shell and printed visor regions with Max photographic material. Its hero uses the original [6.9, 6.9, 7.1] scale and transparent matcap fittings. It is available at `/?helmet=source`; the default retains the authored Max geometry.

This is a usable comparison, not a faithful conversion of one helmet shape into another. Vent layout, visor bounds and transparent fittings differ; rebaking artwork cannot change those physical differences, and some photographic details still conflict with source geometry. That is why the reference geometry has not replaced the default. The reference and Maubian source assets remain intact; only the alternate asset derives from the reference, so it must not be attributed to Maubian.

## Validation

Both homepage variants rendered in ego lite without recorded runtime errors. Desktop default portrait, full Max helmet and source-component helmet were visually inspected. The default was checked at 390x844, including full reveal; there was no horizontal overflow and model/wire scales matched. Original entry/hover lifecycle and torso retention remain. npm build/check, Python parsing and diff whitespace checks passed. Physical-phone and cross-browser results are not claimed.
