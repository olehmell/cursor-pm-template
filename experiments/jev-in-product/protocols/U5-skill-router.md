# Protocol U5 — Template skill router

## Product decision
For a PM ask in this Cursor template, which of the three usecase skills (if any) should load?

## Roster
- `data-analysis` — `usecases/01-data-analysis`
- `prd-writing` — `usecases/02-prd-writing`
- `prototyping` — `usecases/03-prototyping`

Roster JSON: `datasets/u5_skill_roster.json` (name, description, description_full).

## Pattern (skill_suggestion cookbook, simplified)
Small roster (3) → **one** `systemone` call per ask (no 182-wide skim / second rerank):

1. **Choice `which`** — criteria = short description per skill
2. **Gate nouls** (adapted):
   - `acts_on_product_artifacts`
   - `would_follow_template_workflow`
   - `prose_suffices` (**invert**)
3. **`fits::{skill}`** noul per skill — does this skill do the specific thing asked?

### Decision in code
- `gate` = mean of oriented gate nouls
- if `gate < 0.30` → suggest nothing
- else if `max(fits) < 0.30` → nothing
- else winner = Choice `which` (fits only decide whether to speak)

## Dataset
- `datasets/u5_pm_asks.jsonl` (~40–50 asks)
- `gold_skill`: `data-analysis | prd-writing | prototyping | null`
- Mix: clear covered, ambiguous (analysis vs PRD), uncovered
- Rubric frozen **before** API: `datasets/u5_rubric.md`

## Run
`scripts/run_u5_jev.py` → live `jev-latest`; key length check only.
Artifacts: `runs/U5/raw/`, `summary.json`, `metrics.md` via `compute_u5_metrics.py`.

## Metrics
- **wrong_route:** among gold≠null, pred≠gold or pred=null
- **needless_route:** among gold=null, pred≠null
- accuracy overall; confusion matrix; gate calibration notes
