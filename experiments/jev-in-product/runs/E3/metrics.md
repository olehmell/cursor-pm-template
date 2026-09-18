# E3 metrics — prototype critique (live Jev)

- Dataset: `datasets/e3_screens.jsonl` (N=21)
- Model: `jev-latest` → `jev-1.13.0`
- Hypothesis: Users want to store pet medical documents in the app via photo upload (PetID Digital Vet Passport MVP).
- Threshold: noul ≥ 0.5 → advances yes (1)
- API ok / fail: 21 / 0

## advances_hypothesis

| Metric | Value |
| --- | --- |
| N (labeled) | 21 |
| Accuracy @0.5 | 19/21 = **90.5%** |
| Confusion (tp/tn/fp/fn) | 8/11/0/2 |
| False pass rate (fp/N) | **0.0%** |
| ROC-AUC (noul vs gold) | 1.0 |
| Brier score | 0.057 |
| Score mean (all / gold1 / gold0) | 0.361 / 0.731 / 0.025 |
| Score range | [0.020, 0.930] |

### Misses

- `e3-017`: gold=1 pred=0 noul=0.440
- `e3-019`: gold=1 pred=0 noul=0.240

## cta_clarity

| Metric | Value |
| --- | --- |
| N (labeled) | 15 |
| Exact match | 13/15 = **86.7%** |
| Adjacent (±1 level) | 15/15 = **100.0%** |
| Gold dist (low/med/high) | 4/4/7 |
| Pred dist (low/med/high) | 5/2/8 |
| Mean continuous score by gold | low=0.01; med=1.1675; high=1.6857142857142857 |

### Confusion (rows = gold, cols = pred)

| gold \ pred | low | medium | high |
| --- | ---: | ---: | ---: |
| low | 4 | 0 | 0 |
| medium | 1 | 2 | 1 |
| high | 0 | 0 | 7 |

### Misses

- `e3-011`: gold=medium pred=low score=0.98
- `e3-018`: gold=medium pred=high score=1.68

## Calibration notes

- advances_hypothesis false-pass (fp) is dangerous for redesign triage: Jev says screen advances when gold says it does not.
- cta_clarity uses argmax over score-level probabilities (same as E1 severity).
- Rubric frozen in `datasets/e3_rubric.md` before API calls.

## Score distributions

### advances_hypothesis

- `e3-001`: gold=1 noul=0.880
- `e3-002`: gold=1 noul=0.930
- `e3-003`: gold=1 noul=0.770
- `e3-004`: gold=1 noul=0.830
- `e3-005`: gold=1 noul=0.880
- `e3-006`: gold=1 noul=0.880
- `e3-007`: gold=1 noul=0.620
- `e3-008`: gold=0 noul=0.050
- `e3-009`: gold=0 noul=0.020
- `e3-010`: gold=0 noul=0.020
- `e3-011`: gold=0 noul=0.020
- `e3-012`: gold=0 noul=0.020
- `e3-013`: gold=0 noul=0.030
- `e3-014`: gold=0 noul=0.020
- `e3-015`: gold=1 noul=0.840
- `e3-016`: gold=0 noul=0.020
- `e3-017`: gold=1 noul=0.440
- `e3-018`: gold=0 noul=0.020
- `e3-019`: gold=1 noul=0.240
- `e3-020`: gold=0 noul=0.020
- `e3-021`: gold=0 noul=0.030

### cta_clarity

- `e3-001`: gold=high pred=high score=1.98
- `e3-002`: gold=high pred=high score=1.91
- `e3-005`: gold=high pred=high score=2.0
- `e3-006`: gold=medium pred=medium score=1.0
- `e3-008`: gold=medium pred=medium score=1.01
- `e3-009`: gold=high pred=high score=1.43
- `e3-011`: gold=medium pred=low score=0.98
- `e3-013`: gold=low pred=low score=0.02
- `e3-014`: gold=high pred=high score=1.41
- `e3-015`: gold=low pred=low score=0.01
- `e3-017`: gold=low pred=low score=0.0
- `e3-018`: gold=medium pred=high score=1.68
- `e3-019`: gold=low pred=low score=0.01
- `e3-020`: gold=high pred=high score=1.47
- `e3-021`: gold=high pred=high score=1.6
