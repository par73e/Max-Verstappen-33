---
name: MV33
description: A source-pinned Max Verstappen adaptation of the Lando Norris / OFF+BRAND homepage.
colors:
  lime: "#d2ff00"
  lime-off: "#b2c73a"
  dark-green: "#282c20"
  white: "#f4f4ed"
  black: "#111112"
  green-off-white-1: "#dde1d2"
  green-off-white-2: "#b4b8a5"
  dark-green-tint-2: "#535450"
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
    backgroundColor: "{colors.lime}"
    textColor: "{colors.dark-green}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "0 1rem"
    height: "3rem"
  button-nav:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.dark-green}"
    rounded: "{rounded.button}"
    padding: "0 1rem"
    height: "3.75rem"
  button-tertiary:
    backgroundColor: "transparent"
    rounded: "{rounded.tertiary}"
    height: "2.5rem"
    padding: "0 1rem"
  panel-close:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.dark-green}"
    rounded: "{rounded.panel-close}"
    width: "60px"
    height: "60px"
  menu-link:
    textColor: "{colors.green-off-white-1}"
  menu-link-hover:
    textColor: "{colors.lime-off}"
  panel-link:
    textColor: "{colors.lime}"
---

# Design System: MV33

## Overview

**Creative North Star: "The Source-Pinned Racing Stage"**

The visual authority is the Lando Norris / OFF+BRAND homepage, adapted to Max Verstappen for a personal, noncommercial frontend exercise. Preserve its cinematic scroll rhythm, oversized mixed type, lime-and-olive palette, photographic scale and animated controls. This is a description of the implemented system, not permission to invent a new Max identity.

English carries the large compositions; Chinese supports comprehension beneath them. The current WebGL helmet retains the reference mesh with projected Max photography; portrait depth/normals are approximations; the signature is a raster reveal rather than a reconstructed vector stroke animation. Sixteen helmet positions show multiple views of three designs, not sixteen unique designs. These limits preclude claims of complete fidelity.

**Key Characteristics:**
- Full-viewport scenes and scroll-driven transformations.
- Compressed uppercase Mona Sans paired with expressive Brier.
- Acid lime controls against warm olive and chalk surfaces.
- Large photography, clipped reveals and restrained bilingual support.

## Colors

Retain the reference palette even when the subject changes. Frontmatter values are normative DOM tokens; scene-specific WebGL colors remain owned by the engine.

### Primary

- **Acid Lime** (`lime`): primary controls, reveal masks, selection and keyboard focus.
- **Muted Racing Lime** (`lime-off`): selected words, menu hover and secondary scene accents.

### Neutral

- **Deep Olive** (`dark-green`): base canvas, menu and Max content panels; dark lettering on lime.
- **Warm Chalk** (`white`): light surfaces and text on dark scenes.
- **Near Black** (`black`): helmet detail image beds and darkest content regions.
- **Pale Olive Chalk** (`green-off-white-1`): menu lettering and light identity marks.
- **Muted Olive Chalk** (`green-off-white-2`): quieter labels and current menu state.
- **Olive Grey** (`dark-green-tint-2`): helmet framing and secondary dark text.

**The Reference Palette Rule.** Subject replacement must not introduce a new team-color theme or recolor reference controls.

## Typography

**Display Font:** Mona Sans Variable paired with Brier (local WOFF2 files; Arial/sans-serif fallback in reference CSS). **Body Font:** Mona Sans Variable. **Chinese Font:** system-ui/sans-serif.

Use the frontmatter hierarchy as role definitions, not a universal ratio. Display and headline text is uppercase; Brier replaces selected words within the same large composition. Small eyebrows use Mona Sans at (.625rem), line-height (1), variation settings (wght 700, wdth 100). Primary button labels use the label role; nav labels are (1.25rem) on desktop. Chinese support is a separate block with a top margin (1em); it grows to (.8em) at the adapter's mobile breakpoint. Heading translations use (13px), line-height (1.5), tracking (.12em), and top spacing (12px).

