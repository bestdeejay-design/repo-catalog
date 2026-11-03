#!/usr/bin/env python3
"""Ежедневный отчёт по всем репозиториям и всем GitHub Projects.

Что делает:
  1. Обходит владельцев (user-аккаунты и организации), собирает репозитории.
  2. Читает все GitHub Projects v2 через GraphQL — с датами создания/закрытия.
  3. Классифицирует задачи: добавленные сегодня / выполненные сегодня / в процессе.
  4. Собирает активность репозиториев за день: коммиты, issue, PR.
  5. Пишет отчёт в reports/YYYY/YYYY-MM-DD.md + .json и обновляет reports/index.md.

Запуск:
  python3 daily_report.py                 # сегодня
  python3 daily_report.py --date 2026-11-02
  python3 daily_report.py --local         # + локальные долги (незапушенное) в ~/Projects
  python3 daily_report.py --no-repos      # только доски, без обхода репозиториев

Требуется: gh (авторизован, scope project+repo). Больше ничего.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

# --- настройки -----------------------------------------------------------------

TZ = timezone(timedelta(hours=3))          # Europe/Moscow
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECTS_ROOT = SCRIPT_DIR.parent

OWNERS = ["bestdeejay-design", "lovii-tech", "axiiom-ru", "lovii-ru", "rucorp"]

DONE_WORDS = {"done", "готово", "closed", "выполнено", "completed"}
WIP_WORDS = {"in progress", "на проверке", "в работе", "doing", "wip"}
# всё остальное (Todo, Backlog, Бэклог, Ready, К работе, Ждёт, Waiting GO, Frozen,
# пустой статус) считаем не начатым

STALE_DAYS = 14            # «в процессе» без движения дольше этого — в раздел внимания
MAX_COMMITS_SHOWN = 40     # сколько коммитов печатать списком
GRAPHQL_BATCH = 10         # сколько репозиториев в одном GraphQL-запросе
WORKERS = 8

_lock = threading.Lock()


# --- gh ------------------------------------------------------------------------

def gh(args: list[str], allow_fail: bool = False, retries: int = 3) -> str:
    """Вызов gh с повторами. Возвращает stdout; при allow_fail — '' вместо падения."""
    last = ""
    for attempt in range(retries):
        p = subprocess.run(["gh", *args], capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout
        last = (p.stderr or p.stdout or "").strip()
        if "rate limit" not in last.lower() and "secondary" not in last.lower():
            break
    if allow_fail:
        return ""
    raise RuntimeError(f"gh {' '.join(args[:3])}… → {last[:300]}")


def gh_json(args: list[str], default=None, allow_fail: bool = True):
    out = gh(args, allow_fail=allow_fail)
    if not out.strip():
        return default
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return default


def graphql(query: str, variables: dict) -> dict:
    args = ["api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        if isinstance(v, int):
            args += ["-F", f"{k}={v}"]
        elif v is None:
            args += ["-f", f"{k}="]
        else:
            args += ["-f", f"{k}={v}"]
    out = gh(args, allow_fail=True)
    if not out.strip():
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {}


# --- время ---------------------------------------------------------------------

def day_window(day: str) -> tuple[datetime, datetime]:
    d = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=TZ)
    return d, d + timedelta(days=1)


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def in_window(value, start: datetime, end: datetime) -> bool:
    ts = parse_ts(value) if isinstance(value, str) else value
    return bool(ts and start <= ts < end)


# --- репозитории ---------------------------------------------------------------

def discover_repos(owners: list[str]) -> list[dict]:
    repos: list[dict] = []
    seen: set[str] = set()
    for owner in owners:
        data = gh_json(
            ["repo", "list", owner, "--limit", "500", "--json",
             "nameWithOwner,isArchived,isPrivate,pushedAt"],
            default=[],
        ) or []
        for r in data:
            name = r.get("nameWithOwner")
            if not name or name in seen:
                continue
            seen.add(name)
            r["owner"] = name.split("/")[0]
            r["short"] = name.split("/")[1]
            repos.append(r)
    return repos


# --- проекты -------------------------------------------------------------------

PROJECT_QUERY = """
query($owner:String!, $num:Int!, $cursor:String) {
  repositoryOwner(login:$owner) {
    __typename
    ... on ProjectV2Owner {
      projectV2(number:$num) {
        title
        url
        items(first:100, after:$cursor) {
          pageInfo { hasNextPage endCursor }
          nodes {
            id
            createdAt
            updatedAt
            fieldValueByName(name:"Status") {
              ... on ProjectV2ItemFieldSingleSelectValue { name }
            }
            content {
              __typename
              ... on Issue {
                number title url state createdAt closedAt
                repository { nameWithOwner }
              }
              ... on PullRequest {
                number title url state createdAt closedAt mergedAt
                repository { nameWithOwner }
              }
              ... on DraftIssue { title createdAt updatedAt }
            }
          }
        }
      }
    }
  }
}
"""


def list_projects(owners: list[str]) -> list[dict]:
    out: list[dict] = []
    for owner in owners:
        data = gh_json(["project", "list", "--owner", owner, "--limit", "100", "--format", "json"])
        if not data:
            continue
        for p in data.get("projects", []):
            if p.get("closed"):
                continue
            p["owner"] = owner
            out.append(p)
    return out


def project_items(owner: str, number: int) -> list[dict]:
    items: list[dict] = []
    cursor = None
    while True:
        res = graphql(PROJECT_QUERY, {"owner": owner, "num": number, "cursor": cursor})
        node = ((res.get("data") or {}).get("repositoryOwner") or {}).get("projectV2") or {}
        page = node.get("items") or {}
        items.extend(page.get("nodes") or [])
        info = page.get("pageInfo") or {}
        if not info.get("hasNextPage"):
            break
        cursor = info.get("endCursor")
        if not cursor:
            break
    return items


def status_of(item: dict) -> str:
    fv = item.get("fieldValueByName") or {}
    return (fv.get("name") or "").strip()


def kind_of(status: str) -> str:
    s = status.lower()
    if s in DONE_WORDS:
        return "done"
    if s in WIP_WORDS:
        return "wip"
    return "todo"


def flatten_task(item: dict, project: dict) -> dict:
    content = item.get("content") or {}
    ctype = content.get("__typename") or "DraftIssue"
    repo = ((content.get("repository") or {}) or {}).get("nameWithOwner") or ""
    status = status_of(item)
    return {
        "project": f"{project['owner']}/{project['number']}",
        "project_title": project.get("title") or "",
        "project_url": project.get("url") or "",
        "type": ctype,
        "title": content.get("title") or "",
        "url": content.get("url") or project.get("url") or "",
        "number": content.get("number"),
        "repo": repo,
        "status": status,
        "bucket": kind_of(status),
        "state": content.get("state") or "",
        "item_created": item.get("createdAt"),
        "item_updated": item.get("updatedAt"),
        "created_at": content.get("createdAt"),
        "closed_at": content.get("closedAt"),
        "merged_at": content.get("mergedAt"),
    }


# --- активность репозиториев ----------------------------------------------------

def repo_commits(repo: str, since_iso: str) -> list[dict]:
    if not repo:
        return []
    out = gh_json(
        ["api", f"repos/{repo}/commits?since={quote(since_iso, safe='')}&per_page=100"],
        default=[],
    ) or []
    if not isinstance(out, list):
        return []
    return [
        {
            "sha": (c.get("sha") or "")[:7],
            "message": ((c.get("commit") or {}).get("message") or "").split("\n")[0],
            "author": (((c.get("author") or {}) or {}).get("login")
                       or ((c.get("commit") or {}).get("author") or {}).get("name") or "?"),
            "date": ((c.get("commit") or {}).get("author") or {}).get("date"),
            "url": c.get("html_url") or "",
        }
        for c in out
    ]


REPO_GQL = """
query($owner:String!, $name:String!, $since:DateTime!) {
  repository(owner:$owner, name:$name) {
    issues(first:50, filterBy:{since:$since}) {
      nodes { number title url state createdAt closedAt }
    }
    pullRequests(first:50, orderBy:{field:UPDATED_AT, direction:DESC}) {
      nodes { number title url state createdAt closedAt mergedAt updatedAt }
    }
  }
}
"""


def batch_issues_prs(repos: list[dict], since: datetime) -> dict[str, dict]:
    """issues/PR по репозиториям, пачками через GraphQL-алиасы."""
    result: dict[str, dict] = {}
    since_iso = since.isoformat()
    live = list(repos)
    for i in range(0, len(live), GRAPHQL_BATCH):
        chunk = live[i:i + GRAPHQL_BATCH]
        parts = []
        for idx, r in enumerate(chunk):
            parts.append(
                f'r{idx}: repository(owner:{json.dumps(r["owner"])}, name:{json.dumps(r["short"])}) '
                f'{{ issues(first:50, filterBy:{{since:{json.dumps(since_iso)}}}) '
                f'{{ nodes {{ number title url state createdAt closedAt }} }} '
                f'pullRequests(first:50, orderBy:{{field:UPDATED_AT, direction:DESC}}) '
                f'{{ nodes {{ number title url state createdAt closedAt mergedAt updatedAt }} }} }}'
            )
        query = "query { " + " ".join(parts) + " }"
        out = gh_json(["api", "graphql", "-f", f"query={query}"], default={})
        data = (out or {}).get("data") or {}
        if not data and len(chunk) > 1:
            # пачка не прошла целиком — повторяем по одному, чтобы не потерять активность
            for r in chunk:
                result.update(batch_issues_prs([r], since))
            continue
        for idx, r in enumerate(chunk):
            node = data.get(f"r{idx}") or {}
            result[r["nameWithOwner"]] = {
                "issues": (node.get("issues") or {}).get("nodes") or [],
                "prs": (node.get("pullRequests") or {}).get("nodes") or [],
            }
    return result


# --- локальные долги ------------------------------------------------------------

def local_state(project_root: Path) -> list[dict]:
    dirs = [p for p in sorted(project_root.iterdir()) if p.is_dir() and (p / ".git").exists()]

    def one(p: Path) -> dict | None:
        try:
            ahead = behind = 0
            has_upstream = subprocess.run(
                ["git", "-C", str(p), "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
                capture_output=True, text=True).returncode == 0
            if has_upstream:
                cnt = subprocess.run(["git", "-C", str(p), "rev-list", "--left-right", "--count",
                                      "@{u}...HEAD"], capture_output=True, text=True).stdout.split()
                if len(cnt) == 2:
                    behind, ahead = int(cnt[0]), int(cnt[1])
            raw = subprocess.run(["git", "-C", str(p), "status", "--porcelain", "-z"],
                                 capture_output=True, text=True).stdout
            entries = [e for e in raw.split("\0") if e.strip()]
            # собственные файлы отчёта не считаем долгом
            entries = [e for e in entries if not e[3:].startswith("reports/")]
            dirty = len(entries)
            if ahead or dirty or not has_upstream:
                return {"name": p.name, "ahead": ahead, "behind": behind,
                        "dirty": dirty, "remote": has_upstream}
        except Exception:
            return None
        return None

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        rows = [r for r in ex.map(one, dirs) if r]
    return sorted(rows, key=lambda r: (-r["ahead"], -r["dirty"], r["name"]))


# --- рендер ---------------------------------------------------------------------

def esc(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def plural(n: int, forms: tuple[str, str, str]) -> str:
    """Русское склонение: plural(5, ('коммит','коммита','коммитов'))."""
    n = abs(int(n)) % 100
    if 11 <= n <= 14:
        return forms[2]
    n %= 10
    if n == 1:
        return forms[0]
    if 2 <= n <= 4:
        return forms[1]
    return forms[2]


def cut(text: str, n: int = 95) -> str:
    text = esc(text)
    return text if len(text) <= n else text[: n - 1] + "…"


def link(t: dict) -> str:
    label = f"#{t['number']}" if t.get("number") else "карточка"
    return f"[{label}]({t['url']})" if t.get("url") else label


def short_date(ts: str | None) -> str:
    d = parse_ts(ts)
    return d.astimezone(TZ).strftime("%d.%m") if d else "—"


def render_md(ctx: dict) -> str:
    day = ctx["day"]
    d = datetime.strptime(day, "%Y-%m-%d")
    wd = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"][d.weekday()]
    tasks = ctx["tasks"]
    repos = ctx["repos"]
    L: list[str] = []
    n = 0

    def sec(title: str) -> None:
        nonlocal n
        n += 1
        L.append(f"## {n}. {title}")
        L.append("")

    added, done, wip = tasks["added"], tasks["done"], tasks["wip"]
    act = repos["active"]

    L.append(f"# Ежедневный отчёт — {d.strftime('%d.%m.%Y')} ({wd})")
    L.append("")
    L.append(f"Сформирован {ctx['generated'].strftime('%d.%m.%Y %H:%M')} MSK · "
             f"охват: {len(ctx['owners'])} владельцев, {repos['total']} репозиториев "
             f"(архивных {repos['archived']}), {ctx['project_count']} досок, "
             f"{ctx['task_total']} задач.")
    L.append("")
    L.append("> Отчёт собирается автоматически: `repo-catalog/daily_report.py`. "
             "Все отчёты за прошлые дни — в `reports/`, оглавление — `reports/index.md`.")
    L.append("")

    # 1. сводка
    sec("Сводка")
    L.append(f"- **Добавлено сегодня на доски:** {len(added)}")
    L.append(f"- **Выполнено сегодня:** {len(done)}")
    L.append(f"- **В работе сейчас:** {len(wip)}")
    if repos.get("scanned"):
        L.append(f"- **Активность в репозиториях:** {repos['commit_total']} "
                 f"{plural(repos['commit_total'], ('коммит', 'коммита', 'коммитов'))} в "
                 f"{len([r for r in act if r['commits']])} "
                 f"{plural(len([r for r in act if r['commits']]), ('репозитории', 'репозиториях', 'репозиториях'))}, "
                 f"новых issue {repos['issue_new']}, закрыто issue {repos['issue_closed']}, "
                 f"PR открыто {repos['pr_open']}, влито {repos['pr_merged']}")
        silent = repos["total"] - repos["archived"] - len(act)
        L.append(f"- **Без активности сегодня:** {silent} из {repos['total'] - repos['archived']} "
                 f"живых репозиториев")
    else:
        L.append("- **Активность в репозиториях:** не проверялась (`--no-repos`)")
    attention = ctx["attention"]
    if attention:
        L.append(f"- **Требует внимания:** {len(attention)} "
                 f"{plural(len(attention), ('пункт', 'пункта', 'пунктов'))}")
    L.append("")

    # 2. доски
    sec("Доски: состояние на конец дня")
    L.append("| Доска | Всего | Без статуса | Не начато | В работе | Готово | +сегодня | закрыто сегодня |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for p in ctx["boards"]:
        L.append(f"| [{esc(p['title'])}]({p['url']}) `{p['owner']}/{p['number']}` "
                 f"| {p['total']} | {p.get('unset', 0)} | {p['todo']} | {p['wip']} | {p['done']} "
                 f"| {p['added']} | {p['closed']} |")
    L.append("")
    L.append("Колонки «Без статуса / Не начато / В работе / Готово» в сумме дают «Всего».")
    L.append("")

    def task_table(rows: list[dict], created_col: bool = False) -> None:
        if not rows:
            L.append("_Пусто._")
            L.append("")
            return
        if created_col:
            L.append("| Задача | Проект | Статус | Создана | Репозиторий | Ссылка |")
            L.append("|---|---|---|---|---|---|")
        else:
            L.append("| Задача | Проект | Статус | Репозиторий | Ссылка |")
            L.append("|---|---|---|---|---|")
        for t in rows:
            proj = esc(t["project_title"]) or esc(t["project"])
            repo = esc(t["repo"]) or "—"
            status = esc(t["status"]) or "не задан"
            if created_col:
                L.append(f"| {cut(t['title'], 75)} | {cut(proj, 35)} | {status} "
                         f"| {short_date(t['created_at'])} | {repo} | {link(t)} |")
            else:
                L.append(f"| {cut(t['title'], 80)} | {cut(proj, 40)} | {status} | {repo} | {link(t)} |")
        L.append("")

    # 3. добавленные
    sec(f"Добавленные сегодня ({len(added)})")
    if not added:
        L.append("_Сегодня на доски не добавляли ни одной задачи._")
        L.append("")
    else:
        task_table(added, created_col=True)

    # 4. выполненные
    sec(f"Выполненные сегодня ({len(done)})")
    if not done:
        L.append("_Сегодня ничего не закрыто._")
        L.append("")
    else:
        task_table(done)

    # 5. в процессе
    sec(f"В процессе сейчас ({len(wip)})")
    if not wip:
        L.append("_Ни одна задача не в статусе «в работе»._")
        L.append("")
    else:
        L.append("| Задача | Проект | Статус | Репозиторий | Движение | Ссылка |")
        L.append("|---|---|---|---|---|---|")
        for t in wip:
            upd = parse_ts(t["item_updated"])
            age = (ctx["generated"] - upd.astimezone(TZ)).days if upd else None
            move = f"{age} дн. назад" if age is not None else "—"
            L.append(f"| {cut(t['title'], 70)} | {cut(t['project_title'], 35)} "
                     f"| {esc(t['status'])} | {esc(t['repo']) or '—'} | {move} | {link(t)} |")
        L.append("")

    # 6. активность репозиториев
    sec("Активность репозиториев")
    if not repos.get("scanned"):
        L.append("_Обход репозиториев отключён (`--no-repos`)._")
        L.append("")
    if not act:
        if repos.get("scanned"):
            L.append("_За день ни одного коммита, issue или PR._")
            L.append("")
    else:
        L.append("| Репозиторий | Коммиты | Issue + | Issue − | PR + | PR влито |")
        L.append("|---|---:|---:|---:|---:|---:|")
        for r in act:
            L.append(f"| `{esc(r['name'])}` | {r['commits']} | {r['issue_new']} "
                     f"| {r['issue_closed']} | {r['pr_open']} | {r['pr_merged']} |")
        L.append("")
        commits = [c for r in act for c in r["commit_list"]]
        if commits:
            L.append(f"<details><summary>Коммиты за день ({len(commits)})</summary>")
            L.append("")
            for c in commits[:MAX_COMMITS_SHOWN]:
                L.append(f"- `{esc(c['repo'])}` · `{c['sha']}` · {esc(c['author'])}: {cut(c['message'], 110)}")
            if len(commits) > MAX_COMMITS_SHOWN:
                L.append(f"- … и ещё {len(commits) - MAX_COMMITS_SHOWN}")
            L.append("")
            L.append("</details>")
            L.append("")

    # 6a. новые issue вне досок
    outside = ctx["outside"]
    L.append(f"### Новые issue вне досок ({len(outside)})")
    L.append("")
    if not outside:
        L.append("_Все созданные сегодня issue уже стоят на какой-нибудь доске._")
        L.append("")
    else:
        L.append("| Issue | Репозиторий | Ссылка |")
        L.append("|---|---|---|")
        for it in outside[:60]:
            L.append(f"| {cut(it['title'], 80)} | `{esc(it['repo'])}` | [#{it['number']}]({it['url']}) |")
        L.append("")

    # 7. внимание
    sec("Требует внимания")
    if not attention:
        L.append("_Ничего не просрочено, расхождений нет._")
        L.append("")
    else:
        for a in attention:
            L.append(f"- {a}")
        L.append("")

    # 8. локальные долги
    if ctx.get("local") is not None:
        loc = ctx["local"]
        sec("Локальные долги (`~/Projects`)")
        if not loc:
            L.append("_Все клоны чисты и синхронны с remote._")
            L.append("")
        else:
            L.append("| Папка | Впереди | Позади | Изменённых файлов | Remote |")
            L.append("|---|---:|---:|---:|---|")
            for r in loc[:40]:
                L.append(f"| `{esc(r['name'])}` | {r['ahead']} | {r['behind']} | {r['dirty']} "
                         f"| {'есть' if r['remote'] else '**нет**'} |")
            if len(loc) > 40:
                L.append(f"| … ещё {len(loc) - 40} | | | | |")
            L.append("")

    # 9. методика
    sec("Как это посчитано")
    L.append(f"- День — календарный по Москве: с {ctx['start'].strftime('%d.%m %H:%M')} "
             f"до {ctx['end'].strftime('%d.%m %H:%M')} MSK.")
    L.append("- «Добавленные» — карточки, попавшие на доску сегодня (дата карточки в проекте, "
             "не дата issue).")
    L.append("- «Выполненные» — issue/PR, закрытые сегодня, плюс карточки, переведённые в "
             "готовые сегодня.")
    L.append("- Коммиты считаются по ветке по умолчанию каждого репозитория, максимум 100 на репозиторий.")
    L.append("- Задачи с карточки без статуса считаются отдельно — колонка «Без статуса»; "
             "нестандартные статусы попадают в «Не начато» и видны в разделе 3–5.")
    L.append("")
    return "\n".join(L)


# --- сборка ---------------------------------------------------------------------

def build(day: str, with_repos: bool, with_local: bool, owners: list[str]) -> dict:
    start, end = day_window(day)
    generated = datetime.now(TZ)

    repos = discover_repos(owners)
    archived = sum(1 for r in repos if r.get("isArchived"))

    projects = list_projects(owners)
    all_items: list[dict] = []
    boards: list[dict] = []
    for p in projects:
        raw = project_items(p["owner"], int(p["number"]))
        flat = [flatten_task(i, p) for i in raw]
        all_items.extend(flat)
        boards.append({
            "owner": p["owner"], "number": int(p["number"]),
            "title": p.get("title") or "", "url": p.get("url") or "",
            "total": len(flat),
            "todo": sum(1 for t in flat if t["bucket"] == "todo" and t["status"]),
            "unset": sum(1 for t in flat if not t["status"]),
            "wip": sum(1 for t in flat if t["bucket"] == "wip"),
            "done": sum(1 for t in flat if t["bucket"] == "done"),
            "added": sum(1 for t in flat
                         if in_window(t["item_created"], start, end)),
            "closed": sum(1 for t in flat
                          if in_window(t["closed_at"], start, end)
                          or in_window(t["merged_at"], start, end)),
        })

    added = [t for t in all_items if in_window(t["item_created"], start, end)]
    done: list[dict] = []
    for t in all_items:
        if in_window(t["closed_at"], start, end) or in_window(t["merged_at"], start, end):
            done.append(t)
        elif (t["type"] == "DraftIssue" and t["bucket"] == "done"
              and in_window(t["item_updated"], start, end)):
            done.append(t)
    # дедупликация
    seen: set[str] = set()
    done = [x for x in done if not (x["url"] in seen or seen.add(x["url"]))]
    wip = [t for t in all_items if t["bucket"] == "wip" and t["state"] != "CLOSED"]

    boards.sort(key=lambda b: (-b["total"], b["title"]))
    added.sort(key=lambda t: t["item_created"] or "")
    done.sort(key=lambda t: t["closed_at"] or t["merged_at"] or t["item_updated"] or "")
    wip.sort(key=lambda t: t["item_updated"] or "")

    # --- репозитории ---
    active: list[dict] = []
    outside: list[dict] = []
    repo_stats = {"total": len(repos), "archived": archived, "commit_total": 0,
                  "issue_new": 0, "issue_closed": 0, "pr_open": 0, "pr_merged": 0,
                  "scanned": with_repos}

    if with_repos:
        live = [r for r in repos if not r.get("isArchived")]
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            commits_by_repo = dict(zip(
                [r["nameWithOwner"] for r in live],
                ex.map(lambda r: repo_commits(r["nameWithOwner"], start.isoformat()), live),
            ))
        issues_prs = batch_issues_prs(live, start) if live else {}

        board_urls = {t["url"] for t in all_items if t["url"]}
        for r in live:
            name = r["nameWithOwner"]
            cls = commits_by_repo.get(name, [])
            ip = issues_prs.get(name, {"issues": [], "prs": []})
            ins = [i for i in ip["issues"] if in_window(i.get("createdAt"), start, end)]
            icl = [i for i in ip["issues"] if in_window(i.get("closedAt"), start, end)]
            popen = [p for p in ip["prs"] if in_window(p.get("createdAt"), start, end)]
            pmerged = [p for p in ip["prs"] if in_window(p.get("mergedAt"), start, end)]
            if not (cls or ins or icl or popen or pmerged):
                continue
            active.append({
                "name": name, "commits": len(cls),
                "issue_new": len(ins), "issue_closed": len(icl),
                "pr_open": len(popen), "pr_merged": len(pmerged),
                "commit_list": [dict(c, repo=name) for c in cls],
            })
            repo_stats["commit_total"] += len(cls)
            repo_stats["issue_new"] += len(ins)
            repo_stats["issue_closed"] += len(icl)
            repo_stats["pr_open"] += len(popen)
            repo_stats["pr_merged"] += len(pmerged)
            for i in ins:
                if i.get("url") not in board_urls:
                    outside.append({"repo": name, "number": i["number"],
                                    "title": i["title"], "url": i["url"]})

        active.sort(key=lambda r: (-r["commits"], -r["issue_new"], r["name"]))
        outside.sort(key=lambda i: i["repo"])

    # --- внимание ---
    attention: list[str] = []
    for t in wip:
        upd = parse_ts(t["item_updated"])
        if upd and (generated - upd.astimezone(TZ)).days > STALE_DAYS:
            days = (generated - upd.astimezone(TZ)).days
            attention.append(
                f"**{cut(t['title'], 70)}** — в работе, но без движения {days} дн. "
                f"({esc(t['project_title'])}, {link(t)})")
    for t in done:
        if t["bucket"] != "done" and t.get("number"):
            attention.append(
                f"**{cut(t['title'], 70)}** — закрыто сегодня, а на доске статус "
                f"«{esc(t['status']) or 'не задан'}» ({esc(t['project_title'])}, {link(t)})")
    for t in all_items:
        if t["bucket"] == "done" and t["state"] == "OPEN" and t.get("number"):
            attention.append(
                f"**{cut(t['title'], 70)}** — на доске «готово», но issue открыт "
                f"({esc(t['project_title'])}, {link(t)})")
    orphan = [b for b in boards if b["total"] == 0]
    for b in orphan:
        attention.append(f"**{esc(b['title'])}** — доска пуста (`{b['owner']}/{b['number']}`)")

    local = local_state(PROJECTS_ROOT) if with_local else None

    return {
        "day": day,
        "generated": generated,
        "start": start,
        "end": end,
        "owners": owners,
        "project_count": len(projects),
        "task_total": len(all_items),
        "boards": boards,
        "tasks": {"added": added, "done": done, "wip": wip},
        "repos": {**repo_stats, "active": active},
        "outside": outside,
        "attention": attention,
        "local": local,
    }


def write_outputs(ctx: dict, out_dir: Path) -> tuple[Path, Path]:
    year_dir = out_dir / ctx["day"][:4]
    year_dir.mkdir(parents=True, exist_ok=True)
    md_path = year_dir / f"{ctx['day']}.md"
    json_path = year_dir / f"{ctx['day']}.json"

    md_path.write_text(render_md(ctx), encoding="utf-8")

    snapshot = {
        "date": ctx["day"],
        "generated_at": ctx["generated"].isoformat(),
        "window": {"start": ctx["start"].isoformat(), "end": ctx["end"].isoformat()},
        "coverage": {
            "owners": ctx["owners"],
            "repos_total": ctx["repos"]["total"],
            "repos_archived": ctx["repos"]["archived"],
            "projects": ctx["project_count"],
            "tasks_total": ctx["task_total"],
        },
        "summary": {
            "added": len(ctx["tasks"]["added"]),
            "done": len(ctx["tasks"]["done"]),
            "in_progress": len(ctx["tasks"]["wip"]),
            "commits": ctx["repos"]["commit_total"],
            "repos_active": len(ctx["repos"]["active"]),
            "issues_new": ctx["repos"]["issue_new"],
            "issues_closed": ctx["repos"]["issue_closed"],
            "pr_open": ctx["repos"]["pr_open"],
            "pr_merged": ctx["repos"]["pr_merged"],
            "attention": len(ctx["attention"]),
        },
        "boards": ctx["boards"],
        "tasks": ctx["tasks"],
        "repos_active": ctx["repos"]["active"],
        "issues_outside_boards": ctx["outside"],
        "attention": ctx["attention"],
        "local_debt": ctx.get("local"),
    }
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1), encoding="utf-8")

    render_index(out_dir)
    latest = out_dir / "latest.md"
    try:
        if latest.is_symlink() or latest.exists():
            latest.unlink()
        latest.symlink_to(md_path.relative_to(out_dir))
    except OSError:
        pass
    return md_path, json_path


def render_index(out_dir: Path) -> None:
    rows = []
    for f in sorted(out_dir.glob("*/*.json"), reverse=True):
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        sm = s.get("summary") or {}
        rows.append((s.get("date", f.stem), sm))
    lines = [
        "# Отчёты по дням",
        "",
        "Один файл на день: `reports/ГГГГ/ГГГГ-ММ-ДД.md` + машинный снимок `.json`.",
        "Свежий отчёт всегда доступен как `reports/latest.md`.",
        "",
        "Собирается скриптом `../daily_report.py` (см. `README.md` в этой папке).",
        "",
        "| День | Добавлено | Выполнено | В работе | Коммитов | Активных репо | Внимание |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for day, sm in rows:
        lines.append(
            f"| [{day}]({day[:4]}/{day}.md) | {sm.get('added', 0)} | {sm.get('done', 0)} "
            f"| {sm.get('in_progress', 0)} | {sm.get('commits', 0)} "
            f"| {sm.get('repos_active', 0)} | {sm.get('attention', 0)} |")
    if not rows:
        lines.append("| — | | | | | | |")
    (out_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Ежедневный отчёт по всем репозиториям и доскам")
    ap.add_argument("--date", default=datetime.now(TZ).strftime("%Y-%m-%d"),
                    help="день отчёта, ГГГГ-ММ-ДД (по умолчанию сегодня, MSK)")
    ap.add_argument("--out", default=str(SCRIPT_DIR / "reports"), help="куда писать отчёты")
    ap.add_argument("--no-repos", action="store_true", help="не обходить репозитории")
    ap.add_argument("--local", action="store_true", help="добавить локальные долги ~/Projects")
    args = ap.parse_args()

    if not os.environ.get("PATH", "").startswith("/opt/homebrew/bin"):
        os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")

    ctx = build(args.date, not args.no_repos, args.local, OWNERS)
    md, js = write_outputs(ctx, Path(args.out))
    t = ctx["tasks"]
    print(f"{args.date}: добавлено {len(t['added'])}, выполнено {len(t['done'])}, "
          f"в работе {len(t['wip'])}, коммитов {ctx['repos']['commit_total']}, "
          f"внимание {len(ctx['attention'])}")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
