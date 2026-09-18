# Draft: Structured System-One judgments for PM product tasks (E3)

_Working draft — E3 results filled 2026-09-18. Companion to DRAFT-E1.md / DRAFT-E2.md._

## Abstract (E3 addendum)

We close the in-product Jev loop on **prototype critique**. On **N=21** PetID screen descriptions (8 flow screens from `usecases/03-prototyping/` + 13 synthetic controls), with gold frozen in `datasets/e3_rubric.md` *before* API calls, live `jev-latest` (`jev-1.13.0`) achieved **advances_hypothesis** accuracy **90.5%** (19/21; AUC 1.0; false-pass **0%**) and **cta_clarity** exact **86.7%** (13/15) / adjacent **100%**. Misses are false-negatives on degraded upload screens (competing Share/Upload; Skip-dominant layout) plus two medium↔low/high CTA swaps. Vs E1 severity (exact 34.3%), CTA score looks much more reliable on this set; vs E2 noul gates, advances_hypothesis is nearly as strong with safer false-pass profile for redesign triage.

## Method (E3)

1. **Product decision:** Does the screen advance the PetID upload hypothesis, and is the primary CTA clear?
2. **Hypothesis (in state):** Users want to store pet medical documents via photo upload.
3. **State:** screen description / UI copy + optional primary CTA label + hypothesis string.
4. **Questions:** `advances_hypothesis` (noul); `cta_clarity` (score, low|medium|high) when a primary CTA exists.
5. **Gold:** single PM labeler; advances `1`/`0`; cta `low|medium|high|null`; rubric date 2026-09-18.
6. **Run:** sequential `POST https://api.typesafe.ai/v1/systemone`; **21/21 ok, 0 failures**.
7. **Metrics:** noul accuracy @0.5, false-pass, AUC, Brier; CTA exact + adjacent (±1).

## Dataset

| Slice | N |
| --- | --- |
| Total items | 21 |
| Artifact screens (PetID flow + delete modal) | 8 |
| Synthetic negative / control screens | 13 |
| advances_hypothesis labeled | 21 (10 yes / 11 no) |
| cta_clarity labeled | 15 (4 low / 4 med / 7 high); 6 null |

## Findings (E3)

| Judgment | N | Headline | Notes |
| --- | --- | --- | --- |
| advances_hypothesis | 21 | **90.5%** @0.5; AUC **1.0**; fp **0%** | Mean noul gold1 0.73 vs gold0 0.025 |
| cta_clarity | 15 | exact **86.7%**; adjacent **100%** | Perfect on gold-high (7/7) and gold-low (4/4) |

- **Misses (advances):** `e3-017` dual Share+Upload (noul 0.44); `e3-019` Skip-dominant upload copy (noul 0.24) — both gold=yes, pred=no. Model under-credits degraded-but-on-path screens.
- **Misses (CTA):** `e3-011` Get started splash gold=medium→pred=low; `e3-018` Add date form gold=medium→pred=high.
- **Workflow implication:** noul gate is usable to filter “does this screen belong in the hypothesis test?” with low false-alarm risk; CTA score can flag redesign targets (low clarity). Keep human review when layout sabotage (buried CTA) still has on-path copy — those are the FN cases.

## Cross-experiment (brief)

| | E1 analysis | E2 PRD | E3 prototype |
| --- | --- | --- | --- |
| Primitive | choice + score | noul ×2 | noul + score |
| N | 35 | 27 | 21 |
| Headline | theme 68.6%; sev exact 34.3% | mvp 100%; metric 93.8% | adv 90.5%; CTA exact 86.7% |
| Gating readiness | theme triage only | promising PRD lint | promising screen triage + CTA flag |

Pattern: **binary noul with explicit criteria** (E2/E3) outperforms free-form severity score (E1) on these demo sets. Score tasks improve when criteria map to visible UI affordances (CTA) rather than inferred activation impact.

## Limits

Tiny N, many synthetics (13/21), single labeler, text descriptions not pixels, no IAA, PetCare demo only.

## Artifacts

`datasets/e3_screens.jsonl`, `datasets/e3_rubric.md`, `runs/E3/`, `scripts/run_e3_jev.py`, `scripts/compute_e3_metrics.py`.
