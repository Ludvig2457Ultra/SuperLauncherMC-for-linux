#!/usr/bin/env bash
# Auto-sync: watches the project directory and pushes changes to GitHub
set -euo pipefail

PROJECT_DIR="/home/artem/Downloads/SuperLauncher 2.0 Linux"
GIT_SSH="ssh -i /home/artem/.ssh/github -o StrictHostKeyChecking=no"

cd "$PROJECT_DIR"

# Ignored patterns (relative to project dir)
IGNORE_PATTERNS="__pycache__|*.pyc|logs/|temp/|mods_cache/|build/|dist/|.git/"

inotifywait -m -r -e modify,create,delete,move --format '%e %w%f' "$PROJECT_DIR" 2>/dev/null |
while read -r event path; do
    # Skip ignored files
    echo "$path" | grep -qE "$IGNORE_PATTERNS" && continue

    # Debounce: wait 3 seconds after last change
    LAST_TS=$(date +%s)
    sleep 3

    # Check if another change happened during sleep
    CURRENT_TS=$(date +%s)
    if [ $((CURRENT_TS - LAST_TS)) -lt 3 ]; then
        continue
    fi

    # Check if there's anything to commit
    if GIT_SSH_COMMAND="$GIT_SSH" git status --porcelain | grep -q .; then
        echo "[auto-sync] $(date): Changes detected, committing..."
        GIT_SSH_COMMAND="$GIT_SSH" git add -A
        GIT_SSH_COMMAND="$GIT_SSH" git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null || true
        GIT_SSH_COMMAND="$GIT_SSH" git pull --rebase origin main 2>/dev/null || true
        GIT_SSH_COMMAND="$GIT_SSH" git push origin main 2>/dev/null || echo "[auto-sync] Push failed, will retry next change"
        echo "[auto-sync] Done"
    fi
done
