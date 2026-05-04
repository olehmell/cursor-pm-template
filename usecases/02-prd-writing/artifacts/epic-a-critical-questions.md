# Критичні питання для Epic A: Digital Vet Passport

**Мета:** Отримати відповіді на блокуючі питання перед створенням фінального PRD для прототипу

---

## 🔴 БЛОКЕРИ (Must resolve before prototype)

### 1. PDF Library Selection (Engineering)

**Питання:** Який PDF library використовувати для generation?

**Контекст:**
- **jsPDF** (client-side): легкий, але обмежений функціонал
- **PDFKit** (server-side): потужний, але потребує Node.js streams + async queue
- **react-native-pdf**: тільки для preview, не генерує

**Impact:** 
- Якщо PDFKit → потрібен Redis для queue system (+2 дні setup)
- Якщо jsPDF → можливі performance issues на старих телефонах

**Ваше рішення:**
- [ ] Option A: PDFKit на backend (async generation) — recommended by CTO
- [ ] Option B: jsPDF на client (sync generation) — simpler, але ризик performance
- [ ] Option C: Skip PDF export для V1, додати в V2

---

### 2. Manual Entry vs Photo Upload (User Research)

**Питання:** Чи користувачі хочуть вводити дані вручну (structured data), чи просто завантажувати фото паспорту?

**Контекст:**
- PRD передбачає manual entry (дата, назва вакцини, клініка)
- User Research каже: можливо, користувачі очікують "upload photo → done"
- Якщо так → current UX буде frustrating

**Impact:**
- Якщо manual entry only → можливо low adoption
- Якщо photo upload → потрібен інший UI flow

**Ваше рішення:**
- [ ] Option A: Manual entry only (як в PRD) — structured data, але slow
- [ ] Option B: Photo upload only → manually extract data later
- [ ] Option C: Обидва варіанти (manual entry + photo upload) — flexible, але складніше

---

### 3. Onboarding Flow (User Research + Executive)

**Питання:** Коли показувати "Add vaccination" — в onboarding чи delayed prompt?

**Контекст:**
- **In onboarding:** immediate value, але overwhelming (користувач вже втомився)
- **Delayed prompt (Day 3):** less friction, але можливо lower adoption

**Impact:**
- Це впливає на onboarding completion target (+15%)
- Це впливає на feature adoption target (60%)

**Ваше рішення:**
- [ ] Option A: In onboarding (optional step) — як в PRD
- [ ] Option B: Delayed prompt (push notification Day 3)
- [ ] Option C: Contextual prompt (коли user відкриває app 3rd time)

---

### 4. GDPR Compliance (Engineering + Executive)

**Питання:** Чи достатньо current encryption (HTTPS + database at rest), чи потрібне end-to-end encryption?

**Контекст:**
- Current: HTTPS (in transit) + PostgreSQL encryption (at rest) + Firebase Storage encryption
- Medical data sensitive → можливо потрібне E2E encryption
- Якщо так → +2 тижні development (out of scope для V1)

**Impact:**
- Якщо legal review каже "потрібне E2E" → не можемо ship V1 в січні
- Якщо skip → можливі legal risks

**Ваше рішення:**
- [ ] Option A: Current encryption достатньо (get legal approval)
- [ ] Option B: Потрібне E2E encryption → defer V1 або skip documents (text-only)
- [ ] Option C: Ship V1 з current encryption, додати E2E в V2

---

## 🟡 ВАЖЛИВІ (Should resolve before prototype, але є workarounds)

### 5. Feature Naming (User Research)

**Питання:** Чи validated назва "Digital Vet Passport"?

**Контекст:**
- User Research каже: "паспорт" може бути confusing (паспорт = ID документ, не медична картка)
- Альтернативи: "Medical Records", "Health History", "Vaccination Tracker", "Pet Health Card"

**Impact:**
- Назва впливає на comprehension та adoption
- Але це можна A/B тестувати після launch

