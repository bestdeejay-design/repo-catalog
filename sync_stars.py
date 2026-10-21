#!/usr/bin/env python3
"""Сверка STARS.md с реальными звёздами GitHub.

Показывает: новые звёзды, которых нет в STARS.md, и записи в STARS.md,
которых больше нет в звёздах. Ничего не переписывает — только отчёт.

Использование: python3 sync_stars.py
Требования: gh CLI, авторизация (gh auth login).
"""

import json
import re
import subprocess
import sys

STARS_FILE = "STARS.md"
LINK_RE = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)\)")


def fetch_starred():
    out = subprocess.run(
        ["gh", "api", "user/starred?per_page=100", "--paginate"],
        capture_output=True, text=True, check=True,
    ).stdout
    return {r["full_name"].lower() for r in json.loads(out)}


def main():
    starred = fetch_starred()
    try:
        text = open(STARS_FILE, encoding="utf-8").read()
    except FileNotFoundError:
        sys.exit(f"{STARS_FILE} не найден — запускай из корня репозитория")

    listed = {m.lower() for m in LINK_RE.findall(text)}

    new = sorted(starred - listed)
    gone = sorted(listed - starred - {"bestdeejay-design/repo-catalog"})

    print(f"В звёздах: {len(starred)} · в {STARS_FILE}: {len(listed)}")
    if new:
        print(f"\nНовые звёзды, которых нет в каталоге ({len(new)}):")
        for name in new:
            print(f"  + {name}")
    if gone:
        print(f"\nВ каталоге, но звезды уже нет ({len(gone)}):")
        for name in gone:
            print(f"  - {name}")
    if not new and not gone:
        print("\nВсё сходится.")


if __name__ == "__main__":
    main()
