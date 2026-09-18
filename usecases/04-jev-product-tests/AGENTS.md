## Rules for this use case

- Prefer TypeSafe/Jev for structured judgments; do not fake Jev responses with an LLM.
- Never commit API keys. Use env `TYPESAFE_API_KEY` only.
- Store run outputs under `artifacts/`; keep case definitions in `cases/`.
- Update `memory/` when a decision or finding changes.
- Follow https://docs.typesafe.ai — do not invent API shapes.
- Scope stays the three PM use cases only (analysis, PRD, prototyping).
