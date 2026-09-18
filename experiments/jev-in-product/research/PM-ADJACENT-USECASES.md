# Юзкейси, які вже «знайшли» люди — і як вони лягають на PM-світ

Джерела: [TypeSafe use-case map](https://docs.typesafe.ai/concepts/use-case-map.md), [intent routing](https://docs.typesafe.ai/patterns/intent-routing.md), cookbooks, публічні інтеграції (Cloudflare AI, Vercel AI Gateway, Laravel/There There helpdesk, блоги).

Спільний патерн: **не генерувати відповідь**, а за один виклик отримати набір typed рішень → код роутить / лейблить / ескалює.

## 1. Лейблінг вхідної пошти / тікетів

**Що роблять:** паралельні noul/choice на листі:
- це людина чи auto-reply / bounce / spam? (There There + Laravel AI SDK — Freek Van der Herten)
- тема: billing / account / technical / sales
- urgency, frustration, refund intent

**Навіщо:** не платити LLM за summary на кожен OOO; зберегти лейбли в БД і ганяти workflow по колонках.

**PM-аналог:** inbox зворотного зв’язку, Intercom, App Store reviews, sales inbound — ті самі сенсори, інша таксономія продукту.

## 2. Роутинг «на якого агента / чергу»

**Що роблять (docs + Cloudflare examples):**
- Choice: яка черга / який specialist LLM / deterministic handler
- Score: complexity
- confidence < threshold → людина

**Intent routing pattern:** order_status → код без LLM; product_question → specialist LLM; complaint + high complexity → human.

**PM-аналог / оркестрація агентів:**
- тікет → support bot vs billing agent vs eng on-call vs PM
- внутрішній запит → analysis skill vs PRD skill vs prototype (наш U5)
- «який subagent у harness» (Vercel: next tool/subagent у agent loop)

## 3. Лейблінг запитів користувачів (продукт)

**Що в map:** classify intent, product area; detect churn / purchase intent; theme-label interview/survey passages (scientific discovery — прямо про transcripts).

**PM-аналог:**
- feature requests → theme + must-have/later
- NPS verbatims / research quotes → multi-label pain sensors (наш U1 reframing)
- feedback із Telegram/Discord → bucket для backlog

## 4. Оркестрація мультиагентних систем

**Harness engineering (TypeSafe categories):**
- model routing (дешевий vs дорогий LLM)
- skill suggestion (cookbook: 182 skills → suggest at most one)
- continue / retry / ask user / stop
- classify agent traces після рану

**PM-аналог:** Cursor/agent workspace: який use-case завантажити; чи взагалі потрібен скіл; куди ескалювати невпевненість.

## 5. Верифікація того, що вже згенерував LLM

**Universal verification:**
- citation check (чи цитата підтримує claim)
- guardrails на input/output/tool calls
- чи відповідь support відповідає політиці

**PM-аналог:** після драфту PRD — «метрика вимірювана?», «claim підкріплений COMPANY.md?» (наш E2 + U3).

## 6. Lead / recruiting / marketplace (сусідні)

Менш «класичний PM», але той самий м’яз:
- ICP fit + purchase intent на inbound
- resume vs rubric → route to hiring manager
- listing moderation / brand safety

## Карта «форма рішення → PM-приклад»

| Форма | Приклад у PM |
| --- | --- |
| Classification | intent тікета, тема фіч-реквесту |
| Detection | spam/OOO, refund intent, jailbreak у user prompt |
| Scoring | urgency, frustration, CTA clarity |
| Routing | черга / agent / skill |
| Ranking / retrieval | який chunk context дати LLM перед PRD |
| Verification | claim vs джерело, policy lint |

## Що взяти собі з цього списку

Найближче до вже доведеного в наших експериментах:
1. **Mail/ticket triage** (лейбли + роут) — як E2/E3 + публічний helpdesk кейс
2. **Agent/skill orchestration** — U5
3. **Feedback labeling** — U1 (multi-noul), не exclusive theme
4. **Post-LLM PRD/answer verify** — U2/U3

Далі по цінності для «живого продукту»: inbox лейблінг + роут на агента з confidence-gate.
