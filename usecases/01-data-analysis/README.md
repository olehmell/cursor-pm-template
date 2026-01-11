## Use Case 01: Data Analysis (PetCare)

This module is a template for using Cursor to analyze raw product inputs: qualitative interviews + quantitative metrics. Your goal is to turn messy data into a structured, decision-ready narrative.

## What you will do

1. **Interview analysis**: Review transcripts in `interviews/` and identify the biggest onboarding + feeding plan setup pain points.
2. **Metrics analysis**: Use datasets in `metrics/` to validate or challenge your interview-based hypotheses.
3. **Insight report**: Produce a structured report with concrete recommendations to improve **Activation Rate**.

## How to work with Cursor (example prompts)

### Step 1: Qualitative analysis (interviews)

In Cursor Chat, add context and ask for evidence-based insights:

`@interviews @company-context Analyze these interviews. What are the top 3 onboarding problems preventing PetCare users from activating? Use direct quotes as evidence.`

### Step 2: Quantitative analysis (metrics)

Attach the metrics folder and connect the dots:

`@metrics @company-context Look at the data. Do we see a conversion drop at the "Feeding Plan Setup" step? How does it correlate with the interview pain points?`

### Step 3: Create a synthetic persona (optional)

Use insights to generate an additional persona that represents an unmet segment:

`@company-context @PERSONAS.md Based on the interviews, create a new persona: a pet owner who could not figure out feeding plan setup in PetCare. Include goals, frustrations, and a short story.`

## Expected artifacts (save to `artifacts/`)

- **Value Proposition Canvas (Jobs / Pains / Gains)**: `value-proposition-canvas.md`
- **Activation insights report** (recommended): `activation-insights.md`

## Tips

- Use **Composer** for longer reports.
- Ask for **direct quotes** and **specific data points** so conclusions are defensible.
- For larger CSVs, ask for a **Python/Pandas** snippet (or write a small JS/TS script in `scripts/`).
