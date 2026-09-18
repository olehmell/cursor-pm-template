# U5 metrics — Template skill router (live Jev)

- Dataset: `datasets/u5_pm_asks.jsonl` (N=48)
- Model: `jev-latest` → `jev-1.13.0`
- Thresholds: gate ≥ 0.3; max(fits) ≥ 0.3
- Decision: gate=mean(oriented gate nouls); if gate<0.30 → null; elif max(fits)<0.30 → null; else winner=Choice which
- API ok / fail: 48 / 0

## Primary error rates

| Metric | Value |
| --- | --- |
| wrong_route (gold≠null, pred≠gold or null) | 0/38 = **0.0%** |
| needless_route (gold=null, pred≠null) | 1/10 = **10.0%** |
| accuracy (incl. null) | 47/48 = **97.9%** |

## Confusion matrix (rows=gold, cols=pred)

| gold \ pred | data-analysis | prd-writing | prototyping | null |
| --- | --- | --- | --- | --- |
| data-analysis | 13 | 0 | 0 | 0 |
| prd-writing | 0 | 14 | 0 | 0 |
| prototyping | 0 | 0 | 11 | 0 |
| null | 1 | 0 | 0 | 9 |

## Gate calibration

| Slice | mean(gate) | n |
| --- | --- | --- |
| gold_covered | 0.760 | 38 |
| gold_null | 0.243 | 10 |
| pred_routed | 0.751 | 39 |
| pred_null | 0.227 | 9 |

Oriented gate = mean(acts_on_product_artifacts, would_follow_template_workflow, 1−prose_suffices). Below 0.30 → suggest nothing.

## Misses

### needless_route
- `u5-047`: gold=null pred=data-analysis gate=0.390 which=data-analysis fits={'data-analysis': 0.3, 'prd-writing': 0.05, 'prototyping': 0.02} reason=choice_winner

## Notes

- Gold + rubric frozen in `datasets/u5_rubric.md` before API calls.
- Single systemone call per ask (3-skill roster; no 182-wide skim).
- Prefer Choice `which` when gate and max(fits) clear thresholds.
