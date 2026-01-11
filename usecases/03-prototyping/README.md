## Use Case 03: Rapid Prototyping in Cursor

This module is a template for the most “wow” Cursor workflow for PMs: turning a PRD (or a screenshot) into a working interactive prototype.

## What you will do

1. **Build a prototype UI**: Generate UI for a feature from your PRD (for example: Dark Mode toggle, Team Dashboard).
2. **Iterate on design**: Improve the prototype with simple text instructions (“Make buttons more rounded”, “Add a team load chart”).
3. **Test locally**: Run the prototype and validate it in the browser.

## How to work with Cursor (example prompts)

### Step 1: Generate code

Go to `usecases/03-prototyping/` and open Composer (`Cmd+I`).

Example prompt:

`@company-context Create a React component AppearanceSettings.tsx that allows switching the TaskFlow theme. Use Tailwind CSS.`

### Step 2: Install dependencies (first time only)

`yarn install`

### Step 3: Run the dev server

`yarn dev`

## Tips

- Paste a Linear/Asana screenshot and ask: “Recreate this page in TaskFlow style.”
- Use **Lucide React** for icons (already in `package.json`).
- Ask Cursor to generate a small test if you want (unit or UI-level).
