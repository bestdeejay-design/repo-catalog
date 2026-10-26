#!/usr/bin/env python3
"""Генератор каталога репозиториев по всем организациям проекта.

Тянет данные с GitHub CLI (gh repo list) по списку OWNERS и собирает README.md
с группировкой по категориям, пометкой архивных репозиториев и привязкой
локальных папок из ~/Projects.

Использование: python3 generate_catalog.py
Требования: gh CLI, авторизация (scopes: repo).
"""

import json
import os
import subprocess
from collections import OrderedDict

OWNERS = ["bestdeejay-design", "rucorp", "axiiom-ru", "lovii-tech"]
PRIMARY = "bestdeejay-design"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Имя репо -> категория. Репо без категории попадут в «Прочее».
CATEGORIES = OrderedDict([
    ("Продукты и платформы", [
        "pmos", "personal-os", "lovii", "lovii_docs", "lovii_demo",
        "lovii_presentation", "knowledge-base", "voice-assistant",
        "lovii-crm", "lovii-site", "lovii-app", "lovii-core", "lovii-b2b",
        "lovii-admin", "fonotext", "fonotext-server", "briix", "briix-internal",
    ]),
    ("Лендинги и веб-сайты", [
        "axiiom", "axiiom_landing", "mobiap", "paffo", "ishotgirls",
        "neo-consulting", "arental", "arental_2", "arental-rental",
        "aotochka.ru", "pizza", "napolipizza", "pizzaloviiru",
        "univerid", "univerid_demo", "blog", "platforma", "wordpress",
        "static-site", "joer", "kodstudy", "spbgti", "archive-spbgti",
        "ambar", "agents", "hype", "booking", "minigames", "aichat",
        "semyazdrav.ru", "fermaruna", "SS-BMW-site", "alien-cosmic",
        "neverwinter", "atom", "dj1",
    ]),
    ("Демо-приложения и прототипы", [
        "primary", "cashier", "app", "arbat38", "foodie", "qbik",
        "alfred", "logistics", "mvno", "hrmodule", "padl", "dajet",
    ]),
    ("Данные и аналитика", [
        "catalog", "ybase-tsp", "basedata",
    ]),
    ("Инструменты и утилиты", [
        "agent-skills", "raster-to-svg", "imgforge",
        "svg-readme-header-footer", "design-demo", "designer-references",
        "oc-architecture", "opencode-setup", "axiiom-brand-skill",
        "repo-catalog", "presentation-maker",
    ]),
    ("Книги и контент", [
        "shimmer", "awesome-ai-handbook", "awesome-local-llm",
        "awesome-local-ai",
    ]),
    ("Документация", [
        "docs", "docsv", "srs-docs", "accounts", "companies",
        "company-cards", "hub", "rucorp",
    ]),
    ("Черновики (WIP)", [
        "mag", "extension1", "test", "transcribations", "razbor-project-alpha",
    ]),
])

# Архивные локальные папки: не ищем в них свежие правки
ARCHIVE_FOLDERS = {"axiiom", "axiiom_new", "arсhive.bak", "archive", "test", "catalog"}

# Локальная папка -> репозиторий (для привязки рабочих копий)
LOCAL_MAP = {
    "Technolozka": "spbgti",
    "agent-skills": "agent-skills",
    "alien-cosmic": "alien-cosmic",
    "app": "app",
    "arenteral_2": "arental_2",
    "atom": "atom",
    "axiiom-brand-skill": "axiiom-brand-skill",
    "axiiom_github": "axiiom",
    "briix": "briix",
    "briix-internal": "briix-internal",
    "buhtest": "neo-consulting",
    "companies": "companies",
    "company-cards": "company-cards",
    "design-rnd": "design-demo",
    "dj1": "dj1",
    "docs": "docs",
    "fermaruna": "fermaruna",
    "fonotext": "fonotext",
    "fonotext-server": "fonotext-server",
    "foodie": "foodie",
    "imgforge": "imgforge",
    "ishotgirls": "ishotgirls",
    "joer.ru": "joer",
    "ksu": "ksu",
    "lovii": "lovii",
    "lovii-crm": "lovii-crm",
    "lovii-site": "lovii-site",
    "lovii_demo": "lovii_demo",
    "lovii_docs": "lovii_docs",
    "lovii_presentation": "lovii_presentation",
    "mobiap-repo": "mobiap",
    "mobiap-v2": "axiiom",
    "mobiap": "mobiap",
    "neverwinter": "neverwinter",
    "oc-architecture": "oc-architecture",
    "opencode-setup": "opencode-setup",
    "paffo": "paffo",
    "pizza": "pizza",
    "raster-to-svg": "raster-to-svg",
    "references": "designer-references",
    "repo-catalog": "repo-catalog",
    "semyazdrav.ru": "semyazdrav.ru",
    "shimmer": "shimmer",
    "srs-docs": "srs-docs",
    "svg-readme-header-footer": "svg-readme-header-footer",
    "transcribations": "razbor-project-alpha",
    "accounts": "accounts",
    "RuCorp": "rucorp",
    "rucorp-profile": "hub",
    "SS-BMW-site": "SS-BMW-site",
    "test": "test",
}

LOCAL_BY_REPO = {}
for folder, repo in LOCAL_MAP.items():
    LOCAL_BY_REPO.setdefault(repo, []).append(folder)


