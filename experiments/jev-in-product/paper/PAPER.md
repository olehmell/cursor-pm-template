# Structured System-One judgments for PM product tasks: early experiments with TypeSafe Jev

**Branch:** `experiment/jev-product-tasks`  
**Model:** `jev-latest` → `jev-1.13.0` via TypeSafe System One API (`POST https://api.typesafe.ai/v1/systemone`)  
**Date:** 2026-09-18 (Europe/Kiev)

## Abstract

Product managers need repeatable semantic judgments over messy qualitative inputs—interview quotes, PRD sections, prototype screens—yet free-text LLM drafts are hard to evaluate or wire into process. We apply TypeSafe Jev, a System-One model that returns typed answers with probabilities, *inside* existing PM workflows on a PetCare Cursor template. Across three exploratory experiments with gold frozen before any API call: **E1** (N=35 interview passages) theme accuracy **68.6%**, severity exact **34.3%** / adjacent **71.4%** (severity systematically under-scored; `trust_data` weak); **E2** (N=27 PRD items) `mvp_scoped` **100%** (AUC 1.0) and `metric_measurable` **93.8%** (AUC 0.983), false-pass **0%** on both, one miss on NPS (`e2-008`); **E3** (N=21 prototype screens) `advances_hypothesis` **90.5%** (AUC 1.0, fp 0%) and `cta_clarity` exact **86.7%** / adjacent **100%**. Binary noul gates with explicit criteria look far more reliable than free-form severity scoring on these small demo sets. Results are exploratory: tiny N, single labeler, demo PetCare/PetID context.

## Introduction / problem

Interview synthesis, PRD review, and prototype critique still lean on free-text LLM output that is difficult to score, version, or attach to a decision gate. Typed judgments—choice, score, or noul (numeric opinion under limit)—with explicit probabilities may fit PM decision points better: they are auditable, thresholdable, and comparable across runs. This paper asks whether Jev can help *inside* product workflows rather than as a separate chatbot use case. Scope is deliberately narrow: three task families from a PM Cursor template (analysis, PRD, prototyping), PetCare demo product unless noted (E3 uses PetID upload hypothesis).

## Method

For each task family we followed the same loop:

1. Name a concrete product decision (e.g., “is this metric measurable?”).
2. Encode state (passage / section / screen text + frozen COMPANY/PRODUCT or hypothesis context).
3. Define 1–2 typed questions with criteria strings.
4. Build a small gold set with a **single PM labeler**; freeze the rubric in `datasets/` *before* any live API call.
5. Run sequential System One requests with model alias `jev-latest` (API resolved `jev-1.13.0`).
6. Score against gold: accuracy, adjacent match for ordinal scores, false-pass rate and ROC-AUC for noul; inspect high-confidence misses.

Protocols: `protocols/E1-analysis.md`, `protocols/E2-prd.md`, `protocols/E3-prototype.md`. Rubrics: `datasets/e1_rubric.md`, `e2_rubric.md`, `e3_rubric.md`. Live artifacts: `runs/E1/`, `runs/E2/`, `runs/E3/` (raw JSON, `summary.json`, `metrics.md`).

## Experiments

### E1 — Interview analysis (N=35)

**Decision:** Which passages matter for activation, and how severe is the barrier to completing feeding-plan setup within 7 days?  
**Unit:** quote / 2–4 sentence span from `usecases/01-data-analysis/interviews/` (Ukrainian source, English instructions in state).  
**Judgments:** `theme` (choice: `setup_friction | notifications | multi_pet | trust_data | other`); `activation_severity` (score: low | medium | high).  
**Dataset:** `datasets/e1_interview_passages.jsonl`. **API:** 35/35 ok, 0 failures. Details: `runs/E1/metrics.md`, draft notes in `paper/DRAFT-E1.md`.

| Metric | Result |
| --- | --- |
| Theme accuracy | 24/35 = **68.6%** |
| Severity exact | 12/35 = **34.3%** |
| Severity adjacent (±1) | 25/35 = **71.4%** |

Theme tagging is moderately useful for triage (`multi_pet` 3/3 on a tiny slice; `notifications` and `other` recoverable). Weakest class is `trust_data` (often absorbed into `setup_friction` or `other`). Severity is **systematically under-scored** (pred low-heavy vs gold high-heavy); exact match is not ready for gating. Three theme errors had confidence ≥ 0.7—probabilities still help surface review candidates.

### E2 — PRD review gates (N=27)

**Decision:** Before stakeholder review—is the section MVP-scoped? Is each success metric measurable?  
**Unit:** PRD sections / metric bullets from `usecases/02-prd-writing/artifacts/` (25 artifact + 2 synthetic).  
**Judgments:** `mvp_scoped` (noul) and/or `metric_measurable` (noul) at threshold ≥0.5.  
**Dataset:** `datasets/e2_prd_sections.jsonl` (mvp labeled 11; metric labeled 16). **API:** 27/27 ok. Details: `runs/E2/metrics.md`, `paper/DRAFT-E2.md`.

| Judgment | N | Acc @0.5 | AUC | Brier | False pass |
| --- | --- | --- | --- | --- | --- |
| mvp_scoped | 11 | **100%** (11/11) | **1.0** | 0.053 | **0%** |
| metric_measurable | 16 | **93.8%** (15/16) | **0.983** | 0.073 | **0%** |

Strong noul separation (mvp gold1 vs gold0 means 0.78 vs 0.17; metric 0.75 vs 0.11). Sole miss: `e2-008` NPS with survey cadence (gold=yes, noul=0.22)—model may underweight survey instruments vs event telemetry. Near miss: `e2-021` wide V1 laundry list (gold=no, noul=0.46).

