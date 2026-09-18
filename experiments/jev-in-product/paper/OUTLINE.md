# Short paper outline

**Working title:** Structured System-One judgments for PM product tasks: early experiments with TypeSafe Jev

## 1. Problem
Product work (interview synthesis, PRD review, prototype critique) needs repeatable semantic decisions. LLM free-text is hard to evaluate and wire into process. Can a System One model (typed answers + probabilities) help?

## 2. Scope
Only three task families from a PM Cursor template: analysis, PRD, prototyping. PetCare demo context unless swapped.

## 3. Method
For each task family: define 1–2 judgments, build a small gold dataset, run Jev, score vs gold, inspect misses.

## 4. Experiments (planned)
- **E1 Analysis:** theme tagging + activation-severity scoring on interview passages
- **E2 PRD:** MVP-scope check + measurable-metric check on PRD sections
- **E3 Prototype:** hypothesis-fit + CTA clarity on screen descriptions

## 5. Datasets
Source, size, labeling protocol, agreement if multi-labeler (even if N=1 with frozen rubric).

## 6. Results
Tables: accuracy / correlation / calibration notes; latency & cost if useful.

## 7. Discussion
Where probabilities change a PM workflow; failure modes; what stays LLM-drafted.

## 8. Limits & next
Tiny N, demo product context, single labeler.

## Status
Outline only — fill after E1 runs.
