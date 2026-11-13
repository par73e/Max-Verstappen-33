# Four requested fixes · 2026-11-13

## Scope

Recovered the two interrupted requests and two queued requests from mv5. The supplied screenshots identify the archive's missing home entry, the fullscreen RB20 launch photograph, and the Orange Tribute hover image. The text-only request covers the expanding 3 transition and repeated photography. Existing uncommitted full-site work is retained. No deployment or Git publication was performed.

## Navigation

The archive used `data-nav-theme-target="dark"` on a navy surface, making the wordmark and hamburger inks effectively disappear. Its theme now requests light navigation inks and the existing paper hamburger backplate. A visible bilingual Home link precedes the archive heading. Clicking it was verified to return to `/` through the shared transition.

## Page-out transition

Read the live reference DOM and the current script at https://lando.itsoffbrand.io/dev-js/lando-by-OFF+BRAND.05.js through an isolated ego task Space. `.transition-w canvas[data-rive-primary]` owns `page-transition.riv`; `BL`, `EL`, `H$` connect the initial, transition-out and transition-in inputs. The Rive instance reports ready, page-out, page-load-state and page-in animations. Sampling page-out at 0.2, 0.3, 0.4 and 0.5 seconds showed a filled 4 growing until its shape covers the page.

The local 3 was an outlined SVG with a separate background fade during its last 16%. It now uses a solid shape and one continuous 500ms exponential expansion. The focal point moves into a solid part of its lower bowl. Scale is derived from the viewport diagonal so the shape itself fills all corners before the loading field replaces it. This is an SVG adaptation of the observed mechanism, not a reauthored copy of the Rive file. The existing MV loading/reveal lifecycle is retained. Reduced motion hides the numeral and fades the field over 120ms.

## Photography

- Replaced the screenshot's fullscreen standing portrait with a different seated RB20 launch photograph, SI202402140471, credited to Will Cornelius / Red Bull Content Pool. Source: https://f1i.com/news/499603-launch-gallery-red-bull-racing-rb20.html . Original download: https://f1i.com/wp-content/uploads/2024/02/SI202402140471.jpg . JPEG retained in `assets/source/fullscreen/`; 3840×2561 WebP is used on the site. Encoding only; no AI generation, repainting or upscaling.
- Homepage photography now has 23 distinct editorial images in its narrative sections. Known alternate exports of the same shot are not assigned to separate visible sections.
- Added ten real photographs from official Verstappen news articles 6328, 6326, 6324, 6322 and 6320. Individual source URLs and image URLs are retained in `assets-manifest.json`; the images also appear in the asset library.
- Replaced the subpage modulo-10 image assignment with an allocation of unused images, excluding shared section images and known duplicate exports. On Track has 35 unique editorial images; Off Track and Racing Worlds each have 30. Counts are per rendered page's content, excluding the menu's paired blend layers, brand/flag/track artwork, and product reference views. Shared sections intentionally remain consistent across routes.
- Calendar's hidden empty CMS image placeholders use the MV emblem instead of allocating hundreds of repeated race photographs.

## Helmet photograph framing

Each real edition has explicit `wornPosition` metadata. Orange Tribute uses 100% horizontal alignment, centering its helmet/face rather than the source photograph's empty left area. Season 2023 uses 74%. Season 2024 and USA retain their near-central alignment. Original bitmap pixels are unchanged. The reveal window and photograph compensation retain synchronized reversible motion; crop position is separate from animation transforms.

## Verification

- `npm run build`, `npm run check`, `git diff --check` passed; all 13 HTML pages and internal assets were checked.
- Desktop at 1440×900: visually inspected the archive, Orange Tribute and Season 2023 open states, the new photo in its original scroll scene, and a sampled solid-3 frame. The final numeral covered all four viewport corners according to SVG point-in-fill checks. Actual Home click returned to the homepage.
- Archive at 390×844: inspected a fixed-width same-origin preview with the actual page and scripts; Home link was visible and 44px high, the two-column grid fit, horizontal overflow was zero. Native mobile emulation triggered reference resize/navigation behavior and screenshot timeouts, so this is a responsive iframe check, not physical-device or touch verification.
- Reduced motion: numeral hidden; cover completed in approximately 141ms in the sample, followed by complete reveal state.
- Browser evidence: `.impeccable/review/four-fixes-*.png`. These are ignored local review artifacts.
