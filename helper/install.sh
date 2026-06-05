#!/bin/bash
# Install the Better Habits desktop helper as a per-user launch agent.
# No sudo needed. The helper lets the app shut this Mac down + schedule it.
#
# Note: we install into ~/Library/Application Support (NOT ~/Documents), because
# macOS privacy protection (TCC) blocks launchd background processes from reading
# ~/Documents — they'd fail with "Operation not permitted".
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"           # repo root (has the web assets)
APPDIR="$HOME/Library/Application Support/BetterHabits"
PLIST="$HOME/Library/LaunchAgents/com.betterhabits.helper.plist"

mkdir -p "$APPDIR/vendor" "$APPDIR/icons" "$HOME/Library/LaunchAgents"

# helper + the web assets it serves on http://localhost:7421
cp "$SRC/helper/habits-helper.py" "$APPDIR/"
cp "$SRC/index.html" "$SRC/manifest.json" "$SRC/sw.js" "$SRC/apple-touch-icon.png" "$APPDIR/" 2>/dev/null || true
cp "$SRC/vendor/"* "$APPDIR/vendor/" 2>/dev/null || true
cp "$SRC/icons/"*  "$APPDIR/icons/"  2>/dev/null || true

cp "$SRC/helper/com.betterhabits.helper.plist" "$PLIST"
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
sleep 1

echo ""
if curl -s -o /dev/null http://127.0.0.1:7421/status; then
  echo "✓ Helper installed and running (http://localhost:7421)."
else
  echo "⚠ Installed, but not responding yet — check: cat /tmp/betterhabits-helper.err"
fi
echo ""
echo "Pairing token (paste into the app → Wind-down → Connect helper):"
echo ""
echo "    $(cat "$HOME/.better-habits-helper-token" 2>/dev/null)"
echo ""
echo "Tip: on this Mac you can also open  http://localhost:7421  to get the app"
echo "     with shutdown controls already wired up. Re-run this script after you"
echo "     update the app to refresh that local copy."
