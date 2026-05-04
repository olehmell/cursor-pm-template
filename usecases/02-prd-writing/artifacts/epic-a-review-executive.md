# Executive Review: Digital Vet Passport PRD

**Reviewer:** Daria Koval (Head of Product)  
**Date:** 18 січня 2026  
**PRD Version:** Draft v1.0  
**Overall Assessment:** ✅ **Strong strategic fit, approve with budget clarifications**

---

## 1. Strategic Alignment

### ✅ Як це вписується в стратегію

**Connection to Company Goals:**

Цей PRD добре aligned з нашими Q1-Q2 2026 priorities:

1. **"Improve activation and setup UX"** (COMPANY.md priority #1)
   - Digital Vet Passport автоматично заповнює профіль тварини з даних паспорту
   - Очікуване покращення onboarding completion на +15%
   - **Alignment: ✅ Strong**

2. **"Expand beyond feeding tracker"** (Q1 2026 Roadmap goal)
   - Це перший крок до "universal pet care hub"
   - Відповідає на топ-біль користувачів (фрагментація інформації)
   - **Alignment: ✅ Strong**

3. **"Long-term: expand into health records"** (COMPANY.md)
   - Digital Vet Passport — foundation для майбутніх health features
   - Створює data moat (медична історія → lock-in)
   - **Alignment: ✅ Strong**

### ⚠️ Питання щодо пріоритизації

**Opportunity Cost:**

Ми інвестуємо ~6 FTE-weeks в Digital Vet Passport. Що ми НЕ робимо натомість?

**Альтернативи, які ми відкладаємо:**
- Покращення існуючого feeding tracker (current core product)
- "Order food" demand validation (COMPANY.md priority #3)
- Notification system improvements (Epic C залежить від цього)

**Питання:** Чому Digital Vet Passport зараз важливіший за "Order food" validation?

**Відповідь з PRD:**
> "Дані з ветпаспорту автоматично заповнюють профіль тварини, що покращує onboarding"

**Мій коментар:** Це reasonable rationale, але треба quantify impact:
- Якщо onboarding completion +15% → скільки це нових activated users?
- Якщо WAU +20% → який revenue impact (через subscriptions)?
- Чи це більший impact, ніж "Order food" validation?

**Рекомендація:** Додати ROI calculation в PRD (див. секцію 2).

### 🎯 Competitive Positioning

**Market Differentiation:**

Більшість pet care apps фокусуються на:
- Feeding trackers (наш current focus)
- Activity trackers (wearables)
- Social features (pet social networks)

**Digital Vet Passport дає нам:**
- ✅ Differentiation: "all-in-one health hub"
- ✅ Switching cost: користувачі не хочуть переносити медичну історію
- ✅ Partnership opportunities: інтеграція з ветклініками (Q2-Q3)

**Competitive Analysis (треба додати в PRD):**

| Competitor | Vet Passport Feature | Our Advantage |
|------------|:--------------------:|---------------|
| PetDesk | ✅ Yes | Вони фокусуються на clinic integrations (B2B), ми — на B2C |
| Pawtrack | ❌ No | Вони фокусуються на GPS trackers |
| 11pets | ✅ Yes | Наш UX простіший (low-effort setup principle) |

**Висновок:** Ми не перші на ринку, але можемо бути кращими через UX.

---

## 2. Business Impact

### 📊 Expected Value

**Success Metrics з PRD:**

| Метрика | Target | Business Impact |
|---------|:------:|-----------------|
| Feature Adoption | >60% | Якщо 60% з 6,500 MAU = 3,900 users |
| Onboarding Completion | +15% | Якщо baseline 52% → 67% (+15pp) |
| WAU | +20% | Якщо baseline 1,800 → 2,160 (+360 WAU) |

**Питання:** Як це translates в revenue?

**Відсутня інформація в PRD:**
- Який % activated users конвертуються в paid subscribers?
- Який LTV користувача з completed onboarding vs incomplete?
- Який revenue impact від +360 WAU?

### 💰 ROI Calculation (треба додати в PRD)

**Assumptions (треба валідувати з Finance):**
- Conversion rate (activated → paid): ~8% (industry benchmark)
- ARPU (paid subscribers): $5/month
- LTV (12 months): $60
- Churn rate: 5%/month

**Scenario 1: Onboarding Completion +15%**

```
Baseline:
- 1,000 new installs/month × 52% completion = 520 activated users
- 520 × 8% conversion = 42 new paid subscribers/month
- 42 × $60 LTV = $2,520 MRR impact

With Digital Vet Passport:
- 1,000 new installs/month × 67% completion = 670 activated users
- 670 × 8% conversion = 54 new paid subscribers/month
- 54 × $60 LTV = $3,240 MRR impact

Delta: +$720 MRR/month = +$8,640 ARR
```

**Scenario 2: WAU +20% (Retention Impact)**

```
Baseline:
- 1,800 WAU × 8% paid = 144 paid subscribers
- 144 × $5/month = $720 MRR

With Digital Vet Passport:
- 2,160 WAU × 8% paid = 173 paid subscribers
- 173 × $5/month = $865 MRR

Delta: +$145 MRR/month = +$1,740 ARR
```

**Total Projected Impact:**
- Year 1: +$8,640 (onboarding) + $1,740 (retention) = **+$10,380 ARR**
- Year 2: Compounding effect (більше activated users → більше retained users)

**Cost:**
- Development: 6 FTE-weeks × $2,000/week (blended rate) = $12,000
- Infrastructure: Firebase Blaze plan ~$100/month × 12 = $1,200/year
- Maintenance: ~10% development cost/year = $1,200/year

**Total Cost (Year 1):** $14,400

**ROI (Year 1):** ($10,380 - $14,400) / $14,400 = **-28% (negative)**  
**ROI (Year 2):** Assuming 2x impact = **+44% (positive)**

**Payback Period:** ~16-18 months

### 🤔 Чи це worth the investment?

**Pros:**
- ✅ Strategic foundation для health records (long-term value)
- ✅ Competitive differentiation
- ✅ User retention impact (switching cost)

**Cons:**
- ❌ Negative ROI в Year 1
- ❌ Opportunity cost (could build "Order food" validation instead)

**Мій висновок:**

Якщо ми дивимося на Digital Vet Passport як на **standalone feature** → ROI слабкий.

Якщо ми дивимося на це як на **strategic foundation** для health records ecosystem → це good investment.

**Рекомендація:**
- ✅ Approve, але з умовою: додати в PRD roadmap для наступних health features (Q2-Q3)
- ✅ Показати, як Digital Vet Passport enables майбутні features (Smart Reminders, Clinic Integrations, etc.)
- ✅ Додати ROI calculation в PRD (навіть якщо negative в Year 1)

---

## 3. Resource Requirements

### 👥 Team Commitment

**З PRD:**

| Роль | FTE | Duration |
|------|:---:|:--------:|
| Product Manager | 1.0 | 4 тижні |
| UX Designer | 0.8 | 4 тижні |
| iOS Developer | 1.0 | 4 тижні |
| Android Developer | 1.0 | 4 тижні |
| Backend Developer | 1.5 | 4 тижні |
| QA Engineer | 0.8 | 4 тижні |

**Total:** 6.1 FTE-weeks

**Питання:** Чи це realistic з нашим current team capacity?

**Current Team (з COMPANY.md):**
- Mobile Lead + 2 mobile engineers (3 people)
- Backend Lead + 2 backend engineers (3 people)
- 1 Product Designer
- 1 QA Engineer

**Capacity Check:**

Січень 2026 = 4 тижні = 20 робочих днів

**Mobile Team:**
- iOS + Android = 2 FTE × 4 тижні = 8 FTE-weeks available
- Digital Vet Passport needs: 2 FTE × 4 тижні = 8 FTE-weeks
- **Utilization: 100%** ⚠️

**Backend Team:**
- 1.5 FTE × 4 тижні = 6 FTE-weeks needed
- Available: 3 people × 4 тижні = 12 FTE-weeks
- **Utilization: 50%** ✅

**Design Team:**
- 0.8 FTE × 4 тижні = 3.2 FTE-weeks needed
- Available: 1 designer × 4 тижні = 4 FTE-weeks
- **Utilization: 80%** ✅

**Висновок:**
- ✅ Backend і Design мають capacity
- ⚠️ Mobile team буде на 100% utilization (ризик: якщо виникнуть production issues, не буде capacity на hotfixes)

**Рекомендація:**
- Reserve 20% mobile capacity для production support
- Це означає: timeline може розтягнутися до 5 тижнів (не 4)
- Альтернатива: hire contractor для production support на січень

### 💵 Budget Considerations

**З PRD (Infrastructure):**
- Firebase Blaze plan: ~$50-100/month
- Redis (для queue system): included in existing infrastructure

**Додаткові costs (не згадані в PRD):**
- Legal review (GDPR compliance): ~$2,000 (one-time)
- User testing (5-7 interviews): ~$500
- Marketing (email campaign, social media): ~$1,000

**Total Budget (one-time):** $3,500  
**Total Budget (recurring):** $100/month

**Питання:** Чи є approved budget для цього?

**Рекомендація:** Get CEO approval для $3,500 one-time budget до Week 1.

---

## 4. Risks & Mitigation

### 🔴 Business Risks

**Risk 1: Low Adoption (<30%)**

**Impact:** Якщо adoption <30%, ROI стає ще більш negative, і ми витратили 6 FTE-weeks на feature, яку ніхто не використовує.

**Likelihood:** Medium (PRD shows 8.2% users mention lost documents, але чи це означає, що 60% will adopt?)

**Mitigation (з PRD):**
- A/B test onboarding prompts ✅
- In-app tooltips ✅
- Email campaign ✅

**Додаткова mitigation (рекомендую додати):**
- Pre-launch user testing (5-7 users) → validate adoption hypothesis
- Soft launch (10% users) → measure adoption before full rollout
- Fallback plan: якщо adoption <30% після 2 тижнів, pause rollout і iterate

**Risk 2: Не покращує onboarding completion**

**Impact:** Основна business case hypothesis fails → ROI calculation не працює.

**Likelihood:** Medium (PRD assumes +15%, але це не validated)

**Mitigation:**
- A/B test (50% control, 50% treatment) ✅
- Measure onboarding completion weekly ✅
- Iterate на основі feedback ✅

**Додаткова mitigation:**
- Якщо після 2 тижнів немає improvement → pivot strategy (наприклад, зробити Digital Vet Passport частиною onboarding, не optional step)

**Risk 3: Scope Creep**

**Impact:** Timeline розтягується з 4 до 6+ тижнів → затримка інших Q1 priorities (Epic C, Epic D).

**Likelihood:** High (PRD має багато "nice-to-have" features: OCR, offline mode, etc.)

**Mitigation (з PRD):**
- Clear scope definition (what's in V1, what's out) ✅
- Phasing plan ✅

**Додаткова mitigation:**
- Weekly check-ins з CTO (scope review)
- Hard deadline: якщо не готово до Feb 2, ship without PDF export (це least critical feature)

### 🟡 Execution Risks

**Risk 4: Technical Complexity (PDF Generation)**

**Impact:** Engineering review shows PDF generation може бути performance bottleneck.

**Likelihood:** Medium (CTO flagged це як challenge)

**Mitigation:**
- Spike (1 день) для PDF library selection ✅
- Async generation з queue system ✅
- Fallback: skip PDF export для V1, додати в V2

**Risk 5: GDPR Compliance Issues**

**Impact:** Legal review може показати, що нам потрібне end-to-end encryption → +2 тижні development.

**Likelihood:** Low-Medium (ми вже маємо encryption at rest + in transit, але medical data sensitive)

**Mitigation:**
- Legal review до Week 1 (blocker) ✅
- Якщо потрібне E2E encryption → defer до V2, ship V1 without documents (text-only records)

---

## 5. Stakeholder Considerations

### 🤝 Cross-Functional Dependencies

**Engineering (CTO):**
- ✅ Technical feasibility review (completed)
- ⚠️ Concerns: PDF generation performance, GDPR compliance
- **Action:** Spike для PDF library (1 день), legal review (1 день)

**Design (Oksana):**
- ✅ 5 key screens to design (Week 1)
- ⚠️ Concern: timeline tight (0.8 FTE × 4 тижні)
- **Action:** Prioritize core screens (Health Tab, Add Vaccination), defer polish

**Marketing:**
- ❓ Не згадано в PRD
- **Action:** Потрібен GTM plan (email campaign, social media, in-app announcement)
- **Owner:** Marketing Lead (треба assign)

**Partnerships:**
- ❓ Не згадано в PRD
- **Opportunity:** Pilot з 1-2 ветклініками для testimonials
- **Action:** Partnerships Lead reach out до клінік (non-blocking)

**Customer Support:**
- ❓ Не згадано в PRD
- **Action:** Підготувати FAQ, training для support team (Week 3)

### 📢 Customer Communication Plan

**Відсутнє в PRD:**

**Pre-Launch:**
- Email teaser (Week 3): "Coming soon: Digital Vet Passport"
- Social media posts: user testimonials про проблему (lost documents)

**Launch:**
- In-app announcement (banner на home screen)
- Email campaign: "Introducing Digital Vet Passport"
- Social media: demo video (30 seconds)

**Post-Launch:**
- Weekly email: "Did you add your pet's vaccinations?"
- In-app tooltip: "Tip: Upload your pet's passport"

**Рекомендація:** Додати Customer Communication Plan в PRD (owner: Marketing Lead).

---

## 6. Recommendations

### 🔥 Must-Have Changes

**1. Додати ROI Calculation**

Показати business case з numbers:
- Projected revenue impact (+$10K ARR Year 1)
- Cost ($14K)
- Payback period (16-18 months)
- Strategic value (foundation для health records)

**2. Додати Competitive Analysis**

Показати, як ми differentiate від 11pets, PetDesk, та інших competitors.

**3. Додати GTM Plan**

- Customer communication strategy
- Marketing budget ($1K)
- Support team training

**4. Додати Fallback Plan**

Що робимо, якщо:
- Adoption <30% після 2 тижнів?
- Onboarding completion не покращується?
- Timeline розтягується до 6 тижнів?

**5. Clarify Resource Allocation**

- Mobile team на 100% utilization → ризик
- Рішення: hire contractor АБО extend timeline до 5 тижнів

### 🟡 Nice-to-Have Improvements

**6. Додати Long-Term Vision**

Показати roadmap для health records ecosystem:
- Q1: Digital Vet Passport (foundation)
- Q2: Smart Reminders (Epic C) + Clinic Integrations
- Q3: Health Analytics (AI-powered insights)
- Q4: Monetization (premium health features)

**7. Додати User Testimonials**

Quotes з interviews про проблему:
> "Інколи буває, ти не можеш знайти паспорт" — Даша КПІ

Це допомагає stakeholders зрозуміти user pain.

---

## 7. Open Questions

### Питання для PM:

**1. ROI Assumptions**

Чи validated assumptions для ROI calculation?
- Conversion rate (activated → paid): 8%?
- ARPU: $5/month?
- LTV: $60?

**Action:** Validate з Finance/Data team.

**2. Opportunity Cost**

Чому Digital Vet Passport важливіший за "Order food" validation (COMPANY.md priority #3)?

**Action:** Додати prioritization rationale в PRD (можливо, використати KYIV framework).

**3. Marketing Budget**

Чи є approved budget $1K для GTM campaign?

**Action:** Get approval від CEO.

**4. Contractor для Mobile Team**

Чи hire contractor для production support на січень (щоб mobile team міг focus на Digital Vet Passport)?

**Action:** Discuss з CTO + CEO (budget approval).

---

## Summary & Final Recommendation

### ✅ Go / No-Go: **APPROVE with conditions**

**Що добре:**
- ✅ Strong strategic alignment (expand beyond feeding tracker)
- ✅ Clear user pain point (8.2% mention lost documents)
- ✅ Foundation для long-term health records ecosystem
- ✅ Competitive differentiation opportunity

**Що треба покращити:**
- ⚠️ Додати ROI calculation (навіть якщо negative Year 1)
- ⚠️ Додати GTM plan (customer communication, marketing)
- ⚠️ Додати fallback plan (якщо adoption low)
- ⚠️ Clarify resource allocation (mobile team 100% utilization)

**Умови для approval:**

1. **Business Case:**
   - [ ] Додати ROI calculation з assumptions
   - [ ] Додати competitive analysis
   - [ ] Додати long-term vision (Q2-Q4 roadmap)

2. **Execution Plan:**
   - [ ] GTM plan (owner: Marketing Lead)
   - [ ] Fallback plan (якщо adoption <30%)
   - [ ] Resource allocation decision (hire contractor vs extend timeline)

3. **Budget Approval:**
   - [ ] $3,500 one-time budget (legal, user testing, marketing)
   - [ ] $100/month recurring (Firebase Blaze plan)

**Timeline:**
- Approve PRD: ✅ (з умовами вище)
- Resolve conditions: Week 1, Day 1-2
- Engineering kickoff: Week 1, Day 3

**Next Steps:**
1. PM додає ROI calculation, GTM plan, fallback plan (1 день)
2. Marketing Lead створює customer communication strategy (1 день)
3. CEO approves budget $3,500 (1 день)
4. CTO + PM decide: hire contractor vs extend timeline (1 день)
5. Engineering kickoff meeting (Week 1, Day 3)

---

**Reviewer:** Daria Koval (Head of Product)  
**Status:** ✅ Approved with conditions  
**Confidence Level:** High (80%) — strong strategic fit, але треба validate ROI assumptions

**Final Note:**

Це good PRD з clear vision. Мої concerns — це не про "чи робити", а про "як зробити краще". З modifications вище, це буде excellent foundation для Q1 success.

Let's ship it! 🚀
