---
name: MV33
description: A source-pinned Max Verstappen adaptation of the Lando Norris / OFF+BRAND homepage.
colors:
  racing-orange: "#ef6b19"
  soft-orange: "#f2a268"
  orange-ink: "#b84310"
  midnight-navy: "#101b30"
  raised-navy: "#1a2a44"
  cool-paper: "#f4f6fa"
  paper-shade: "#e4eaf2"
  near-black: "#080e19"
  text-soft: "#d8e1ed"
  text-muted: "#a6b6cb"
  slate-blue: "#5c718e"
  gallery-ink: "#344865"
  entry-midnight: "#101823"
typography:
  display:
    fontFamily: "Mona Sans Variable, Arial, sans-serif"
    fontSize: "7.9375rem"
    lineHeight: 0.906
    letterSpacing: "-0.0625rem"
    fontVariation: "'wght' 660, 'wdth' 93"
  display-brier:
    fontFamily: "Brier, Arial, sans-serif"
    fontSize: "8.25rem"
    fontWeight: 700
    lineHeight: 0.83
    letterSpacing: "-0.1875rem"
  headline:
    fontFamily: "Mona Sans Variable, Arial, sans-serif"
    fontSize: "4.5rem"
    lineHeight: 0.886
    letterSpacing: "-0.125rem"
    fontVariation: "'wght' 750, 'wdth' 93"
  body:
    fontFamily: "Mona Sans Variable, Arial, sans-serif"
    fontSize: "1.25rem"
    lineHeight: 1.25
    letterSpacing: "-0.0125rem"
    fontVariation: "'wght' 500, 'wdth' 100"
  label:
    fontFamily: "Mona Sans Variable, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 800
    lineHeight: 1
    fontVariation: "'wdth' 86"
  chinese:
    fontFamily: "system-ui, sans-serif"
    fontSize: "0.72em"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "0.04em"
rounded:
  button: "0.54rem"
  tertiary: "0.411875rem"
  small: "1rem"
  med: "3rem"
  large: "6.25rem"
  panel-close: "10px"
spacing:
  gap: "1.25rem"
  mini: "1rem"
  small: "2rem"
  med: "3rem"
  large: "4rem"
  xlarge: "5rem"
components:
  button-primary:
    backgroundColor: "{colors.racing-orange}"
    textColor: "{colors.midnight-navy}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "0 1rem"
    height: "3rem"
  button-nav:
    backgroundColor: "{colors.racing-orange}"
    textColor: "{colors.midnight-navy}"
    rounded: "{rounded.button}"
    padding: "0 1rem"
    height: "3.75rem"
  button-tertiary:
    backgroundColor: "transparent"
    rounded: "{rounded.tertiary}"
    height: "2.5rem"
    padding: "0 1rem"
  panel-close:
    backgroundColor: "{colors.racing-orange}"
    textColor: "{colors.midnight-navy}"
    rounded: "{rounded.panel-close}"
    width: "60px"
    height: "60px"
  menu-link:
    textColor: "{colors.text-soft}"
  menu-link-hover:
    textColor: "{colors.soft-orange}"
  panel-link:
    textColor: "{colors.soft-orange}"
  edition-link:
    textColor: "{colors.orange-ink}"
    rounded: "8px"
    padding: "12px 18px"
  gallery-caption:
    textColor: "{colors.gallery-ink}"
---

# Design System: MV33

## Overview

**Creative North Star: "The Source-Pinned Racing Stage"**

The visual authority is the Lando Norris / OFF+BRAND homepage, adapted to Max Verstappen for a personal, noncommercial frontend exercise. Preserve its cinematic scroll rhythm, oversized mixed type, navy-and-orange palette, photographic scale and animated controls. This is a description of the implemented system, not permission to invent a new Max identity.

English carries the large compositions; Chinese supports comprehension beneath them. The hero uses the credited Maubian geometry with source-derived 2023 SVG paint separations baked to a lossless 4096px atlas; original hardware maps and tightly clipped photographic vents/latch remain separate from physical reflections. Solid and wireframe share geometry and transforms. The 2024 edition retains photographic paint with the shared material finish; portrait depth/normals are approximations; the signature is an orange traced-SVG reveal rather than a reconstructed stroke-by-stroke animation. Sixteen helmet positions show multiple views of three designs, not sixteen unique designs. The portrait uses studio-source RGB with an extracted alpha, inferred depth and derived normals packed at 4096px; packing size is not native source-photo resolution. These limits preclude claims of complete fidelity.

