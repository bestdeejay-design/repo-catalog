# Заметки к `PROJECTS.md` — служебное, в публикацию не идёт

Рабочие пометки к подборке проектов. Сам список — в [`PROJECTS.md`](./PROJECTS.md), он же вставляется разделом `## Projects` в README профиля `bestdeejay-design`.

## Что собрано

Срез GitHub API на 27.10.2026: **137** репозиториев в трёх аккаунтах — `bestdeejay-design` (личный), `rucorp`, `lovii-tech`.

- в подборку вошло **75**: 58 публичных со ссылкой, 17 приватных — только название и описание;
- у 17 приватных репозиториев на GitHub пустое описание — тексты взяты из их README (`lovii-core`, `lovii-b2b`, `lovii-admin`, `lovii-app`, `lovii_docs`, `fonotext-server`, `briix-internal`, `infra`, `security`, `mail`, `domains_finder`, `docs`, `agent-hub`, `dajet-ui`, `dajet-editor`, `lovii-crm`, `SS-BMW-site`);
- правило проверки: приватный репозиторий никогда не получает ссылку; стало публичным — ссылка появляется автоматически (это и должен делать скрипт).

## Что не вошло (62 репозитория)

| Категория | Репозитории |
|---|---|
| Форки | `atom`, `DigUp`, `flowsint`, `awesome-local-llm`, `awesome-local-ai` |
| Архивы | `arental_3`, `static-site`, `napolipizza`, `arental-rental` |
| Пустые | `mag`, `extension1`, `lovii-app-pages-shots`, `lovii-pay` |
| Служебные | `accounts`, `companies`, `.github`, `demo-repository` |
| Песочницы и клоны под аудит | `test`, `lovii-app-arena`, `archive-gallery-arena`, `alien-cosmic-dist`, `ace`, `razbor-project-alpha` |
| Дампы чатов | `chats`, `chats-audit`, `chats-job`, `qwen-chats`, `deepseek-chats` |
| Слабые однотипные демо | `app`, `primary`, `blog`, `kodstudy`, `hype`, `pizza`, `univerid_demo`, `arbat38`, `spbgti-docs` |

`razbor-project-alpha` — внутренний проект заказчика, в README прямо сказано «не публиковать никогда»; в подборку не идёт и впредь.

## Версии README

В репозитории профиля `bestdeejay-design/bestdeejay-design` два файла:

| Файл | Что это |
|---|---|
| `README.md` | Основная, английская. Раздел `## Projects` — дословно отсюда, из `PROJECTS.md`. |
| `README.ru.md` | Русская версия, лайт: без бейджей, SVG-шапки и карточек активности; те же достижения и кейсы, плюс полный список проектов по-русски. |

Переключатель языка есть в обоих файлах. Английский — основной, русский — вторичный (не наоборот: профиль читают и снаружи).

## Структура подборки

- разделы с **больше чем двумя** репозиториями — таблица под спойлером, над ним описание состава;
- разделы с одним-двумя (`Fonotext`, `Fintech`) — раскрыты;
- LOVII — ведущий блок: публичная часть (3) и внутренние проекты (8) двумя подблоками внутри спойлера;
- проекты второго плана (`BRIIX`, `personal-os`, `pmos`, `opencode-setup`, `aotochka.ru`, `autopulse-sto`, `agents`) — внизу, в разделе «More projects».

## Следующий шаг — автоматизация

1. `projects.json` — манифест кураторства: состав, раздел, короткое описание, стек, примечания. Без него автопрогон затрёт ручную работу.
2. `generate_projects.py` — манифест + данные GitHub API (видимость, звёзды, архивность, язык) → пересборка `PROJECTS.md`.
3. Триггеры: `schedule` раз в сутки + `workflow_dispatch`; коммит только при diff. Мгновенная реакция на новый репозиторий потребует org-webhook — отдельная задача.