### E3 — Prototype critique (N=21)

**Decision:** Does the screen advance the PetID upload hypothesis, and is the primary CTA clear?  
**Hypothesis (in state):** Users want to store pet medical documents via photo upload.  
**Unit:** screen descriptions—8 from `usecases/03-prototyping/` + 13 synthetic controls (text, not pixels).  
**Judgments:** `advances_hypothesis` (noul @0.5); `cta_clarity` (score low|medium|high when a primary CTA exists).  
**Dataset:** `datasets/e3_screens.jsonl` (cta labeled 15). **API:** 21/21 ok. Details: `runs/E3/metrics.md`, `paper/DRAFT-E3.md`.

| Judgment | N | Headline | Notes |
| --- | --- | --- | --- |
| advances_hypothesis | 21 | **90.5%** @0.5; AUC **1.0**; fp **0%** | Mean noul gold1 0.73 vs gold0 0.025 |
| cta_clarity | 15 | exact **86.7%**; adjacent **100%** | Perfect on gold-high (7/7) and gold-low (4/4) |

Advances misses are false-negatives on degraded-but-on-path screens (`e3-017` dual Share+Upload, noul 0.44; `e3-019` Skip-dominant upload, noul 0.24). CTA misses: two medium↔low/high swaps (`e3-011`, `e3-018`).

## Findings

| | E1 analysis | E2 PRD | E3 prototype |
| --- | --- | --- | --- |
| Primitive | choice + score | noul ×2 | noul + score |
| N | 35 | 27 | 21 |
| Headline | theme 68.6%; sev exact 34.3% | mvp 100%; metric 93.8% | adv 90.5%; CTA exact 86.7% |
| Dangerous errors | severity under-score | 0 false-pass; 1 FN (NPS) | 0 false-pass; 2 FN (layout sabotage) |
| Gating readiness | theme triage only | promising pre-review lint | promising screen triage + CTA flag |

**Cross-cutting pattern:** binary **noul with explicit criteria** (E2/E3) outperforms free-form severity score (E1) on these demo sets. Score tasks improve when criteria map to visible UI affordances (CTA clarity) rather than inferred activation impact. False-pass rate of 0% on E2 and E3 noul gates is encouraging for shipping safety but must not be over-read given tiny N.

## Discussion — when Jev helps PM workflows

- **Interview synthesis (E1):** use theme tags as a *first-pass sorter*; keep humans on severity until recalibrated (richer state, more examples, or ordinal recalibration). Probabilities flag high-confidence mistakes for review.
- **PRD review (E2):** noul gates look usable as *pre-review lint* for MVP scope and metric quality. Keep a human eye on survey/NPS-style metrics (the one miss). Prefer false-negatives over false-passes when blocking stakeholder review.
- **Prototype critique (E3):** noul gate can filter “does this screen belong in the hypothesis test?” with low false-alarm risk on this set; CTA score can flag redesign targets. Human review still needed when layout sabotage coexists with on-path copy (FN cases).
- **What stays LLM-drafted:** narrative synthesis, PRD prose, and redesign suggestions. Jev is a judgment layer, not a drafting replacement.

## Limits

- **Tiny N** (35 / 27 / 21) and **single labeler**—no inter-annotator agreement.
- **Demo product context** (PetCare / PetID); E3 is majority synthetic (13/21); E2 has 2 synthetics.
- Ukrainian interview passages with English instructions (E1); screen **text descriptions**, not pixels (E3).
- Perfect or near-perfect AUC on E2/E3 may not hold on messier real PRDs and screens.
- No production A/B of workflow time saved; exploratory only.

## Next steps

1. Optional E1 severity recalibration (shorter criteria, bilingual state, or few-shot exemplars).
2. Expand E2/E3 with real non-demo PRDs and pixel-level or Figma-exported screens; add a second labeler for κ.
3. Wire high-precision noul gates into Cursor PM skills as optional lint steps (threshold + human override).
4. Track calibration (Brier / reliability) as N grows; do not ship automated blocking on severity-style scores until exact match improves.

## Stability (reproducibility)

A follow-up **K=5** identical-request study on a stratified subsample (E1=12, E2=10, E3=8; 150 API calls, 0 failures) asks whether answers *repeat*, not whether they match gold. Overall **90%** of items were perfect 5/5 on discrete answers and **93.3%** reached ≥4/5; all **18** noul fields on E2/E3 met documented stable thresholds (range ≤0.10, std ≤0.05). E2 and E3 were **100%** perfect; residual flips are E1 severity near ordinal boundaries (`e1-016`, `e1-024`) plus one low-confidence theme flip (`e1-008`). **Bottom line:** noul product gates look stable enough for optional pre-review lint; E1 severity exact labels do not. Full tables and discussion: [`paper/STABILITY.md`](STABILITY.md), `runs/stability/metrics.md`.

## Artifacts index

| Experiment | Dataset | Rubric | Runs |
| --- | --- | --- | --- |
| E1 | `datasets/e1_interview_passages.jsonl` | `datasets/e1_rubric.md` | `runs/E1/` |
| E2 | `datasets/e2_prd_sections.jsonl` | `datasets/e2_rubric.md` | `runs/E2/` |
| E3 | `datasets/e3_screens.jsonl` | `datasets/e3_rubric.md` | `runs/E3/` |

Per-experiment drafts retained: `paper/DRAFT-E1.md`, `DRAFT-E2.md`, `DRAFT-E3.md`. This file consolidates them.
