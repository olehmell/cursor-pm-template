# PRD: Digital Vet Passport

**Epic A | Q1 2026 | January (Weeks 1-4)**

---

## Description: What is it?

Digital Vet Passport — це цифрова медична картка тварини всередині PetCare додатку, яка дозволяє власникам зберігати всю медичну інформацію (вакцинації, хвороби, документи) в одному місці, завжди мати її під рукою та ділитися з ветклініками або членами сім'ї.

**Ключова цінність:** Замість паперового паспорту, який можна загубити або забути вдома, власники мають цифровий паспорт, який завжди з ними в телефоні.

---

## Problem: What problem is this solving?

### Основна проблема

**"Інколи буває, ти не можеш знайти паспорт"** — Даша КПІ

Власники тварин стикаються з фрагментацією медичної інформації:
- 📄 Паперовий ветпаспорт губиться або залишається вдома
- 📱 Фото документів розкидані по галереї телефону
- 🗂️ Немає єдиного місця для історії хвороб та лікувань
- 🏥 При відвідуванні нової клініки важко швидко показати повну історію
- 🚨 В екстрених ситуаціях критична інформація може бути недоступна

### Дані з досліджень

- **8.2%** опитаних згадують втрату документів як проблему
- **3 з 3** респондентів в інтерв'ю згадували складність з організацією медичної інформації
- Особливо критично для нових власників, які не знають, що треба трекати

---

## Why: How do we know this is a real problem and worth solving?

### Валідація проблеми

