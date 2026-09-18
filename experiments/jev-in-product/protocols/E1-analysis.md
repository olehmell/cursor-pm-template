# Protocol E1 — Data analysis judgments

## Product decision
Which interview passages matter for **activation**, and how severe is the barrier?

## Judgments
1. `theme` (choice): setup_friction | notifications | multi_pet | trust_data | other
2. `activation_severity` (score): low | medium | high vs “completes feeding plan setup within 7 days”

## Dataset
- Source: `usecases/01-data-analysis/interviews/`
- Unit: passage (quote or 2–4 sentence span)
- Target size: 30–50 passages (generate more via split if thin)
- Labels: freeze a short rubric; label offline before seeing Jev

## Run
POST systemone with state `{passage, themes, activation_definition}` and the two questions.

## Metrics
- Theme: accuracy vs gold; confusion matrix
- Severity: exact match + adjacent-allowed; optional Spearman if mapped 1–3
- Note high-confidence wrong answers

## Artifact
`runs/E1/` + update paper sections 4–6
