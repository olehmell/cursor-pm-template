# Чернетка поста для @olehmell_kitchen

Пробував Laya (typed-decisions) — open-source System 1 для структурованих рішень

Коротко: це не чат-модель. Ти даєш стан (лист, тікет, JSON) і вузькі typed-питання — так/ні з імовірністю (`noul`), вибір з списку (`choice`), оцінка по шкалі (`score`). Один forward pass, без генерації тексту: нічого парсити і «вигадати JSON». Далі код роутить / лейблить / ескалює.

По факту ближче до **енкодера з класифікаційними хедами**, ніж до генеративки: зрозумів текст → видав розподіл по твоїх класах. У Laya таксономію задаєш у питанні на льоту. Нюанс: base-чекпоінти на їх typed-decisions бенчі near-chance; цифра **~0.77** — це вже **`laya-typed-decisions`** після fine-tune під їх чотири воркфлоу. Тобто «вау без тюну» слабше, ніж у маркетингу; вау скоріше **Apache 2.0 + self-host + свій FT**.

По тарифікації: у LLM платиш і за input, і за роздутий output. У Laya на своєму залозі **$0 за API**. Для порівняння hosted Jev ~**$0.042 / 1M input**, output too cheap to meter.

Куди вже тикають:

1. **Лейблінг пошти/тікетів** — spam/OOO vs живий клієнт, черга, urgency.
2. **Роутинг на агента** — intent + confidence → код / specialist LLM / людина.
3. **Guardrails / moderation** — jailbreak, toxicity перед дорогою моделлю.
4. **Харнес** — який skill/модель вантажити, continue/retry/ask/stop.

Я прогнав entity-кейси (UA телефонні рядки, тези про людину, матч назв компаній) head-to-head на тих самих сетах (zero-shot, CPU): **Jev API** vs **Laya multilingual** vs **`laya-typed-decisions`** vs **jeff** (self-host drop-in під TypeSafe API на GLiFormer — те, про що писали в @zaduha).

| UC | Jev | Laya multi | Laya typed | jeff |
| --- | ---: | ---: | ---: | ---: |
| UC1 токени (phone-book) | **95%** | 26% | 16% | 23% |
| UC2 релевантність тези | **92%** | 44% | 56% | 56% |
| UC3 same-entity назв | **87%** | 19% | 60% | 20% |

Open-source картина: Laya typed краще за multi на UC2/UC3, jeff близький до typed на UC2, але UC1/UC3 у нього валяться (масове `прізвище` / `uncertain`). **Jev попереду на всіх трьох.** Висновок: self-host аналоги (Laya / jeff≈GLiFormer) — нормальна база під свій FT або дешевий контур, не drop-in паритет з hosted Jev на нашому UA entity-харнесі.

Висновок для себе: typed System 1 — сенсори в софті, не заміна Claude/Codex. Self-host + контроль ваг → Laya + свій FT. Готовий hosted API на вузьких гейтах → поки Jev (у мене на PM-гейтах і skill-роутері вже лягало).

Хто вже ставив Laya typed у проді або FT під свій inbox — киньте в коменти.

Laya typed: https://huggingface.co/convaiinnovations/laya-typed-decisions  
jeff (GLiFormer): https://github.com/logan-markewich/jeff  
Бенч: https://github.com/olehmell/phd/blob/experiment/jev-entity-tasks/experiments/jev-entity-tasks/comparison/COMPARISON-LAYA-VS-JEV.md
