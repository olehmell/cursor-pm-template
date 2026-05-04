# Engineering Review: Digital Vet Passport PRD

**Reviewer:** Andrii Melnyk (CTO)  
**Date:** 18 січня 2026  
**PRD Version:** Draft v1.0  
**Overall Assessment:** ✅ **Feasible with moderate complexity** — можемо побудувати за 4 тижні, але є кілька технічних ризиків, які треба адресувати

---

## 1. Technical Feasibility

### ✅ Що технічно можливо

**Backend (Node.js + PostgreSQL):**
- CRUD API для vaccination records — straightforward, 2-3 дні
- Firebase Storage integration — вже використовуємо для pet photos, можна переіспользувати
- PDF generation — є готові бібліотеки (jsPDF, PDFKit)
- Household sync — вже маємо shared access logic для feeding plans, можна адаптувати

**Mobile (React Native):**
- File picker — react-native-image-picker (вже в проекті)
- PDF preview — react-native-pdf (нова залежність, але stable)
- Upload progress — можна зробити з react-native-fs
- Share dialog — react-native-share (вже в проекті)

**Висновок:** Технічно все feasible, нових технологій майже немає.

### ⚠️ Constraints і обмеження

1. **Firebase Storage limits:**
   - Free tier: 5GB storage, 1GB/day downloads
   - З 6,500 MAU і 10MB per user = потенційно 65GB (need paid plan)
   - **Action:** Upgrade to Blaze plan (pay-as-you-go) — ~$50-100/month

2. **PDF generation performance:**
   - Генерація PDF на backend для 50+ записів може займати 5-10 секунд
   - **Action:** Додати queue system (Bull + Redis) для async processing

3. **Mobile storage:**
   - Якщо користувач завантажить 50 документів по 5MB = 250MB на пристрої
   - **Action:** Implement lazy loading + cache eviction policy

### 🚫 Блокери

**НЕМАЄ критичних блокерів**, але треба вирішити до Week 1:
- [ ] Firebase Blaze plan approval (потребує бюджет від CEO)
- [ ] Redis setup для queue system (Infrastructure team, 1-2 дні)

---

## 2. Implementation Complexity

### Effort Estimate (LOE)

| Компонент | Складність | Estimate | Коментар |
|-----------|:----------:|:--------:|----------|
| **Backend API (CRUD)** | 🟢 Low | 2-3 дні | Стандартний CRUD, є шаблони |
| **Firebase Storage integration** | 🟢 Low | 1-2 дні | Вже використовуємо для photos |
| **PDF generation** | 🟡 Medium | 3-4 дні | Треба research бібліотек + template design |
| **Household sync logic** | 🟡 Medium | 2-3 дні | Адаптація існуючої логіки |
| **Mobile UI (5 screens)** | 🟡 Medium | 5-6 днів | Стандартні екрани, але треба polish |
| **File upload + compression** | 🟡 Medium | 2-3 дні | Compression logic + progress tracking |
| **Export PDF mobile** | 🟢 Low | 1-2 дні | Wrapper для backend API |
| **QA + bug fixes** | 🟡 Medium | 3-4 дні | Regression testing + edge cases |

**Total Estimate:** ~20-27 днів (3-4 тижні з 2 iOS + 2 Android + 1.5 Backend = ~5.5 FTE)

**Висновок:** Timeline в PRD (4 тижні) — **realistic, але tight**. Якщо виникнуть непередбачені проблеми, можемо не встигнути.

### Що straightforward, що складно

**Straightforward (80% роботи):**
- ✅ CRUD API
- ✅ File picker integration
- ✅ Basic UI screens
- ✅ Firebase Storage upload

**Складно (20% роботи, але 50% ризику):**
- ⚠️ PDF generation (template design + performance)
- ⚠️ Image compression (balance якість vs розмір)
- ⚠️ Conflict resolution для household sync (що якщо два користувачі редагують одночасно?)
- ⚠️ Error handling для upload failures (retry logic, offline mode)

---

## 3. Key Challenges

### 🔴 Critical Challenges

**1. PDF Generation Performance**

