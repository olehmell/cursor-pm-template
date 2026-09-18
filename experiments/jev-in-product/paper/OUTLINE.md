# Short paper outline

**Working title:** Structured System-One judgments for PM product tasks: early experiments with TypeSafe Jev

## 1. Problem
Product work (interview synthesis, PRD review, prototype critique) needs repeatable semantic decisions. LLM free-text is hard to evaluate and wire into process. Can a System One model (typed answers + probabilities) help?

## 2. Scope
Only three task families from a PM Cursor template: analysis, PRD, prototyping. PetCare demo context unless swapped.

## 3. Method
For each task family: define 1–2 judgments, build a small gold dataset, run Jev, score vs gold, inspect misses.

## 4. Experiments
- **E1 Analysis:** theme tagging + activation-severity scoring on interview passages — **DONE (N=35, live API)**
- **E2 PRD:** MVP-scope check + measurable-metric check on PRD sections — **dataset scaffolded**
- **E3 Prototype:** hypothesis-fit + CTA clarity on screen descriptions — planned

## 5. Datasets
E1: `datasets/e1_interview_passages.jsonl` + `e1_rubric.md` (single labeler, frozen rubric). E2 stub: `e2_prd_sections.jsonl`.

## 6. Results
E1 theme acc **68.6%**; severity exact **34.3%**, adjacent **71.4%**. See `runs/E1/metrics.md` and `paper/DRAFT-E1.md (DRAFT.md is gitignored by template)`.

## 7. Discussion
Where probabilities change a PM workflow; failure modes; what stays LLM-drafted.

## 8. Limits & next
Tiny N, demo product context, single labeler. E2 complete; optional E1 severity recalibration; E3 next.

## Status
**E1 complete** (dataset + live Jev + metrics + draft abstract/method/results). Outline + draft updated 2026-09-18; tracked draft is `DRAFT-E1.md`.

## E2 status (2026-09-18)

**E2 complete** — N=27; mvp_scoped 100% (11/11); metric_measurable 93.8% (15/16); false-pass 0%; see `runs/E2/metrics.md` and `paper/DRAFT-E2.md`.