**Якісні дані (інтерв'ю, n=3):**
- Даша КПІ: пряме згадування втрати паспорту
- Даша Дев: складність пошуку історії при екстреній ситуації
- Ігор: проблема з трекінгом різних термінів вакцинацій

**Кількісні дані (опитування, n=220):**
- 8.2% згадують втрату документів
- 19.1% потребують нагадувань про вакцинації (пов'язана проблема)
- NPS = -20.5 (фрагментація інформації — один з топ-болів)

### Чому варто вирішувати зараз

1. **Стратегічна важливість:** Це перший крок до розширення PetCare з "трекера корму" в "універсальний хаб для догляду"
2. **Синергія з іншими фічами:** Дані з ветпаспорту автоматично заповнюють профіль тварини (вік, порода, вага), що покращує onboarding
3. **Foundation для майбутнього:** Створює базу для Epic C (Smart Reminders) та довгострокової стратегії health records
4. **Конкурентна перевага:** Більшість конкурентів фокусуються тільки на годуванні; ми йдемо далі

---

## Success: How do we know if we've solved this problem?

### Ключові метрики успіху

| Метрика | Baseline | Target (4 тижні після запуску) | Вимірювання |
|---------|:--------:|:------------------------------:|-------------|
| **Feature Adoption** | 0% | > 60% | % користувачів, що додали мін. 1 запис про вакцинацію АБО завантажили мін. 1 документ |
| **Onboarding Completion** | TBD* | +15% | % користувачів, що завершили setup профілю тварини |
| **Weekly Active Users** | TBD* | +20% | WAU, що відкривають розділ "Health" мін. 1 раз на тиждень |
| **Documents per User** | 0 | > 2 | Середня кількість доданих записів/документів на активного користувача |

*Baseline метрики треба виміряти до запуску (Week 0)

### Якісні індикатори успіху

**Успіх:**
- ✅ Користувачі згадують Digital Vet Passport як "must-have" фічу в опитуваннях
- ✅ Зменшення скарг на "не можу знайти інформацію" в support
- ✅ Користувачі показують паспорт в клініках (feedback від партнерів)

**Провал:**
- ❌ Adoption < 30% через 4 тижні
- ❌ Користувачі додають документи, але ніколи не повертаються до них (0 repeat visits)
- ❌ Негативний feedback про складність інтерфейсу

### Аналітика (треба додати)

**Події для трекінгу:**
```
- health_tab_opened
- vaccination_record_added
- vaccination_record_edited
- vaccination_record_deleted
- document_uploaded (properties: file_type, file_size)
- document_viewed
- medical_history_viewed
- medical_history_exported_pdf
- health_data_synced (для household sharing)
```

**Воронка активації:**
```
1. Користувач відкрив розділ "Health"
2. Користувач натиснув "Add vaccination" АБО "Upload document"
3. Користувач заповнив форму / вибрав файл
4. Користувач зберіг запис
5. Користувач повернувся до розділу "Health" протягом 7 днів
```

---

## Audience: Who are we building for?

### Основна аудиторія (Primary)

**Нові власники тварин (особливо цуценят/кошенят)**
- Вік: 25-40 років
- Поведінка: активно шукають інформацію, хочуть "все робити правильно"
- Біль: не знають, що треба трекати, бояться щось пропустити
- Цінність: чекліст + шаблони + історія в одному місці

**Власники з декількома тваринами**
- Поведінка: складно тримати в голові графіки для кожної тварини
- Біль: плутанина з термінами вакцинацій
- Цінність: окремі паспорти для кожної тварини, швидке перемикання

### Вторинна аудиторія (Secondary)

**Households з декількома caretakers**
- Поведінка: різні члени сім'ї водять тварину до лікаря
- Біль: "хто останній раз був у ветеринара?", "яку вакцину робили?"
- Цінність: синхронізація даних між пристроями

**Власники, що часто змінюють клініки**
- Поведінка: переїзди, пошук кращого лікаря
- Біль: кожен раз заново розповідати історію хвороб
- Цінність: експорт медкарти в PDF для нової клініки

### Хто НЕ є цільовою аудиторією (для V1)

- ❌ Ветклініки (інтеграція з клініками — поки skip)
- ❌ Заводчики з великою кількістю тварин (>5)
- ❌ Користувачі без смартфонів

---

## What: Roughly, what does this look like in the product?

### User Stories (Must-Have для V1)

```
✅ US-101: Як власник, я хочу додавати записи про вакцинації (дата, назва, клініка),
          щоб не шукати паперовий паспорт

✅ US-102: Як власник, я хочу завантажувати фото/PDF документів (до 10MB),
          щоб мати їх завжди під рукою

✅ US-103: Як власник, я хочу бачити історію хвороб у хронологічному порядку,
          щоб швидко показати новому лікарю

✅ US-104: Як власник, я хочу експортувати медкарту в PDF,
          щоб надіслати в клініку перед візитом
```

### Acceptance Criteria

**Додавання запису про вакцинацію:**
- [ ] Форма з полями: дата, назва вакцини, клініка (опціонально), нотатки (опціонально)
- [ ] Можливість додати фото/PDF документу до запису
- [ ] Валідація: дата не може бути в майбутньому
- [ ] Збереження займає < 3 секунд

**Завантаження документів:**
- [ ] Підтримка форматів: JPG, PNG, PDF
- [ ] Максимальний розмір файлу: 10MB
- [ ] Попередній перегляд перед завантаженням
- [ ] Compression для зображень (зменшення розміру без втрати якості)
- [ ] Error handling: "файл занадто великий", "формат не підтримується"

**Перегляд історії:**
- [ ] Хронологічний список (найновіші зверху)
- [ ] Фільтри: всі записи / тільки вакцинації / тільки хвороби
- [ ] Пошук за назвою вакцини або клініки
- [ ] Швидкий перегляд документів (tap to open)
- [ ] Edit/Delete для кожного запису

**Експорт в PDF:**
- [ ] Генерація PDF з логотипом PetCare
- [ ] Включає: інфо про тварину + всі записи + мініатюри документів
- [ ] Можливість вибрати період (всі записи / останні 6 міс / останній рік)
- [ ] Share через системний діалог (email, messenger, etc.)

**Синхронізація (household sharing):**
- [ ] Автоматична синхронізація при додаванні нового запису
- [ ] Конфлікт-резолюшн (якщо два користувачі редагують одночасно)
- [ ] Нотифікація для household members: "Олена додала запис про вакцинацію"

### Що НЕ входить в V1 (Scope Out)

- ❌ OCR для автоматичного розпізнавання дат (nice-to-have, можливо V2)
- ❌ Інтеграція з ветклініками (клініки можуть автоматично додавати записи)
- ❌ Нагадування про майбутні вакцинації (це Epic C: Smart Reminders)
- ❌ Аналіз здоров'я на основі AI
- ❌ Інтеграція з wearables (трекери активності для тварин)

### UI/UX Flow (High-Level)

```mermaid
---
config:
  layout: elk
  theme: forest
  look: classic
---
flowchart TD
    A[Home Screen] --> B[Tap на Pet Profile]
    B --> C[Pet Details Screen]
    C --> D[Tab: Health]
    D --> E{Перший раз?}
    E -->|Так| F[Empty State: "Add first vaccination"]
    E -->|Ні| G[Medical History List]
    F --> H[Add Vaccination Form]
    G --> H
    G --> I[Tap на запис]
    I --> J[Vaccination Details]
    J --> K[Edit / Delete / View Document]
    G --> L[Export to PDF]
    L --> M[Share Dialog]
```

### Ключові екрани (для дизайну)

1. **Health Tab (Empty State)**
   - Ілюстрація + "Add your first vaccination record"
   - CTA: "Add Vaccination" (primary button)
   - Secondary CTA: "Upload Document"

2. **Health Tab (With Data)**
   - Хронологічний список записів
   - Кожен запис: іконка вакцини, назва, дата, клініка
   - Floating Action Button: "+" (додати новий запис)
   - Top bar: фільтри + пошук + "Export PDF"

3. **Add Vaccination Form**
   - Date picker (default: today)
   - Text input: назва вакцини (з автокомплітом популярних вакцин)
   - Text input: клініка (опціонально, з автокомплітом)
   - Text area: нотатки (опціонально)
   - "Upload Document" (опціонально)
   - Buttons: "Cancel" / "Save"

4. **Vaccination Details**
   - Вся інформація про запис
   - Прикріплений документ (якщо є): tap to open full screen
   - Buttons: "Edit" / "Delete" / "Share"

5. **Export PDF Preview**
   - Попередній перегляд PDF
   - Вибір періоду (dropdown: All / Last 6 months / Last year)
   - Button: "Share PDF"

---

## How: What is the experiment plan?

### Гіпотеза

**Якщо ми додамо Digital Vet Passport з можливістю зберігати вакцинації та документи в одному місці, то:**
- Feature adoption буде > 60% (користувачі додадуть мін. 1 запис)
- Onboarding completion збільшиться на +15% (бо дані з паспорту автозаповнюють профіль)
- Weekly active users збільшаться на +20% (користувачі повертаються, щоб додати нові записи)

**Тому що:**
- Фрагментація медичної інформації — це топ-біль користувачів (8.2% згадують втрату документів)
- Користувачі вже зберігають фото паспортів в галереї, але це незручно
- Наявність даних про тварину (з паспорту) дозволяє нам давати персоналізовані поради (вік, порода, вага)

### Експеримент (A/B Test)

**Контрольна група (Control - 50%):**
- Існуючий onboarding без Digital Vet Passport
- Профіль тварини заповнюється вручну

**Тестова група (Treatment - 50%):**
- Новий onboarding з промо Digital Vet Passport
- Після створення профілю: "Add your first vaccination" (опціональний крок)
- In-app tooltip: "Tip: Upload your pet's passport to auto-fill profile"

**Тривалість:** 4 тижні після запуску

**Критерії успіху експерименту:**
- Feature adoption (Treatment) > 60%
- Onboarding completion (Treatment) > Onboarding completion (Control) + 15%
- WAU (Treatment) > WAU (Control) + 20%
- Статистична значущість: p < 0.05

### Rollout Plan

**Week 1 (Soft Launch):**
- 10% користувачів (тільки нові реєстрації)
- Фокус: виявлення критичних багів, збір першого feedback
- Daily monitoring: crash rate, upload success rate

**Week 2 (Expanded Beta):**
- 50% користувачів (нові + існуючі, що активували onboarding)
- A/B test починається
- Збір аналітики: adoption, engagement, retention

**Week 3-4 (Full Rollout):**
- 100% користувачів
- Продовження A/B тесту
- Підготовка до ретроспективи

**Week 5 (Post-Launch Review):**
- Аналіз результатів A/B тесту
- User interviews (5-7 користувачів, що активно використовують фічу)
- Рішення: ship to 100% permanently АБО iterate

### Metrics Dashboard (для моніторингу)

**Real-time metrics (щоденний моніторинг):**
- Crash rate в розділі "Health"
- Upload success rate (% успішних завантажень документів)
- API latency для Firebase Storage

**Weekly metrics (щотижневий review):**
- Feature adoption rate
- Onboarding completion rate
- WAU (Health tab visitors)
- Documents per user
- Export PDF usage

**Qualitative feedback:**
- In-app NPS survey (через 7 днів після першого використання)
- Support tickets tagged "health" / "vet passport"
- App Store reviews (моніторинг згадок про медичну картку)

---

## When: When does it ship and what are the milestones?

### Timeline (January 2026, Weeks 1-4)

**Week 1 (Jan 6-12): Design & Specs**
- [ ] Day 1-2: Finalize PRD (цей документ) + stakeholder review
- [ ] Day 3-5: UX/UI дизайн (5 ключових екранів)
- [ ] Day 5: Design review + approval
- [ ] Day 5: Engineering kickoff meeting

**Week 2 (Jan 13-19): Development Sprint 1**
- [ ] Backend: API для CRUD операцій (vaccination records)
- [ ] Backend: Firebase Storage setup для документів
- [ ] Mobile: UI для Health Tab + Add Vaccination Form
- [ ] Mobile: File picker integration
- [ ] QA: Test plan document

**Week 3 (Jan 20-26): Development Sprint 2**
- [ ] Backend: Export to PDF API
- [ ] Backend: Household sync logic
- [ ] Mobile: Medical History List + Details screen
- [ ] Mobile: Export PDF + Share functionality
- [ ] QA: Testing Sprint 1 features

**Week 4 (Jan 27 - Feb 2): Testing & Soft Launch**
- [ ] Day 1-3: QA full regression testing
- [ ] Day 3: Bug bash (вся команда)
- [ ] Day 4: Soft launch (10% users)
- [ ] Day 5-7: Monitoring + hotfixes (якщо потрібно)

**Week 5 (Feb 3-9): Full Rollout**
- [ ] Day 1: Expanded beta (50% users) + A/B test start
- [ ] Day 3: Full rollout (100% users)
- [ ] Day 5: Marketing push (email, social media, in-app announcement)
- [ ] Day 7: First weekly metrics review

### Dependencies

**Блокери (Must be resolved):**
- ✅ Firebase Storage setup (Infrastructure team)
- ✅ PDF generation library (evaluate options: react-native-pdf, jsPDF)
- ✅ Analytics events implementation (tracking plan approval)

**Nice-to-have (не блокують запуск):**
- 🔄 Партнерство з 1-2 ветклініками для пілотного feedback
- 🔄 Юридична консультація щодо GDPR compliance (шифрування медичних даних)

### Resource Allocation

| Роль | FTE | Фокус |
|------|:---:|-------|
| **Product Manager (You)** | 1.0 | Координація, metrics, user feedback |
| **UX Designer** | 0.8 | 5 екранів + empty states + onboarding flow |
| **iOS Developer** | 1.0 | Health Tab UI, file picker, PDF export |
| **Android Developer** | 1.0 | Health Tab UI, file picker, PDF export |
| **Backend Developer** | 1.5 | API, Firebase Storage, PDF generation, sync logic |
| **QA Engineer** | 0.8 | Test plan, regression, automation |

**Total:** ~6 FTE-weeks

---

## Technical Notes

### Architecture

**Backend (Node.js + PostgreSQL):**
```
Tables:
- vaccination_records (id, pet_id, date, vaccine_name, clinic, notes, created_at, updated_at)
- medical_documents (id, vaccination_record_id, file_url, file_type, file_size, uploaded_at)

API Endpoints:
- POST /api/pets/:petId/vaccinations (create)
- GET /api/pets/:petId/vaccinations (list)
- GET /api/pets/:petId/vaccinations/:id (get)
- PUT /api/pets/:petId/vaccinations/:id (update)
- DELETE /api/pets/:petId/vaccinations/:id (delete)
- POST /api/pets/:petId/vaccinations/:id/documents (upload)
- GET /api/pets/:petId/medical-history/export (PDF)
```

**Mobile (React Native):**
```
Screens:
- HealthTabScreen (list)
- AddVaccinationScreen (form)
- VaccinationDetailsScreen (details)
- ExportPDFScreen (preview + share)

Libraries:
- react-native-image-picker (file picker)
- react-native-pdf (PDF preview)
- react-native-share (share dialog)
- @react-native-firebase/storage (file upload)
```

**Storage (Firebase Storage):**
```
Structure:
/medical-documents/{userId}/{petId}/{documentId}.{ext}

Security Rules:
- Користувач може читати/писати тільки свої документи
- Household members можуть читати документи спільних pets
```

### Security & Privacy

**GDPR Compliance:**
- [ ] Шифрування медичних даних в базі (at rest)
- [ ] HTTPS для всіх API запитів (in transit)
- [ ] Можливість видалити всі дані (GDPR right to be forgotten)
- [ ] Privacy policy update: згадати зберігання медичних даних

**Access Control:**
- [ ] Тільки власник pet profile + household members можуть бачити дані
- [ ] Audit log для sensitive операцій (delete vaccination record)

### Performance

**Targets:**
- Upload document (5MB): < 10 секунд
- Load medical history: < 2 секунди
- Generate PDF: < 5 секунд
- Sync between devices: < 3 секунди

**Optimization:**
- Image compression перед upload (reduce file size by 50-70%)
- Lazy loading для списку записів (pagination: 20 items per page)
- Caching для medical history (invalidate on update)

---

## Risks & Mitigation

| Ризик | Ймовірність | Вплив | Мітигація |
|-------|:-----------:|:-----:|-----------|
| **Низька adoption (<30%)** | Середня | Високий | - A/B test onboarding prompts<br>- In-app tooltips<br>- Email campaign: "Did you know?"<br>- Gamification: "Complete your pet's profile" badge |
| **Складність UI (користувачі не розуміють, як додати запис)** | Середня | Високий | - User testing перед запуском (5-7 користувачів)<br>- Empty state з чітким CTA<br>- Onboarding tutorial (опціонально) |
| **Проблеми з upload великих файлів** | Висока | Середній | - Compression перед upload<br>- Retry logic<br>- Clear error messages<br>- Limit file size to 10MB |
| **Користувачі не повертаються після першого додавання** | Середня | Високий | - Push notification: "Add your next vaccination"<br>- Синергія з Epic C (Smart Reminders)<br>- Email: "Your pet's health history is incomplete" |
| **GDPR compliance issues** | Низька | Високий | - Юридична консультація до запуску<br>- Шифрування даних<br>- Clear privacy policy |
| **Технічний борг (швидкий MVP)** | Висока | Середній | - 20% часу на рефакторинг<br>- Code review standards<br>- Tech debt backlog |

---

## Open Questions

**Для Product Team:**
- [ ] Чи потрібен нам окремий onboarding tutorial для Digital Vet Passport, чи достатньо empty state + tooltips?
- [ ] Чи варто додати шаблони популярних вакцин (автокомпліт), щоб зменшити typing?
- [ ] Як ми будемо валідувати, що користувачі дійсно показують паспорт в клініках? (feedback loop)

**Для Engineering:**
- [ ] Яку PDF library використовувати? (react-native-pdf vs jsPDF vs інше)
- [ ] Чи потрібна нам CDN для документів, чи Firebase Storage достатньо?
- [ ] Як ми будемо хендлити конфлікти при одночасному редагуванні (household sync)?

**Для Design:**
- [ ] Чи потрібні нам різні іконки для різних типів вакцин (rabies, distemper, etc.)?
- [ ] Як ми показуємо прогрес upload великого файлу? (progress bar, spinner, etc.)
- [ ] Чи потрібен нам dark mode для Health Tab?

**Для Marketing:**
- [ ] Як ми будемо промотувати цю фічу? (email, push, social media)
- [ ] Чи варто зробити партнерство з 1-2 клініками для testimonials?
- [ ] Чи потрібен нам landing page для Digital Vet Passport?

---

## Success Story (Vision)

**Через 3 місяці після запуску:**

Олена, власниця 6-місячного цуценяти, відкриває PetCare і бачить нагадування: "Time for Рекс's rabies vaccination". Вона натискає на нагадування, бачить всю історію попередніх вакцинацій, і розуміє, що це дійсно час.

Вона їде в нову ветклінику (переїхала в інший район). Лікар питає: "Які вакцини вже зробили?". Олена відкриває PetCare, натискає "Export PDF", і за 5 секунд надсилає повну медичну історію Рекса на email клініки.

Після візиту вона фотографує новий запис в паперовому паспорті, додає в PetCare, і система автоматично створює нагадування про наступну вакцинацію через 3 місяці.

Її чоловік (household member) отримує нотифікацію: "Олена додала запис про вакцинацію". Він відкриває додаток і бачить оновлену історію.

**Результат:** Олена більше ніколи не губить паперовий паспорт, не забуває про вакцинації, і завжди має всю інформацію під рукою. PetCare став її "single source of truth" для здоров'я Рекса.

---

## Appendix: Related Documents

- [Q1 2026 Roadmap](./Q1-2026-roadmap.md) — контекст Epic A в загальному роадмапі
- [PRODUCT.md](../../company-context/PRODUCT.md) — product philosophy та principles
- [COMPANY.md](../../company-context/COMPANY.md) — company strategy та metrics
- [Socratic Questioning](../templates/socratic-questioning.md) — framework для валідації PRD

---

**Автор:** Senior PM, PetCare  
**Дата створення:** 18 січня 2026  
**Останнє оновлення:** 18 січня 2026  
**Статус:** Draft → Ready for Review  
**Reviewers:** Head of Product, CTO, UX Designer

---

**Next Steps:**
1. [ ] Stakeholder review (Head of Product, CTO)
2. [ ] Design kickoff (UX Designer)
3. [ ] Engineering estimation (Tech Lead)
4. [ ] Analytics tracking plan approval (Data team)
5. [ ] Legal review (GDPR compliance)
6. [ ] Marketing plan (GTM team)
