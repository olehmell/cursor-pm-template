# E2 metrics — PRD review gates (live Jev)

- Dataset: `datasets/e2_prd_sections.jsonl` (N=27)
- Model: `jev-latest` → `jev-1.13.0`
- Threshold: noul ≥ 0.5 → yes (1)
- API ok / fail: 27 / 0

## mvp_scoped

| Metric | Value |
| --- | --- |
| N (labeled) | 11 |
| Accuracy @0.5 | 11/11 = **100.0%** |
| Confusion (tp/tn/fp/fn) | 5/6/0/0 |
| False pass rate (fp/N) | **0.0%** |
| ROC-AUC (noul vs gold) | 1.0 |
| Brier score | 0.053 |
| Score mean (all / gold1 / gold0) | 0.445 / 0.782 / 0.165 |
| Score range | [0.080, 0.910] |

### Misses

- none

## metric_measurable

| Metric | Value |
| --- | --- |
| N (labeled) | 16 |
| Accuracy @0.5 | 15/16 = **93.8%** |
| Confusion (tp/tn/fp/fn) | 9/6/0/1 |
| False pass rate (fp/N) | **0.0%** |
| ROC-AUC (noul vs gold) | 0.983 |
| Brier score | 0.073 |
| Score mean (all / gold1 / gold0) | 0.507 / 0.746 / 0.108 |
| Score range | [0.020, 0.970] |

### Misses

- `e2-008`: gold=1 pred=0 noul=0.220

## Calibration notes

- Compare mean noul on gold=1 vs gold=0; separation indicates usable ranking even when @0.5 accuracy is modest.
- False pass (fp) is the dangerous error for shipping: Jev says yes when gold is no.
- Rubric frozen in `datasets/e2_rubric.md` before API calls.

## Score distributions (id, gold, noul)

### mvp_scoped

- `e2-001`: gold=1 noul=0.910
- `e2-006`: gold=1 noul=0.820
- `e2-007`: gold=1 noul=0.860
- `e2-010`: gold=0 noul=0.080
- `e2-012`: gold=0 noul=0.130
- `e2-017`: gold=1 noul=0.760
- `e2-018`: gold=0 noul=0.110
- `e2-021`: gold=0 noul=0.460
- `e2-022`: gold=1 noul=0.560
- `e2-023`: gold=0 noul=0.130
- `e2-027`: gold=0 noul=0.080

### metric_measurable

- `e2-002`: gold=1 noul=0.840
- `e2-003`: gold=0 noul=0.020
- `e2-004`: gold=1 noul=0.870
- `e2-005`: gold=0 noul=0.060
- `e2-008`: gold=1 noul=0.220
- `e2-009`: gold=0 noul=0.180
- `e2-011`: gold=1 noul=0.600
- `e2-013`: gold=1 noul=0.870
- `e2-014`: gold=1 noul=0.760
- `e2-015`: gold=1 noul=0.750
- `e2-016`: gold=1 noul=0.670
- `e2-019`: gold=0 noul=0.120
- `e2-020`: gold=0 noul=0.240
- `e2-024`: gold=1 noul=0.910
- `e2-025`: gold=0 noul=0.030
- `e2-026`: gold=1 noul=0.970
