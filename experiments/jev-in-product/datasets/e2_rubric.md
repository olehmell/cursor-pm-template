# E2 gold rubric (frozen before Jev runs)

**Product decision:** Before stakeholder review, is a PRD section **MVP-scoped**, and is each success metric **measurable** in the PetCare COMPANY/PRODUCT sense?

Labeler: single PM (Oleh) with this rubric; labels assigned offline before any Jev call. Date frozen: 2026-09-18.

Gold encoding: `1` = yes, `0` = no, `null` = question not applicable to this item (skip in metrics).

## mvp_scoped (noul → gold 1/0)

Ask: *Does this section define a tight MVP / V1 gate with clear product boundaries (in and/or out), not vision, risk fluff, or unbounded roadmap?*

| Gold | Include when… |
| --- | --- |
| `1` | Explicit in-scope / out-of-scope lists; named core value loop (e.g. upload→view); deferred features called out; hypothesis tied to a minimal prototype. |
| `0` | Vision / “universal hub” / multi-epic roadmap goals; risk/mitigation notes; resource/budget debates; feature laundry lists without cuts; success-story prose. |

**Tie-break:** Prefer `0` if the text expands scope or sells a quarter rather than gating a shippable slice. A short “out of V1” list alone → `1`.

**Skip (`null`):** Pure metric bullets with no scope claim.

## metric_measurable (noul → gold 1/0)

Ask: *Is this a success metric that is operationally measurable (named metric + who/what/when event definition), preferably with a target — matching COMPANY.md / PRODUCT.md metric style?*

| Gold | Include when… |
| --- | --- |
| `1` | Named metric + operational definition (numerator/denominator or event) and usually a target/baseline (e.g. Upload Completion Rate % who uploaded ≥1 doc in onboarding; Feature Adoption % who added ≥1 vaccination record; NPS with survey cadence). |
| `0` | Vague vibes (“no major issues”, “must-have in surveys”, “fewer support complaints”) without event definition; open-ended qualitative questions; expected impact tables with only %-deltas and no measurement method; “user happiness” without instrument. |

**Company metric context (frozen into Jev state):** Activation = completes feeding setup within 7 days; North Star ≈ weekly active households with updated stock or confirmed refill; health metrics include retention, notification opt-in/open, reorder CTA CTR. Prefer labels that would survive a metrics review against that bar.

**Skip (`null`):** Scope / risk / process sections that are not claiming a metric.

## Item unit

PRD section, scope block, or metric bullet from `usecases/02-prd-writing/artifacts/` (+ synthetic only if needed, marked `synthetic: true`). Prefer verbatim Ukrainian/English from artifacts; light compression OK if meaning preserved.
