# Чернетка поста для @olehmell_kitchen

Пробував Laya (typed-decisions) — open-source System 1 для структурованих рішень

Коротко: це не чат-модель. Ти даєш стан (лист, тікет, JSON) і вузькі typed-питання — так/ні з імовірністю (`noul`), вибір з списку (`choice`), оцінка по шкалі (`score`). Один forward pass, без генерації тексту: нічого парсити і «вигадати JSON». Далі код роутить / лейблить / ескалює.

По факту ближче до **енкодера з класифікаційними хедами**, ніж до генеративки: зрозумів текст → видав розподіл по твоїх класах. У Laya таксономію теж задаєш у питанні на льоту. Нюанс від авторів: base-чекпоінти на їх typed-decisions бенчі near-chance; цифра **~0.77** — це вже **`laya-typed-decisions`** після fine-tune під такі воркфлоу. Тобто «вау без тюну» тут слабше, ніж у маркетингу; вау скоріше **Apache 2.0 + self-host + свій FT/калібрування**.

По тарифікації контраст з генеративними ще жорсткіший: у LLM платиш і за input, і за роздутий output. У Laya на своєму залозі **$0 за API** (електрика/GPU твої). Для порівняння: hosted Jev зараз ~**$0.042 / 1M input**, output too cheap to meter.

Куди вже тикають (і куди сама Laya цілиться):

1. **Лейблінг пошти/тікетів** — spam/OOO vs живий клієнт, черга, urgency.
2. **Роутинг на агента** — intent + confidence → код / specialist LLM / людина.
3. **Guardrails / moderation** — jailbreak, toxicity, перед тим як кликати дорогу модель.
4. **Харнес** — який skill/модель вантажити, continue/retry/ask/stop.

Я паралельно ганяв entity-кейси (телефонні рядки UA, тези про людину, матч назв компаній) і порівняв **Jev API** з **Laya multilingual zero-shot** на тих самих датасетах. Коротко: Jev там 87–95%, Laya multilingual без FT — 19–44%. Це не вирок typed-decisions чекпоінту (його на цих сетах я ще не ганяв), а сигнал: open-source System 1 — це **база під спеціалізацію**, не drop-in «поставив і забув» на своєму домені.

Висновок для себе: typed System 1 (Laya / Jev-клас) — сенсори в софті, не заміна Claude/Codex. Генерацію лишаєш LLM; лейбл/роут/verify — у швидкий encoder-контур. Якщо потрібен self-host і контроль ваг — дивись Laya typed-decisions + свій FT. Якщо потрібен готовий hosted API «з коробки» на вузьких гейтах — поки зручніше Jev (у мене на PM-гейтах і skill-роутері воно вже лягало).

Хто вже ставив Laya в проді або FT під свій inbox — киньте в коменти, цікаво порівняти сетапи.

Laya: https://huggingface.co/convaiinnovations/laya · https://laya.convaiinnovations.com  
Мій бенч Jev vs Laya multilingual: https://github.com/olehmell/phd/blob/experiment/jev-entity-tasks/experiments/jev-entity-tasks/comparison/COMPARISON-LAYA-VS-JEV.md
