# Projects

> Заготовка раздела «Projects» для README профиля `bestdeejay-design` — тексты английские, как пойдут в публикацию.
> Собрано 27.10.2026 из **137** репозиториев трёх аккаунтов (`bestdeejay-design`, `rucorp`, `lovii-tech`): **58** публичных со ссылкой, **17** приватных — только название и описание.
> Обновление пока ручное; автоматизация — следующим шагом (скрипт-сборщик + триггер на новые репозитории).

58 public repositories with open source and 17 private ones shown by name — a selection from 137 repos across three accounts. Forks, archived projects, empty drafts and one-off sandboxes are left out. 🔒 marks repositories whose source stays closed.

---

### 🛍 LOVII — platform for neighbourhood marketplaces

White-label SaaS for launching local marketplaces: a district, a food court, a shopping mall or a city area gets its own audience, catalog and courier network — all running on one shared core. Merchants list goods and services, customers see **what is actually in stock nearby and how many minutes it is on foot**, delivery lands in 15–30 minutes. Status: MVP, mini-pilot completed in Saint Petersburg.

Nine repositories cover the whole product: storefront, commerce core, partner cabinet, admin panel, mobile app, design system, documentation corpus, restaurant CRM/ERP and the public white paper.

| Repository | What it is | Stack |
|:--|:--|:--|
| [**lovii**](https://github.com/bestdeejay-design/lovii) · [live](https://lovii.ru/) | White paper and the public face of the platform: how a district marketplace works, why the economy is isolated per district, merchant onboarding, MVP status. | HTML · GitHub Pages |
| [**lovii-demo**](https://github.com/bestdeejay-design/lovii-demo) · [live](https://lovii.mobiap.com/) | Working storefront demo on static hosting: 14 shops and 39 products, stock availability, walking distance in minutes, roles of shop, ambassador and investor, light and dark themes. | JavaScript · GitHub Pages |
| [**lovii-invest**](https://github.com/bestdeejay-design/lovii-invest) | Investor site: loyalty programme, payments, marketplace of local offers, unit economics; funding model — equity, not digital assets. | HTML · CSS |

<details>
<summary><b>Внутренние проекты платформы (8)</b></summary>

<br>

| Repository | What it is | Stack |
|:--|:--|:--|
| 🔒 **lovii-core** | Commerce core and the single source of truth across the monorepo: multi-merchant catalog, cart and checkout, orders, loyalty. The only service allowed to write into commerce tables — partner and admin panels go through whitelisted actions. | PHP 8.5 · Laravel 13 · PostgreSQL · Redis · Meilisearch |
| 🔒 **lovii-b2b** | Partner cabinet: merchants, branches, catalog and orders in one panel. Phone + OTP authentication against the core API, multi-tenant, no login/password path at all. | PHP · Filament v5 · PostGIS |
| 🔒 **lovii-admin** | Super-admin panel: roles for support, operations and moderation, plus a full audit trail. Reads core tables read-only and writes only through whitelisted actions. | PHP · Filament v5 · RBAC |
| 🔒 **lovii-app** | Customer mobile web app: shop pages, catalog, cart, checkout and order tracking. | Vue 3 · TypeScript · Vite |
| [**lovii-design**](https://github.com/bestdeejay-design/lovii-design) | Design system «Лови»: tokens, components, theming, Do/Don't rules and acceptance checklists — written for people and AI agents alike, shipped as one CSS file. | HTML · CSS · Design tokens |
| 🔒 **lovii_docs** | Documentation corpus of the platform: 14 modules described as-is against the code, the canon (BRD, PRD, architecture, data model, API spec), analysis of the 85-table database and a gallery of all 60 app screens. | Markdown · HTML |
| [**lovii-crm**](https://github.com/lovii-tech/lovii-crm) · [live](https://lovii-tech.github.io/lovii-crm/) | Restaurant CRM/ERP: from order and receipt to kitchen, product write-offs and couriers. Market research, specifications for 11 domains, franchise book and the legal minimum for launch. | MkDocs Material · GitHub Pages |
| [**platforma**](https://github.com/rucorp/platforma) | Corporate site of the operating company behind the local-economy infrastructure: products, solutions, contacts. | HTML · CSS · JS |

</details>

---

### 🎧 Fonotext — speech analytics for phone calls

Turns call recordings into structured data: 100% coverage instead of the usual 3% QC sample, transcripts with speakers and timecodes, per-call classification, script compliance with evidence, dashboards.

| Repository | What it is | Stack |
|:--|:--|:--|
| [**fonotext**](https://github.com/bestdeejay-design/fonotext) · [live](https://bestdeejay-design.github.io/fonotext/) | Product repository: architecture, ASR/LLM model selection, capacity planning, API spec, POC stand. | Python |
| 🔒 **fonotext-server** | Deployment contour of the stand: server layout, hardware rules, release boundaries between public and private docs. | Python · Markdown |

---

### 💳 Fintech & payment integrations

| Repository | What it is | Stack |
|:--|:--|:--|
| [**mock-services**](https://github.com/rucorp/mock-services) | Mock bank acquiring and fiscal (OFD) services to test payment integrations against official provider protocols — no live terminal needed. | JavaScript · Node.js |

---

### 🖥 macOS apps — the Dajet family

Native Swift apps built around one idea: software that stays quiet.

| Repository | What it is | Stack |
|:--|:--|:--|
| [**dajet-player**](https://github.com/bestdeejay-design/dajet-player) | Quiet native music player: SwiftUI + AVFoundation, local library, no cloud, MIT. | Swift · SwiftUI |
| [**dajet-browser**](https://github.com/bestdeejay-design/dajet-browser) | Minimal macOS browser — search fork, MIT; chrome reduced to what you actually use. | Swift · AppKit |
| 🔒 **dajet-editor** | Native text editor for Apple Silicon: Swift 6, AppKit, TextKit 2. | Swift · AppKit |
| 🔒 **dajet-ui** | Shared native UI kit for the whole app family: one visual language, system materials. | Swift · SwiftUI |
| [**sweet-no-sleep**](https://github.com/bestdeejay-design/sweet-no-sleep) | Menu-bar desktop pet Kiwi that keeps your Mac awake — 6★. | Swift · AppKit |

---

### 🎮 Games, music & interactive

| Repository | What it is | Stack |
|:--|:--|:--|
| [**alien-cosmic**](https://github.com/bestdeejay-design/alien-cosmic) · [live](https://bestdeejay-design.github.io/alien-cosmic/) | Real-time strategy in the browser: 15-mission campaign, 3 factions, base building, fog of war, AI opponent. Pure JavaScript, no build step, no dependencies — 6★. | JavaScript · Canvas |
| [**terran-rts**](https://github.com/bestdeejay-design/terran-rts) | StarCraft-style RTS for GitHub Pages: Canvas rendering and Web Audio, zero dependencies. | JavaScript · Canvas |
| [**minigames**](https://github.com/bestdeejay-design/minigames) | Collection of small browser games — one file each, playable immediately. | JavaScript |
| [**shimmer**](https://github.com/bestdeejay-design/shimmer) · [live](https://bestdeejay-design.github.io/shimmer/) | Shimmer — a philosophical sci-fi saga about consciousness and cycles of time. Two books, read online — 6★. | JavaScript · HTML |
| [**dajet**](https://github.com/bestdeejay-design/dajet) | Creative memory gallery: a music gallery for AI-generated tracks with a full listening experience. | JavaScript |
| [**dj1**](https://github.com/bestdeejay-design/dj1) · [live](https://dj1.ru) | DJ1.RU — music player and gallery, AI tracks by Riffusion, vinyl-style interface. | JavaScript |
| [**joer**](https://github.com/bestdeejay-design/joer) · [live](https://joer.ru) | JOER — internet radio with an adaptive visual atmosphere. | JavaScript · CSS |
| [**qbik**](https://github.com/bestdeejay-design/qbik) | Glossy magazine generator: editor, templates, PDF export. | JavaScript |

---

### 🤖 AI & developer tooling

| Repository | What it is | Stack |
|:--|:--|:--|
| [**awesome-ai-handbook**](https://github.com/bestdeejay-design/awesome-ai-handbook) | Practical guide to AI: from running your first local model to building your own agents — 52 files on LLMs, Ollama, RAG, prompt engineering and local tooling. **48★** | HTML · Markdown |
| [**agent-skills**](https://github.com/bestdeejay-design/agent-skills) · [live](https://bestdeejay-design.github.io/agent-skills/) | 59 skills for AI coding agents: frontend perfection (Lighthouse audit), secret scanner, security review, coverage analyzer, API contract testing, SEO toolkit, repo hygiene. **5★** | Python · JSON manifests |
| [**chronos**](https://github.com/bestdeejay-design/chronos) | Documentation timekeeper — 5 AI agents (Chronos, Censor, Dewey, Veles, Canon) that catch duplicates, broken links, orphans and stale pages. Stdlib-only CLI. | Python |
| 🔒 **agent-hub** | GitHub as the single bus for agents: issue = task, comment = report, PR = result, Actions = execution and audit. | Shell · Actions |
| [**aichat**](https://github.com/bestdeejay-design/aichat) | Local multi-provider chat client for AI models — works fully offline in the browser. | JavaScript |
| [**knowledge-base**](https://github.com/bestdeejay-design/knowledge-base) | RAG service for a corporate knowledge base on free-tier and local models, no paid keys. | TypeScript |
| [**voice-assistant**](https://github.com/bestdeejay-design/voice-assistant) | Voice RAG assistant: Whisper for speech, local knowledge base for answers, macOS speech for replies. | TypeScript · Python |
| [**repo-catalog**](https://github.com/bestdeejay-design/repo-catalog) | Catalog of my own repositories and curated external ones, regenerated by script — the map this list was built from. | Python |
| [**imgforge**](https://github.com/bestdeejay-design/imgforge) | Crop and optimise images right in the browser: ratios, exact sizes, quality, target weight. | JavaScript |
| [**raster-to-svg**](https://github.com/bestdeejay-design/raster-to-svg) | PNG → SVG tracer: pure-Python engine plus vtracer, local web UI with magnifier and presets. | Python |
| [**svg-readme-header-footer**](https://github.com/bestdeejay-design/svg-readme-header-footer) | Single-file editor for animated SVG banners for GitHub READMEs, with live preview. | HTML · JavaScript |
| [**resume**](https://github.com/bestdeejay-design/resume) · [live](https://bestdeejay-design.github.io/resume/) | My resume in CTO / CDTO / CPO versions: master file, build rules, published site. | HTML · Python |

---

### 🏗 Websites & client work

| Repository | What it is | Stack |
|:--|:--|:--|
| [**axiiom**](https://github.com/rucorp/axiiom) · [live](https://axiiom.ru/) | AXIIOM corporate site — web and mobile development, UI/UX, fintech solutions. | HTML |
| [**arental**](https://github.com/rucorp/arental) · [live](http://arental.ru/) | ATMOSFERA — full-cycle digital agency: lead generation, integrations, marketing automation. | HTML |
| [**fermaruna**](https://github.com/bestdeejay-design/fermaruna) · [live](https://fermaruna.ru) | Farm Runskaya — organic farm in the upper Volga: potatoes, vegetables, farm shop. | HTML |
| [**ksu**](https://github.com/bestdeejay-design/ksu) | Portfolio of a graphic designer: identity, branding, typography, UI/UX, illustration, packaging. 16 projects, PWA, EN/RU. | HTML · CSS · PWA |
| [**paffo**](https://github.com/rucorp/paffo) | Custom coat atelier — Italian wool, cashmere, leather; two fittings, 21-day production. | HTML |
| [**neo-consulting**](https://github.com/bestdeejay-design/neo-consulting) · [live](https://bestdeejay-design.github.io/neo-consulting/) | Accounting outsourcing landing: 16 sections, SEO, Saint Petersburg. | HTML · GitHub Pages |
| [**semyazdrav.ru**](https://github.com/bestdeejay-design/semyazdrav.ru) | Plant care landing plus an SEO knowledge base on feeding indoor plants. | HTML |
| [**SS-BMW-site**](https://github.com/bestdeejay-design/SS-BMW-site) | One-page site for a specialised BMW service: gallery, services, lead form. | HTML · CSS · JS |
| [**spbgti**](https://github.com/bestdeejay-design/spbgti) | SPbGTI university site on Eleventy: history, departments, admissions. | HTML · Eleventy |
| 🔒 **archive-spbgti** | Historical archive of SPbGTI: Directus CMS plus gallery — archive.ti200.ru. | HTML · Directus |
| [**univerid**](https://github.com/bestdeejay-design/univerid) | UniverID — digital ecosystem for universities: gradebook, schedule, dean's office chat. 2★ | HTML |

---

### ⚙️ Infrastructure, security & engineering practice

| Repository | What it is | Stack |
|:--|:--|:--|
| 🔒 **infra** | Ansible bootstrap for servers: Ubuntu 24.04, Headscale/Tailscale networking, Loki/Promtail logs, Nginx + PHP-FPM, PostgreSQL, Laravel deploys. | Ansible · Jinja |
| 🔒 **security** | Security contour of the platform: rules, access matrix, audit results — facts about who can reach what, never secrets. | Shell · Markdown |
| 🔒 **mail** | Inbound mail on own domains: provider comparison, working Postfix + postsrsd setup, DNS zones, runbook, external reviews. | Shell · Postfix |
| 🔒 **domains_finder** | Domain Finder v2: automated search and monitoring of short 2–3 character domains, role-split workers, confidence scoring. | PHP · Docker · Supervisor |
| 🔒 **docs** | Software requirements specification for a grocery-delivery aggregator: 4,240+ lines, 2 volumes, 14 business processes, 7 ADRs. | Markdown |
| [**catalog**](https://github.com/bestdeejay-design/catalog) | Venue categories dataset — hierarchy, icons, ordering — plus validation and analysis scripts. | JavaScript · JSON |

---

### 🧪 Prototypes & demos

<details>
<summary><b>Interface prototypes built to prove a flow end-to-end (11)</b></summary>

<br>

| Repository | What it is | Stack |
|:--|:--|:--|
| [**booking**](https://github.com/bestdeejay-design/booking) | Grand Hotel — room booking demo: catalog, online reservation, cart, payment flow. | JavaScript |
| [**foodie**](https://github.com/bestdeejay-design/foodie) | Restaurant search and booking: 12 cuisines, 8 venues with menus, favourites, chat. | JavaScript |
| [**padl**](https://github.com/bestdeejay-design/padl) | PadelPro — padel club management: court booking, clients, schedule, analytics. | JavaScript |
| [**cashier**](https://github.com/bestdeejay-design/cashier) | Mobile cashier — POS terminal and analytics for cafés and restaurants. | JavaScript |
| [**hrmodule**](https://github.com/bestdeejay-design/hrmodule) | HR Motivation — points, levels, badges and leaderboards for corporate motivation. | JavaScript |
| [**logistics**](https://github.com/bestdeejay-design/logistics) | Logistics — picker and courier apps for assembly and delivery. | JavaScript |
| [**mvno**](https://github.com/bestdeejay-design/mvno) | eSIM Travel — MVNO companion for travellers: eSIM, tours, hotels, flights. | JavaScript |
| [**ambar**](https://github.com/bestdeejay-design/ambar) | AMBAR — investment landing for a food hub with kitchens and IT infrastructure. | HTML |
| [**ishotgirls**](https://github.com/bestdeejay-design/ishotgirls) | ISHOT — training journal: streaks, personal records, gear. | HTML |
| [**mobiap**](https://github.com/bestdeejay-design/mobiap) | MOBIAP — English-language landing for fintech platforms: loyalty, payments, PCI DSS. | HTML |
| 🔒 **pizzaloviiru** | Pizzeria landing with a JSON-driven menu and image pipeline. | JavaScript |

</details>

---

### 📦 Остальное

<details>
<summary><b>Проекты второго плана (8)</b></summary>

<br>

**BRIIX — AI marketer.** Reads a company's site, builds a Brand DNA profile, generates a content plan and on-brand posts, publishes on schedule and reports analytics — zero effort on input.

| Repository | What it is | Stack |
|:--|:--|:--|
| [**briix**](https://github.com/rucorp/briix) | Public product site: landing, 20-slide presentation, investor section, unit-economics calculator. | HTML · GitHub Pages |
| 🔒 **briix-internal** | Private workspace: canonical business document, full technical specification, financial model, architecture, risks. | Markdown |

**Прочие проекты.**

| Repository | What it is | Stack |
|:--|:--|:--|
| [**personal-os**](https://github.com/bestdeejay-design/personal-os) | Personal operations centre: notes, kanban, calendar, files, profiles, RAG agent — all local. | TypeScript |
| [**pmos**](https://github.com/bestdeejay-design/pmos) | Event-driven microservice monorepo: 16 CRUD services, NATS JetStream, schema-per-service, 5 sagas, strict TypeScript. | TypeScript · NATS · PostgreSQL |
| [**opencode-setup**](https://github.com/bestdeejay-design/opencode-setup) | Working environment for AI coding agents: configs, MCP servers, skills and a maintenance service. | Shell |
| [**aotochka.ru**](https://github.com/rucorp/aotochka.ru) · [live](https://aotochka.ru/) | Corporate site of JSC Tochka. | JavaScript |
| [**autopulse-sto**](https://github.com/bestdeejay-design/autopulse-sto) | Premium full-cycle car service site on Next.js, dark theme. | TypeScript · Next.js |
| [**agents**](https://github.com/bestdeejay-design/agents) | AXIIOM technology group: digital transformation, fintech, payment integrations, cybersecurity. | HTML |

</details>

---

### Что не вошло

Отсеяно 62 репозитория: форки (`atom`, `DigUp`, `flowsint`, `awesome-local-llm`, `awesome-local-ai`), архивы (`arental_3`, `static-site`, `napolipizza`, `arental-rental`), пустые (`mag`, `extension1`, `lovii-app-pages-shots`, `lovii-pay`), служебные (`accounts`, `companies`, `.github`, `demo-repository`), разовые песочницы и клоны под аудит (`test`, `lovii-app-arena`, `archive-gallery-arena`, `alien-cosmic-dist`, `ace`, `razbor-project-alpha`), дампы чатов (`chats`, `chats-audit`, `chats-job`, `qwen-chats`, `deepseek-chats`) и слабые однотипные демо.

Если что-то из этого нужно вернуть в список — скажите, добавлю.
