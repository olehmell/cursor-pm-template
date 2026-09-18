# Did we misunderstand Jev’s value?

## What we tested (v1)
Offline gold-label accuracy on PM artifacts: exclusive theme Choice + severity Score on interviews; binary PRD/prototype nouls. Measured like a classifier bakeoff.

## What TypeSafe says Jev is for
- **AI-powered software**, not agents: code owns control flow; Jev supplies narrow common-sense judgments ([how to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md)).
- **Composable**: structured, parallel, comparable, ~100ms, calibrated, self-consistent.
- **Decompose** broad judgments into atomic questions; **compose in code** (weights, thresholds, confidence gates).
- **Not for**: generation, math/counting, date arithmetic, heavy indirection, fat irrelevant state ([jev-1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md)).

## What our numbers actually say
| Pattern | Result | Interpretation |
| --- | --- | --- |
| Narrow noul gates (E2/E3) | 90–100% + high stability | Plays to Jev: literal yes/no that code can `if` on |
| Exclusive theme Choice (E1) | ~69% | Forced one label when passages are multi-label; Choice is relative, not absolute |
| Severity Score exact (E1) | ~34% exact, boundary flip in stability | Score levels weak as numeric truth; jaggedness warns against treating score as magnitude |
| Stability | Noul 100% stable; E1 flaky at boundaries | Product lint OK; soft rubrics not |

**Likely mistake:** treating Jev as “better LLM tagging for reports” instead of “programmable sensors inside a product workflow.”

## Better product use cases (v2)

### U1 — Multi-label insight sensors (replace E1 theme Choice)
For each interview passage, **parallel nouls** (`setup_friction?`, `notifications?`, `trust_data?`, `activation_blocker?`) + optional composite weight in code. Rank passages by `activation_blocker` noul. Matches “decompose spam” guidance; allows multi-theme truth.

### U2 — PRD CI lint (productize E2)
On PRD save/PR: speculative fan-out of many nouls (MVP scope, measurable metric, invents number?, contradicts COMPANY.md) → confidence-gate fail/warn/pass. Value is the **workflow**, not the offline accuracy table.

### U3 — Agent context guard (new, high TypeSafe fit)
Before an LLM writes analysis/PRD: classify/rerank retrieved `company-context` chunks (RAG cookbook); citation-check claims against source files. Jev verifies; LLM generates.

### U4 — Prototype test triage (evolve E3)
User-test notes → parallel friction nouls + composite “redesign priority” in code; escalate mid-noul to human.

### U5 — Template skill router (meta)
Incoming PM ask → Choice over {analysis, prd, prototype, none} + noul “needs a skill at all?” (skill_suggestion cookbook). Ships inside Cursor template itself.

### U6 — Feature → classical model (research stretch)
Export nouls/scores as features; train small model on labeled activation outcomes (autoresearch cookbook). Jev as feature factory, not final judge.

## Recommended next experiment
**U1 on the same 35 passages** (re-label gold as multi-label nouls) + compare ranking quality vs old exclusive theme. Same data, better question shape — tests the reframing cheaply.
