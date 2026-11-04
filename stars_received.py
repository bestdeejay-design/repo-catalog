#!/usr/bin/env python3
"""Рейтинг полученных звёзд: сколько ⭐ собрали мои репозитории.

Обратная сторона STARS.md: там каталог чужих репозиториев, которым звезду
поставил я, здесь — сводка по моим собственным: кто сколько звёзд получил.

Режимы:
  python3 stars_received.py          — пересобрать RATING.md и напечатать сводку
  python3 stars_received.py --json   — только сводка в JSON, файл не трогать

Требования: gh CLI, авторизация (gh auth login).
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

OWNERS = ["bestdeejay-design", "rucorp", "axiiom-ru", "lovii-tech", "dajetbro"]
OUT = "RATING.md"
DATE = dt.date.today().isoformat()
DESC_LIMIT = 110


def fetch_owner(owner):
    out = subprocess.run(
        ["gh", "api", f"users/{owner}/repos?per_page=100&type=owner", "--paginate"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        sys.exit(f"gh api для {owner} упал: {out.stderr.strip()[:300]}")
    return json.loads(out.stdout or "[]")


def collect():
    repos, seen = [], set()
    for owner in OWNERS:
        for r in fetch_owner(owner):
            key = (r.get("full_name") or "").lower()
            if not key or key in seen:
                continue
            seen.add(key)
            repos.append({
                "full_name": r["full_name"],
                "url": r["html_url"],
                "stars": r.get("stargazers_count") or 0,
                "language": r.get("language") or "—",
                "description": (r.get("description") or "").strip(),
                "fork": bool(r.get("fork")),
                "archived": bool(r.get("archived")),
            })
    repos.sort(key=lambda x: (-x["stars"], x["full_name"].lower()))
    return repos


def cell(text):
    text = " ".join(text.split()).replace("|", "\\|")
    if len(text) > DESC_LIMIT:
        text = text[: DESC_LIMIT - 1].rstrip() + "…"
    return text


def render(repos):
    total = sum(r["stars"] for r in repos)
    with_stars = [r for r in repos if r["stars"] > 0]
    owners = {}
    for r in repos:
        o = r["full_name"].split("/")[0]
        agg = owners.setdefault(o, {"repos": 0, "stars": 0})
        agg["repos"] += 1
        agg["stars"] += r["stars"]

    lines = [
        "# Рейтинг полученных звёзд",
        "",
        "Обратная сторона [STARS.md](./STARS.md): там — чужие репозитории, которым звезду поставил я,",
        "здесь — сколько звёзд собрали **мои** репозитории со стороны. Файл генерируется,",
        "руками не править: `python3 stars_received.py`.",
        "",
        f"- Сверено: **{DATE}** — дата последнего изменения цифр (файл перезаписывается только тогда,\n  когда меняются числа, чтобы недельная сверка не плодила пустые коммиты)",
        f"- Публичных репозиториев: **{len(repos)}** у {len(owners)} владельцев",
        f"- Звёзд всего: **{total}**, хотя бы одна звезда — у **{len(with_stars)}**",
        f"- Без звёзд: **{len(repos) - len(with_stars)}**",
        "",
        "## По владельцам",
        "",
        "| Владелец | Репозиториев | Звёзд |",
        "|---|---|---|",
    ]
    for o, agg in sorted(owners.items(), key=lambda kv: (-kv[1]["stars"], kv[0])):
        lines.append(f"| `{o}` | {agg['repos']} | {agg['stars']} |")

    lines += [
        "",
        f"## Топ репозиториев ({len(with_stars)})",
        "",
        "| # | Репозиторий | ★ | Язык | Что это |",
        "|---|---|---|---|---|",
    ]
    for i, r in enumerate(with_stars, 1):
        mark = " 📦" if r["archived"] else (" 🍴" if r["fork"] else "")
        desc = cell(r["description"]) or "—"
        lines.append(
            f"| {i} | [`{r['full_name']}`]({r['url']}){mark} | {r['stars']} | "
            f"{r['language']} | {desc} |"
        )
    lines += [
        "",
        "Строки есть только у репозиториев с ⭐ ≥ 1. Остальные "
        f"{len(repos) - len(with_stars)} публичных репозиториев без звёзд — это норма для рабочих",
        "репозиториев под задачи, а не под аудиторию.",
        "",
        "## Что видно",
        "",
    ]
    if with_stars and total:
        top = with_stars[0]
        share = round(100 * top["stars"] / total)
        lines.append(
            f"- Половина рейтинга держится на одном репозитории: `{top['full_name']}` — "
            f"{top['stars']} из {total} ({share}%), а не на всём портфеле."
            if share >= 40 else
            f"- Самый заметный репозиторий: `{top['full_name']}` — {top['stars']} из {total} звёзд ({share}%)."
        )
        lines.append(
            f"- Медиана по репозиториям со звёздами — "
            f"{sorted(r['stars'] for r in with_stars)[len(with_stars) // 2]}."
        )
    else:
        lines.append("- Звёзд нет ни у одного репозитория.")

    lines += [
        "",
        "## Как обновлять",
        "",
        "- `python3 stars_received.py` — пересобрать файл (нужен `gh`, авторизованный под владельцем).",
        "- Входит в недельную сверку звёзд (понедельник, 10:00 MSK) вместе с `sync_stars.py`.",
        "",
    ]
    return "\n".join(lines), {
        "date": DATE,
        "repos": len(repos),
        "owners": len(owners),
        "stars_total": total,
        "with_stars": len(with_stars),
        "top": [
            {"repo": r["full_name"], "stars": r["stars"]}
            for r in with_stars[:5]
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="только сводка, файл не писать")
    args = ap.parse_args()

    repos = collect()
    text, summary = render(repos)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    def without_date(chunk):
        return "\n".join(l for l in chunk.split("\n") if not l.startswith("- Сверено:"))

    old = ""
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            old = f.read()
    if old and without_date(old) == without_date(text):
        print(
            f"Цифры не изменились: {summary['repos']} репозиториев · "
            f"{summary['stars_total']} звёзд — {OUT} не трогаю"
        )
        return

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(
        f"Репозиториев: {summary['repos']} · звёзд: {summary['stars_total']} · "
        f"со звёздами: {summary['with_stars']} → {OUT}"
    )
    for r in summary["top"]:
        print(f"  {r['repo']} — {r['stars']}")


if __name__ == "__main__":
    main()
