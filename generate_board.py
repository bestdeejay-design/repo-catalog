#!/usr/bin/env python3
"""Собирает BOARD.md — канбан по каталогу репозиториев.

Источники (единственные места правды):
  TASKS.md          — приоритеты P1/P2/P3 и треки A/B/C/D
  OPTIONS.md        — кандидаты, которых ещё нет в звёздах
  STARS-ARCHIVE.md  — снятые звёзды (история)

Карточка = репозиторий. Колонка = стадия. Двигать карточку = менять приоритет
в TASKS.md; доска пересобирается workflow-ом.

Использование: python3 generate_board.py
"""

import datetime as dt
import re

TASKS = "TASKS.md"
OPTIONS = "OPTIONS.md"
ARCHIVE = "STARS-ARCHIVE.md"
OUT = "BOARD.md"

TRACKS = {"A": "Центр агентов", "B": "macOS", "C": "LOVII CRM", "D": "Прочее", "E": "Игры"}

ROW = re.compile(r"^\|\s*\[`?([^`\]]+)`?\]\((https://github\.com/[^)]+)\)\s*\|(.*)$")
ARCH = re.compile(r"^-\s*\[([^\]]+)\]\((https://github\.com/[^)]+)\)\s*—\s*(.*)$")


def cells(rest: str):
    return [c.strip() for c in rest.split("|")]


def parse_tasks():
    """Возвращает список карточек: repo, url, stars, prio, track, note."""
    cards, track = [], None
    for line in open(TASKS, encoding="utf-8"):
        m = re.match(r"^## ([A-E])\.", line)
        if m:
            track = m.group(1)
            continue
        if line.startswith("## "):
            track = None
            continue
        r = ROW.match(line)
        if not r or not track:
            continue
        name, url, rest = r.group(1), r.group(2), r.group(3)
        c = cells(rest)
        if len(c) < 2:
            continue
        stars = c[0].replace("*", "")
        prio = c[1].replace("*", "").strip()
        note = c[2] if len(c) > 2 else ""
        if prio not in ("P1", "P2", "P3"):
            continue
        cards.append({
            "name": name, "url": url, "stars": stars,
            "prio": prio, "track": track, "note": note,
        })
    return cards


def parse_drop():
    """Репозитории, помеченные на снятие звезды (секция в TASKS.md)."""
    cards, inside = [], False
    for line in open(TASKS, encoding="utf-8"):
        if "Снять звезду" in line:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if not inside:
            continue
        r = ROW.match(line)
        if not r:
            continue
        c = cells(r.group(3))
        cards.append({"name": r.group(1), "url": r.group(2),
                      "note": c[0] if c else "", "track": "—"})
    return cards


