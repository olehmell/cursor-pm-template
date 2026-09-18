## Use Case 04: Jev product-work tests (TypeSafe)

Workspace for testing **Jev** (TypeSafe System One) on the three PM-template product workflows: data analysis, PRD writing, and prototyping.

Live docs: [docs index](https://docs.typesafe.ai/llms.txt), [use-case map](https://docs.typesafe.ai/concepts/use-case-map.md), [HTTP API](https://docs.typesafe.ai/api.md).

## Principle

Cursor/LLMs draft narratives and UI. **Jev owns typed product judgments** (route / score / verify) with probabilities code can act on.

## Layout

| Path | Purpose |
| --- | --- |
| `memory/` | Plan, decisions, session log |
| `cases/` | Concrete Jev cases per PM use case |
| `artifacts/` | Live run outputs |
| `scripts/` | Call helpers (`TYPESAFE_API_KEY`) |

## Rollout order

1. **01 data-analysis** — theme + severity on interviews
2. **02 prd-writing** — MVP-scope + measurable-metric gates
3. **03 prototyping** — hypothesis fit + CTA clarity

See `memory/plan.md`.
