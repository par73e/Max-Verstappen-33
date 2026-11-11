# GPU budget correction — 2026-11-10

Sir reported excessive GPU load after the fit/material improvements. Read-only macOS AGX counters measured Device/Renderer Utilization at 95%, later 70% and 76%, with recoveryCount 0. These are whole-system readings, not per-tab GPU attribution. Chrome's GPU helper, other browser renderers, WindowServer and other workloads were active; CPU process percentages were not presented as GPU percentages. No unrelated app/process was stopped.

## Source findings

Reviewed owning code first: retained reference/lando-engine.js RQ.update is registered on the GSAP ticker without a frame budget or a document.hidden guard; all active scene/renderer work runs each tick. The project had raised desktop DPR from the source 1.25 to 2 and allocated a full-size DPR-scaled, 4x-MSAA helmet target. Clearcoat/normal/iridescence shading adds cost per pixel. Stable shader program counts in testing do not indicate continuous recompilation.

## Changes

- public/render-budget.js is loaded before the engine. It caps WebGL submissions at 60 FPS while interacting/loading, and 30 FPS after 1.8 seconds without input. Hidden documents submit no WebGL work. The renderer receives the actual accepted frame delta, preserving pointer easing as the submission rate changes. GSAP UI/scroll timelines are not globally throttled.
- Full-screen pixel ratio: min(devicePixelRatio, desktop 1.5 / mobile 2, sqrt(3,000,000/(width×height))). Original image assets, photographic texture packing and DOM/SVG resolution are unchanged.
- Helmet target independently caps DPR at 1.25 and area at 2,000,000 pixels; samples are 2 rather than 4. Resizing uses the same calculation. This changes framebuffer cost, not model scale, camera fit or physical material parameters.
- Independent edition pages use DPR at most 1.5 and redraw only when OrbitControls/resize/entrance/view/wireframe state changes. Their existing hidden/out-of-view guards remain.
- Ordinary check now includes syntax validation of render-budget.js. Existing tabs require reloading to run this code.

## Verification

Build, seven JS syntax checks and git diff --check passed. One task-owned preview was used, then closed; no extra live reference page was opened during the GPU investigation.

At a 1470×812 desktop viewport / Retina display:

- Main DPR 1.5; helmet buffer 1838×1015 with 2 samples. The prior DPR-2 / 4-sample helmet allocation at that viewport uses about 80% fewer MSAA samples in the new buffer (about 3.73 million versus 19.10 million MSAA samples per render). This is a framebuffer comparison, not an 80% claim about total machine GPU utilization.
- Idle sample: 22 accepted scene frames over roughly one second, under the 30 FPS ceiling on this busy machine. Shader programs stayed 19 → 19; errors empty.
- Ego's managed pages remained document.hidden=false when opening a blank tab, so that attempt did not establish an actual background-tab test. A temporary synthetic document.hidden=true integration check instead measured zero accepted scene frames and zero renderer calls over one second; the override was removed immediately. Real Chrome background-tab behavior is not claimed as directly tested.
- Actual full-helmet screenshot inspected after the budget change; framing/materials retained. Evidence: /tmp/mv33-gpu-final-helmet.png.
- Independent 2023 page: zero renderer submissions during a one-second idle sample after its entrance. Right-view rotation and wireframe switch redraw correctly; errors empty. Evidence: /tmp/mv33-gpu-demand-render.png.

No controlled whole-system before/after reduction is claimed: other workloads varied, and the user's existing Chrome page was not refreshed or taken over. No commit, push, deployment or knowledge-base update.

## Follow-up comparison after Sir's clarification

Sir clarified that opening the original Norris homepage also showed roughly 80% GPU use, and asked for comparison before treating this as an abnormal background workload. No further source/quality/frame-budget changes were made in this follow-up.

Used one task-owned ego lite tab sequentially, with the same 1440×900 viewport and DPR-2 display, waiting for each entry to complete. No second heavy reference page was opened alongside it. Short observations:

| Metric | MV33 | Live Norris |
| --- | --- | --- |
| Three successive whole-system GPU readings | 58%, 64%, 70% | 60%, 61%, 64% |
| Drawing buffer | 2160×1350 | 1800×1125 |
| GL draw submissions / second | about 507 | about 567 |
| requestAnimationFrame interval p95 | 49.1 ms | 50 ms |
| RAF intervals over 50 ms in ~1.5s | 2 | 1 |

MV33's accepted scene-render sample was about 23 FPS while idle; the RAF interval measurement above is browser scheduling, not an exact GPU frame-time measurement. GL draw counts were measured with temporary wrappers around draw calls, restored immediately. System GPU counters include other applications, and the two sites use different default render resolutions and material/geometry pipelines; these are short practical comparisons, not an isolated performance benchmark or per-tab GPU attribution.

The two sites fell within similar load/scheduling ranges in this sample. This supports Sir's observation that continuous foreground WebGL effects themselves can cause substantial utilization, rather than demonstrating a MV33-specific runaway background workload. The earlier renderer guards remain; quality was not reduced further. The comparison tab/Space was closed afterward. Evidence that the original page had completed entry: /tmp/mv33-gpu-compare-norris.png.

## Subsequent lettering repair · same day

The earlier2Mpx/DPR1.25 helmet-only cap above is historical. The lettering repair raises that target to DPR2/5Mpx/2samples and reuses it when the pose/camera/texture revision is unchanged. Main3Mpx/DPR1.5 and60active/30idle caps remain. The old allocation comparison must not be used as a measurement of the updated helmet target. See `navy-orange-and-clean-helmet-2026-11-10.md`.
