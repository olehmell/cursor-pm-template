## Cursor workspace template for Product Managers (PetCare example)

This repository is a **starter template** that helps a PM quickly set up an AI-assisted workspace for their own product tasks (analysis → PRD → prototype). It ships with a realistic (fictional) example context: **PetCare** (a mobile app for pet feeding planning and care).

## Template structure

The template is split into three use cases:

1. **[01-data-analysis](usecases/01-data-analysis/)**: Analyze interview transcripts and product metrics, then produce a clear insights report.
2. **[02-prd-writing](usecases/02-prd-writing/)**: Write a PRD from a template, add diagrams, and get stakeholder-style review.
3. **[03-prototyping](usecases/03-prototyping/)**: Turn PRDs or screenshots into an interactive React prototype.

## Company context (shared across use cases)

All exercises use the PetCare context in `company-context/`:
- `COMPANY.md`: Mission, metrics (Q1 2026), team structure.
- `PRODUCT.md`: Product principles, key features, roadmap.
- `PERSONAS.md`: User personas (Alex, Chloe, Jordan).
- `COMPETITIVE.md`: Competitive landscape.

Tip: include `@company-context` in your prompts so the model has the full product context.

## How instructions work (`AGENTS.md`)

This repo uses `AGENTS.md` files as **instruction bundles** (rules, constraints, expected output format) scoped to folders.

- In **Cursor**, these instructions are picked up as rules and help keep outputs consistent.
- In **Claude Code**, the same Markdown instruction files can be reused as a starting point (e.g., by referencing or copying the relevant instructions into your Claude setup).

## Agents

- **[Reviewer Agent](agents/reviewer/)**: Reviews PRDs and analysis from different stakeholder/persona perspectives.

## Getting started

1. Update `company-context/` to match your product (or keep PetCare as the demo).
2. Pick a module in `usecases/` (start with `usecases/01-data-analysis/`).
3. Follow the `README.md` inside that folder and save outputs to its `artifacts/`.
