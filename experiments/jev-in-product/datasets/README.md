# Datasets

Place gold sets here as CSV/JSONL.

## E1 (analysis) — ready
- `e1_interview_passages.jsonl` — columns: `id,source_file,passage,gold_theme,gold_severity,notes`
- `e1_rubric.md` — frozen labeling rubric

## E2 (PRD) — scaffold
- `e2_prd_sections.jsonl` — provisional gold for `mvp_scoped` / `metric_measurable`
- `e2_NOTES.md` — labeling hints; expand before live runs

Do not put API keys in this folder.

## E3 (prototype) — ready
- `e3_screens.jsonl` — screen descriptions; gold `advances_hypothesis` / `cta_clarity`
- `e3_rubric.md` — frozen labeling rubric (hypothesis + CTA clarity)
