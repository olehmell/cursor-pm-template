# Protocol E2 — PRD review gates

## Product decision
Before stakeholder review: is a PRD section MVP-scoped, and is each success metric measurable?

## Judgments
1. `mvp_scoped` (noul)
2. `metric_measurable` (noul) — needs COMPANY-style metric definition in state

## Dataset
- Source: `usecases/02-prd-writing/artifacts/` (+ synthetic sections if needed)
- Unit: PRD section or metric bullet
- Target: ~20–30 items with clear gold

## Metrics
Calibration of noul vs binary gold; false “pass” rate (dangerous for shipping)

---

## Scaffold status (2026-09-18)

Initial dataset: `datasets/e2_prd_sections.jsonl` (12 items from PRD/MVP/roadmap artifacts) + `datasets/e2_NOTES.md`.
**No live Jev E2 runs yet** — expand to ~20–30 and freeze rubric before calling API.
