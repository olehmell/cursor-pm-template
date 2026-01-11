## Use Case 02: PRD Writing (PetCare)

This module is a template for turning a feature idea into a high-quality PRD using Cursor, including diagrams and stakeholder-style review.

## What you will do

1. **Write a PRD**: Create a PRD for “Smart Food Scanner” or “Household Sync” using `templates/Lennys-PRD-Template.md`.
2. **Add diagrams**: Generate Mermaid diagrams to visualize flows and system behavior.
3. **Review and iterate**: Use the Reviewer agent to critique the PRD from different persona/stakeholder perspectives.

## How to work with Cursor (example prompts)

### Step 0: Ask Socratic questions (required)

Open [socratic-questioning](./socratic-questioning.md), answer the questions, and only then proceed to writing.

### Step 1: Generate a PRD draft

Create a new `.md` file in `artifacts/` and ask Cursor to fill the template:

`@company-context @templates/Lennys-PRD-Template.md Write a PRD for the Smart Food Scanner feature. Jordan (Collaborative Caregiver) needs it to evaluate food ingredients for Mochi. Consider competitors from COMPETITIVE.md.`

### Step 2: Add a Mermaid diagram

`Add a Mermaid diagram to the User Flow section showing: scan barcode → fetch product → show ingredient analysis → save to pet profile.`

### Step 3: Get a review from the Reviewer agent

`@reviewer Review this PRD: @artifacts/smart-food-scanner-prd.md from Jordan’s perspective. What’s missing to make this genuinely useful for a cat with chronic issues?`

## Tips

- Use **Composer** for longer documents.
- Ask Cursor to draft **Success Metrics** using `@COMPANY.md` and your PRD’s scope.
- Mermaid renders best when your file extension is `.md`.