def parse_options():
    """Кандидаты в звёзды из OPTIONS.md."""
    cards, in_section = [], False
    for line in open(OPTIONS, encoding="utf-8"):
        if line.startswith("## Кандидаты в звёзды"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        r = ROW.match(line)
        if not r:
            continue
        c = cells(r.group(3))
        if len(c) < 4:
            continue
        cards.append({
            "name": r.group(1), "url": r.group(2),
            "stars": c[0].replace("*", ""), "lic": c[1],
            "note": c[3], "idea": c[4] if len(c) > 4 else "",
        })
    return cards


def parse_archive():
    cards = []
    try:
        text = open(ARCHIVE, encoding="utf-8")
    except FileNotFoundError:
        return cards
    for line in text:
        m = ARCH.match(line)
        if m:
            cards.append({"name": m.group(1), "url": m.group(2), "note": m.group(3)})
    return cards


def esc(s: str, limit: int = 90) -> str:
    s = (s or "").replace("|", "\\|").replace("\n", " ").strip()
    return s if len(s) <= limit else s[: limit - 1] + "…"


def table(cards, cols=("Репозиторий", "★", "Трек", "Что взять")):
    if not cards:
        return "_пусто_\n"
    out = ["| " + " | ".join(cols) + " |", "|---|---|---|---|"]
    for c in cards:
        track = c.get("track") or TRACKS.get(c.get("track", ""), "—")
        out.append(
            f"| [`{c['name']}`]({c['url']}) | {c.get('stars', '—')} | {track} | {esc(c.get('note', ''))} |"
        )
    return "\n".join(out) + "\n"


def dedupe(cards):
    """Один репозиторий может стоять в нескольких треках — на доске это одна карточка."""
    rank = {"P1": 1, "P2": 2, "P3": 3}
    seen = {}
    for c in cards:
        key = c["url"].lower()
        if key not in seen:
            c["tracks"] = [c["track"]]
            seen[key] = c
            continue
        cur = seen[key]
        if c["track"] not in cur["tracks"]:
            cur["tracks"].append(c["track"])
        if rank[c["prio"]] < rank[cur["prio"]]:
            cur["prio"] = c["prio"]
        if len(c["note"]) > len(cur["note"]):
            cur["note"] = c["note"]
    for c in seen.values():
        c["track"] = " + ".join(TRACKS.get(t, t) for t in c["tracks"])
    return list(seen.values())


def main():
    cards = dedupe(parse_tasks())
    by_prio = {p: [c for c in cards if c["prio"] == p] for p in ("P1", "P2", "P3")}
    candidates = parse_options()
    drop = parse_drop()
    archive = parse_archive()

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"""# Канбан каталога

> Собрано автоматически: {now}. Руками не править — перезапишется.
> Карточка = репозиторий. Колонка = стадия. Источник правды — `TASKS.md`
> (приоритеты), `OPTIONS.md` (кандидаты), `STARS-ARCHIVE.md` (архив).

**Как двигать карточку.** Поменяй приоритет в `TASKS.md`: `P1` — беру сейчас,
`P2` — референс, `P3` — полка. Ставишь звезду новому репозиторию — его подхватит
плановая сверка и положит в нужную колонку.

## 🚀 Беру в работу (P1) — {len(by_prio['P1'])}

{table(by_prio['P1'])}

## 📚 Референс (P2) — {len(by_prio['P2'])}

{table(by_prio['P2'])}

## 🗂 На полке (P3) — {len(by_prio['P3'])}

{table(by_prio['P3'])}

## 🧪 Кандидаты, ещё не в звёздах — {len(candidates)}

Взяты из `OPTIONS.md`. Отметь звезду — попадут в каталог при следующей сверке.

| Репозиторий | ★ | Лицензия | Зачем |
|---|---|---|---|
"""
    for c in candidates:
        md += f"| [`{c['name']}`]({c['url']}) | {c['stars']} | {c['lic']} | {esc(c['note'])} |\n"

    md += f"""
## 🗑 Помечены на снятие — {len(drop)}

Ещё в звёздах, но пользы не видно. Снять звезду — уйдут в архив, останутся в истории.

"""

    md += table(drop, ("Репозиторий", "★", "Трек", "Почему")) if drop else "_пусто_\n"

    md += f"""
## 🗄 Архив: снятые звёзды — {len(archive)}

Остаются для истории. Возвращаются в каталог, если звезда поставлена снова.

"""
    md += table(archive, ("Репозиторий", "было", "Описание")) if archive else "_пусто_\n"
    md += "\n---\n\nВсего в каталоге: **%d** · кандидатов: **%d** · в архиве: **%d**\n" % (
        len(cards), len(candidates), len(archive)
    )

    open(OUT, "w", encoding="utf-8").write(md)
    print(f"OK: {OUT} — P1 {len(by_prio['P1'])}, P2 {len(by_prio['P2'])}, "
          f"P3 {len(by_prio['P3'])}, на снятие {len(drop)}, кандидатов {len(candidates)}, архив {len(archive)}")


if __name__ == "__main__":
    main()
