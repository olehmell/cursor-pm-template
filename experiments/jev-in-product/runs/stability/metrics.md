# Jev stability study (reproducibility)

**K** = 5 identical requests per item (same state+questions).
**Model:** `jev-latest` → resolved per-response.
**Sample:** E1=12, E2=10, E3=8 (total 30 items, 150 planned API calls).
**API failures:** 0 (rate-limit hits noted: 0).

## Stability thresholds (documented)

- Noul **stable** if range (max−min) ≤ **0.1** and sample std ≤ **0.05**.
- Discrete perfect = all K runs identical on the item's discrete answer keys.
- ≥4/5 = mode of the discrete tuple appears in at least 4 of K runs.

## Aggregate

| Metric | Value |
| --- | --- |
| Items with full K=5 ok | 30 / 30 |
| % perfect 5/5 identical discrete | **90.0%** (27/30) |
| % ≥4/5 discrete | **93.3%** (28/30) |
| Noul fields stable (range≤0.1, std≤0.05) | **100.0%** (18/18) |
| E1 theme mean mode-agreement | 0.983 |
| E1 severity mean mode-agreement | 0.933 |
| E2 mvp_scoped mean mode-agreement | 1.000 |
| E2 metric_measurable mean mode-agreement | 1.000 |
| E3 advances_hypothesis mean mode-agreement | 1.000 |
| E3 cta_clarity mean mode-agreement | 1.000 |

## E1 per-item

| id | theme mode | theme agree | theme #uniq | sev mode | sev agree | sev exact | sev adj | perfect 5/5 | ≥4/5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| e1-006 | setup_friction | 1.0 | 1 | medium | 1.0 | 1.0 | 1.0 | True | True |
| e1-008 | trust_data | 0.8 | 2 | low | 1.0 | 1.0 | 1.0 | False | True |
| e1-018 | notifications | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |
| e1-027 | other | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |
| e1-001 | notifications | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |
| e1-003 | multi_pet | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |
| e1-007 | setup_friction | 1.0 | 1 | medium | 1.0 | 1.0 | 1.0 | True | True |
| e1-010 | other | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |
| e1-015 | trust_data | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |
| e1-016 | setup_friction | 1.0 | 1 | high | 0.6 | 0.6 | 1.0 | False | False |
| e1-024 | trust_data | 1.0 | 1 | high | 0.6 | 0.6 | 1.0 | False | False |
| e1-025 | notifications | 1.0 | 1 | low | 1.0 | 1.0 | 1.0 | True | True |

## E2 per-item

| id | discrete key | mode | agree | #uniq | noul mean | noul std | noul range | noul stable | perfect 5/5 | ≥4/5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| e2-001 | mvp_scoped | 1 | 1.0 | 1 | 0.896 | 0.008944 | 0.02 | True | True | True |
| e2-010 | mvp_scoped | 0 | 1.0 | 1 | 0.086 | 0.005477 | 0.01 | True | True | True |
| e2-017 | mvp_scoped | 1 | 1.0 | 1 | 0.788 | 0.004472 | 0.01 | True | True | True |
| e2-021 | mvp_scoped | 0 | 1.0 | 1 | 0.456 | 0.005477 | 0.01 | True | True | True |
| e2-022 | mvp_scoped | 1 | 1.0 | 1 | 0.59 | 0.015811 | 0.04 | True | True | True |
| e2-002 | metric_measurable | 1 | 1.0 | 1 | 0.844 | 0.008944 | 0.02 | True | True | True |
| e2-003 | metric_measurable | 0 | 1.0 | 1 | 0.02 | 0.0 | 0.0 | True | True | True |
| e2-008 | metric_measurable | 0 | 1.0 | 1 | 0.214 | 0.016733 | 0.04 | True | True | True |
| e2-011 | metric_measurable | 1 | 1.0 | 1 | 0.614 | 0.013416 | 0.03 | True | True | True |
| e2-025 | metric_measurable | 0 | 1.0 | 1 | 0.03 | 0.0 | 0.0 | True | True | True |

## E3 per-item

| id | adv mode | adv agree | noul mean | noul std | noul range | noul stable | cta mode | cta agree | perfect 5/5 | ≥4/5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| e3-001 | 1 | 1.0 | 0.874 | 0.005477 | 0.01 | True | high | 1.0 | True | True |
| e3-006 | 1 | 1.0 | 0.882 | 0.008367 | 0.02 | True | medium | 1.0 | True | True |
| e3-008 | 0 | 1.0 | 0.05 | 0.0 | 0.0 | True | medium | 1.0 | True | True |
| e3-009 | 0 | 1.0 | 0.02 | 0.0 | 0.0 | True | high | 1.0 | True | True |
| e3-013 | 0 | 1.0 | 0.03 | 0.0 | 0.0 | True | low | 1.0 | True | True |
| e3-015 | 1 | 1.0 | 0.834 | 0.005477 | 0.01 | True | low | 1.0 | True | True |
| e3-017 | 0 | 1.0 | 0.434 | 0.02881 | 0.08 | True | low | 1.0 | True | True |
| e3-019 | 0 | 1.0 | 0.234 | 0.008944 | 0.02 | True | low | 1.0 | True | True |

## Notable unstable items

### Discrete flip / low agreement
- `e1-008` (E1): theme 4× trust_data / 1× setup_friction (mode_agreement=0.8); severity 5/5 low
- `e1-016` (E1): discrete_mode_count=3, unique=2, keys=['theme', 'severity']
- `e1-024` (E1): discrete_mode_count=3, unique=2, keys=['theme', 'severity']

## Sample IDs

- **E1:** e1-006, e1-008, e1-018, e1-027, e1-001, e1-003, e1-007, e1-010, e1-015, e1-016, e1-024, e1-025
- **E2:** e2-001, e2-010, e2-017, e2-021, e2-022, e2-002, e2-003, e2-008, e2-011, e2-025
- **E3:** e3-001, e3-006, e3-008, e3-009, e3-013, e3-015, e3-017, e3-019
