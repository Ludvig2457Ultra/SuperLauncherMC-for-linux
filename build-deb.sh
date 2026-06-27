#!/usr/bin/env bash
# Build helper for Debian/Ubuntu/Linux Mint
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEB_DIR="$ROOT_DIR/debian"

echo "==> Building Debian package for SuperLauncher"
echo "    (Ubuntu / Debian / Linux Mint)"

# Ensure the .desktop file is in the debian dir
cp "$ROOT_DIR/superlauncher.desktop" "$DEB_DIR/superlauncher.desktop"

# Build the package
dpkg-buildpackage -us -uc -b

echo ""
echo "==> Done! Debian packages are in: $ROOT_DIR/.."
echo ""
ls -lh "$ROOT_DIR/../"*.deb 2>/dev/null || echo "(no .deb files found)"