def fetch_repos():
    """Возвращает {(owner, name): {...}} по всем организациям."""
    fields = ["name", "description", "visibility", "primaryLanguage",
              "updatedAt", "homepageUrl", "repositoryTopics", "isArchived"]
    repos = {}
    for owner in OWNERS:
        proc = subprocess.run(
            ["gh", "repo", "list", owner, "--limit", "300", "--json", ",".join(fields)],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            print(f"WARN: {owner}: {proc.stderr.strip()[:120]}")
            continue
        for r in json.loads(proc.stdout):
            repos[(owner, r["name"])] = {
                "description": (r.get("description") or "").strip(),
                "visibility": r.get("visibility", ""),
                "language": (r.get("primaryLanguage") or {}).get("name", "") if r.get("primaryLanguage") else "",
                "updated": (r.get("updatedAt") or "")[:10],
                "homepage": r.get("homepageUrl") or "",
                "topics": [t["name"] for t in (r.get("repositoryTopics") or [])],
                "archived": bool(r.get("isArchived")),
            }
    return repos


def fmt_row(key, meta):
    owner, name = key
    desc = meta["description"] or "—"
    if len(desc) > 100:
        desc = desc[:97].rstrip() + "…"
    lang = meta["language"] or "—"
    vis = "🔓" if meta["visibility"] == "PUBLIC" else "🔒"
    local = ", ".join(LOCAL_BY_REPO.get(name, [])) or "—"
    updated = meta["updated"]
    if meta["archived"]:
        vis += " 📦"
    home = f" [🌐]({meta['homepage']})" if meta["homepage"] else ""
    label = name if owner == PRIMARY else f"{owner}/{name}"
    return f"| [`{label}`](https://github.com/{owner}/{name}){home} | {desc} | {lang} | {vis} | {local} | {updated} |"


def local_folders_without_remote():
    """Папки в ~/Projects, которые не привязаны к репозиторию."""
    out = []
    try:
        entries = sorted(os.listdir(ROOT))
    except OSError:
        return out
    for entry in entries:
        path = os.path.join(ROOT, entry)
        if not os.path.isdir(path) or entry.startswith("."):
            continue
        if entry in LOCAL_MAP:
            continue
        git = os.path.join(path, ".git")
        if not os.path.exists(git):
            out.append(entry)
    return out


def build_md(repos):
    lines = []
    lines.append("# Каталог репозиториев")
    lines.append("")
    lines.append(f"Всего репозиториев: **{len(repos)}** "
                 f"в организациях {', '.join('`' + o + '`' for o in OWNERS)}. "
                 "Сгенерировано скриптом `generate_catalog.py` — запускай `python3 generate_catalog.py`, чтобы обновить.")
    lines.append("")
    lines.append("Легенда: 🔓 публичный · 🔒 приватный · 📦 архив (read-only) · 🌐 ссылка на сайт · локальная папка в `~/Projects`")
    lines.append("")
    lines.append("См. также: **[STARS.md](./STARS.md)** — каталог внешних репозиториев из моих ⭐ · "
                 "**[STARS-REVIEW.md](./STARS-REVIEW.md)** — разбор ключевых · "
                 "**[TASKS.md](./TASKS.md)** — звёзды под три текущие задачи · "
                 "**[IDEAS.md](./IDEAS.md)** — идеи и полезные исходники · **[OPTIONS.md](./OPTIONS.md)** — идеи с топ-3 вариантами · "
                 "**[STARS-ARCHIVE.md](./STARS-ARCHIVE.md)** — снятые звёзды (история).")
    lines.append("")

    def entries_for(name):
        found = [(k, v) for k, v in repos.items() if k[1] == name]
        found.sort(key=lambda kv: (kv[0][0] != PRIMARY, kv[0][0]))
        return found

    for cat, names in CATEGORIES.items():
        present = []
        for n in names:
            present.extend(entries_for(n))
        if not present:
            continue
        lines.append(f"## {cat} ({len(present)})")
        lines.append("")
        lines.append("| Репозиторий | Описание | Язык | Доступ | Локально | Обновлён |")
        lines.append("|---|---|---|---|---|---|")
        for key, meta in sorted(present, key=lambda kv: kv[0][1]):
            lines.append(fmt_row(key, meta))
        lines.append("")

    known = {n for names in CATEGORIES.values() for n in names}
    others = [(k, r) for k, r in sorted(repos.items()) if k[1] not in known]
    if others:
        lines.append(f"## Прочее ({len(others)})")
        lines.append("")
        lines.append("| Репозиторий | Описание | Язык | Доступ | Локально | Обновлён |")
        lines.append("|---|---|---|---|---|---|")
        for key, meta in others:
            lines.append(fmt_row(key, meta))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Локальные папки без remote (в `~/Projects`)")
    lines.append("")
    folders = local_folders_without_remote()
    if folders:
        lines.append("| Папка | Примечание |")
        lines.append("|---|---|")
        for folder in folders:
            note = "архив" if folder in ARCHIVE_FOLDERS else "рабочая копия / не-репозиторий"
            lines.append(f"| `{folder}` | {note} |")
    else:
        lines.append("_нет_")
    lines.append("")
    return "\n".join(lines)


def main():
    repos = fetch_repos()
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(build_md(repos))
    archived = sum(1 for r in repos.values() if r["archived"])
    print(f"OK: README.md собран, {len(repos)} репозиториев (архивных: {archived})")


if __name__ == "__main__":
    main()
