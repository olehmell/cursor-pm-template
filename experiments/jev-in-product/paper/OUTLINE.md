# Short paper outline

**Working title:** Structured System-One judgments for PM product tasks: early experiments with TypeSafe Jev

## 1. Problem
Product work (interview synthesis, PRD review, prototype critique) needs repeatable semantic decisions. LLM free-text is hard to evaluate and wire into process. Can a System One model (typed answers + probabilities) help?

## 2. Scope
Only three task families from a PM Cursor template: analysis, PRD, prototyping. PetCare demo context unless swapped (E3 = PetID).

## 3. Method
For each task family: define 1–2 judgments, build a small gold dataset, run Jev, score vs gold, inspect misses.

## 4. Experiments
- **E1 Analysis:** theme tagging + activation-severity scoring on interview passages — **DONE (N=35, live API)**
- **E2 PRD:** MVP-scope check + measurable-metric check on PRD sections — **DONE (N=27, live API)**
- **E3 Prototype:** hypothesis-fit + CTA clarity on screen descriptions — **DONE (N=21, live API)**

## 5. Datasets
- E1: `datasets/e1_interview_passages.jsonl` + `e1_rubric.md`
- E2: `datasets/e2_prd_sections.jsonl` + `e2_rubric.md`
- E3: `datasets/e3_screens.jsonl` + `e3_rubric.md`

## 6. Results
- E1: theme acc **68.6%**; severity exact **34.3%**, adjacent **71.4%**. See `runs/E1/metrics.md`.
- E2: mvp_scoped **100%** (AUC 1.0); metric_measurable **93.8%** (AUC 0.983); fp 0% both; miss `e2-008` NPS. See `runs/E2/metrics.md`.
- E3: advances_hypothesis **90.5%** (AUC 1.0, fp 0%); cta_clarity exact **86.7%**, adjacent **100%**. See `runs/E3/metrics.md`.

## 7. Discussion
Where probabilities / noul change a PM workflow; failure modes; what stays LLM-drafted. See consolidated paper.

## 8. Limits & next
Tiny N, demo product context, single labeler. Optional E1 severity recalibration; expand real PRDs/screens; second labeler; wire lint gates.

## Status
**FILLED** — consolidated short paper written 2026-09-18 in `paper/PAPER.md` (~1350 words). Per-experiment drafts retained as `DRAFT-E1.md`, `DRAFT-E2.md`, `DRAFT-E3.md`. Model: `jev-latest` → `jev-1.13.0`.