**Ваше рішення:**
- [ ] Option A: "Digital Vet Passport" (як в PRD)
- [ ] Option B: "Health Records"
- [ ] Option C: "Medical History"
- [ ] Option D: Інша назва: _______________

---

### 6. Empty State UX (User Research)

**Питання:** Що показувати в empty state?

**Current (PRD):**
```
"Add your first vaccination"
[CTA Button]
```

**Recommended (User Research):**
```
[Illustration]
"Keep all your pet's medical records in one place"

[Examples]
- Rabies vaccination (Jan 15, 2026)
- Health checkup (Nov 5, 2025)

[CTA] Add First Record
[Secondary] Upload Passport Photo
```

**Impact:**
- Покращує comprehension та conversion
- Але потрібна додаткова ілюстрація (design time)

**Ваше рішення:**
- [ ] Option A: Simple empty state (як в PRD) — швидше
- [ ] Option B: Rich empty state (recommended) — краще UX, але +1 день design

---

### 7. Resource Allocation (Executive)

**Питання:** Mobile team на 100% utilization — як хендлити production issues?

**Контекст:**
- Mobile team: 2 FTE × 4 тижні = 8 FTE-weeks
- Digital Vet Passport потребує: 8 FTE-weeks
- Якщо production issue → немає capacity

**Impact:**
- Ризик: timeline розтягується до 5 тижнів
- Або: production issues не фіксяться вчасно

**Ваше рішення:**
- [ ] Option A: Reserve 20% capacity для production support → timeline 5 тижнів
- [ ] Option B: Hire contractor для production support → budget $3-5K
- [ ] Option C: Accept risk (100% utilization) → tight timeline

---

### 8. Budget Approval (Executive)

**Питання:** Чи є approved budget для one-time costs?

**Breakdown:**
- Legal review (GDPR): $2,000
- User testing (n=5-7): $500
- Marketing campaign: $1,000
- **Total: $3,500**

**Impact:**
- Без legal review → GDPR risk
- Без user testing → UX risk
- Без marketing → low adoption

**Ваше рішення:**
- [ ] Budget approved: $3,500
- [ ] Budget approved partially: $______
- [ ] Budget not approved → skip some items

---

## 🟢 NICE-TO-HAVE (Не блокують prototype, можна вирішити пізніше)

### 9. Templates для Vaccines (User Research)

**Питання:** Чи додавати autocomplete для популярних вакцин?

**Impact:** Reduces typing, але +1 день development

**Ваше рішення:**
- [ ] Yes, додати в V1
- [ ] No, додати в V2

---

### 10. Progressive Disclosure (User Research)

**Питання:** Чи спрощувати форму "Add Vaccination" (Quick Add vs Detailed Add)?

**Impact:** Reduces cognitive load, але складніший UI

**Ваше рішення:**
- [ ] Yes, додати progressive disclosure
- [ ] No, одна форма (як в PRD)

---

### 11. Offline Mode (Engineering)

**Питання:** Чи підтримувати offline mode для V1?

**Impact:** +2-3 дні development, але кращий UX

**Ваше рішення:**
- [ ] Yes, додати в V1
- [ ] No, skip для V1, додати в V2

---

## Інструкція для заповнення

Будь ласка, дайте відповіді на **БЛОКЕРИ (1-4)** та **ВАЖЛИВІ (5-8)**.

Для NICE-TO-HAVE (9-11) можна дати відповіді опціонально (або я сам прийму рішення на основі best practices).

**Формат відповіді:**

```
1. PDF Library: Option A (PDFKit на backend)
2. Manual Entry vs Photo: Option C (обидва варіанти)
3. Onboarding Flow: Option B (delayed prompt)
4. GDPR: Option A (current encryption достатньо)
5. Feature Naming: Option B ("Health Records")
6. Empty State: Option B (rich empty state)
7. Resource Allocation: Option A (reserve 20%, timeline 5 тижнів)
8. Budget: Approved $3,500
9. Templates: Yes
10. Progressive Disclosure: No
11. Offline Mode: No
```

---

Після отримання відповідей я створю фінальний PRD, оптимізований для передачі на прототип.
