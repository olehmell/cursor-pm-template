## Repository Overview

This is a **workspace template for Product Managers** demonstrating AI-assisted PM workflows using the fictional PetCare app (a mobile app for pet feeding planning and care). The repository contains three main use cases (data analysis, PRD writing, prototyping) and a shared company context.

## Project Structure

```
cursor-meetup/
├── company-context/        # Shared PetCare product context
│   ├── COMPANY.md         # Mission, metrics (Q1 2026), team structure
│   ├── PRODUCT.md         # Product principles, features, roadmap
│   ├── PERSONAS.md        # User personas (Alex, Chloe, Jordan)
│   └── COMPETITIVE.md     # Competitive landscape
├── usecases/
│   ├── 01-data-analysis/  # Interview & metrics analysis workflows
│   ├── 02-prd-writing/    # PRD writing with templates & review
│   └── 03-prototyping/    # React prototyping environment
└── agents/
    └── reviewer/          # Stakeholder/persona review agent
```

## Key Concepts

### AGENTS.md Files
This repository uses `AGENTS.md` files as **instruction bundles** scoped to folders. These contain:
- Rules and constraints for that workflow
- Expected output formats
- Framework preferences
- Quality standards

Always check for `AGENTS.md` in the relevant folder before performing tasks.

### Company Context
All work should reference `company-context/` files. The fictional PetCare context includes:
- **North Star Metric**: Weekly Active Households with Updated Stock or Confirmed Refill
- **Product Principles**: "Low-effort setup", "At a glance clarity", "Pet-first"
- **Key Personas**: Alex (Data-Driven Guardian), Chloe (First-Time Protector), Jordan (Collaborative Caregiver)

## Use Case 1: Data Analysis

**Location**: `usecases/01-data-analysis/`

**Purpose**: Analyze interview transcripts and product metrics to produce actionable insights.

**Key Instructions** (from `AGENTS.md`):
- Prioritize findings that impact the North Star Metric
- Reference specific personas when identifying pain points
- Format reports with: Executive Summary, Key Findings (with evidence), Recommendations (ranked by impact/effort)
- Use Value Proposition Canvas (Pains, Gains, Jobs) framework
- Use KYIV prioritization framework (see `KYIV-framework.md`)

**Data Sources**:
- `interviews/`: Qualitative interview transcripts
- `metrics/`: CSV files with user behavior data (breed_info, dogs_dataset, user-survey-responses)

**Outputs**: Save artifacts to `artifacts/` folder (e.g., `value-proposition-canvas.md`, `activation-insights.md`)

**Python Analysis**: For large CSV files, suggest Python/Pandas code snippets. A virtual environment exists at `.venv/` (Python 3.13).

## Use Case 2: PRD Writing

**Location**: `usecases/02-prd-writing/`

**Purpose**: Write PRDs using templates and get stakeholder/persona reviews.

**Key Instructions** (from `AGENTS.md`):
- Always check `@PRODUCT.md` for alignment with "Low-effort setup" and "At a glance clarity" principles
- Reference `@COMPANY.md` when defining success metrics
- Consider impact on all three personas (Alex, Chloe, Jordan)
- **CRITICAL**: Ask questions from `socratic-questioning.md` BEFORE writing the PRD
- Plan to include persona reviews and reviewer agent feedback in separate artifacts

**Template**: Use `templates/Lennys-PRD-Template.md` as the base structure.

**Review Workflow**:
1. Answer Socratic questions first
2. Write PRD draft
3. Add Mermaid diagrams for flows
4. Get review from `@reviewer` agent (references `reviewers/prd-review.md`)
5. Create persona-specific review artifacts

**Outputs**: Save to `artifacts/` folder.

## Use Case 3: Prototyping

**Location**: `usecases/03-prototyping/`

**Purpose**: Turn PRDs or screenshots into interactive React prototypes.

**Tech Stack**:
- React 18.2 with TypeScript
- Vite (build tool)
- Tailwind CSS 3.3
- Lucide React (icons)
- Additional: clsx, tailwind-merge

**Key Instructions** (from `AGENTS.md`):
- Use React + TypeScript + Tailwind CSS
- Use Lucide React for all icons
- Ensure responsive design with "clean and polished" look
- If working from a PRD from `usecases/02-prd-writing/`, stick to those requirements

**Commands**:
```bash
cd usecases/03-prototyping/

# Install dependencies (first time only)
yarn install

# Run development server
yarn dev

# Build for production
yarn build

# Preview production build
yarn preview
```

**Development**: Vite dev server runs on default port (usually 5173). Component files should be created in the appropriate structure with TypeScript.

## Reviewer Agent

**Location**: `agents/reviewer/`

**Purpose**: Provide critical, constructive, persona-driven feedback on PRDs and analysis.

**Knowledge Base**: Always references full `company-context/` (COMPANY.md, PRODUCT.md, PERSONAS.md, COMPETITIVE.md).

**Response Format**:
1. Executive Summary of Feedback
2. Persona Perspectives (at least 2 relevant ones)
3. Strategic Alignment Score (1-10)
4. Actionable Recommendations (bulleted list)

**Review Types**:
- PRD reviews: Uses `reviewers/prd-review.md` template
- Data analysis reviews: Uses `reviewers/analysis-review.md` template

**Usage**: Reference `@reviewer` and the artifact to review.

## Important Constraints

### For Data Analysis
- Always include direct quotes or specific data points as evidence
- Rank recommendations by impact/effort
- Create separate files in `artifacts/` for each deliverable

### For PRD Writing
- Must complete `socratic-questioning.md` before writing
- Include "Persona Impact" section covering Alex, Chloe, and Jordan
- Add Mermaid diagrams for user flows
- Success metrics must reference company metrics (activation, retention, North Star)

### For Prototyping
- Components must be responsive
- Follow TaskFlow tech stack (from PRODUCT.md)
- No generic development practices or unnecessary complexity

## Workflow Philosophy

This template demonstrates **low-friction PM workflows**:
1. **Context is centralized** (`company-context/`) and reused across use cases
2. **Instructions are scoped** (folder-level `AGENTS.md` files)
3. **Artifacts are versioned** (saved to `artifacts/` folders)
4. **Reviews are systematic** (Reviewer agent provides consistent feedback)

Scripts should be placed in `./scripts/` subfolder of the relevant use case.
