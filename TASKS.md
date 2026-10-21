# Каталог под мои задачи

Зачем этот файл: звёзды я ставлю не «интересно вообще», а «вероятно пригодится». Здесь каждый
репозиторий привязан к одной из трёх текущих задач и к конкретному действию.

Три основные задачи и отдельный трек E — игры:

| Трек | Что это | Что считаем успехом |
|---|---|---|
| **A. Центр агентов** | Одно место, откуда запускаются, мониторятся и подтверждаются все агенты | Вижу статус всех сессий, ставлю задачи в очередь, подтверждаю действия, не переключаясь по терминалам |
| **B. Нативные macOS-приложения** | Dajet Player / Editor / Browser + новые утилиты, нативные интерфейсы | Продукт на Swift/SwiftUI, который неотличим от системного |
| **C. LOVII CRM** | CRM локальных маркетплейсов, где агент ведёт записи, а человек подтверждает | Агент сам обогащает карточки, каждое изменение — с доказательством |
| **E. Игры** | alien-cosmic, terran-rts, minigames — браузерные RTS и мини-игры | Играбельная сборка на GitHub Pages без сборщика; движок не мешает правилам |

Приоритеты: **P1** — брать в работу сейчас · **P2** — референс, когда дойдут руки ·
**P3** — полка (знать, что есть).

Полные описания всех 88 — в [STARS.md](./STARS.md). Разбор восьмёрки — в [STARS-REVIEW.md](./STARS-REVIEW.md).

**Доска каталога:** [BOARD.md](./BOARD.md) — те же репозитории, но по стадиям.

**Идеи с вариантами:** [OPTIONS.md](./OPTIONS.md) — 11 идей, у каждой формулировка и топ-3 репозитория (основной + альтернатива + дополнение).

---

## A. Центр агентов

**Что именно строим:** процесс-демон, который держит очередь задач, запускает агентов в песочницах,
собирает статусы и просит подтверждения. Интерфейс — панель + menu bar/нотч. Инструменты — MCP,
CLI, браузер. Модели — любые, с ротацией и учётом квот.

### Первые три шага

1. **Очередь задач вместо чата.** Взять модель из `BloopAI/vibe-kanban`: задача → несколько
   параллельных агентов → человек разбирает результат. Карточка задачи = единица работы.
2. **Единый прокси к моделям.** `lidge-jun/opencodex` — один клиент, любой провайдер, без
   переписывания кода при смене модели. Сверху — `razzant/claudexor` для учёта квот.
3. **Статус и подтверждения.** Схема из `asafofer/perch`: агент сам сообщает «закончил / прошу
   разрешения», человек отвечает из панели, одна клавиша возвращает в сессию.

### Репозитории

