# Draft: Structured System-One judgments for PM product tasks

_Working draft — E1 results filled 2026-09-18. Keep under ~1500 words._

## Abstract

Product managers need repeatable semantic judgments over messy qualitative inputs (interview quotes, PRD sections, prototype screens). We apply TypeSafe Jev (`jev-latest`), a System-One model that returns typed answers with probabilities, *inside* existing PM workflows rather than as a separate use case. In experiment **E1** (data analysis), we labeled **N=35** Ukrainian interview passages with a frozen rubric for theme (`setup_friction | notifications | multi_pet | trust_data | other`) and activation severity (`low | medium | high` vs completing feeding-plan setup within 7 days), then scored live API outputs against gold. Theme accuracy was **68.6%**; severity exact match **34.3%** and adjacent match **71.4%**. Theme tagging looks promising for triage; severity is systematically under-scored and not yet reliable for gating. Sample size is small and single-labeled — results are exploratory.

## Introduction

Interview synthesis and PRD review still lean on free-text LLM drafts that are hard to evaluate or wire into process. Typed judgments (choice / score / noul) with explicit probabilities may fit PM decision points better. This paper reports early in-product experiments on a PetCare Cursor template: analysis (E1), PRD (E2), prototyping (E3).

## Method (E1)

1. **Product decision:** Which interview passages matter for activation, and how severe is the barrier?
2. **State:** passage text + frozen activation definition in the request `state`.
3. **Questions:** `theme` (choice, 5 options) and `activation_severity` (score, 3 levels).
4. **Gold:** single PM labeler, rubric frozen in `datasets/e1_rubric.md` *before* any API call.
5. **Run:** sequential `POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer` key; model alias `jev-latest` (resolved `jev-1.13.0`); 0 API failures.
6. **Metrics:** theme accuracy; severity exact + adjacent (±1); confusion notes; high-confidence misses.

## Experiments

### E1 — Analysis (complete, exploratory)

- Source: 3 interviews under `usecases/01-data-analysis/interviews/`
- Unit: quote / 2–4 sentence span
- **N = 35** (target was 30–50)
- Live Jev run artifacts: `runs/E1/`

### E2 — PRD (scaffolded)

Dataset stub `datasets/e2_prd_sections.jsonl` from `usecases/02-prd-writing/artifacts/`; protocol in `protocols/E2-prd.md`. Full Jev runs deferred.

### E3 — Prototype (planned)

See `protocols/E3-prototype.md`.

## Findings (E1)

| Metric | Result (N=35) |
| --- | --- |
| Theme accuracy | 24/35 = **68.6%** |
| Severity exact | 12/35 = **34.3%** |
| Severity adjacent | 25/35 = **71.4%** |

- **What worked:** `multi_pet` perfect on tiny slice (3/3); `notifications` and `other` reasonably recoverable; probabilities useful for spotting high-confidence errors (3 theme errors with conf ≥ 0.7).
- **What did not:** severity under-prediction (pred distribution low-heavy vs gold high-heavy); `trust_data` confused with `setup_friction` / `other`.
- **Workflow implication:** use Jev theme tags as a *first-pass sorter* for interview synthesis; keep human review for severity until recalibrated with richer state or more examples.

## Conclusion

Typed System-One judgments can sit inside PM analysis without inventing a new use case. On this small E1 set, theme choice is moderately useful; activation severity score needs work before product gating. Next: E2 PRD section checks; optional E1 recalibration with bilingual state and severity few-shot exemplars.

## Limits

Tiny N, demo product, single labeler, Ukrainian passages + English instructions, no inter-annotator agreement.
