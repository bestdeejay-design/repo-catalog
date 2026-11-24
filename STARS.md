# Каталог звёзд — внешние репозитории

Что это: каталог чужих репозиториев, которым я поставил ⭐, с описанием на русском —
что это на самом деле, чем полезно и что из него можно забрать в свои проекты.

- Всего в звёздах: **134** (сверено через `gh api user/starred`, 2026-11-24)
- Свои репозитории здесь не дублируются полностью — только те, что я лайкнул (раздел «Свои»).
- Каталог **моих** репозиториев — в [README.md](./README.md).
- Обратная сторона — [RATING.md](./RATING.md): сколько ⭐ собрали мои репозитории (считает `stars_received.py`).
- Подробный разбор девятки — в [STARS-REVIEW.md](./STARS-REVIEW.md).
- **Куда применять: [TASKS.md](./TASKS.md)** — все звёзды, привязанные к трём текущим задачам (центр агентов, macOS-приложения, lovii-crm) с приоритетами.
- Идеи и «что читать руками» — в [IDEAS.md](./IDEAS.md).
- **Идеи с вариантами: [OPTIONS.md](./OPTIONS.md)** — 11 идей, у каждой формулировка и топ-3 репозитория.
- Снятые звёзды не пропадают: они уходят в [STARS-ARCHIVE.md](./STARS-ARCHIVE.md) (история).
- **Игры:** отдельный трек E в [TASKS.md](./TASKS.md) — в звёздах из игрового один движок-референс
  (`fheroes2`, раздел 13), остальное ведётся там (свои проекты + кандидаты на разбор).
- Когда была последняя проверка — в [STARS-STATUS.md](./STARS-STATUS.md).

Легенда: ★ — звёзды на момент снятия слепка · 🟢 брать в работу · 🟡 полезно как справочник · ⚪ просто на полке.

Обновление слепка: `gh api 'user/starred?per_page=100' --paginate` → сверить состав.

---

