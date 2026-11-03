#!/bin/bash
# Ежедневный отчёт по всем репозиториям и доскам — обёртка для launchd.
# Собирает отчёт, коммитит его в repo-catalog и пушит. Лог — $HOME/.local/share/daily-report/run.log
set -u

export PATH="/opt/homebrew/bin:$PATH"
REPO="$HOME/Projects/repo-catalog"
STATE="$HOME/.local/share/daily-report"
mkdir -p "$STATE"

# защита от наложения прогонов
if ! mkdir "$STATE/lock" 2>/dev/null; then
  echo "$(date '+%F %T') предыдущий прогон ещё идёт, выходим" >>"$STATE/run.log"
  exit 0
fi
trap 'rmdir "$STATE/lock" 2>/dev/null' EXIT

exec >>"$STATE/run.log" 2>&1
echo "=== $(date '+%F %T') ==="
cd "$REPO" || { echo "нет $REPO"; exit 1; }

git pull --rebase --quiet || echo "pull не удался — работаем с тем, что есть"
/usr/bin/python3 daily_report.py --local || { echo "сборка упала"; exit 1; }

if [ -n "$(git status --porcelain reports/ 2>/dev/null)" ]; then
  git add reports/
  git -c commit.gpgsign=false commit -q -m "reports: $(date +%F)" || echo "коммит не удался"
  git push --quiet || { echo "push не удался, пробую pull --rebase"; git pull --rebase --quiet && git push --quiet; }
else
  echo "изменений в reports/ нет"
fi

echo "готово: $(date '+%F %T')"
