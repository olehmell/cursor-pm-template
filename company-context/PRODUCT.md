# PetCare Product Overview

**Your complete guide to the PetCare app**

---

## What is PetCare?

PetCare is a mobile app that helps pet owners **plan feeding**, **track how much food is left**, and **get reminders before they run out**. Over time, PetCare becomes the “autopilot” for recurring pet care (food, consumables, and later health records).

### Core Value Proposition

**For pet owners who forget to buy food (and feel guilty when they do),** PetCare provides a simple, low-effort way to **see days remaining, get timely nudges, and reorder at the right moment.** Unlike generic trackers or shop apps, PetCare focuses on **planning + reminders first**, then adds **local delivery** through partners.

---

## Product Philosophy

### Key Principles

**1. Low-effort setup**
- First feeding plan setup should take minutes, not 20+ taps
- Defaults are opinionated (users can adjust later)

**2. “At a glance” clarity**
- The home screen answers: “Are my pets covered?”
- Show days remaining and the next key action

**3. Gentle, useful notifications**
- Reminders must feel supportive, not spammy
- Time + tone matter as much as the content

**4. Shared responsibility**
- Households often have multiple caretakers
- One source of truth prevents “I thought you bought it”

**5. Local-first partnerships**
- We win by integrating into local purchase habits
- We start with “demand proxy” CTAs, then deepen partnerships

---

## Core Features (MVP)

### 1. Feeding Plan Setup (one or multiple pets)

**What users can do:**
- Add pet(s) and basic profile data
- Set daily consumption (grams/servings)
- Add multiple food types (track in parallel)

**Why it matters:**
- Without a plan, “days remaining” is unreliable
- Multi-food tracking is common (wet + dry; different brands)

### 2. Stock Tracking (“How much is left?”)

**What users can do:**
- Enter starting amount (manual)
- Update stock with minimal friction (quick edit)
- See days remaining / number of feedings left

### 3. Notifications

**What users can do:**
- Feeding-time reminders
- Low-food alerts (“reorder soon”)
- Household notifications (shared account)

### 4. “Order Food” (Demand Proxy)

**What users can do (MVP):**
- Tap a CTA to “Order food”
- For MVP this can redirect to maps/search (validate intent before building checkout)

---

## Hypothesis Backlog (Examples)

These are examples of MVP hypotheses we test via UX and messaging experiments:

1. If we auto-calculate “days remaining”, users will reduce “forgot to buy food” incidents.
2. If “add food” supports barcode scanning, conversion to paid will increase.
3. If users can track multiple foods, weekly app visits will increase.
4. If feeding reminders exist, daily visits will increase.
5. If low-food alerts exist, repeat stock updates will increase.
6. If an “order” CTA exists, we can validate willingness to buy from the app.
7. If households can share access, WAU increases.
8. If households can share access, repeat “stock updates” increase.
9. If we offer a food database / quick select, setup time drops meaningfully.
10. If users can “reuse last plan”, retention improves and setup time drops.

---

## Roadmap (Simplified)

### MVP (Now)

✅ Feeding plan setup  
✅ Multi-food tracking  
✅ Days remaining dashboard  
✅ Notifications (feeding + low food)  
✅ Multi-device / shared access (basic)  
✅ “Order food” demand proxy CTA

### MSP (Soon)

📅 Partner-based delivery checkout (pilot city)  
📅 Smart portion adjustment as pets grow (age/weight-based suggestions)  
📅 Home screen widget (quick check of days remaining)

### MLP (Later)

🔬 Auto-reorder (subscriptions)  
🔬 Delivery status sync (order shipped/delivered)  
🔬 Personalized nutrition guidance (contextual, not “generic AI”)  
🔬 Extend beyond food to other consumables (litter, treats, meds)

---

## Product Metrics

### North Star Metric

**Weekly Active Households with Updated Stock or Confirmed Refill**  
Rationale: ties usage directly to the core “don’t run out” outcome.

### Product Health Metrics

**Activation**
- Definition: completes feeding setup within 7 days

**Retention**
- 4-week retention (cohort-based)

**Notification Value**
- Opt-in rate and “open after notification” rate

**Reorder Intent**
- “Order” CTA click-through rate (and later click → purchase conversion)

---

## Pricing & Packaging (Current Direction)

**Free**
- 1 pet
- Basic feeding plan + days remaining
- Limited notifications

**Plus (Subscription)**
- Multiple pets + multiple caretakers
- Advanced notifications and reminders
- Widgets and “reuse last plan”

**Partner Revenue (Pilot)**
- Affiliate/referral commissions from partner shops (where applicable)

---

## Technology Stack (Current)

**Mobile:** React Native  
**Backend:** Node.js  
**Data:** Postgres (core), analytics pipeline (events + cohorts)

---

## Product Documentation

Product docs live in Notion and are based on internal discovery notes and MVP hypotheses (source context: `https://www.notion.so/omell/13e49d656ffc80e4b4b3d14b074d5a01`).