| Репозиторий | ★ | P | Что взять под центр агентов |
|---|---|---|---|
| [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | 256k | P2 | «Всё есть плагин»: инструменты, хуки, сессии как расширения. Скелет расширяемости ядра |
| [`code-yeongyu/oh-my-openagent`](https://github.com/code-yeongyu/oh-my-openagent) | 70k | P2 | Явный граф работ вместо свободного чата: как декомпозиция превращается в исполняемый DAG |
| [`XiaomiMiMo/MiMo-Code`](https://github.com/XiaomiMiMo/MiMo-Code) | 14k | P3 | Пример связки «агент под конкретную модель» и её ограничения |
| [`lidge-jun/opencodex`](https://github.com/lidge-jun/opencodex) | 18k | **P1** | Прокси-слой: один формат API для Claude/Gemini/Grok/DeepSeek. Ставить первым |
| [`razzant/claudexor`](https://github.com/razzant/claudexor) | 516 | P2 | Учёт квот и ротация аккаунтов между харнессами |
| [`BloopAI/vibe-kanban`](https://github.com/BloopAI/vibe-kanban) | 28k | **P1** | Модель «задача → параллельные агенты → разбор». Главный UX-референс для очереди |
| [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) | 163k | P2 | Ролевые инструкции агентов: брать структуру, не текст |
| [`ANDRETRIPOL/OpenGhost`](https://github.com/ANDRETRIPOL/OpenGhost) | 266 | P2 | Как устроен «агент на компьютере»: свой движок, инструменты ОС, разрешения |
| [`jgouviergmail/LIA-Assistant`](https://github.com/jgouviergmail/LIA-Assistant) | 75 | P2 | Human-in-the-Loop в LangGraph: где именно ставится подтверждение шага |
| [`danielmiessler/Fabric`](https://github.com/danielmiessler/Fabric) | 44k | **P1** | 266 паттернов + формат «папка = паттерн = system.md». Библиотека умений центра |
| [`Jeffallan/claude-skills`](https://github.com/Jeffallan/claude-skills) | 12k | **P1** | Структура `SKILL.md` + assets: как писать навыки, которые действительно работают |
| [`alirezarezvani/claude-skills`](https://github.com/alirezarezvani/claude-skills) | 28k | P2 | Источник идей и антипример: 380 навыков без каталога — свалка |
| [`bestdeejay-design/agent-skills`](https://github.com/bestdeejay-design/agent-skills) | 5 | **P1** | Своя точка сборки: сюда складывать отобранные навыки |
| [`bestdeejay-design/opencode-setup`](https://github.com/bestdeejay-design/opencode-setup) | 1 | **P1** | Своя среда: конфиги, MCP-серверы, сервис обслуживания |
| [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) | 97k | **P1** | Реестр MCP: сначала искать готовый сервер, потом писать свой |
| [`thesysdev/openui`](https://github.com/thesysdev/openui) | 13k | **P1** | Язык генерации UI (−67% токенов) + стриминговый рендер. Интерфейс для агента |
| [`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser) | 44k | **P1** | Браузерный инструмент агента: snapshot → действие → проверка. Замена Playwright-скриптов |
| [`larashero3-dotcom/lieflat-charts`](https://github.com/larashero3-dotcom/lieflat-charts) | 6.3k | P2 | Скилл, который отдаёт готовый HTML-график вместо зависимости в проекте |
| [`pascalorg/editor`](https://github.com/pascalorg/editor) | 25k | P2 | Упаковка «продукт + CLI + MCP» в одном репозитории |
| [`arthurpanhku/DocSentinel`](https://github.com/arthurpanhku/DocSentinel) | 88 | P2 | Маленький, но целый MCP-продукт: вход-документ, выход-оценка с обоснованием |
| [`langgenius/dify`](https://github.com/langgenius/dify) | 159k | P2 | Как устроена платформа воркфлоу: ноды, инструменты, графы |
| [`signerless/llm-checker`](https://github.com/signerless/llm-checker) | 3k | **P1** | CLI сканирует железо и говорит, какие модели потянет. Не гадать — померить |
| [`vava-nessa/free-coding-models`](https://github.com/vava-nessa/free-coding-models) | 2.8k | P2 | 170+ бесплатных кодовых моделей с бенчмарками |
| [`mnfst/awesome-free-llm-apis`](https://github.com/mnfst/awesome-free-llm-apis) | 11k | P2 | Постоянно бесплатные LLM API для прототипов |
| [`PurpleDoubleD/locally-uncensored`](https://github.com/PurpleDoubleD/locally-uncensored) | 2.4k | P2 | «Всё в одном» на локальных моделях: чат, картинки, видео, кодовый агент |
| [`NirDiamant/agents-towards-production`](https://github.com/NirDiamant/agents-towards-production) | 22k | **P1** | Курс до прода: память, observability, guardrails — ровно то, чего не хватает центру |
| [`NirDiamant/RAG_Techniques`](https://github.com/NirDiamant/RAG_Techniques) | 30k | P2 | 30+ техник RAG — под `knowledge-base` и `voice-assistant` |
| [`microsoft/ai-agents-for-beginners`](https://github.com/microsoft/ai-agents-for-beginners) | 78k | P2 | Систематическая база по агентам |
| [`patchy631/ai-engineering-hub`](https://github.com/patchy631/ai-engineering-hub) | 38k | P2 | Разборы реальных архитектур LLM-приложений |
| [`Shubhamsaboo/awesome-llm-apps`](https://github.com/Shubhamsaboo/awesome-llm-apps) | 142k | P2 | 100+ готовых приложений: брать целиком и адаптировать |
| [`arnabbagxd/Brand-building-skills`](https://github.com/arnabbagxd/Brand-building-skills) | 770 | P2 | Навыки по бренду: стратегия, нейминг, tone of voice — под AXIIOM |
| [`zai-org/GLM-skills`](https://github.com/zai-org/GLM-skills) | 476 | P3 | Официальный формат скиллов как эталон |
| [`YouMind-OpenLab/ai-image-prompts-skill`](https://github.com/YouMind-OpenLab/ai-image-prompts-skill) | 1315 | P3 | 10 000 промптов, упакованных в скилл |
| [`TonyL1u/nano-ai`](https://github.com/TonyL1u/nano-ai) | 172 | P3 | Компактный чат-UI с мультипровайдерностью |
| [`slavakurilyak/awesome-ai-agents`](https://github.com/slavakurilyak/awesome-ai-agents) | 2.5k | P3 | Навигация по агентной экосистеме |
| [`caramaschiHG/awesome-ai-agents-2026`](https://github.com/caramaschiHG/awesome-ai-agents-2026) | 2k | P3 | Срез 2026: что вообще существует |
| [`ShaikhWarsi/free-ai-tools`](https://github.com/ShaikhWarsi/free-ai-tools) | 1k | P3 | Бесплатные инструменты для экспериментов |
| [`bestdeejay-design/awesome-ai-handbook`](https://github.com/bestdeejay-design/awesome-ai-handbook) | 48 | P2 | Свой справочник: от локальной модели до своих агентов |
| [`bestdeejay-design/chronos`](https://github.com/bestdeejay-design/chronos) | 1 | P2 | 5 агентов для документации — готовый пример мульти-агентной схемы |
| [`mazze93/stratum`](https://github.com/mazze93/stratum) | 2 | P2 | Эпистемический леджер решений: тот же приём, что в crm, но в чистом виде |

**Чего в звёздах нет, а для центра нужно:** брокер очередей с приоритетами, хранилище сессий
агентов, слой секретов и политик. Это писать самому — донора нет.

---

## B. Нативные приложения macOS

**Что именно строим:** Dajet Player / Editor / Browser и рядом — утилиты в menu bar. Всё на
Swift/SwiftUI/AppKit, без Electron. Ключевое — ощущение системного приложения.

### Первые три шага

1. **Меню-бар и нотч как интерфейс.** `asafofer/perch` — самый свежий пример: Swift 6,
   `Package.swift`, `Sources/`, `Tests/`, стабильная локальная подпись через `make-dev-cert.sh`
   (иначе macOS сбрасывает разрешения при каждой пересборке).
2. **Гигиена деструктивных операций.** `tw93/Mole`: `--dry-run`, предпросмотр, явное
   подтверждение, лог. Переносится на любые «удалить/очистить».
3. **Доноры кода и карта рынка.** `jaywcjlove/awesome-swift-macos-apps` — разделы Audio,
   Browser, Editors, Local LLM, AI Agent Monitoring. Смотреть, где тесно, а где пусто.

### Репозитории

| Репозиторий | ★ | P | Что взять под macOS-линейку |
|---|---|---|---|
| [`asafofer/perch`](https://github.com/asafofer/perch) | 21 | **P1** | Нотч-UI, статусы агентов, approve/deny, возврат в сессию. Swift 6 + Tests — читаемый образец |
| [`tw93/Mole`](https://github.com/tw93/Mole) | 72k | **P1** | UX безопасной деструктивной утилиты: dry-run, предпросмотр, лог. Плюс open-core модель |
| [`jaywcjlove/awesome-swift-macos-apps`](https://github.com/jaywcjlove/awesome-swift-macos-apps) | 1.8k | **P1** | Карта рынка и доноры кода для Dajet-семейства |
| [`driceroland/Search`](https://github.com/driceroland/Search) | 2.6k | **P1** | База `dajet-browser`: минимум кода для нормального WebKit-браузера |
| [`ARahim3/DigUp`](https://github.com/ARahim3/DigUp) | 5.3k | **P1** | On-device поиск по содержимому файлов — upstream моего `DigUp` |
| [`gluonfield/enchanted`](https://github.com/gluonfield/enchanted) | 6k | P2 | Нативный клиент к локальным моделям: UI-референс для «AI внутри приложения» |
| [`PurpleDoubleD/locally-uncensored`](https://github.com/PurpleDoubleD/locally-uncensored) | 2.4k | P2 | Локальная AI-студия: как собрать чат + генерацию в одном приложении |
| [`clash-verge-rev/clash-verge-rev`](https://github.com/clash-verge-rev/clash-verge-rev) | 153k | P2 | Tauri-панель + системный трей + профили: референс, если понадобится кроссплатформенность |
| [`t8y2/dbx`](https://github.com/t8y2/dbx) | 27k | P2 | «Маленький нативный клиент» на Rust: 25 МБ против гигантов |
| [`bestdeejay-design/sweet-no-sleep`](https://github.com/bestdeejay-design/sweet-no-sleep) | 7 | P2 | Свой menu bar pet — база для будущих утилит в трее |
| [`obsproject/obs-studio`](https://github.com/obsproject/obs-studio) | 78k | P3 | Захват экрана/стриминг: справочник, если понадобится запись |
| [`dajetbro/dajetbro`](https://github.com/dajetbro/dajetbro) | 1 | P3 | Свой профиль бренда Dajet |

---

## C. LOVII CRM

**Что именно строим:** CRM, где агент обогащает карточки заведений/клиентов, а каждое изменение
несёт доказательство. Человек только подтверждает спорное. Плюс оплата, роли, аудит.

### Первые три шага

1. **Леджер доказательств.** `trycompai/crm`: инструменты возвращают наблюдения
   (`crm.signature-block`, `github.account-identity`), а леджер решает — писать в запись или
   отдать человеку как предложение. Никаких «уверен на 0.8».
2. **Права и роли для агента.** `croffasia/itsaplan`: у агента есть роль, права и слот
   исполнителя. Часть действий требует approve. **Лицензия AGPL-3.0 — изучать, но код не втаскивать.**
3. **Тесты оплаты без провайдера.** `rucorp/mock-services`: моки эквайринга и ОФД.

### Репозитории

| Репозиторий | ★ | P | Что взять под lovii-crm |
|---|---|---|---|
| [`trycompai/crm`](https://github.com/trycompai/crm) | 12k | **P1** | `apps/agent/agent/tools/` (24 инструмента), `skills/evidence.md`, `identity-matching.md`, `schedules/`, `adrs/`. Эталон целиком |
| [`croffasia/itsaplan`](https://github.com/croffasia/itsaplan) | 1.7k | **P1** | Роли/права агента, назначение задач, REST + webhooks + MCP. Только чтение (AGPL) |
| [`rucorp/mock-services`](https://github.com/rucorp/mock-services) | 6 | **P1** | Моки банковского эквайринга и ОФД: тестировать оплату без реальных ключей |
| [`mazze93/stratum`](https://github.com/mazze93/stratum) | 2 | P2 | Append-only леджер решений с гейтами доверия — концепция «доказательство вместо уверенности» |
| [`reconurge/flowsint`](https://github.com/reconurge/flowsint) | 9.9k | P2 | Граф связей и визуальное расследование — антифрод, связи заведений/клиентов |
| [`arthurpanhku/DocSentinel`](https://github.com/arthurpanhku/DocSentinel) | 88 | P2 | MCP-оценка документов и опросников: проверка карточек по документам |
| [`presenton/presenton`](https://github.com/presenton/presenton) | 11k | P2 | Документ → презентация, self-hosted, с API. КП и отчёты для клиентов |
| [`langgenius/dify`](https://github.com/langgenius/dify) | 159k | P2 | Self-hosted RAG/воркфлоу: поддержка базы знаний по заведениям |
| [`oauth2-proxy/oauth2-proxy`](https://github.com/oauth2-proxy/oauth2-proxy) | 15k | P2 | Закрыть внутренние сервисы логином без написания auth |
| [`caddyserver/caddy`](https://github.com/caddyserver/caddy) | 78k | P2 | HTTPS/деплой self-hosted: один бинарь, сертификаты сами |
| [`thedaviddias/Front-End-Checklist`](https://github.com/thedaviddias/Front-End-Checklist) | 75k | P2 | Приёмочный чек-лист интерфейсов: встроить в ревью lovii-crm и лендингов AXIIOM |
| [`pawelmalak/flame`](https://github.com/pawelmalak/flame) | 6.6k | P3 | Внутренний портал со ссылками на сервисы |
| [`lovii-tech/lovii-core`](https://github.com/lovii-tech/lovii-core) | 1 | **P1** | Своё ядро платформы |
| [`lovii-tech/lovii-app`](https://github.com/lovii-tech/lovii-app) | 1 | **P1** | Своё клиентское приложение (Vue) |
| [`lovii-tech/lovii-admin`](https://github.com/lovii-tech/lovii-admin) | 1 | **P1** | Своя админка |
| [`lovii-tech/lovii-b2b`](https://github.com/lovii-tech/lovii-b2b) | 1 | **P1** | Своя B2B-часть |
| [`bestdeejay-design/lovii`](https://github.com/bestdeejay-design/lovii) | 4 | P2 | Публичный фасад платформы |
| [`bestdeejay-design/lovii-demo`](https://github.com/bestdeejay-design/lovii-demo) | 3 | P3 | Демо для клиентов |
| [`axiiom-ru/lovii`](https://github.com/axiiom-ru/lovii) | 1 | P3 | Документы для публикации |
| [`rucorp/accounts`](https://github.com/rucorp/accounts) | 1 | P2 | Карта аккаунтов, почт, SSH — операционная гигиена |

---

## D. Модели, медиа и прочее

| Репозиторий | ★ | P | Что взять |
|---|---|---|---|
| [`koda-dernet/Side-Step`](https://github.com/koda-dernet/Side-Step) | 159 | P2 | Обучение/инференс ACE-Step 1.5: своя генерация музыки для `dajet` и `joer` |
| [`QwenLM/Qwen-Image`](https://github.com/QwenLM/Qwen-Image) | 8.4k | P3 | Картинки с сильным рендером текста: баннеры, обложки |
| [`zai-org/GLM-Image`](https://github.com/zai-org/GLM-Image) | 1.1k | P3 | Авторегрессионная генерация изображений — архитектурно интересно |
| [`XiaomiMiMo/MiMo-V2-Flash`](https://github.com/XiaomiMiMo/MiMo-V2-Flash) | 1.4k | P3 | Дешёвая reasoning-модель под агентные циклы |
| [`Tencent-Hunyuan/Hy3`](https://github.com/Tencent-Hunyuan/Hy3) | 671 | P3 | Экономика инференса 295B MoE |
| [`BEPb/image_to_prompt`](https://github.com/BEPb/image_to_prompt) | 49 | P3 | Картинка → промпт (2023, учебный) |
| [`BEPb/Image_Colorization`](https://github.com/BEPb/Image_Colorization) | 53 | P3 | Раскрашивание ч/б (2023, учебный) |
| [`delbeke/vectorizer`](https://github.com/delbeke/vectorizer) | 4 | P3 | Растр → SVG, простой пример |
| [`bestdeejay-design/raster-to-svg`](https://github.com/bestdeejay-design/raster-to-svg) | 1 | P3 | Свой PNG→SVG конвертер |
| [`bestdeejay-design/imgforge`](https://github.com/bestdeejay-design/imgforge) | 1 | P3 | Обрезка/оптимизация картинок в браузере |
| [`laravel/laravel`](https://github.com/laravel/laravel) | 85k | P2 | Заготовка под PHP-проекты (`basedata`, `lovii-tech`) |
| [`ashleve/lightning-hydra-template`](https://github.com/ashleve/lightning-hydra-template) | 5.4k | P3 | Правильная структура ML-экспериментов, если понадобится обучение |
| [`bestdeejay-design/ksu`](https://github.com/bestdeejay-design/ksu) | 1 | P3 | Портфолио дизайнера |
| [`bestdeejay-design/shimmer`](https://github.com/bestdeejay-design/shimmer) | 6 | P3 | Книга/сайт «Мерцание» |
| [`bestdeejay-design/bestdeejay-design`](https://github.com/bestdeejay-design/bestdeejay-design) | 4 | P3 | Профиль GitHub |
| [`axiiom-ru/axiiom-ru`](https://github.com/axiiom-ru/axiiom-ru) | 1 | P3 | Профиль AXIIOM |
| [`rucorp/arental`](https://github.com/rucorp/arental) | 1 | P3 | Лендинг digital-агентства |

**Снять звезду / не тратить время:**

| Репозиторий | Почему |
|---|---|
| [`kriptong/litca-ru`](https://github.com/kriptong/litca-ru) | Нет описания, пусто, назначение неизвестно |
| [`1Crazymoney/agency-agents`](https://github.com/1Crazymoney/agency-agents) | Копия `msitarzewski/agency-agents` |
| [`1Crazymoney/mythos-agent`](https://github.com/1Crazymoney/mythos-agent) | 2 звезды, признаков жизни нет |

## E. Игры

**Что это на самом деле.** `alien-cosmic` — своя игра на своём движке, не мод и не форк: свой
фиксированный тик 30 Гц, свой A*, свои приказы, свой ИИ, свой баланс в `config.js`. Внешние
движки здесь не фундамент — ядро уже написано. Они могут пригодиться только точечно.

**Что уже есть (по коду и документации репозитория).**

- 17 модулей, ~684 КБ исходников на чистом JS: без сборки, без зависимостей, ES-модули.
- Логика и рендер разделены: `Game.tick()` с фиксированным шагом, `Game.render(alpha)` с
  интерполяцией `prevX/prevY → x/y`.
- Приказы — данные (`unit.order`: move, attackMove, attack, gather, build, repair, garrison).
  Это и есть заготовка реплеев и сетевой игры: команда сети = та же структура приказа.
- Баланс целиком в `config.js`: юниты, здания, улучшения, биомы, профиль ИИ.
- 15 миссий в 3 актах, 3 фракции, 8 зданий, 8 юнитов × 2 скина, туман войны, синтезированный
  звук через Web Audio, генератор карт с гарантией проходимости.
- **Проверки уже есть:** `scripts/check.mjs` (статический анализ), `scripts/smoke.mjs`
  (прогон всей игры headless через реальный `game.js`) и **17** `scripts/sim_*.mjs`
  (движение, добыча, стройка, ремонт, туман, экономика, UI, тач, i18n).
- **Своя доска уже есть:** `scripts/gh_board_setup.py` создаёт GitHub Projects V2
  «Alien Cosmic — задачи» со статусами Бэклог / К работе / В работе / На проверке / Ждёт / Готово;
  `scripts/gh_issues_seed.py` — посев задач в Issues. Оба идемпотентны, нужен токен со скоупом `project`.
- Документация: `ARCHITECTURE.md`, `ROADMAP.md`, `SCENARIO.md`, аудиты, дизайн-система,
  `design/ZAI_MAILBOX.md` и `ARENA_TASK.md` — переписка с внешними агентами прямо в репозитории.

**Чего нет (по факту проверки дерева репозитория).**

| Пробел | Почему это важно | Приоритет |
|---|---|---|
| **Нет CI**: `.github/` — 0 файлов, `package.json` нет | 17 симов и smoke не запускаются сами: регресс попадает в `main`, только если забыл прогнать руками | **P1** |
| Нет единой команды запуска | В `scripts/` **62 файла** (симы, проверки, одноразовые прогоны, генераторы скриншотов). Новичок не знает, что и в каком порядке гонять | **P1** |
| `units.js` 134 КБ, `ui.js` 102 КБ, `game.js` 88 КБ | Каждая правка — риск задеть соседнее; диффы огромные | P1 |
| Репозиторий 66 МБ, скриншоты в `design/shots` | Клон и работа агентов замедляются | P2 |
| Реплеев нет, хотя приказы уже данные | Без реплея нет отладки баланса и нет сети | P2 |
| Сеть (lockstep) не начата | Архитектура готова, реализации нет | P3 |
| Две доски: Projects в alien-cosmic и `agent-hub` отдельно | Раздвоение статусов: задача есть там, а отчёт здесь. Оставить одну | P2 |
| Токен читается из `git remote get-url` | Токен лежит в `.git/config`; при утечке — доступ к репозиторию. Нужен `gh auth token` или env | P2 |

**Первые три шага.**

1. **Раннер + CI.** Задание уже лежит в репозитории: [`TASK_CI_AND_TESTS.md`](https://github.com/bestdeejay-design/alien-cosmic/blob/main/TASK_CI_AND_TESTS.md).
   Одна команда `node scripts/test.mjs`, за ней `.github/workflows/ci.yml`. Это дешевле любого
   рефакторинга и сразу закрывает главную дыру.
2. **Разрезать `units.js` и `ui.js`** по швам, которые уже есть в коде: движение, бой, добыча,
   ремонт; для UI — панели, тултипы, миникарта.
3. **Реплей как лог команд** `(тик, приказ, цель)` + детерминированный прогон — фундамент сети.

**Решение по доске.** Основная — GitHub Projects V2 в `alien-cosmic` (`gh_board_setup.py`).
`agent-hub` для этого проекта не используется: он про протокол отчётов агентов, а не про
доску задач. Зафиксировано в `TASK_CI_AND_TESTS.md`, §10.

**Свои репозитории**

| Репозиторий | ★ | P | Роль |
|---|---|---|---|
| [`bestdeejay-design/alien-cosmic`](https://github.com/bestdeejay-design/alien-cosmic) | 6 | **P1** | Игра и движок. Основная линия развития |
| [`bestdeejay-design/alien-cosmic-dist`](https://github.com/bestdeejay-design/alien-cosmic-dist) | 1 | **P1** | Приватный дом разработки: исходники, история, ресерчи, симы |
| [`bestdeejay-design/terran-rts`](https://github.com/bestdeejay-design/terran-rts) | 0 | P2 | Отдельный полигон стиля StarCraft на Canvas — не часть alien-cosmic |
| [`bestdeejay-design/minigames`](https://github.com/bestdeejay-design/minigames) | 0 | P3 | Мини-игры для проверки механик на малом объёме |

**Внешние движки — только точечно (не фундамент)**

| Репозиторий | ★ | Лицензия | Когда брать |
|---|---|---|---|
| [`pixijs/pixijs`](https://github.com/pixijs/pixijs) | 48k | MIT | Если Canvas 2D перестанет держать кадр на больших картах: WebGL-рендер, батчинг |
| [`OpenRA/OpenRA`](https://github.com/OpenRA/OpenRA) | 18k | GPL-3.0 | Референс по очередям приказов и netcode. Только чтение, код не втаскивать |
| [`phaserjs/phaser`](https://github.com/phaserjs/phaser) | 41k | MIT | Не нужен: своя логика и сцены уже есть. Смотреть только идеи организации сцен |
| [`excaliburjs/Excalibur`](https://github.com/excaliburjs/Excalibur) | 2.4k | BSD-2 | То же: альтернатива своему циклу, а не дополнение |
| [`kaplayjs/kaplay`](https://github.com/kaplayjs/kaplay) | 1.8k | MIT | Для быстрых прототипов мини-игр, не для RTS |
| [`boardgameio/boardgame.io`](https://github.com/boardgameio/boardgame.io) | 12k | MIT | Не подходит: пошаговые игры, а не RTS в реальном времени |

---

## Сводка: что делать в первую очередь

| # | Действие | Репозиторий | Трек |
|---|---|---|---|
| 1 | Поставить прокси провайдеров и перестать переписывать клиентов | `opencodex` | A |
| 2 | Взять схему очереди задач у vibe-kanban | `vibe-kanban` | A |
| 3 | Внедрить «наблюдение → леджер → запись/предложение» | `trycompai/crm` | C |
| 4 | Моки оплаты в тестах LOVII | `rucorp/mock-services` | C |
| 5 | Browser-инструмент агента вместо Playwright-скриптов | `agent-browser` | A |
| 6 | Нотч-панель статусов агентов на Swift 6 | `perch` | A+B |
| 7 | Пройти `agents-towards-production` (память, observability, guardrails) | `NirDiamant` | A |
| 8 | Ввести в репозитории `AGENTS.md` + `.agents/` + `llms.txt` | `Mole`, `crm` | все |
| 9 | Разделить симуляцию и рендер в alien-cosmic | своё | E |

---

## Как держать актуальным

- `python3 sync_stars.py` — сверяет каталог с реальными звёздами, показывает новые и снятые.
- `python3 sync_stars.py --apply` — применяет: снятые звёзды переносит в `STARS-ARCHIVE.md`
  (с датой, звёздами, языком и описанием) и убирает их строки из рабочих файлов.
- Автопроверка каждые 48 часов: cron-задача сама запускает сверку, дописывает новые звёзды
  с описанием и треком, отправляет снятые в архив, коммитит и присылает отчёт.
- Новая звезда вручную: сначала сюда (трек + P + «что взять»), потом в `STARS.md` (категория + описание).
- Раз в квартал: пересмотреть P1 — если за квартал не пригодилось, опустить в P2/P3.
- Если репозиторий перестал быть нужен — снять звезду и строку, иначе каталог теряет смысл.