**Key Characteristics:**

- Full-viewport scenes and scroll-driven transformations.
- Compressed uppercase Mona Sans paired with expressive Brier.
- Orange controls against midnight navy, cool white and blue-grey surfaces.
- Large photography, clipped reveals and restrained bilingual support.

## Colors

Sir approved a global navy/orange identity on 2026-11-10. Preserve the reference structure and motion, while adapting colors by their role. Frontmatter values are normative DOM tokens; scene-specific WebGL colors remain owned by the engine.

### Primary

- **Racing Orange** (`racing-orange`): primary controls, reveal masks, identity marks, selection and keyboard focus.
- **Soft Orange** (`soft-orange`): selected words, menu hover and links on navy panels, menus and footers.
- **Orange Ink** (`orange-ink`): small edition links and active edition controls on paper.

### Neutral

- **Midnight Navy** (`midnight-navy`): base canvas, expanded menu and Max content panels; dark lettering on orange.
- **Raised Navy** (`raised-navy`): the inherited first dark-surface tint and tonal layering.
- **Cool Paper** (`cool-paper`): light surfaces and text on dark scenes.
- **Paper Shade** (`paper-shade`): pale scene fields and large edition-year lettering.
- **Near Black** (`near-black`): helmet detail image beds and darkest content regions.
- **Soft Blue Grey** (`text-soft`): menu lettering and light identity marks.
- **Muted Blue Grey** (`text-muted`): quiet labels on navy, credits and the current menu state.
- **Slate Blue** (`slate-blue`): helmet framing, dividers and secondary dark text.
- **Gallery Ink** (`gallery-ink`): homepage gallery captions on the light field; also edition control lettering and footer dividers.
- **Entry Midnight** (`entry-midnight`): the deeper fullscreen entry/loading field.

**The Identity Color Rule.** Navy carries dark scenes; orange carries primary actions and marks. Soft orange accents navy; orange ink carries small links on paper. Light scenes use cool paper and blue-grey neutrals. Preserve source CSS names as compatibility hooks, while naming the visual roles above. Apply the same roles to DOM, scene colors and derived identity SVGs; the embedded Rive canvases receive a bounded output palette filter without changing their animation. Photography and authentic helmet paint retain their source colors.

**The Caption Context Rule.** Use gallery ink for captions on light gallery fields; reserve muted blue grey for quiet copy on navy. A shared inherited text class does not override its actual background context.

## Typography

**Display Font:** Mona Sans Variable paired with Brier (local WOFF2 files; Arial/sans-serif fallback in reference CSS). **Body Font:** Mona Sans Variable. **Chinese Font:** system-ui/sans-serif.

Use the frontmatter hierarchy as role definitions, not a universal ratio. Display and headline text is uppercase; Brier replaces selected words within the same large composition. The user-pinned small source labels use Mona Sans at (.625rem), line-height (1), variation settings (wght 700, wdth 100). Primary button labels use the label role; nav labels are (1.25rem) on desktop. Chinese support is a separate block with a top margin (1em); it grows to (.8em) at the adapter's mobile breakpoint. Heading translations use (13px), line-height (1.5), tracking (.12em), and top spacing (12px).

**The English Composition Rule.** Keep Chinese explanatory copy subordinate to the English display; do not force long translations into the original display line boxes.

## Layout

The embedded CSS in `public/index.html` scales the root font against a design width of (1728), with a desktop unit (16) and container clamp (992–1920px). At widths up to (991px), it uses unit (20) and clamp (768–991px); up to (767px), clamp (480–767px); up to (479px), unit (48) and clamp (320–479px). A rem is therefore not a fixed 16px. Preserve this mechanism before adjusting individual sizes.

The reference main grid has four columns of (23.55%) with the gap token; helmet tiles use four equal columns and near-square aspect ratio (406.89 / 411). General desktop container padding matches the gap; narrow portrait containers use (1rem). Preserve the original section-specific responsive rules and viewport-height scenes rather than replacing them with a generic card grid.

Max panels are fixed, scrollable overlays at z-index (1000), padded (100px max(25px, 6vw) 70px). Their media grid has three columns and gaps (24px), changing at (767px) to two columns with gaps (15px) and panel padding (100px 20px 40px). Panel prose has a maximum width (65ch), with type (17px / 1.8).

## Elevation & Depth

