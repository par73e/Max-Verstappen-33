# Homepage helmet size — 2026-11-10

Sir requested a slightly larger helmet, referencing the Norris homepage. Checked the live reference hero DOM and `[data-gl-helmet="hover"]` trigger, then inspected the real full-helmet state in the reference and MV33 at the same 1470×812 viewport. The reference helmet occupies slightly more of the view.

Raised the default artist helmet scale uniformly by 5% in `scripts/helmet-scene.js` (from [7.2, 6.6, 7.1] to [7.56, 6.93, 7.455]). The solid model and wireframe still share position, scale and rotation; source-fit comparison remains unchanged. Build and syntax/whitespace checks pass. Desktop full reveal and 390×844 emulated mobile full reveal were inspected; mobile reveal was invoked via the existing scene method, not a physical-device interaction. Runtime errors were empty and there was no horizontal page overflow. The mobile composition fills the narrow viewport and clips the helmet's extreme sides, as the previous composition already did; the enlargement makes that crop slightly stronger. No claim of exact source geometry or user acceptance.

## Second adjustment

Sir felt the first increase was still too small. The desktop artist helmet scale is now [8.064, 7.392, 7.952], roughly 6.7% larger than the prior adjustment; the narrow layout retains the earlier scale because it already fills and crops against the screen edges. Scale is reapplied on viewport resize, and the wireframe follows the solid helmet. Desktop 1470×812 and emulated 390×844 full reveals were inspected; mobile reveal was invoked through the scene method. Runtime errors were empty, and mobile page width remained 390 px. The desktop helmet crown reaches behind the top MV mark, as a visual tradeoff of the larger presentation; user acceptance remains pending.