**Проблема:**
- Генерація PDF для 50+ записів + images може займати 10-15 секунд
- Користувач буде чекати → поганий UX

**Рішення:**
```
Option A (Recommended): Async generation
- POST /api/pets/:petId/medical-history/export → returns job_id
- Client polls GET /api/jobs/:jobId/status
- Коли готово: download URL
- Pros: не блокує UI, можна показати progress
- Cons: складніша імплементація (queue system)

Option B: Client-side generation
- Генерувати PDF на мобільному пристрої
- Pros: швидше для малих документів
- Cons: performance issues на старих телефонах, складно з images
```

**Рекомендація:** Почати з Option A (async), якщо не встигаємо — fallback на sync з timeout 30 секунд.

**2. Image Compression Strategy**

**Проблема:**
- Користувачі завантажують фото паспортів з камери (5-10MB)
- Firebase Storage costs + mobile storage + slow uploads

**Рішення:**
```javascript
// Compression на клієнті перед upload
import ImageResizer from 'react-native-image-resizer';

const compressImage = async (uri) => {
  return await ImageResizer.createResizedImage(
    uri,
    1920, // max width
    1920, // max height
    'JPEG',
    80, // quality (80% = good balance)
  );
};

// Expected: 5MB → 500KB-1MB (10x reduction)
```

**Рекомендація:** Compression на клієнті + показувати preview перед upload ("Image will be compressed to X MB").

**3. Conflict Resolution (Household Sync)**

**Проблема:**
```
Scenario:
1. User A edits vaccination record (offline)
2. User B edits same record (offline)
3. Both come online → conflict

Current feeding plan logic: last write wins (not ideal for medical data)
```

**Рішення:**
```
Option A (Recommended): Optimistic locking
- Додати version field до vaccination_records
- При update: WHERE id = ? AND version = ?
- Якщо version mismatch → show conflict dialog

Option B: Operational Transform (складно)
- Merge changes автоматично
- Pros: no user intervention
- Cons: complex, overkill for V1
```

**Рекомендація:** Option A (optimistic locking) + conflict dialog: "Someone else updated this record. Keep your version or theirs?"

### 🟡 Medium Challenges

**4. Offline Mode**

**Питання з PRD:** Що якщо користувач додає запис offline?

**Рішення:**
- Використати AsyncStorage для local cache
- Queue uploads коли з'явиться інтернет
- Показувати "Syncing..." badge

**Estimate:** +2-3 дні на offline support (можна skip для V1, додати в V2)

**5. File Upload Retry Logic**

**Питання з PRD:** Що якщо upload fails на 90%?

**Рішення:**
```javascript
// Retry з exponential backoff
const uploadWithRetry = async (file, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await uploadToFirebase(file);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(2 ** i * 1000); // 1s, 2s, 4s
    }
  }
};
```

**Estimate:** +1 день на retry logic

---

## 4. Performance & Scalability

### Load Considerations

**Current scale (6,500 MAU):**
- Якщо 60% adoption = 3,900 користувачів
- Якщо кожен додасть 3 документи = 11,700 documents
- Якщо середній розмір 2MB (після compression) = 23GB storage

**Projected scale (1 рік, 50,000 MAU):**
- 30,000 користувачів × 5 документів × 2MB = 300GB storage
- Firebase Storage cost: ~$0.026/GB/month = $7.8/month (cheap!)

**Висновок:** Scalability не проблема для storage.

### Database Performance

**Queries to optimize:**

```sql
-- Найчастіший query: get medical history
SELECT * FROM vaccination_records
WHERE pet_id = ?
ORDER BY date DESC
LIMIT 20;

-- Index needed:
CREATE INDEX idx_vaccination_records_pet_id_date
ON vaccination_records(pet_id, date DESC);

-- Query для household sync:
SELECT * FROM vaccination_records
WHERE pet_id IN (SELECT pet_id FROM household_pets WHERE user_id = ?)
AND updated_at > ?;

-- Index needed:
CREATE INDEX idx_vaccination_records_updated_at
ON vaccination_records(updated_at);
```

**Action:** Додати ці індекси в migration (Week 2).

