#!/usr/bin/env python3
"""Генератор каталога репозиториев bestdeejay-design.

Тянет данные с GitHub CLI (gh repo list) и собирает README.md
с группировкой по категориям и привязкой локальных папок.

Использование: python3 generate_catalog.py
Требования: gh CLI, авторизация.
"""

import json
import subprocess
from collections import OrderedDict

OWNER = "bestdeejay-design"

# Имя репо -> категория. Репо без категории попадут в «Прочее».
CATEGORIES = OrderedDict([
    ("Продукты и платформы", [
        "pmos", "personal-os", "lovii", "lovii_docs", "lovii_demo",
        "lovii_presentation", "knowledge-base", "voice-assistant",
    ]),
    ("Лендинги и веб-сайты", [
        "axiiom", "axiiom_landing", "mobiap", "paffo", "ishotgirls",
        "neo-consulting", "arental", "arental_2", "arental-rental",
        "aotochka.ru", "pizza", "napolipizza", "pizzaloviiru",
        "univerid", "univerid_demo", "blog", "platforma", "wordpress",
        "static-site", "joer", "kodstudy", "spbgti", "archive-spbgti",
        "ambar", "agents", "hype", "booking", "minigames", "aichat",
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
        "oc-architecture", "opencode-setup",
    ]),
    ("Книги и контент", [
        "shimmer", "awesome-ai-handbook", "awesome-local-llm",
        "awesome-local-ai",
    ]),
    ("Документация", [
        "docs", "docsv", "srs-docs",
    ]),
    ("Черновики (WIP)", [
        "mag", "extension1",
    ]),
])

# Локальная папка -> репозиторий (для привязки рабочих копий)
LOCAL_MAP = {
    "Technolozka": "spbgti",
    "agent-skills": "agent-skills",
    "app": "app",
    "arenteral_2": "arental_2",
    "axiiom_github": "axiiom",
    "buhtest": "neo-consulting",
    "design-rnd": "design-demo",
    "dj1": "dj1",
    "docs": "docs",
    "foodie": "foodie",
    "imgforge": "imgforge",
    "ishotgirls": "ishotgirls",
    "ksu": "ksu",
    "lovii": "lovii",
    "lovii_demo": "lovii_demo",
    "lovii_docs": "lovii_docs",
    "lovii_presentation": "lovii_presentation",
    "mobiap-repo": "mobiap",
    "mobiap-v2": "axiiom",
    "mobiap": "mobiap",
    "oc-architecture": "oc-architecture",
    "opencode-setup": "opencode-setup",
    "paffo": "paffo",
    "pizza": "pizza",
    "raster-to-svg": "raster-to-svg",
    "references": "designer-references",
    "shimmer": "shimmer",
    "srs-docs": "srs-docs",
    "svg-readme-header-footer": "svg-readme-header-footer",
}

LOCAL_BY_REPO = {}
for folder, repo in LOCAL_MAP.items():
    LOCAL_BY_REPO.setdefault(repo, []).append(folder)


def fetch_repos():
    """Возвращает {name: {description, visibility, language, updated, homepage, topics}}."""
    fields = ["name", "description", "visibility", "primaryLanguage",
              "updatedAt", "homepageUrl", "repositoryTopics"]
    out = subprocess.run(
        ["gh", "repo", "list", OWNER, "--limit", "200", "--json", ",".join(fields)],
        capture_output=True, text=True, check=True,
    ).stdout
    repos = {}
    for r in json.loads(out):
        repos[r["name"]] = {
            "description": (r.get("description") or "").strip(),
            "visibility": r.get("visibility", ""),
            "language": (r.get("primaryLanguage") or {}).get("name", "") if r.get("primaryLanguage") else "",
            "updated": (r.get("updatedAt") or "")[:10],
            "homepage": r.get("homepageUrl") or "",
            "topics": [t["name"] for t in (r.get("repositoryTopics") or [])],
        }
    return repos


def fmt_row(name, meta):
    desc = meta["description"] or "—"
    if len(desc) > 100:
        desc = desc[:97].rstrip() + "…"
    lang = meta["language"] or "—"
    vis = "🔓" if meta["visibility"] == "PUBLIC" else "🔒"
    local = ", ".join(LOCAL_BY_REPO.get(name, [])) or "—"
    updated = meta["updated"]
    home = f" [🌐]({meta['homepage']})" if meta["homepage"] else ""
    return f"| [`{name}`](https://github.com/{OWNER}/{name}){home} | {desc} | {lang} | {vis} | {local} | {updated} |"


def build_md(repos):
    lines = []
    lines.append(f"# Каталог репозиториев — {OWNER}")
    lines.append("")
    lines.append(f"Всего репозиториев: **{len(repos)}**. "
                 "Сгенерировано скриптом `generate_catalog.py` — запускай `python3 generate_catalog.py`, чтобы обновить.")
    lines.append("")
    lines.append("Легенда: 🔓 публичный · 🔒 приватный · 🌐 ссылка на сайт · локальная папка в `~/Projects`")
    lines.append("")

    for cat, names in CATEGORIES.items():
        present = [(n, repos[n]) for n in names if n in repos]
        if not present:
            continue
        lines.append(f"## {cat} ({len(present)})")
        lines.append("")
        lines.append("| Репозиторий | Описание | Язык | Доступ | Локально | Обновлён |")
        lines.append("|---|---|---|---|---|---|")
        for name, meta in sorted(present):
            lines.append(fmt_row(name, meta))
        lines.append("")

    # Прочее — всё, что не попало в категории
    known = {n for names in CATEGORIES.values() for n in names}
    others = [(n, r) for n, r in sorted(repos.items()) if n not in known]
    if others:
        lines.append(f"## Прочее ({len(others)})")
        lines.append("")
        lines.append("| Репозиторий | Описание | Язык | Доступ | Локально | Обновлён |")
        lines.append("|---|---|---|---|---|---|")
        for name, meta in others:
            lines.append(fmt_row(name, meta))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Локальные папки без remote (в `~/Projects`)")
    lines.append("")
    lines.append("| Папка | Примечание |")
    lines.append("|---|---|")
    no_remote = [
        "aotochka.ru", "arental", "axiiom", "axiiom-ru", "axiiom_new",
        "best", "dajet", "design-rnd", "docv", "factmat", "local-coding",
        "neo-deck", "platforma", "reddit", "research", "research_pull",
        "skills-repo", "test", "архив/archive", "презентация",
    ]
    for folder in no_remote:
        lines.append(f"| `{folder}` | рабочая копия / не-репозиторий |")
    lines.append("")
    return "\n".join(lines)


def main():
    repos = fetch_repos()
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(build_md(repos))
    print(f"OK: README.md собран, {len(repos)} репозиториев")


if __name__ == "__main__":
    main()