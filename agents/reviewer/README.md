## Reviewer Agent (PetCare)

This agent helps Product Managers get high-quality feedback on their artifacts (PRDs, analyses, plans) from different stakeholder and persona perspectives.

## How to use

1. In Cursor Chat, include the agent folder as context: `@reviewer`.
2. Ask for a review of a specific file or from a specific persona angle, for example:
   - `@reviewer Review this PRD: @artifacts/smart-food-scanner-prd.md`
   - `@reviewer Review this from Alex’s perspective (Data-Driven Guardian).`
   - `@reviewer How would this feature help Chloe (First-Time Protector)?`

## What it checks

Using `@company-context`, the agent evaluates:
- Alignment with company goals (activation, retention, North Star metric).
- Persona impact (Alex, Chloe, Jordan) and tradeoffs across segments.
- Competitive differentiation and positioning.
- Feasibility, risks, and unclear requirements.

## Review structure (what you should expect)

Each review includes:
1. **Executive Summary of Feedback**
2. **Persona Perspectives** (at least 2 relevant ones)
3. **Strategic Alignment Score** (1–10)
4. **Actionable Recommendations**