### API Rate Limits

**Firebase Storage:**
- Free tier: 50,000 reads/day, 20,000 writes/day
- З 3,900 користувачів × 3 reads/day = 11,700 reads/day (OK)
- З 3,900 користувачів × 1 write/week = 560 writes/day (OK)

**Висновок:** Rate limits не проблема.

### Caching Strategy

**Рекомендація:**
```
1. Mobile cache (AsyncStorage):
   - Cache medical history for 24 hours
   - Invalidate on update

2. Backend cache (Redis):
   - Cache GET /api/pets/:petId/vaccinations for 5 minutes
   - Invalidate on POST/PUT/DELETE

3. Firebase Storage:
   - Set Cache-Control: max-age=86400 (24 hours)
```

**Estimate:** +1-2 дні на caching implementation

---

## 5. Recommendations

### 🔥 Must-Have Changes

**1. Додати Technical Specs секцію в PRD:**

```markdown
## Technical Specifications

### Database Schema
```sql
CREATE TABLE vaccination_records (
  id UUID PRIMARY KEY,
  pet_id UUID REFERENCES pets(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  vaccine_name VARCHAR(255) NOT NULL,
  clinic VARCHAR(255),
  notes TEXT,
  version INT DEFAULT 1, -- для optimistic locking
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  created_by UUID REFERENCES users(id)
);

CREATE TABLE medical_documents (
  id UUID PRIMARY KEY,
  vaccination_record_id UUID REFERENCES vaccination_records(id) ON DELETE CASCADE,
  file_url TEXT NOT NULL,
  file_type VARCHAR(10) NOT NULL, -- jpg, png, pdf
  file_size_bytes INT NOT NULL,
  thumbnail_url TEXT, -- для preview
  uploaded_at TIMESTAMP DEFAULT NOW()
);
```

### API Contracts
```typescript
// POST /api/pets/:petId/vaccinations
interface CreateVaccinationRequest {
  date: string; // ISO 8601
  vaccine_name: string;
  clinic?: string;
  notes?: string;
  document?: File; // multipart/form-data
}

interface VaccinationResponse {
  id: string;
  pet_id: string;
  date: string;
  vaccine_name: string;
  clinic: string | null;
  notes: string | null;
  document: DocumentResponse | null;
  version: number;
  created_at: string;
  updated_at: string;
}
```
```

**2. Додати Error Handling секцію:**

```markdown
## Error Handling

### Upload Errors
- File too large (>10MB): "File size exceeds 10MB. Please choose a smaller file."
- Unsupported format: "Only JPG, PNG, and PDF files are supported."
- Network error: "Upload failed. Check your connection and try again."
- Storage quota exceeded: "Storage limit reached. Please contact support."

### Sync Errors
- Conflict detected: "This record was updated by [User Name]. Keep your changes or use theirs?"
- Network timeout: "Sync failed. Your changes are saved locally and will sync when online."

### PDF Export Errors
- Too many records (>100): "Export limited to 100 records. Please select a date range."
- Generation timeout: "PDF generation is taking longer than expected. We'll email it to you."
```

**3. Додати Performance Targets:**

```markdown
## Performance Targets

| Operation | Target | Measurement |
|-----------|:------:|-------------|
| Load medical history (20 records) | < 1s | p95 latency |
| Upload document (5MB, compressed) | < 8s | p95 latency |
| Generate PDF (50 records + images) | < 10s | p95 latency |
| Sync between devices | < 3s | p95 latency |

### Monitoring
- Track upload success rate (target: >95%)
- Track PDF generation success rate (target: >98%)
- Track sync conflict rate (target: <1%)
```

### 🟡 Nice-to-Have Improvements

**4. Phasing для зменшення ризику:**

```
Week 2 (MVP):
- ✅ Add vaccination record (text only, no documents)
- ✅ View medical history
- ✅ Basic sync

Week 3 (Documents):
- ✅ Upload documents
- ✅ Image compression
- ✅ Retry logic

Week 4 (Export):
- ✅ Export to PDF
- ✅ Share functionality
```

**Rationale:** Якщо PDF generation виявиться складнішим, ми все одно shipнемо core functionality.

**5. Додати Rollback Plan:**

```markdown
## Rollback Plan

### Критерії для rollback:
- Crash rate > 2%
- Upload success rate < 80%
- Critical security vulnerability

### Rollback process:
1. Feature flag: disable "Health" tab for new users
2. Keep existing users (no data loss)
3. Fix issue in hotfix branch
4. Re-enable after validation
```

---

## 6. Open Questions

### Технічні питання, які треба вирішити до Week 1:

**1. PDF Library Selection**

**Options:**
- **jsPDF** (client-side): 45KB, easy, але limited features
- **PDFKit** (server-side): powerful, але requires Node.js streams
- **react-native-pdf** (viewer only): не генерує PDF

**Питання:** Який library використовувати для generation?

**Рекомендація:** PDFKit на backend (async generation) + react-native-pdf для preview.

**2. Conflict Resolution UX**

**Scenario:** User A і User B одночасно редагують запис.

**Питання:** Який UX показувати при конфлікті?

**Options:**
- A) Dialog: "Keep your version" / "Use their version"
- B) Merge view (side-by-side comparison)
- C) Auto-merge (last write wins)

