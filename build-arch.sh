#!/usr/bin/env bash
# Build helper for Arch Linux
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Building Arch Linux package for SuperLauncher"

if ! command -v makepkg &>/dev/null; then
    echo "ERROR: makepkg not found. Are you on Arch Linux?"
    exit 1
fi

cd "$ROOT_DIR"
makepkg -si

echo ""
echo "==> Done! Installed superlauncher"
