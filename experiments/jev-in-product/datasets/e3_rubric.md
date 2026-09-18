# E3 gold rubric (frozen before Jev runs)

**Product decision:** Does this prototype screen advance the PetID upload hypothesis, and (when a primary CTA exists) how clear is that CTA?

**Hypothesis (frozen):** Users want to store pet medical documents in the app via photo upload.

Labeler: single PM (Oleh) with this rubric; labels assigned offline before any Jev call. Date frozen: 2026-09-18.

Gold encoding:
- `advances_hypothesis`: `1` = yes, `0` = no
- `cta_clarity`: `low` | `medium` | `high`, or `null` if no primary CTA applicable (skip in CTA metrics)

## advances_hypothesis (noul → gold 1/0)

Ask: *Does this screen meaningfully advance testing or delivering “store pet medical docs via photo upload”?*

| Gold | Include when… |
| --- | --- |
| `1` | Screen is on the upload/store/view path: invite photo capture, preview/confirm upload, upload progress/success, empty state that prompts document upload, gallery of stored docs, or viewer of stored medical photos. |
| `0` | Unrelated product surface (feeding, community, clinic map, profile/privacy, marketing invite), delete-only confirmation that removes docs without advancing store, text-date vaccine entry without photo upload, or copy that never mentions medical docs / photo upload. |

**Tie-break:** Prefer `0` if the screen could ship without teaching or enabling photo upload of medical docs. Viewing/storing already-uploaded docs counts as `1` (closes the value loop). Delete confirmation alone → `0`.

## cta_clarity (score → low|medium|high)

Ask only when a **primary CTA** exists (button/FAB/link that is the main next action). Skip (`null`) for auto-progress screens, success flashes with no button, or pure viewers with only back/swipe chrome.

| Gold | Include when… |
| --- | --- |
| `high` | One clear primary control with action label matching the intended next step (e.g. “Take Photo”, “Upload”, “Upload Document”); visually dominant (primary style / full-width). |
| `medium` | Primary exists but is icon-only, slightly ambiguous, or secondary-styled while still discoverable; or Cancel is the clear safe action on a destructive modal. |
| `low` | Vague labels (“Next”, “Continue”, “OK”), competing equal-weight CTAs, primary action buried under Skip/Share, or labeled action that does not match upload/store intent. |

**Tie-break:** Score clarity of the *primary* control for a user trying to complete photo upload of a medical doc — not overall visual polish.

## Item unit

Screen description / copy snippet derived from `usecases/03-prototyping/` (8 flow screens + Delete modal) plus marked `synthetic: true` negative controls. Prefer verbatim UI copy from `src/screens/`.
