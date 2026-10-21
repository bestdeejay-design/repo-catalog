#!/usr/bin/env python3
"""Сверка каталога звёзд с реальными звёздами GitHub.

Режимы:
  python3 sync_stars.py            — только отчёт (ничего не меняет)
  python3 sync_stars.py --json     — отчёт в JSON (для агента/скриптов)
  python3 sync_stars.py --apply    — применить: снятые звёзды перенести в
                                     STARS-ARCHIVE.md и убрать их строки из
                                     STARS.md / TASKS.md; обновить слепок

Слепок stars_snapshot.json хранит полные данные по звёздам, чтобы у снятого
репозитория осталось описание в архиве, даже когда GitHub его уже не отдаёт.

Требования: gh CLI, авторизация (gh auth login).
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys

FILES = ("STARS.md", "TASKS.md")
ARCHIVE = "STARS-ARCHIVE.md"
SNAPSHOT = "stars_snapshot.json"
LINK_RE = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)\)")
DATE = dt.date.today().isoformat()


def fetch_starred():
    out = subprocess.run(
        ["gh", "api", "user/starred?per_page=100", "--paginate"],
        capture_output=True, text=True, check=True,
    ).stdout
    repos = {}
    for r in json.loads(out):
        repos[r["full_name"].lower()] = {
            "full_name": r["full_name"],
            "stars": r["stargazers_count"],
            "language": r.get("language") or "—",
            "description": (r.get("description") or "").strip(),
            "pushed_at": r["pushed_at"][:10],
            "archived": r.get("archived", False),
            "url": r["html_url"],
        }
    return repos


def load_snapshot():
    try:
        with open(SNAPSHOT, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def read_files():
    texts = {}
    for name in FILES:
        try:
            texts[name] = open(name, encoding="utf-8").read()
        except FileNotFoundError:
            sys.exit(f"{name} не найден — запускай из корня репозитория")
    return texts


def strip_rows(texts, removed):
    """Убирает строки таблиц, где упомянут снятый репозиторий."""
    changed = {}
    for name, text in texts.items():
        out, dropped = [], 0
        for line in text.split("\n"):
            low = line.lower()
            if line.lstrip().startswith("|") and any(
                f"github.com/{r}" in low for r in removed
            ):
                dropped += 1
                continue
            out.append(line)
        if dropped:
            changed[name] = (("\n".join(out)).rstrip() + "\n", dropped)
    return changed


def append_archive(removed_meta):
    try:
        text = open(ARCHIVE, encoding="utf-8").read()
    except FileNotFoundError:
        text = (
            "# Архив звёзд\n\n"
            "Репозитории, с которых снята звезда. Удаляются из рабочего каталога\n"
            "(`STARS.md` / `TASKS.md`), но остаются здесь для истории.\n\n"
            "Формат строки: дата снятия — репозиторий — звёзды на момент снятия — язык — описание автора.\n"
        )
    stem = f"## Снято {DATE}"
    if stem not in text:
        text = text.rstrip() + f"\n\n{stem}\n\n"
    for m in removed_meta:
        text += (
            f"- [{m['full_name']}]({m['url']}) — ★{m['stars']} · {m['language']} · "
            f"{m['description'] or 'без описания'}\n"
        )
    open(ARCHIVE, "w", encoding="utf-8").write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="вывести отчёт в JSON")
    ap.add_argument("--apply", action="store_true", help="применить изменения")
    args = ap.parse_args()

    starred = fetch_starred()
    snapshot = load_snapshot()
    texts = read_files()

    listed = set()
    for text in texts.values():
        listed |= {m.lower() for m in LINK_RE.findall(text)}

    new = sorted(set(starred) - listed)
    gone = sorted(listed - set(starred) - {"bestdeejay-design/repo-catalog"})

    report = {
        "date": DATE,
        "starred_count": len(starred),
        "listed_count": len(listed),
        "added": [starred[n] for n in new],
        "removed": [snapshot.get(n) or {"full_name": n, "url": f"https://github.com/{n}",
                                        "stars": 0, "language": "—", "description": ""}
                    for n in gone],
        "applied": False,
    }

    if args.apply and gone:
        changed = strip_rows(texts, gone)
        for name, (text, _) in changed.items():
            open(name, "w", encoding="utf-8").write(text)
        append_archive(report["removed"])
        report["applied"] = True
        report["stripped_rows"] = {k: v[1] for k, v in changed.items()}

    if args.apply:
        with open(SNAPSHOT, "w", encoding="utf-8") as f:
            json.dump(starred, f, ensure_ascii=False, indent=1, sort_keys=True)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"В звёздах: {report['starred_count']} · в каталоге: {report['listed_count']}")
    for name in FILES:
        print(f"  {name}: {len({m.lower() for m in LINK_RE.findall(texts[name])})} ссылок")
    if report["added"]:
        print(f"\nНовые звёзды, которых нет в каталоге ({len(new)}):")
        for r in report["added"]:
            print(f"  + {r['full_name']} ★{r['stars']} · {r['language']} · {r['description'][:80]}")
    if report["removed"]:
        print(f"\nЗвезда снята ({len(gone)}):")
        for r in report["removed"]:
            print(f"  - {r['full_name']}")
        print("  → в архив попадут при запуске с --apply")
    if not new and not gone:
        print("\nВсё сходится.")
    if report["applied"]:
        print(f"\nПрименено: архив обновлён, слепок сохранён ({SNAPSHOT}).")


if __name__ == "__main__":
    main()
