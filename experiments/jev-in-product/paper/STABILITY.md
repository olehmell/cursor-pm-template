# Appendix: Answer stability (reproducibility) of TypeSafe Jev

**Branch:** `experiment/jev-product-tasks`  
**Question:** Given identical state+questions, how often does `jev-latest` return the same discrete answers across K reruns? (Accuracy vs gold is out of scope here.)  
**Design:** Stratified subsample — E1 N=12 (mix themes/severities; includes prior theme misses), E2 N=10 (5 `mvp_scoped` + 5 `metric_measurable`, including the NPS miss and near-threshold items), E3 N=8 (mix advances + CTA; includes prior FNs). **K=5** identical requests per item → **150** live API calls. Raw: `runs/stability/raw/{E1,E2,E3}/{id}_r{1-5}.json`. Tables: `runs/stability/metrics.md`, `runs/stability/summary.json`.

**Documented noul-stable thresholds:** range (max−min) ≤ **0.10** and sample std ≤ **0.05**.

## Headline results

| Metric | Value |
| --- | --- |
| API failures / rate-limits | **0** / 0 |
| Perfect 5/5 identical discrete answers | **90.0%** (27/30) |
| ≥4/5 discrete mode | **93.3%** (28/30) |
| Noul fields stable (18 noul fields on E2+E3) | **100%** |
| E2 / E3 perfect 5/5 | **100%** / **100%** |
| E1 perfect 5/5 | **75%** (9/12); ≥4/5 **83.3%** |

Mean mode-agreement: E1 theme **0.983**, E1 severity **0.933**; E2 mvp/metric and E3 advances/CTA all **1.000**.

## Notable unstable items

All instability was confined to **E1 severity** (and one low-confidence theme flip):

| Item | Behavior |
| --- | --- |
| `e1-008` | Theme 4× `trust_data` / 1× `setup_friction` (low confidence ~0.3–0.4); severity always `low` |
| `e1-016` | Theme stable `setup_friction`; severity 3× `high` / 2× `medium` (continuous scores ~1.40–1.47 near the medium/high boundary) |
| `e1-024` | Theme stable `trust_data`; severity 3× `high` / 2× `medium` (scores ~1.14–1.30) |

No E2 or E3 item flipped a binary gate or CTA label across five runs. Closest noul noise: `e3-017` advances noul range **0.08** (still under the 0.10 stable bar); threshold-adjacent `e2-021` (mean noul 0.456) and `e2-022` (0.59) never crossed 0.5.

## Is Jev stable enough for product gates?

**Yes for noul product gates (E2/E3-style), with caveats; not yet for E1-style severity gating.**

- **Noul binary gates** (MVP scope, metric measurable, advances hypothesis) were **reproducible**: 100% identical discrete decisions and 100% noul-stable under the stated thresholds on this sample—including prior accuracy misses. That is what you want for a pre-review lint: the same PRD section or screen should not randomly pass then fail.
- **CTA score** (E3) was likewise 5/5 identical on every sampled screen.
- **Choice theme** (E1) is mostly stable (mean mode-agreement 0.983); the one flip was a known ambiguous miss with low confidence—probabilities still signal review.
- **Ordinal severity** is the weak spot: near mid/high boundaries the argmax label can flip while continuous scores stay close. Adjacent agreement remained 100% on the unstable items, but exact labels are not gate-ready.

**Product implication:** ship optional Cursor lint on **noul ≥ threshold** with human override; do **not** auto-block on severity exact labels until boundary behavior is tightened (recalibration or require confidence / margin). Stability here complements—not replaces—the accuracy findings in `PAPER.md`.

## Limits

Small stratified sample (30 items), K=5, single model alias (`jev-latest` → `jev-1.13.0`), no deliberate prompt perturbation. Re-run after model bumps.
