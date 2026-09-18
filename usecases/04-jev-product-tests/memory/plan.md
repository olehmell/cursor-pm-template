# Plan: Jev on PM-template use cases

Scoped to **01 data-analysis**, **02 prd-writing**, **03 prototyping** only.

## Shared pattern

1. State = use-case artifacts + `@company-context`
2. Questions = noul / choice / score (one narrow judgment each)
3. Code/agent = thresholds, file writes to `artifacts/`
4. Validate = small labeled gold set before trusting in the workflow

## 01 — Data analysis

| Judgment | Primitive | Product use |
| --- | --- | --- |
| Theme of a passage | choice | consistent tagging |
| Activation pain? | noul | filter noise |
| Severity for activation | score | prioritize |
| Quote supports hypothesis? | noul | evidence check |
| Metric contradicts claim? | noul | qual↔quant bridge |

**First build:** theme + severity on `usecases/01-data-analysis/interviews/`.

## 02 — PRD writing

| Judgment | Primitive | Product use |
| --- | --- | --- |
| Section is MVP-scoped? | noul | scope-creep flag |
| Success metric measurable? | noul | crisp metrics |
| Persona fit | choice | audience check |
| Claim supported by evidence? | noul | anti-handwave |
| Reviewer severity by lens | score | structured review |

**First build:** MVP-scope + measurable-metric on one PRD in `artifacts/`.

## 03 — Prototyping

| Judgment | Primitive | Product use |
| --- | --- | --- |
| Screen advances hypothesis? | noul | cut vanity screens |
| CTA clarity | score | copy review |
| Tone supportive not spammy? | noul | tone gate |
| Feedback → friction bucket | choice | synthesize tests |

**First build:** hypothesis fit + CTA clarity on the PetID screen list.

## Out of scope

Support triage demos, extra template modules, replacing LLM drafting with Jev.