**Рекомендація:** Option A для V1 (simplest), Option B для V2.

**3. Offline Support Scope**

**Питання:** Чи підтримувати offline mode для V1?

**Trade-off:**
- Pros: кращий UX, працює без інтернету
- Cons: +2-3 дні development, складніша sync logic

**Рекомендація:** Skip для V1, додати в V2 якщо user feedback показує need.

**4. Image Thumbnail Generation**

**Питання:** Чи генерувати thumbnails для preview в списку?

**Trade-off:**
- Pros: швидший load списку, менше трафіку
- Cons: +1-2 дні, додатковий storage cost

**Рекомендація:** Yes, генерувати thumbnails (200×200px) на backend при upload.

**5. GDPR Compliance Details**

**Питання:** Чи потрібне end-to-end encryption для медичних даних?

**Current approach:**
- HTTPS (in transit) ✅
- Database encryption at rest (PostgreSQL) ✅
- Firebase Storage encryption (default) ✅

**Питання:** Чи достатньо цього для GDPR?

**Рекомендація:** Консультація з юристом до Week 1. Якщо потрібне E2E encryption — це +1-2 тижні development (out of scope для V1).

---

## Summary & Final Recommendation

### ✅ Go / No-Go: **GO with modifications**

**Що добре в PRD:**
- ✅ Чітка scope definition
- ✅ Realistic timeline (4 тижні)
- ✅ Добре продумані acceptance criteria
- ✅ Phasing plan (soft launch → full rollout)

**Що треба покращити:**
- ⚠️ Додати детальні technical specs (database schema, API contracts)
- ⚠️ Додати error handling strategy
- ⚠️ Додати performance targets + monitoring plan
- ⚠️ Вирішити open questions (PDF library, conflict resolution, GDPR)

**Ризики:**
- 🔴 PDF generation performance (mitigation: async generation)
- 🟡 Timeline tight (mitigation: phasing, skip offline mode для V1)
- 🟡 GDPR compliance (mitigation: legal review до Week 1)

**Final Estimate:**
- **Best case:** 3.5 тижні (якщо все йде smooth)
- **Realistic:** 4 тижні (як в PRD)
- **Worst case:** 5 тижнів (якщо PDF generation або GDPR стануть блокерами)

**Рекомендація:** Approve PRD з умовою, що:
1. Додамо technical specs секцію (1 день, PM + Tech Lead)
2. Вирішимо PDF library selection (1 день, spike)
3. Legal review для GDPR (1 день, консультація)

---

**Reviewer:** Andrii Melnyk (CTO)  
**Status:** ✅ Approved with modifications  
**Next Steps:**
- [ ] PM додає technical specs до PRD
- [ ] Tech Lead робить spike для PDF library (1 день)
- [ ] Legal review для GDPR compliance (1 день)
- [ ] Engineering kickoff meeting (Week 1, Day 1)
