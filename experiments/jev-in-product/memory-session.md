# Session notes

## 2026-09-18 (loop 2 — E2 live run)
- Branch: `experiment/jev-product-tasks` only.
- Expanded E2 dataset to **N=27** (25 artifact + 2 synthetic); gold + rubric frozen in `datasets/e2_rubric.md` **before** API.
- Live Jev `jev-latest` → `jev-1.13.0`: **27/27 ok, 0 failures**. Key length confirmed 107 (not printed).
- Metrics @ noul≥0.5: **mvp_scoped 11/11 = 100%** (AUC 1.0, Brier 0.053, fp 0%); **metric_measurable 15/16 = 93.8%** (AUC 0.983, Brier 0.073, fp 0%). Miss: e2-008 NPS.
- Artifacts: `runs/E2/raw|summary.json|metrics.md`, `paper/DRAFT-E2.md`, scripts `run_e2_jev.py` / `compute_e2_metrics.py`.
- E1 vs E2: E2 binary noul gates much stronger than E1 severity; theme triage still the E1 win.
- Next: optional E3 prototype protocol; do not push to main.

## 2026-09-18 (loop 1 — E1 live run)
- Built E1 dataset: **35** passages; theme acc **68.6%**; severity exact **34.3%** / adjacent **71.4%**; tip ~13fc2d75.
- Next was E2 (done above).

## Earlier 2026-09-18
- Deliverable: datasets + tests + short paper.
- Git: branch `experiment/jev-product-tasks` only (main reverted).
