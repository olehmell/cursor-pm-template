# Experiment: Jev inside product tasks

**Not a new PM use case.** Jev is a judgment engine we apply *inside* the existing template workflows:

1. Data analysis (`usecases/01-data-analysis`)
2. PRD writing (`usecases/02-prd-writing`)
3. Prototyping (`usecases/03-prototyping`)

Goal: design judgments → build/find datasets → run tests → write a **short paper** on what works for product work.

## Structure

| Path | Purpose |
| --- | --- |
| `paper/` | Short paper draft + outline |
| `datasets/` | Labeled / generated evaluation sets |
| `protocols/` | How we run each product-task experiment |
| `runs/` | Raw Jev outputs + scored summaries |

## Method (shared)

1. Pick a concrete product decision inside one of the three tasks.
2. Express it as TypeSafe questions (noul / choice / score) over real state.
3. Build a small labeled dataset (gold judgments from PM criteria).
4. Call Jev; compare to gold; report agreement, calibration, failure modes.
5. Write up: when Jev helps product work vs when it does not.

Live API: `POST https://api.typesafe.ai/v1/systemone` with `TYPESAFE_API_KEY`.
Docs: https://docs.typesafe.ai/llms.txt
