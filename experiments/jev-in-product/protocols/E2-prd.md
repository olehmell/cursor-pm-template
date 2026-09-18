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

## Status (2026-09-18 — complete)

Dataset: `datasets/e2_prd_sections.jsonl` (**N=27**) + frozen `datasets/e2_rubric.md`.
Live Jev: `runs/E2/` — mvp_scoped **100%** (11), metric_measurable **93.8%** (16); 0 API failures.
