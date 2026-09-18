# U5 gold rubric — Template skill router (frozen before Jev runs)

**Product decision:** For a PM ask in this Cursor template, which of the three usecase skills (if any) should load?

**Roster (frozen):** `data-analysis` | `prd-writing` | `prototyping` — see `u5_skill_roster.json`.

Labeler: single PM (Oleh) with this rubric; gold assigned offline **before** any Jev call. Date frozen: 2026-09-19 (Europe/Kiev).

## Labels

| `gold_skill` | Use when the ask primarily… |
| --- | --- |
| `data-analysis` | Analyzes interviews, survey quotes, metrics/CSVs, funnels, or activation insight synthesis → report/canvas recommendations. |
| `prd-writing` | Writes, drafts, scopes, reviews, or diagrams a PRD / feature spec / roadmap section using templates or stakeholder review. |
| `prototyping` | Builds or iterates an interactive UI prototype (React screens, flows, clickable MVP) to validate a hypothesis. |
| `null` | No template skill should load: definitions/explainers, greetings, scheduling/calendar, unrelated coding, general advice with no artifact workflow, or asks outside the three usecases. |

## Tie-breaks

1. **Artifact + template workflow wins over chat.** If a careful PM would open a usecase folder and follow its README/AGENTS, label that skill — not `null`.
2. **Analysis vs PRD:** Interview/metrics → insights = `data-analysis`. Feature requirements / Lenny template / reviewer loop = `prd-writing`. “Turn insights into a PRD” → `prd-writing` (writing is the ask). “What did interviews say about activation?” → `data-analysis`.
3. **PRD vs prototype:** Spec/doc/Mermaid in markdown = `prd-writing`. Runnable React screens / yarn-dev prototype = `prototyping`. “PRD then prototype” → prefer the **primary verb** in the ask; if equal, `prd-writing` (doc-first in this template).
4. **Ambiguous but covered:** Prefer the skill whose documented workflow matches the **output artifact** named in the ask.
5. **Uncovered / prose-only:** “What is a North Star metric?”, “hello”, meeting times, leetcode, general product theory with no template artifact → `null`.

## Metrics (post-run)

- **wrong_route:** among `gold_skill ≠ null`, share where `pred ≠ gold` or `pred = null`.
- **needless_route:** among `gold_skill = null`, share where `pred ≠ null`.
- **accuracy:** overall exact match including null.
- Confusion matrix over `{data-analysis, prd-writing, prototyping, null}`.

## Router decision (code, not gold)

Gate = mean of oriented gate nouls (`prose_suffices` inverted). If gate < 0.30 → suggest nothing. Else if max(fits) < 0.30 → nothing. Else winner = Choice `which` (fits only gate whether to speak; Choice picks which).