**The English Composition Rule.** Keep Chinese explanatory copy subordinate to the English display; do not force long translations into the original display line boxes.

## Layout

The embedded CSS in `public/index.html` scales the root font against a design width of (1728), with a desktop unit (16) and container clamp (992–1920px). At widths up to (991px), it uses unit (20) and clamp (768–991px); up to (767px), clamp (480–767px); up to (479px), unit (48) and clamp (320–479px). A rem is therefore not a fixed 16px. Preserve this mechanism before adjusting individual sizes.

The reference main grid has four columns of (23.55%) with the gap token; helmet tiles use four equal columns and near-square aspect ratio (406.89 / 411). General desktop container padding matches the gap; narrow portrait containers use (1rem). Preserve the original section-specific responsive rules and viewport-height scenes rather than replacing them with a generic card grid.

Max panels are fixed, scrollable overlays at z-index (1000), padded (100px max(25px, 6vw) 70px). Their media grid has three columns and gaps (24px), changing at (767px) to two columns with gaps (15px) and panel padding (100px 20px 40px). Panel prose has a maximum width (65ch), with type (17px / 1.8).

## Elevation & Depth

The visible language relies on photographic layering, WebGL lighting, clipping, scale and scene color changes rather than a reusable card-shadow scale. Do not promote unused Webflow reset shadows into design tokens. Menus overlay the page; panels sit above navigation. The engine's head reveal lasts (1.1s), with wireframe, distortion and pointer response; track transitions last (2s). The panel enters over (.55s) with `cubic-bezier(.16,1,.3,1)` and a vertical shift (40px). Only that panel animation has an explicit reduced-motion override in the adapter; this does not imply that the whole engine disables motion.

## Shapes

Keep compact rounded rectangular controls, larger curved scene masks and elliptical wipes. Use the extracted button and surface radii by role rather than making every surface a pill. Helmet frames retain their SVG silhouette and near-square footprint; photographs fill their original scene slots. Max panel close controls shrink to (50px) square on mobile while keeping their radius.

## Components

- **Primary and nav buttons:** lime fill, olive text, thin lime border; primary and nav heights differ. Preserve split-character text movement and original Rive arrow/menu behavior. The sidecar offers isolated appearance previews, not a replacement animation engine.
- **Tertiary control:** transparent background, current-color border and smaller height; inherits surrounding scene color.
- **Navigation:** fixed brand/center identity/store/menu arrangement, with scene-driven light/dark identity changes. Expanded menu fills the viewport with clipped reveals, photographic columns and large links; current links are muted and inactive, hover links use muted lime.
- **Helmet tile:** near-square outlined display frame, layered reveal and clickable detail entry. Preserve image containment; runtime background removal may leave edge artifacts.
- **Max content panel:** dark overlay with lime links/close control, large uppercase title and bilingual body. On/off-track and race entries currently open panels, not recreated subpages.

Sidecar component previews use inline SVG and scoped CSS, and omit photographic assets/runtime canvases. The loaded site has no user-facing form input component to document.

## Do's and Don'ts

### Do:

- Do compare changes at the same viewport and scroll position as the reference.
- Do preserve original DOM hooks, Rive controls, fluid sizing and scene rhythm.
- Do keep English display copy prominent and Chinese support readable.
- Do keep fidelity limits explicit when describing the result.

### Don't:

- Don't replace the pinned layout or button system with a newly invented sports theme.
- Don't describe the helmet mesh, portrait depth or raster signature as authentic Max 3D/vector reconstructions.
- Don't present sixteen helmet views as sixteen distinct designs or sample race data as live scheduling.

Source audit: `PRODUCT.md`, `README.md`, `public/reference/lando-offbrand.shared.6e09a725a.css`, embedded styles and markup in `public/index.html`, `public/mv33.css`, and scene configuration in `public/engine.js`. This documentation pass extracts source facts; it does not add a new browser or cross-device fidelity claim.
