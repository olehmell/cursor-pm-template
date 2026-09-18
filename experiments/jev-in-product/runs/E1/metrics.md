# E1 metrics — interview theme + activation severity

**Run date:** 2026-09-18 (Europe/Kiev)  
**Model:** `jev-latest` (API returned `jev-1.13.0`)  
**N:** 35 passages (gold labeled offline before any Jev call; see `datasets/e1_rubric.md`)  
**API failures:** 0 / 35  
**Usage:** 26 819 input tokens, 2 632 output tokens  

## Headline

| Metric | Value |
| --- | --- |
| Theme accuracy | **24 / 35 = 68.6%** |
| Severity exact match | **12 / 35 = 34.3%** |
| Severity adjacent match (±1 level) | **25 / 35 = 71.4%** |

## Theme confusion (rows = gold, cols = pred)

| gold \ pred | setup_friction | notifications | multi_pet | trust_data | other |
| --- | ---: | ---: | ---: | ---: | ---: |
| setup_friction | 8 | 1 | 0 | 0 | 3 |
| notifications | 1 | 4 | 0 | 0 | 0 |
| multi_pet | 0 | 0 | 3 | 0 | 0 |
| trust_data | 3 | 0 | 0 | 3 | 2 |
| other | 0 | 1 | 0 | 0 | 6 |

**Notes**

- `multi_pet` was perfect (3/3) on this tiny slice.
- `trust_data` is the weakest class (3/8): often absorbed into `setup_friction` (document/clinic unification) or `other`.
- `setup_friction` ↔ `other` boundary is noisy when passages describe lost passports or novice knowledge without explicit “setup” language.

### High-confidence theme errors (confidence ≥ 0.7)

| id | gold | pred | conf |
| --- | --- | --- | ---: |
| e1-006 | trust_data | setup_friction | 0.77 |
| e1-019 | setup_friction | other | 0.81 |
| e1-021 | trust_data | other | 0.72 |

## Severity confusion (rows = gold, cols = pred)

| gold \ pred | low | medium | high |
| --- | ---: | ---: | ---: |
| low | 7 | 0 | 1 |
| medium | 8 | 4 | 1 |
| high | 9 | 4 | 1 |

**Predicted distribution:** low=24, medium=8, high=3  
**Gold distribution:** low=8, medium=13, high=14  

**Mean continuous score by gold band:** low→0.35, medium→0.67, high→0.60  

### Severity failure mode

Jev **systematically under-scores activation severity** on this set: most gold-`high` passages land as `low` or `medium`. Continuous scores barely separate medium vs high gold (0.67 vs 0.60). Possible causes:

1. Passages are short Ukrainian spans; activation definition is in English in `state` — model may underweight the 7-day feeding-plan criterion.
2. Rubric asked for *activation* impact; dramatic life stories still often true-`high` for setup, but the model treats them as general care anecdotes → `low`.
3. Score criteria strings were long; argmax over levels is conservative toward `low`.

Adjacent match (71.4%) is usable for triage; exact match (34.3%) is **not** ready for automated gating without recalibration or richer state.

## Honest limits

- Single labeler, frozen rubric, N=35, demo PetCare context.
- No second annotator / κ.
- Ukrainian source + English instructions mix.
- No calibration plot beyond confusion tables (sample too small for reliable ECE).

## Artifacts

- Dataset: `datasets/e1_interview_passages.jsonl`
- Rubric: `datasets/e1_rubric.md`
- Raw responses: `runs/E1/raw/e1-*.json`
- Summary: `runs/E1/summary.json`
- Machine metrics: `runs/E1/metrics.json`