## 1. Агенты и обвязка вокруг них (13)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | 256k | TS | Харнесс для агентов, где «всё есть плагин» | 🟢 Эталон плагинной архитектуры агента: инструменты, хуки, сессии — как отдельные расширения, а не ветки в коде |
| [`code-yeongyu/oh-my-openagent`](https://github.com/code-yeongyu/oh-my-openagent) | 70k | TS | Агентный раннер с «graph engineering»: ключевым словом собирает граф задач | 🟢 Идея явного графа работ вместо свободного чата; смотреть, как декомпозиция превращается в исполняемый DAG |
| [`XiaomiMiMo/MiMo-Code`](https://github.com/XiaomiMiMo/MiMo-Code) | 14k | TS | Кодовый агент, где модель и агент ко-эволюционируют | 🟡 Пример, как продуктовый агент связан с конкретной моделью и её ограничениями |
| [`lidge-jun/opencodex`](https://github.com/lidge-jun/opencodex) | 18k | TS | Прокси-слой: один формат API для Claude/Gemini/Grok/DeepSeek под Codex и Claude Code | 🟢 Практичная вещь: держать одного клиента и менять провайдера без переписывания |
| [`razzant/claudexor`](https://github.com/razzant/claudexor) | 516 | TS | Control plane над несколькими харнессами (Claude Code, Codex, Cursor, OpenCode) с учётом квот и ротацией | 🟡 Как жить с лимитами: квоты, ротация аккаунтов, единый диспетчер запусков |
| [`Alishahryar1/free-claude-code`](https://github.com/Alishahryar1/free-claude-code) | 64k | Python | Мульти-харнесс: Claude Code, Codex, Antigravity, VSCode, Pi и OpenCode через один вход | 🟢 Референс к центру агентов: как несколько CLI-агентов жить под общим интерфейсом без переписывания |
| [`BloopAI/vibe-kanban`](https://github.com/BloopAI/vibe-kanban) | 28k | Rust | Канбан-доска поверх coding-агентов | 🟡 Приём «очередь задач → параллельные агенты»: человек не сидит в чате, а разбирает результат |
| [`leepokai/Codync`](https://github.com/leepokai/Codync) | 901 | Rust | Опенсорсная замена Grok Bot: свои подписки Claude Code, Codex, Gemini CLI, Cursor и ещё 40+ агентов как боты, которым пишешь с телефона | 🟡 Прямой референс к центру агентов: хост на Rust, iOS-приложение на SwiftUI, Electron на десктопе. Смотреть, как устроен мост «мессенджер ↔ локальный агент» и как агент живёт вне терминала |
| [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) | 163k | Shell | «Агентство» из ролевых агентов (фронтенд, SMM, исследования) | ⚪ Огромный сборник ролей-промптов; брать как идеи ролевых инструкций, не как код |
| [`ANDRETRIPOL/OpenGhost`](https://github.com/ANDRETRIPOL/OpenGhost) | 266 | JS | Десктопный AI-агент для Win/macOS/Linux с собственным движком | 🟡 Как устроен «агент на компьютере»: свой engine, инструменты ОС, локальные разрешения |
| [`jgouviergmail/LIA-Assistant`](https://github.com/jgouviergmail/LIA-Assistant) | 75 | Python | Мульти-агентный ассистент на LangGraph с Human-in-the-Loop | 🟡 Готовая схема «человек подтверждает шаг» в LangGraph-графе |
| [`affaan-m/ECC`](https://github.com/affaan-m/ECC) | 310k | JS | Харнесс-оптимизация агентов: наборы навыков, «инстинктов», памяти, безопасности и research-first цикла для Claude Code, Codex, Opencode, Cursor | 🟡 Как поведение агента разложено на переносимые слои (навык / инстинкт / память / политика) — сверять со своим `AGENTS.md`, забирать структуру, не объём |
| [`Graphify-Labs/graphify`](https://github.com/Graphify-Labs/graphify) | 153k | Python | Кодовая база вместе с доками, SQL-схемами, конфигами и PDF превращается в граф знаний: локальный детерминированный разбор AST (tree-sitter), у каждого ребра объяснение, векторного хранилища нет; оформлено как скилл `/graphify` для Claude Code, Cursor, Codex, Gemini CLI | 🟢 Под `knowledge-base` и `lovii-crm`: граф вместо «нарезки на чанки» — связи и происхождение каждого ребра видны, ответ можно проверить. Смотреть заодно, как скилл упаковал тяжёлый пайплайн |

## 2. Промпты, скиллы, паттерны (15)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`nick-vels/skills`](https://github.com/nick-vels/skills) | 530 | HTML | Скилл Autopilot: идея → спека → нарезка на задачи → сборка → приёмка по исходному брифу | 🟢 Эталон «спека вместо чата»: агент спрашивает только в точках развилки и сам открывает дашборд прогресса. Забирать схему стадий, а не текст |
| [`danielmiessler/Fabric`](https://github.com/danielmiessler/Fabric) | 44k | Go | CLI + библиотека «паттернов» — **266** промпт-шаблонов в `data/patterns` | 🟢 Лучшая в мире коллекция прикладных промптов: саммари, разбор статей, письмо в своём голосе. Каждый паттерн — отдельная папка с `system.md` |
| [`Jeffallan/claude-skills`](https://github.com/Jeffallan/claude-skills) | 12k | Python | 67 навыков для full-stack разработчика | 🟢 Набор рабочих skill-файлов: смотреть структуру `SKILL.md` + assets, а не текст |
| [`alirezarezvani/claude-skills`](https://github.com/alirezarezvani/claude-skills) | 28k | Python | 380+ навыков, 30+ агентов, 70+ команд | 🟡 Крупнейшая свалка скиллов — как источник идей и как антипример «много, но без системы» |
| [`arnabbagxd/Brand-building-skills`](https://github.com/arnabbagxd/Brand-building-skills) | 770 | Shell | Навыки по бренду: стратегия, нейминг, айдентика, tone of voice | 🟡 Прямо под AXIIOM/бренд-проекты: чек-листы, а не «магия» |
| [`YouMind-OpenLab/ai-image-prompts-skill`](https://github.com/YouMind-OpenLab/ai-image-prompts-skill) | 1315 | TS | 10 000+ промптов для картинок, оформлено как skill | 🟡 Библиотека промптов + способ упаковать её в скилл |
| [`zai-org/GLM-skills`](https://github.com/zai-org/GLM-skills) | 476 | Python | Официальные скиллы для семейства GLM | ⚪ Официальный формат скиллов — полезно как референс «как надо» |
| [`larashero3-dotcom/lieflat-charts`](https://github.com/larashero3-dotcom/lieflat-charts) | 6.3k | HTML | Навык, который превращает данные в интерактивные HTML-графики | 🟢 Идея «скилл вместо библиотеки»: результат — готовый HTML, а не зависимость в проекте |
| [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) | 97k | — | Каталог MCP-серверов | 🟢 Главный справочник по MCP: искать готовый сервер раньше, чем писать свой |
| [`bestdeejay-design/agent-skills`](https://github.com/bestdeejay-design/agent-skills) | 5 | Python | Мой набор из 59 скиллов | ⚪ Своё — точка сборки личных скиллов |
| [`Nutlope/hallmark`](https://github.com/Nutlope/hallmark) | 41k | CSS | Анти-«AI-slop» скилл для дизайна: правила, как не выглядеть шаблонно | 🟡 Забрать приёмы в свои дизайн-скиллы и в проверку вёрстки перед сдачей |
| [`heydamir/unslop`](https://github.com/heydamir/unslop) | 8.3k | JS | Скилл для Claude Code и Codex: находит в интерфейсе признаки «вайбкода» (фиолетовые градиенты, свечения, эмодзи-подписи, крикливые заголовки, неровные отступы) и переделывает экран проходами, как дизайнер на ревью | 🟢 Прямо в приёмку лендингов AXIIOM и прототипов: сначала аудит и направление из продукта, потом правки слоями — отступы, цвет, иконки, текст, типографика, сетка, детали, движение. Работает в React/Vue/Svelte/Tailwind и по одной ссылке на живой сайт |
| [`ComposioHQ/awesome-claude-skills`](https://github.com/ComposioHQ/awesome-claude-skills) | 80k | Python | Курируемый список Claude-скиллов, ресурсов и инструментов для настройки агентных воркфлоу | 🟡 Каталог «что уже сделано скиллом» — искать здесь раньше, чем писать своё (там же Composio, Rube, MCP-обвязки) |
| [`multica-ai/andrej-karpathy-skills`](https://github.com/multica-ai/andrej-karpathy-skills) | 235k | — | Один файл `CLAUDE.md`, который правит поведение Claude Code: наблюдения Андрея Карпати о типичных ошибках LLM в коде | 🟢 Антипример к «простыне правил»: короткий файл, где каждая строка — конкретная ошибка и запрет. Прямо в наш `AGENTS.md` |
| [`obsidianmd/obsidian-skills`](https://github.com/obsidianmd/obsidian-skills) | 54k | Shell | Официальные скиллы Obsidian: учат агента работать с Markdown, Bases и JSON Canvas | 🟡 Как вендор описывает свои открытые форматы для агента — образец скилла к собственному формату (`personal-os`, заметки) |

## 3. Готовые продукты, у которых учатся архитектуре (8)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`trycompai/crm`](https://github.com/trycompai/crm) | 12k | TS | CRM, спроектированная «вокруг агента»: агент — не фича, а тот, кто ведёт заметки | 🟢 Лучший в подборке пример агент-first продукта: evidence-леджер, инструменты, которые сообщают наблюдения, а не уверенность |
| [`croffasia/itsaplan`](https://github.com/croffasia/itsaplan) | 1.7k | TS | Self-hosted альтернатива Linear/Plane, где агенты — полноценные исполнители | 🟢 Референс «агент как участник команды»: роли, права, назначение задач, REST + webhooks + MCP |
| [`reconurge/flowsint`](https://github.com/reconurge/flowsint) | 9.9k | TS | Платформа графовых расследований (кибербез) | 🟡 Как строить расширяемый граф-редактор и визуальный анализ связей — под антифрод/финтех |
| [`arthurpanhku/DocSentinel`](https://github.com/arthurpanhku/DocSentinel) | 88 | Python | MCP-сервер для оценки документов и опросников по безопасности | 🟡 Узкий, но аккуратный кейс «MCP как продукт»: вход — документ, выход — оценка с обоснованием |
| [`presenton/presenton`](https://github.com/presenton/presenton) | 11k | TS | Открытый генератор презентаций с API (аналог Gamma) | 🟢 Прямой кандидат в пайплайн: слайды по документу + API, self-hosted |
| [`langgenius/dify`](https://github.com/langgenius/dify) | 159k | Python | Платформа для агентных воркфлоу и RAG | 🟡 Индустриальный стандарт self-hosted LLM-платформы: как устроены графы, ноды, инструменты |
| [`mazze93/stratum`](https://github.com/mazze93/stratum) | 2 | HTML | «Эпистемический леджер решений»: append-only лог с гейтами доверия | 🟡 Малоизвестно, но концепция совпадает с crm: решения с доказательствами, а не с уверенностью |
| [`pawelmalak/flame`](https://github.com/pawelmalak/flame) | 6.6k | TS | Self-hosted стартовая страница с закладками | 🟡 Простой референс «домашний портал»: можно поднять как внутренний портал AXIIOM |

## 4. Generative UI и фронтенд (6)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`thesysdev/openui`](https://github.com/thesysdev/openui) | 13k | TS | Открытый стандарт generative UI: компактный язык разметки, который модель стримит и рантайм рисует | 🟢 Ключевая идея: UI как токен-экономный DSL (до −67% токенов против JSON) + стриминг в React/Vue/Svelte/Angular |
| [`thedaviddias/Front-End-Checklist`](https://github.com/thedaviddias/Front-End-Checklist) | 75k | MDX | Чек-лист современного веба (обновлён под AI-агентов) | 🟡 Готовый приёмочный список для лендингов AXIIOM — встроить в ревью |
| [`TonyL1u/nano-ai`](https://github.com/TonyL1u/nano-ai) | 172 | TS | Кросс-платформенный AI-чат-клиент | ⚪ Компактный пример чат-UI и мультипровайдерности |
| [`nexu-io/open-design`](https://github.com/nexu-io/open-design) | 105k | TS | Локальный воркспейс дизайн-агента: прототипы, дашборды, презентации, motion и видео по брифу и своей дизайн-системе, с общим ревью | 🟢 Схема «бриф → дизайн-система → артефакт → правки агента» для AXIIOM и прототипов: скиллы, шаблоны и плагины лежат открыто и переносятся в свои проекты. Смотреть, как ревью встроено в сам проект, а не в чат |
| [`AR13X3/halation`](https://github.com/AR13X3/halation) | 91 | JS | Браузерный редактор анимированных градиентных фонов: текстурное стекло, «жидкие» поверхности, бесшовные видео-лупы; WebGL-шейдеры | 🟡 Фоны для лендингов AXIIOM без видеомонтажа: генератор отдаёт готовый шейдер и луп. Смотреть, как упакован «дизайн-инструмент в браузере» |
| [`patch-gg/pixelfx`](https://github.com/patch-gg/pixelfx) | 9k | JS | 244 пиксель-арт эффекта, каждый — небольшой кусок кода на canvas; в комплекте скилл Claude Code, чтобы собрать свой | 🟡 Прямо в трек E: взрывы, вспышки, дым для `alien-cosmic` и мини-игр из готовых сниппетов, без ассетов |

## 5. macOS, Swift и локальные утилиты (10)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`tw93/Mole`](https://github.com/tw93/Mole) | 72k | Shell | CLI-чистильщик/оптимизатор macOS + TUI-анализатор диска, с нативными приложениями | 🟢 Эталон «безопасной деструктивной утилиты»: `--dry-run`, предпросмотр, отдельный skill для агентов, `llms.txt` |
| [`asafofer/perch`](https://github.com/asafofer/perch) | 21 | Swift | Приложение в «челке» Mac: показывает, что делают coding-агенты, и даёт ответить/вернуться в сессию | 🟢 Ниша «человек + много агентов»: live-статус, Allow/Deny из нотча, точный возврат в нужную вкладку/панель |
| [`jaywcjlove/awesome-swift-macos-apps`](https://github.com/jaywcjlove/awesome-swift-macos-apps) | 1.8k | Swift | Курируемый список open-source macOS-приложений на Swift | 🟢 Карта рынка и доноров кода для Dajet-семейства: Audio, Browser, Editors, AI, Menu bar |
| [`driceroland/Search`](https://github.com/driceroland/Search) | 2.6k | Swift | Маленький быстрый WebKit-браузер для macOS | 🟢 База `dajet-browser` — смотреть, как из минимума собрать нормальный браузер |
| [`ARahim3/DigUp`](https://github.com/ARahim3/DigUp) | 5.3k | Swift | Поиск по содержимому файлов на Mac локально | 🟡 Upstream моего `DigUp`: как устроен on-device поиск и эмбеддинги |
| [`gluonfield/enchanted`](https://github.com/gluonfield/enchanted) | 6k | Swift | iOS/macOS-клиент к приватным self-hosted LLM (Ollama) | 🟡 Нативный клиент к локальным моделям — UI-референс |
| [`PurpleDoubleD/locally-uncensored`](https://github.com/PurpleDoubleD/locally-uncensored) | 2.4k | TS | Локальная AI-студия: чат, картинки, видео, кодовый агент | 🟡 Как собрать «всё в одном» на локальных моделях |
| [`ddalcu/mlx-serve`](https://github.com/ddalcu/mlx-serve) | 2.3k | Zig | Нативный сервер инференса для Apple Silicon: один бинарь + Swift-приложение, API OpenAI/Anthropic/Ollama на одном порту, без Python | 🟢 Рабочая замена Ollama на Mac: `mlx-serve launch claude` наводит Claude Code на локальную модель, приложение даёт меню-бар, чат и менеджер моделей. Референс «локальная модель как сервис внутри продукта» для Dajet-линейки |
| [`justinwetch/HIGAgentSkills`](https://github.com/justinwetch/HIGAgentSkills) | 731 | Python | Скилл-справочник по Apple HIG: 157 выжимок из гайдлайнов iOS/iPadOS/macOS/tvOS/visionOS/watchOS, срез OS 27 и iPhone Duo | 🟡 Приёмка интерфейсов Dajet и питомца по гайдлайнам Apple без чтения сайта: агент сначала цитирует норму, потом правит. Забирать формат `SKILL.md` + `references/` и enforce-режим (два ревьюера, порог 90/100) |
| [`iina/iina`](https://github.com/iina/iina) | 47k | Swift | Современный видеоплеер для macOS поверх mpv: Swift + AppKit, открытый код целиком | 🟡 Референс нативного медиаплеера: интеграция mpv-ядра, меню, настройки, сборка без Xcode-магии — под `dajet` |

## 6. Модели и генерация медиа (15)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`OpenBMB/MiniCPM-V`](https://github.com/OpenBMB/MiniCPM-V) | 27k | Python | On-device мультимодальная серия: MiniCPM-V 4.7 (35B-A3B MoE и 1B), MiniCPM-o 4.5 со зрением и речью | 🟡 Локальное зрение на своём железе: 3 ГБ памяти на телефоне, GGUF/llama.cpp-ветки. Кандидат в «AI внутри приложения» без облака |
| [`QwenLM/Qwen-Image`](https://github.com/QwenLM/Qwen-Image) | 8.4k | Python | Модель генерации изображений с сильным рендером текста | 🟡 Картинки с надписями — под баннеры/обложки |
| [`zai-org/GLM-Image`](https://github.com/zai-org/GLM-Image) | 1.1k | Python | Авторегрессионная генерация изображений | ⚪ Альтернатива диффузии, интересна архитектурно |
| [`XiaomiMiMo/MiMo-V2-Flash`](https://github.com/XiaomiMiMo/MiMo-V2-Flash) | 1.4k | — | Компактная reasoning/agent-модель | ⚪ Дешёвая модель под агентные циклы |
| [`Tencent-Hunyuan/Hy3`](https://github.com/Tencent-Hunyuan/Hy3) | 671 | Python | 295B MoE (21B активных), ставка на стоимость инференса | ⚪ Смотреть на экономику, не на размер |
| [`koda-dernet/Side-Step`](https://github.com/koda-dernet/Side-Step) | 159 | Python | Скрипты обучения/файнтюна для ACE-Step 1.5 (генерация музыки) с CLI и TUI | 🟡 Под музыкальные проекты (`dajet`, `joer`): как делать свои модели, а не только API |
| [`nexu-io/html-video`](https://github.com/nexu-io/html-video) | 4.8k | HTML | HTML/CSS → настоящий MP4 локально: 21 шаблон, подключаемые движки рендера, агент собирает ролик из ссылки, репозитория или промпта | 🟢 Видео для AXIIOM и презентаций без After Effects и оплаты за рендер: кадр — это HTML, финал — ffmpeg. Заодно образец «шаблон + агент + локальный рендер» |
| [`Lightricks/LTX-2`](https://github.com/Lightricks/LTX-2) | 10k | Python | Официальный пакет инференса и LoRA-тренинга для аудио-видео модели LTX-2: генерация видео вместе со звуком | 🟡 Локальное видео со звуком одной моделью — под ролики AXIIOM и презентации. Сначала смотреть требования к VRAM, потом обещать |
| [`lipku/LiveTalking`](https://github.com/lipku/LiveTalking) | 11k | Python | Цифровой человек в реальном времени: потоковый говорящий аватар с липсинком (wav2lip, MuseTalk, ER-NeRF) | 🟡 Референс «лицо + голос» для контента и демо: как стыкуются TTS, липсинк и стриминг. Тяжёлый — только как образец пайплайна |

### Речь и голос (TTS)

Отдельной группой: синтез речи — другой класс задач, чем картинки и музыка. Критерий здесь
простой — работает ли локально на CPU и есть ли русский.

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`hexgrad/kokoro`](https://github.com/hexgrad/kokoro) | 9.7k | Python | Kokoro-82M: TTS на 82 млн параметров, веса под Apache, библиотека ставится через pip | 🟡 Самый лёгкий офлайн-голос из всей шестёрки: идёт на CPU, зависимость — `pip install kokoro` + espeak-ng. Реальный кандидат на озвучку внутри приложения |
| [`resemble-ai/chatterbox`](https://github.com/resemble-ai/chatterbox) | 27k | Python | Семейство TTS от Resemble AI: Multilingual V3 (0.5B), Turbo 350M для голосовых агентов, Nano 110M | 🟡 Nano даёт 3× реального времени на 8 ядрах CPU и понимает теги `[laugh]`/`[cough]` — голос локального агента без GPU |
| [`fishaudio/fish-speech`](https://github.com/fishaudio/fish-speech) | 33k | Python | Открытый TTS с клонированием голоса (линейки S1/S2, Drama), Docker-образ, многоязычность | 🟡 Свой TTS-сервер для медиа-проектов: клон голоса у себя, без биллинга за символы |
| [`2noise/ChatTTS`](https://github.com/2noise/ChatTTS) | 40k | Python | Диалоговый TTS: просодия управляется как параметр — смех, паузы, вставки; пока только английский и китайский | ⚪ Идея «эмоция — это параметр синтеза, а не отдельная модель». Русского нет, поэтому только референс |
| [`myshell-ai/OpenVoice`](https://github.com/myshell-ai/OpenVoice) | 38k | Python | Клонирование тембра голоса + управление стилем (эмоция, темп, акцент), V2 — шесть языков, zero-shot | ⚪ Академический эталон клонирования тембра и переноса стиля. В списке языков русского нет — смотреть архитектуру, не внедрять |
| [`SWivid/F5-TTS`](https://github.com/SWivid/F5-TTS) | 15k | Python | TTS на flow matching: Diffusion Transformer + ConvNeXt V2 и трюк Sway Sampling | ⚪ Архитектурный референс: как flow matching заменяет авторегрессию в синтезе речи и почему Sway Sampling улучшает качество без переобучения |

## 7. Инфраструктура, браузер, self-hosted, безопасность (10)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`ModernRelay/omnigraph`](https://github.com/ModernRelay/omnigraph) | 1.7k | Rust | Графовая БД поверх объектного хранилища: типизированная онтология, ветки как в git, единый поиск (граф + вектор + BM25) | 🟢 Референс под lovii-crm: ветка на агента, three-way merge и политика на каждую запись — подтверждение встроено в данные, а не в интерфейс |
| [`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser) | 44k | Rust | CLI-автоматизация браузера, сделанная для агентов: семантические локаторы, snapshot страницы, проверка состояния | 🟢 Замена самодельных Playwright-скриптов: агент «смотрит» страницу текстом, а не селекторами |
| [`caddyserver/caddy`](https://github.com/caddyserver/caddy) | 78k | Go | Веб-сервер с автоматическим HTTPS | 🟢 Стандарт для self-hosted: один бинарь, сертификаты сами |
| [`oauth2-proxy/oauth2-proxy`](https://github.com/oauth2-proxy/oauth2-proxy) | 15k | Go | Реверс-прокси с аутентификацией (Google, OIDC, Azure) | 🟢 Как закрыть внутренние сервисы логином без написания auth |
| [`clash-verge-rev/clash-verge-rev`](https://github.com/clash-verge-rev/clash-verge-rev) | 153k | Rust | GUI-клиент прокси на Tauri для всех ОС | 🟡 Референс Tauri-приложения «панель + системный трей» |
| [`rucorp/mock-services`](https://github.com/rucorp/mock-services) | 6 | JS | Моки банковского эквайринга и ОФД для тестов платёжных интеграций | 🟢 Прямо в финтех-проекты: тестировать оплату без реальных провайдеров |
| [`bestdeejay-design/raster-to-svg`](https://github.com/bestdeejay-design/raster-to-svg) | 1 | Python | Мой PNG→SVG конвертер | ⚪ Своё |
| [`immich-app/immich`](https://github.com/immich-app/immich) | 120k | TS | Self-hosted фото- и видеоменеджер, альтернатива Google Photos: мобильные приложения (Flutter), сервер на NestJS, веб на SvelteKit | 🟢 Готовая замена облаку для фотоархива + образцовая архитектура «мобильный клиент + свой сервер + фоновая загрузка». Смотреть, как сделан бэкап с телефона без ручных действий |
| [`photoprism/photoprism`](https://github.com/photoprism/photoprism) | 40k | Go | AI-фото-приложение для своего сервера: Go + TensorFlow, поиск по содержимому, лица, геометки | 🟡 Более консервативный вариант, чем `immich`: один бинарь + Docker, сильный офлайн-поиск по смыслу |
| [`LibrePhotos/librephotos`](https://github.com/LibrePhotos/librephotos) | 8.2k | Python | Self-hosted служба управления фото: Django + ML-модели для распознавания | 🟡 Третий вариант для сравнения: питоновский стек, если понадобятся свои ML-модели поверх архива |

## 8. Обучение, подборки и бесплатные API (12)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`NirDiamant/agents-towards-production`](https://github.com/NirDiamant/agents-towards-production) | 22k | Jupyter | Туториалы «от прототипа агента до продакшена» | 🟢 Самый практичный курс по агентам: код-ноутбуки, а не слайды |
| [`NirDiamant/RAG_Techniques`](https://github.com/NirDiamant/RAG_Techniques) | 30k | Jupyter | 30+ техник RAG с кодом | 🟢 Настольная книга по RAG — под `knowledge-base`, `voice-assistant` |
| [`microsoft/ai-agents-for-beginners`](https://github.com/microsoft/ai-agents-for-beginners) | 78k | Jupyter | 18 уроков по агентам от Microsoft | 🟡 Систематическая база + мультиязычность |
| [`patchy631/ai-engineering-hub`](https://github.com/patchy631/ai-engineering-hub) | 38k | Jupyter | Глубокие туториалы по LLM/RAG/агентам | 🟡 Разборы реальных архитектур |
| [`Shubhamsaboo/awesome-llm-apps`](https://github.com/Shubhamsaboo/awesome-llm-apps) | 142k | Python | 100+ готовых LLM-приложений и агентов | 🟢 Кладовая рецептов: брать приложение целиком и адаптировать |
| [`Arindam200/awesome-ai-apps`](https://github.com/Arindam200/awesome-ai-apps) | 16.7k | Python | 138 запускаемых LLM-приложений и агентов: текстовые агенты, голосовые ассистенты, RAG, MCP-инструменты, файнтюн-пайплайны; каждый проект — своя папка с README, зависимостями и `.env.example` | 🟢 Брать папку целиком и запускать: от стартера на 5 минут до многоагентной системы. Ровный источник рецептов для центра агентов — без сборки окружения с нуля |
| [`slavakurilyak/awesome-ai-agents`](https://github.com/slavakurilyak/awesome-ai-agents) | 2.5k | Go | 300+ агентных ресурсов | 🟡 Навигация по экосистеме |
| [`caramaschiHG/awesome-ai-agents-2026`](https://github.com/caramaschiHG/awesome-ai-agents-2026) | 2k | — | 300+ агентов/фреймворков, срез 2026 | 🟡 Быстрый обзор «что вообще есть» |
| [`mnfst/awesome-free-llm-apis`](https://github.com/mnfst/awesome-free-llm-apis) | 11k | JS | Постоянно бесплатные LLM API | 🟢 Для прототипов без бюджета |
| [`ShaikhWarsi/free-ai-tools`](https://github.com/ShaikhWarsi/free-ai-tools) | 1k | TS | Бесплатные/дешёвые AI-инструменты, IDE, инфраструктура | 🟡 Экономия на этапе экспериментов |
| [`vava-nessa/free-coding-models`](https://github.com/vava-nessa/free-coding-models) | 2.8k | HTML | 170+ бесплатных кодовых моделей с бенчмарками и установкой в CLI | 🟢 Практичный список «чем кодить бесплатно» |
| [`signerless/llm-checker`](https://github.com/signerless/llm-checker) | 3k | JS | CLI: сканирует железо и говорит, какие модели потянет | 🟡 Не гадать, а померить перед запуском локальной модели |

## 9. Разработка и утилиты (7)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`t8y2/dbx`](https://github.com/t8y2/dbx) | 27k | Rust | 25 МБ клиент к 100+ базам данных | 🟡 Как сделать «маленький нативный клиент»: Rust + минимализм |
| [`veloxbase/veloxdb`](https://github.com/veloxbase/veloxdb) | 828 | TS | Desktop-клиент к 13 СУБД (PostgreSQL, MySQL, SQLite, DuckDB, Mongo, Redis, ClickHouse, Cassandra и др.) на Rust + Tauri 2, без облака и телеметрии | 🟡 Та же ниша, что `dbx`, но с другой стороны: Tauri 2 вместо чистого Rust, дерево подключений + SQL-редактор + грид. Референс нативного десктопа к данным и заодно рабочий инструмент смотреть базу `lovii-crm` |
| [`pascalorg/editor`](https://github.com/pascalorg/editor) | 25k | TS | Открытый 3D-редактор архитектуры + локальный CLI + MCP | 🟡 Реальный пример «продукт + MCP + CLI» в одном репозитории |
| [`laravel/laravel`](https://github.com/laravel/laravel) | 85k | Blade | PHP-фреймворк | ⚪ Заготовка, держу для PHP-проектов (`basedata`, `lovii-tech`) |
| [`ashleve/lightning-hydra-template`](https://github.com/ashleve/lightning-hydra-template) | 5.4k | Python | Шаблон ML-экспериментов (PyTorch Lightning + Hydra) | 🟡 Если понадобится обучение моделей — структура конфигов сразу правильная |
| [`obsproject/obs-studio`](https://github.com/obsproject/obs-studio) | 78k | C | OBS Studio | ⚪ Справочник по захвату экрана/стримингу |
| [`neurocyte/flow`](https://github.com/neurocyte/flow) | 2.5k | Zig | TUI-редактор кода на Zig: tree-sitter на 70+ языков, LSP, мультикурсор, режимы Vim/Emacs/Helix | ⚪ Сам редактор не нужен, но инженерия полезна: ≤6 мс на кадр, гибридный rope/piece-table, тысячи курсоров. Смотреть, если понадобится свой быстрый TUI на больших файлах |

## 10. Свои и смежные организации (в звёздах у меня) (19)

| Репозиторий | ★ | Стек | Что это |
|---|---|---|---|
| [`bestdeejay-design/lovii`](https://github.com/bestdeejay-design/lovii) | 4 | HTML | LOVII — white-label SaaS локальных маркетплейсов |
| [`bestdeejay-design/lovii-demo`](https://github.com/bestdeejay-design/lovii-demo) | 3 | JS | Демо-версия LOVII |
| [`bestdeejay-design/awesome-ai-handbook`](https://github.com/bestdeejay-design/awesome-ai-handbook) | 48 | HTML | Практическое руководство по AI: от локальной модели до своих агентов |
| [`bestdeejay-design/chronos`](https://github.com/bestdeejay-design/chronos) | 1 | Python | 5 AI-агентов для документации |
| [`bestdeejay-design/opencode-setup`](https://github.com/bestdeejay-design/opencode-setup) | 1 | Shell | Настройка среды opencode (Sisyphus) |
| [`bestdeejay-design/imgforge`](https://github.com/bestdeejay-design/imgforge) | 1 | JS | Обрезка/оптимизация картинок в браузере |
| [`bestdeejay-design/ksu`](https://github.com/bestdeejay-design/ksu) | 1 | HTML | Портфолио дизайнера |
| [`bestdeejay-design/shimmer`](https://github.com/bestdeejay-design/shimmer) | 6 | JS | «Мерцание» — книга/сайт |
| [`bestdeejay-design/sweet-no-sleep`](https://github.com/bestdeejay-design/sweet-no-sleep) | 7 | Swift | MenuBar-питомец, не дающий Mac уснуть |
| [`bestdeejay-design/bestdeejay-design`](https://github.com/bestdeejay-design/bestdeejay-design) | 4 | Python | Профиль GitHub |
| [`axiiom-ru/axiiom-ru`](https://github.com/axiiom-ru/axiiom-ru) | 1 | — | Профиль AXIIOM |
| [`axiiom-ru/lovii`](https://github.com/axiiom-ru/lovii) | 1 | HTML | Документы LOVII для публикации |
| [`rucorp/arental`](https://github.com/rucorp/arental) | 1 | HTML | Лендинг digital-агентства |
| [`rucorp/accounts`](https://github.com/rucorp/accounts) | 1 | — | Карта моих аккаунтов, почт и SSH |
| [`lovii-tech/lovii-core`](https://github.com/lovii-tech/lovii-core) | 1 | PHP | Ядро платформы LOVII |
| [`lovii-tech/lovii-b2b`](https://github.com/lovii-tech/lovii-b2b) | 1 | PHP | B2B-часть LOVII |
| [`lovii-tech/lovii-admin`](https://github.com/lovii-tech/lovii-admin) | 1 | PHP | Админка LOVII |
| [`lovii-tech/lovii-app`](https://github.com/lovii-tech/lovii-app) | 1 | Vue | Клиентское приложение LOVII |
| [`dajetbro/dajetbro`](https://github.com/dajetbro/dajetbro) | 1 | — | Профиль Dajet |

Ещё одна своя звезда — `bestdeejay-design/alien-cosmic` (P1) — живёт только в [TASKS.md](./TASKS.md),
трек E: это рабочая игра, а не карточка каталога. Поэтому 133 строки в каталоге + он = 134 звезды.

## 11. На разбор / непонятное (3)

| Репозиторий | ★ | Стек | Что это |
|---|---|---|---|
| [`kriptong/litca-ru`](https://github.com/kriptong/litca-ru) | 1 | — | Пустое описание, непонятное назначение — разобрать или снять звезду |
| [`1Crazymoney/agency-agents`](https://github.com/1Crazymoney/agency-agents) | 2 | — | Копия `msitarzewski/agency-agents` — держать не нужно |
| [`1Crazymoney/mythos-agent`](https://github.com/1Crazymoney/mythos-agent) | 2 | — | «AI security agent, который охраняет код» — проверить, живой ли |

## 12. Прочее (5)

| Репозиторий | ★ | Стек | Что это |
|---|---|---|---|
| [`net-merge/net-merge`](https://github.com/net-merge/net-merge) | 2.6k | Go | Складывает несколько интернет-каналов в один: Wi-Fi + Ethernet + телефонный хотспот |
| [`BEPb/image_to_prompt`](https://github.com/BEPb/image_to_prompt) | 49 | Python | Картинка → промпт (2023, учебный) |
| [`BEPb/Image_Colorization`](https://github.com/BEPb/Image_Colorization) | 53 | Python | Раскрашивание ч/б изображений (2023, учебный) |
| [`delbeke/vectorizer`](https://github.com/delbeke/vectorizer) | 4 | JS | Растр → SVG, простой пример |
| [`Talilard1/KoLib`](https://github.com/Talilard1/KoLib) | 6 | Kotlin | Библиотека электронных книг и менеджер Kobo для Android: каталог книг и комиксов, отправка на ридер, чтение и правка; GPL-3.0, 12 языков, без аккаунта |

---

## 13. Игры (1)

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`ihhub/fheroes2`](https://github.com/ihhub/fheroes2) | 3.5k | C++ | Переписанный с нуля движок Heroes of Might and Magic II: своя карта, бои, ИИ, сохранения, высокое разрешение | ⚪ Референс для трека E: детерминированный пошаговый цикл, ИИ на карте, формат сохранений. GPL-2.0 — смотреть, код не втаскивать |

---

## 14. Заметки, Obsidian и личная база знаний (9)

Появилось разом девять штук — это один осознанный заход: строить базу знаний на открытых
форматах (Markdown, JSON Canvas, Bases), а не на вендорном облаке. Полезны не «заметки в Obsidian»,
а три вещи: чистый Markdown из любой ссылки, формат канваса и структура хранилища, которая не
разваливается. Плюс `immich`/`photoprism` из раздела 7 — та же логика для фото.

| Репозиторий | ★ | Стек | Что это | Чем полезен |
|---|---|---|---|---|
| [`obsidianmd/obsidian-clipper`](https://github.com/obsidianmd/obsidian-clipper) | 5.6k | TS | Официальное расширение Web Clipper: выделить и сохранить страницу в заметку из браузера (Chrome, Firefox, Safari, Edge, Brave) | 🟡 Главный вход материала в базу: смотреть, как устроен путь «клип → чистый Markdown» и шаблоны под сайты |
| [`kepano/clipper-templates`](https://github.com/kepano/clipper-templates) | 1.6k | — | Готовые шаблоны Web Clipper под конкретные сайты (YouTube, GitHub, статьи) | 🟡 Забирать шаблоны и правила извлечения полей вместо своих селекторов |
| [`kepano/defuddle`](https://github.com/kepano/defuddle) | 10k | TS | Достаёт основное содержимое любой страницы в Markdown: CLI и библиотека, readability-подход | 🟢 Чистый текст из ссылки для RAG и заметок без браузера — под `knowledge-base` и сбор материала: снимает половину работы самописных парсеров |
| [`obsidianmd/jsoncanvas`](https://github.com/obsidianmd/jsoncanvas) | 3.9k | JS | Открытый формат данных для бесконечных канвасов: JSON + спецификация | 🟡 Формат схем и досок, который переживёт смену инструмента — кандидат в `personal-os` вместо вендорного |
| [`obsidianmd/obsidian-importer`](https://github.com/obsidianmd/obsidian-importer) | 1.8k | TS | Импорт в Markdown из Apple Notes, OneNote, Evernote, Notion, Google Keep, Airtable, CSV и других | 🟡 Готовый ответ на «как свезти старый архив заметок в одну базу» |
| [`obsidianmd/obsidian-help`](https://github.com/obsidianmd/obsidian-help) | 2k | JS | Исходники справки Obsidian — документация продукта в открытом виде | ⚪ Источник точных формулировок про Bases, свойства и синтаксис, когда пишем скиллы и скрипты |
| [`obsidianmd/obsidian-developer-docs`](https://github.com/obsidianmd/obsidian-developer-docs) | 577 | JS | Документация для разработчиков плагинов и тем Obsidian | ⚪ Если понадобится свой плагин или автоматизация хранилища |
| [`kepano/obsidian-minimal`](https://github.com/kepano/obsidian-minimal) | 5.7k | CSS | Тема Minimal: вид без отвлечений, гибкая настройка, тёмный и светлый режимы | ⚪ Референс дизайн-системы для заметок: как из CSS-переменных собрать тему с двумя режимами |
| [`kepano/kepano-obsidian`](https://github.com/kepano/kepano-obsidian) | 6.3k | — | Личное хранилище Obsidian от Kepano (CEO Obsidian) как шаблон: подход «снизу вверх» — заметки собираются из интересов, а не из папок | 🟡 Живой пример структуры базы, которая не разваливается: смотреть на теги, MOC-заметки и связи, не на оформление |

---

## Что видно по слепку целиком

1. **Звёзды — это три разных интереса, а не один:** (а) как строить агентов и обвязку, (б) macOS/Swift-продукты, (в) подборки «где взять бесплатно». Держать их в одном списке без категорий — главная причина, почему такой список быстро забывается.
2. **Много дублей-подборок** (awesome-ai-agents ×2, claude-skills ×2, awesome-local-ai/llm у себя) — 30–40% звёзд дают 5% пользы. Реальная ценность в 10–12 репозиториях.
3. **Сильный перекос в «агент-first» архитектуру** — crm, itsaplan, perch, Mole, openui, agent-browser сходятся в одном: агент — это отдельный процесс с инструментами, очередью и правами, а не чат-бокс в UI.
4. **Новый стандарт репозитория:** `AGENTS.md` + `.agents/` + `.claude-plugin/` + `evals/` + `llms.txt`. Так сделано у crm, Mole, itsaplan, perch, agent-browser. Мой зоопарк это почти нигде не использует.
5. **Пустых/мёртвых звёзд немного** — 3 штуки (раздел 11), их можно снять.
