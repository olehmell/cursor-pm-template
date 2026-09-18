# Draft: Structured System-One judgments for PM product tasks (E2)

_Working draft — E2 results filled 2026-09-18. Companion to DRAFT-E1.md._

## Abstract (E2 addendum)

We extend the in-product Jev loop to **PRD review gates**. On **N=27** PetCare PRD sections/metric bullets (25 from artifacts + 2 marked synthetic), with gold frozen in `datasets/e2_rubric.md` *before* API calls, live `jev-latest` (`jev-1.13.0`) noul judgments achieved **mvp_scoped** accuracy **100%** (11/11; AUC 1.0; false-pass 0%) and **metric_measurable** accuracy **93.8%** (15/16; AUC 0.983; false-pass 0%) at threshold ≥0.5. One miss: NPS with survey cadence scored low (noul 0.22) despite gold=yes. Vs E1 (theme 68.6%, severity exact 34.3%), E2 binary gates look far more reliable on this small set — likely easier task + clearer criteria in state.

## Method (E2)

1. **Product decision:** Before stakeholder review — is the section MVP-scoped? Is each success metric measurable?
2. **State:** PRD section text + frozen COMPANY/PRODUCT metric bar (activation, north star, health metrics) + short COMPANY.md/PRODUCT.md excerpts.
3. **Questions:** `mvp_scoped` (noul) and/or `metric_measurable` (noul) depending on item type; criteria true/false strings from rubric.
4. **Gold:** single PM labeler; `1`/`0`/`null` (null = skip); rubric date 2026-09-18.
5. **Run:** sequential `POST https://api.typesafe.ai/v1/systemone`; 27/27 ok, 0 failures.
6. **Metrics:** accuracy @0.5; false-pass rate; ROC-AUC on noul; Brier; score distributions by gold.

## Dataset

| Slice | N |
| --- | --- |
| Total items | 27 |
| mvp_scoped labeled | 11 (5 yes / 6 no) |
| metric_measurable labeled | 16 (10 yes / 6 no) |
| Synthetic controls | 2 (happiness fail; COMPANY activation pass) |

Sources: `usecases/02-prd-writing/artifacts/` (MVP PRD, full PRD, Q1 roadmap, critical questions).

## Findings (E2)

| Judgment | N | Acc @0.5 | AUC | Brier | False pass |
| --- | --- | --- | --- | --- | --- |
| mvp_scoped | 11 | **100%** | 1.00 | 0.053 | **0%** |
| metric_measurable | 16 | **93.8%** | 0.98 | 0.073 | **0%** |

- **Calibration:** Mean noul gold1 vs gold0 — mvp 0.78 vs 0.17; metric 0.75 vs 0.11 (strong separation).
- **Miss:** `e2-008` NPS (−20.5→>0, monthly survey) gold=1 but noul=0.22 — model may underweight survey instruments vs event telemetry.
- **Near miss:** `e2-021` wide V1 laundry gold=0, noul=0.46 (just under threshold).
- **Workflow implication:** noul gates look usable as *pre-review lint* for MVP scope and metric quality; keep human eye on survey/NPS-style metrics; false-pass rate 0% on this set is encouraging for shipping safety but N is tiny.

## E1 vs E2 (brief)

| | E1 analysis | E2 PRD |
| --- | --- | --- |
| Primitive | choice + score | noul ×2 |
| Headline | theme 68.6%; sev exact 34.3% | mvp 100%; metric 93.8% |
| Failure mode | severity under-score | rare FN on NPS |
| Ready for gating? | theme triage only | promising pre-review lint |

## Limits

Tiny N, single labeler, demo PRDs, 2 synthetics, Ukrainian/English mix, no IAA. Perfect mvp accuracy may not hold on messier real PRDs.

## Artifacts

`datasets/e2_prd_sections.jsonl`, `datasets/e2_rubric.md`, `runs/E2/`, `scripts/run_e2_jev.py`.