The visible language relies on photographic layering, WebGL lighting, clipping, scale and scene color changes rather than a reusable card-shadow scale. Do not promote unused Webflow reset shadows into design tokens. Menus overlay the page; panels sit above navigation. The engine's head reveal lasts (1.1s), with wireframe, distortion and pointer response; track transitions last (2s). The panel enters over (.55s) with `cubic-bezier(.16,1,.3,1)` and a vertical shift (40px). The adapter disables panel entrance and identity-logo transitions for reduced motion; edition pages disable CSS animation/transitions and smooth scrolling. These scoped overrides do not imply that the whole homepage engine disables motion.

## Shapes

Keep compact rounded rectangular controls, larger curved scene masks and elliptical wipes. Use the extracted button and surface radii by role rather than making every surface a pill. Helmet frames retain their SVG silhouette and near-square footprint; photographs fill their original scene slots. Max panel close controls shrink to (50px) square on mobile while keeping their radius.

## Components

- **MV loading mark:** native orange SVG assembly on entry midnight, with a (.72s) three-piece entrance, staggered (.04s / .20s), followed by a (1.8s) opacity breath while loading. The mounted sequence has a (1050ms) minimum assembly window before its (.85s) silhouette reveal; actual asset readiness still controls exit. Reduced motion removes assembly/breath and uses a (180ms) fade. Preserve the same source transition lifecycle release pointer input and pause the hidden SVG animations on completion.
- **Primary and nav buttons:** orange fill, navy text, thin orange border; primary and nav heights differ (the inherited mobile nav variant grows to 4.7rem). Preserve split-character text movement and original Rive arrow/menu behavior. The sidecar offers isolated appearance previews, not a replacement animation engine.
- **Tertiary control:** transparent background, current-color border and smaller height; inherits surrounding scene color.
- **Navigation:** fixed brand/center identity/menu arrangement (shopping controls removed), with scene-driven light/dark identity changes. Expanded menu fills the viewport with clipped reveals, photographic columns and large links; current links are muted and inactive, hover links use soft orange.
- **Helmet tile:** near-square outlined display frame, layered reveal and clickable detail entry. Preserve image containment; runtime background removal may leave edge artifacts.
- **Max content panel:** navy overlay with soft-orange links and an orange close control (soft orange on hover), large uppercase title and bilingual body. On/off-track and race entries currently open panels, not recreated subpages.
- **Edition links:** outlined compact rectangles (8px radius), padding (12px 18px), system-ui text (700 13px / 1.3); orange ink on paper and soft orange in menu/footer contexts. Hover fills orange with navy ink. Footer links stack with an (8px) gap, use (11px) text and (10px 12px) padding; hide below (767px) to preserve the helmet lane.
- **Helmet edition pages:** `/helmets/season-2023/` and `/helmets/zandvoort-2024/` present one 3D model on cool paper, an edition title and pale year, camera/line-mode controls, source photography and a next-edition link. The same Mona/Brier pairing remains. Desktop title is (clamp(60px, 7vw, 132px)), weight (780), line-height (.91); the first line uses Brier. At (900px) the title becomes (65px), story becomes one column, and controls span the viewport; at (480px), the photo gallery becomes one column. Hardware, livery alignment and shape remain approximate reconstructions, not official scans or UV masters.

Sidecar component previews use inline SVG and scoped CSS, and omit photographic assets/runtime canvases. The loaded site has no user-facing form input component to document.

## Do's and Don'ts

### Do:

- Do compare changes at the same viewport and scroll position as the reference.
- Do preserve original DOM hooks, Rive controls, fluid sizing and scene rhythm.
- Do keep English display copy prominent and Chinese support readable.
- Do keep fidelity limits explicit when describing the result.
- Do judge small-text colors against the actual scene field and retain the pinned original source labels.

### Don't:

- Don't replace the pinned layout or button system with a newly invented sports theme.
- Don't describe the reconstructed helmet paint as an official UV master or scan, inferred portrait depth as measured depth, or the traced signature reveal as authentic stroke reconstruction.
- Don't present sixteen helmet views as sixteen distinct designs or sample race data as live scheduling.

Source audit: `PRODUCT.md`, `.impeccable/surfaces/navy-orange.md`, `theme/palette.json`, `public/theme.css` (both root and body scope), `public/reference/lando-offbrand.shared.6e09a725a.css`, embedded styles and markup in `public/index.html`, `public/mv33.css`, `public/helmet-page.css`, `public/helmet-materials.js`, and `scripts/helmet-scene.js`. This documentation pass extracts source facts; it does not add a new browser or cross-device fidelity claim.
