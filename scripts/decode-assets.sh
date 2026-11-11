#!/bin/sh
# Decode base64-bundled binary assets (launcher icon) into place.
# Binaries are stored as *.b64 in the repo because the GitHub MCP push path
# is text-only; the APK still ends up with real local files (offline).
set -e
cd "$(dirname "$0")/.."
mkdir -p assets
base64 -d assets-b64/icon.png.b64 > assets/icon.png
echo "decoded assets OK"
