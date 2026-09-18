# E1 gold rubric (frozen before Jev runs)

**Product decision:** Which interview passages matter for **activation**, and how severe is the barrier?

**Activation definition (frozen):** User completes feeding-plan setup within 7 days of first open (PetCare demo context: schedule, portions, reminders for one or more pets).

Labeler: single PM (Oleh) with this rubric; labels assigned offline before any Jev call. Date frozen: 2026-09-18.

## theme (choice)

| Label | Include when the passage primarily concerns… |
| --- | --- |
| `setup_friction` | Difficulty starting / configuring care routines, apps, documents, feeding schedules, onboarding checklists, or first-weeks adaptation that blocks getting set up. |
| `notifications` | Forgetting doses/vaccines/walks; need for reminders, calendars, push signals, periodic check-ins. |
| `multi_pet` | Balancing or differentiating care across **two or more** animals (time split, shared feeding times, different needs). |
| `trust_data` | Distrust or uncertainty about information sources (Google horror, conflicting sites, shady food labels, unreliable apps, clinic records fragmentation). |
| `other` | Emotional benefits, community, travel, gadgets, SOS clinic search, etc. that do not clearly fit the four above. Prefer `other` over stretching a theme. |

**Tie-break:** If two themes apply, pick the one most relevant to whether the user would finish feeding-plan setup in 7 days. Mentions of “reminders about vaccines” → `notifications` even if vaccines are medical. Multi-pet feeding schedule → `multi_pet` over `setup_friction`.

## activation_severity (score levels)

Ordered low → medium → high relative to the activation definition.

| Level | Meaning |
| --- | --- |
| `low` | Mild annoyance or nice-to-have; unlikely to stop feeding-plan setup within 7 days. |
| `medium` | Noticeable friction; may delay setup or cause incomplete configuration, but a motivated user can finish in a week. |
| `high` | Strong barrier; confusion, panic, lost docs, or broken trust that plausibly prevents completing feeding-plan setup within 7 days. |

**Notes for severity:** Severity is about **activation impact**, not overall life severity. A dramatic disease story can still be `low` for feeding-plan activation if it does not affect setup. First-week chaos and “I don’t know what to feed / when” skew `high`.

## Passage unit

Quote or 2–4 sentence span from `usecases/01-data-analysis/interviews/`. Prefer respondent speech over interviewer. Keep original Ukrainian wording; light cleanup of ASR only when meaning is clear.
