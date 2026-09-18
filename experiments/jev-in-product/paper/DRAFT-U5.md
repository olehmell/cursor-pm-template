# Draft: Template skill router with System-One (U5)

_Working draft — U5 results filled 2026-09-19. Exploratory; small N._

## Abstract

PM Cursor templates expose multiple usecase “skills” (data analysis, PRD writing, prototyping). Agents that guess from a roster often load the wrong skill or load one when none fits. We adapt TypeSafe’s skill_suggestion cookbook to a **3-skill** roster: one `systemone` call combining Choice `which`, adapted gate nouls, and per-skill `fits` nouls. On **N=48** frozen PM asks (gold labeled before API), live Jev (`jev-latest` → `jev-1.13.0`) achieved **wrong_route 0.0%** (0/38 covered) and **needless_route 10.0%** (1/10 uncovered); overall accuracy **97.9%**. Gate mean separated covered (0.76) from null (0.24). One miss: a CEO status email was routed to `data-analysis` at gate 0.39 / fits 0.30 on the boundary.

## Introduction

E1–E3 tested Jev *inside* each usecase (theme tags, PRD gates, prototype CTAs). U5 asks a different product question: **which template skill to load**, if any — the routing surface before those workflows run. The TypeSafe cookbook uses two calls over 182 Hermes skills; with three documented usecases we collapse to one call.

## Method

1. **Roster:** short `description` + `description_full` from usecase READMEs (`datasets/u5_skill_roster.json`).
2. **State:** `{request, context}` — the PM ask.
3. **Questions (one request):** Choice `which` (3 options); gate nouls `acts_on_product_artifacts`, `would_follow_template_workflow`, `prose_suffices` (inverted); `fits::{name}` × 3.
4. **Decision:** gate = mean(oriented); if gate < 0.30 or max(fits) < 0.30 → null; else Choice winner.
5. **Gold:** single PM labeler; rubric in `datasets/u5_rubric.md` frozen before any call.
6. **Run:** `scripts/run_u5_jev.py`; 48/48 ok, 0 failures.

## Findings

| Metric | Result (N=48) |
| --- | --- |
| wrong_route | 0/38 = **0.0%** |
| needless_route | 1/10 = **10.0%** |
| accuracy (incl. null) | 47/48 = **97.9%** |

Confusion: diagonal perfect on all three skills; sole off-diagonal is null→`data-analysis` (`u5-047`).

**Gate calibration:** mean gate on gold-covered 0.760 vs gold-null 0.243 — usable separation at 0.30. Boundary miss had gate 0.390 and max(fits) exactly 0.30.

**What worked:** Clear asks and ambiguous analysis-vs-PRD items (e.g. insights→PRD) resolved correctly via Choice + fits. Uncovered definitions/greetings/scheduling mostly gate-rejected.

**What did not:** Soft “produce a narrative artifact” asks without a usecase folder (`u5-047` CEO email) can clear a low gate/fits bar.

## Workflow implication

Ship an optional `<skill_relevance>` line from this router before loading usecase AGENTS/README context. Prefer silent null over a wrong skill. Consider raising fits threshold slightly (e.g. 0.35) or adding an explicit “status email / chat only” negative example in gate criteria if needless_route matters more than recall.

## Limits

Tiny roster (3), synthetic asks, single labeler, PetCare/PetID demo context, no agent-in-the-loop measurement (router-only, not Hermes load rates).

## Artifacts

`protocols/U5-skill-router.md`, `datasets/u5_*.jsonl|md|json`, `runs/U5/`, `scripts/run_u5_jev.py`, `scripts/compute_u5_metrics.py`.
