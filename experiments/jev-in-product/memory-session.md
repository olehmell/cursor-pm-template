# Session notes

## 2026-09-18 (loop 1 — E1 live run)
- Clarified: Jev is a *method* for product tasks, not a 4th use case.
- Built E1 dataset: **35** passages from 3 interviews; rubric frozen in `datasets/e1_rubric.md` before API.
- Ran live TypeSafe Jev (`jev-latest` → `jev-1.13.0`): **0 failures**.
- Metrics: theme acc **68.6%**; severity exact **34.3%**, adjacent **71.4%**; severity systematically under-scored.
- Updated `paper/DRAFT-E1.md (DRAFT.md is gitignored by template)`, `paper/OUTLINE.md`, `runs/E1/metrics.md`.
- Next: scaffold/finish E2 PRD dataset; optional E1 severity recalibration; do not push to main.

## Earlier 2026-09-18
- Deliverable: datasets + tests + short paper.
- Git: branch `experiment/jev-product-tasks` only (main reverted).
