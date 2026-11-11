# MV loader animation and driver-content audit · 2026-11-10

## Authorized scope and direction

Sir requested a visible MV logo animation while refreshing/loading and a full adaptation of Norris-specific driver/team/championship text into accurate Verstappen information. This extends the existing source-pinned navy/orange surface.

- Visual thesis: restrained orange MV vector assembly on the existing midnight field.
- Content plan: driver identity → dated championship/debut history → track/off-track → actual racing ecosystem → archive/social/footer.
- Interaction thesis: assemble the native mark, hold with a restrained opacity pulse while assets load, then use its silhouette to reveal the homepage. Reduced motion uses a short fade.

## Source-first reference evidence

On 2026-11-10, inspected the live `https://landonorris.com/` DOM in a new ego task Space and fetched its current `https://lando.itsoffbrand.io/dev-js/lando-by-OFF+BRAND.05.js` through that page. The transition wrapper contains `.transition-rive canvas[data-rive-primary]` and a `Load Norris` fallback button. Its Rive file is `page-transition.riv`, artboard/state machine `page-transition`, inputs `initial`, `transition-out`, `transition-in`; runtime animation names are `ready`, `page-out`, `page-load-state`, `page-in`. The live `BL`/`EL`/`H$` lifecycle matches the retained implementation. The source hides transition interaction after page-in. The MV implementation keeps that lifecycle, using authored native SVG motion rather than claiming the Norris Rive has been reauthored.

## Loading implementation

`public/loader.css` is inlined into first-paint CSS by `scripts/build.py`; the loading poster animates before the full engine is mounted. `public/intro.js` assembles the same three native MV paths over .72s, staggered .04/.20s, followed by a subtle 1.8s opacity breath. No heavy raster/video asset or another WebGL scene is introduced.

The mounted mark receives a minimum1050ms assembly window even on cached refreshes. Actual asset readiness still owns reveal timing; no fake loading percentage is shown. The existing .85s MV-mask reveal follows. Completion hides the layer and releases pointer input. `cover` restarts animations and cancels pending reveal work; reduced motion disables assembly/breath and uses a180ms fade without zoom. Role/status and loading labels refer to Max.

## Factual sources, checked 2026-11-10

- Formula 1 driver profile: https://www.formula1.com/en/drivers/max-verstappen — Netherlands, Red Bull Racing, four championships and2021–2024 history. Current cumulative totals are intentionally omitted, since they change during the season.
- Oracle Red Bull Racing driver biography: https://www.redbullracing.com/int-en/drivers/max-verstappen/ — Toro Rosso debut in2015 aged17; Spanish GP win on Red Bull debut in2016; four consecutive titles through2024.
- Official Verstappen news: https://news.verstappen.com/en/article/6112/ — Team Redline renamed Verstappen Sim Racing on23March2026; part of the wider Verstappen Racing ecosystem, spanning GT and simulation.
- Retained photo provenance cross-check: https://news.verstappen.com/en/article/6348/ confirms São Paulo material from6November2026; source image URLs in `assets-manifest.json` separately identify São Paulo/Mexico City2026. Those dates are archive captions, not claims about the next race or a win.

## Changes by surface

- `content/max.json` centralizes verified driver facts, milestones, source URLs, copy and verification date. Biography panels link to those official sources.
- Rewrote the main statement and both gallery narrative passages around Max's four titles and2016 debut win; removed Norris's childhood/first-title promotional language and first-person quotation implication.
- On Track now describes Red Bull and2021–2024 titles; Off Track describes GT/sim racing. The discovery entry opens an actual Max biography with2015/2016/2021–2024 milestones.
- Replaced the former partners/campaigns framing with Racing / Beyond F1, without presenting Norris's sponsors as Max endorsements. Updated the formerly Team Redline marquee label to Verstappen Sim Racing.
- Changed the static Next Race card/navigation to Race Archive. It retains the source circuit drawing and links to an archive panel with the official calendar, rather than falsely asserting a current next event.
- Changed the inherited gallery result badge1 toMV; no unverified result is attached to the substituted photographs.
- Reworded the footer campaign line, kept the fan-made status explicit, corrected social image metadata to the serious portrait, and corrected `og:type` to `website`.
- Retained Norris/OFF+BRAND in the About panel as design-source attribution. Technical selectors, source filenames and provenance remain; they are not driver biography.
- Kept authentic2023/2024 helmet information, model credits and source photography. No current car-number claim is inferred from the project nameMV33 or historical helmet artwork.
- Fixed the visual-only hero canvas intercepting the biography entry; text sizing/placement remain and its click target is expanded with balanced padding/margin.

## Verification

`npm run build`, `npm run check` and the rendered-DOM audit pass. Visible static text and identity attributes contain no Norris/McLaren attribution; attribution remains only in the About panel. The biography, static metadata and built JSON agree on the four dated titles. Browser evidence, mobile/reduced-motion results and limitations are recorded below after final checks.

### Final browser evidence

- Task-owned ego Space11; desktop1440×900 and touch-emulated390×844. Live refresh observation recorded poster/loading/revealing/complete states and non-final SVG transform/opacity frames; no script/resource errors recorded.
- Captured actual SVG entrance poses at300ms and800ms through paused browser animations for visual inspection. The settled mark remains the native MV silhouette; the empty center aperture is not exposed during loading.
- The real pointer click on Discover Max opens the verified biography. Mobile On Track opens the same career milestones; waited for panel opacity1 before judging readability. Desktop/mobile document and panel horizontal overflow were0.
- Mobile footer and longer Race Archive navigation label fit the existing layout. Source touch lock was initialized normally.
- Reduced-motion cover/reveal completed in198ms during the sample, with0 active loading animations, unchanged reveal progress0 (no zoom), hidden completion state and pointer-events:none.
- Screenshots are review evidence under `/tmp/mv33-loader-assembly.png`, `/tmp/mv33-loader-settled.png`, `/tmp/mv33-career-mobile.png`, `/tmp/mv33-biography-footer-mobile.png` and related task captures. These are temporary local files, not published site assets.
- Physical-device, other-browser and sustained GPU measurements were not repeated for this SVG/content change. No site deployment, source commit or remote publication was requested/performed.
- Final completion also pauses the loading SVG animations, so the hidden breath does not continue running. The legacy Rive menu changes its accessible label to `Open menu` after closing; selector retries against the initial `Open navigation menu` label were test-locator failures, not runtime errors. Archive interaction was verified through the visible first-screen race card. The source's hidden partnerships CTA stays hidden; racing information is accessible via Off Track and the inline section copy.
