# Case 01: Interview theme + activation severity

## Intent
Tag an interview passage with a theme and score how badly it hurts activation — first judgment for use case 01.

## State (fill from a real interview file)

```json
{
  "passage": "REPLACE_WITH_QUOTE",
  "themes": ["setup_friction", "notifications", "multi_pet", "trust_data", "other"],
  "activation_definition": "Completes feeding plan setup within 7 days"
}
```

## Questions

```json
{
  "theme": {
    "type": "choice",
    "instructions": "Which theme best fits `passage`?",
    "criteria": {
      "setup_friction": "Hard to set up feeding plan or onboarding steps",
      "notifications": "Reminders tone, timing, or spam concerns",
      "multi_pet": "Household or multiple-pet coordination",
      "trust_data": "Does not trust stock/days-remaining numbers",
      "other": "Does not fit the themes above"
    }
  },
  "activation_severity": {
    "type": "score",
    "instructions": "How much does `passage` indicate a barrier to activation as defined?",
    "criteria": {
      "low": "Mild annoyance; user would still finish setup",
      "medium": "Likely to delay or abandon without help",
      "high": "Blocks completing feeding plan setup"
    }
  }
}
```

## Success criteria
- Theme is stable across paraphrase of the same quote.
- Severity ranks known hard blockers above mild preference comments.

## Runs
_None yet._
