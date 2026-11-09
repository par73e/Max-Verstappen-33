# Source-first corrections - 2026-11-09

The live original bundle still hashes to 6ad2c0d7ab90feeebfc79568a85614242ce8d481cd563efbcd7259fec2a3fa17, identical to reference/lando-engine.js. Acquired through ego after direct HTTP returned 403. Source inspection preceded visual validation.

## Entry sequence

Original BL() loads page-transition.riv and its initial / transition-in / transition-out state-machine inputs. H$ starts transition-in and hides its overlay after 500 ms. The previous adaptation hid that Rive canvas and overlaid a static MV image, preserving the callbacks but losing the animated cutout. Separately, the signature adapter defaulted missing scroll input to progress 1, making a raster signature appear before its Rive state was ready.

intro.js now implements an MV SVG cutout zoom through the original BL / EL / H$ lifecycle. It does not claim to be a modified Rive animation. The loading logo is a sharp vector; the zoom mask reveals the initialized scene. Signature scroll progress defaults to zero until its actual input is available. Reduced-motion duration is shorter. The original header/menu Rive files remain active.

## Head and helmet registration

Reference model bounds: width about .07335, height .07707. Supplied model bounds: width .06770, height .077. Reusing [6.9,6.9,7.1] scales made the new mesh relatively narrow/long. Hero scale is now [7.2,6.25,6.9]. Wireframe copies all three transforms; the source perspective camera remains at z=3 desktop and z=3.75 mobile. Standalone model/wire groups use the corresponding fit ratios.

The portrait texture retains scale 2.6 and x=-606; y shifts from 155 to 280 in a 2048-square plane. This registers the face/eye/chin region against the source's head-plane/visor relationship while preserving shoulders and upper body. Depth bulge centre follows the texture shift. The final fit is checked in the rendered source camera, not by centring an independent DOM image.

## Materials

Original F9 separates shell, glass and plastic and uses an HDR environment with physical materials. The final pipeline reconstructs only the painted shell at 4096px. Glass and plastic retain the artist's authored UVs and normal detail. The ORACLE strip is part of the plastic mesh: projecting it onto glass as well created a duplicate, displaced band. The visor now uses an opaque coated-metal material without photo reflections. `depthWrite` is explicitly restored when converting the original transparent material to opaque, preventing the rear shell from being drawn through the visor. Hardware keeps its matching source textures.

The front shell's forehead projection is registered independently above the authored band. View weights use exponent 64 and a small front preference of 4 rather than 1000, shortening the overlap that created duplicate side decals. Horizontal confidence is normalized separately for the 2023 crown, with a finite weight floor to avoid numerical underflow/black patches. The Orange Tribute top photograph has its front at the top of the image: its projection up vector is (0,-1,0), correcting the previously reversed crown. These are reconstructed liveries, with geometry/detail differences from an official scan.

Unused source visor color/metalness images are removed on export. The final GLBs are around 3 MB each, with the detailed source normal maps retained.

## Validation scope

Loading vector logo and the intermediate MV-shaped cutout were visually captured. The completed desktop scene has signature scroll opacity zero at the top, matching model/wire scales and rotation, and no recorded runtime errors. Mobile 390x844 was checked through the source hoverAnimation state for fit; this is not a physical-phone gesture test. Standalone route loaded the shared material helper successfully.
