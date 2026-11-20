#!/usr/bin/env bash
# landing-factory installer.
#
#   ./install.sh                 skills into ~/.claude/skills (all projects)
#   ./install.sh --project       skills into ./.claude/skills (this project only)
#
# Existing skills with the same name are backed up to <name>.bak.<timestamp> first.
# The templates (brief, architecture, gates, page skeleton) are copied into the landing-factory skill.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude"
while [ $# -gt 0 ]; do
  case "$1" in
    --project) DEST="$(pwd)/.claude" ;;
    -h|--help) sed -n 2,8p "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

mkdir -p "$DEST/skills"
for s in "$HERE"/skills/*/; do
  name="$(basename "$s")"
  if [ -d "$DEST/skills/$name" ]; then
    mv "$DEST/skills/$name" "$DEST/skills/$name.bak.$(date +%s)"
    echo "backed up existing $name"
  fi
  cp -R "$s" "$DEST/skills/$name"
  echo "installed skill $name"
done
mkdir -p "$DEST/skills/landing-factory/templates"
cp -R "$HERE"/templates/. "$DEST/skills/landing-factory/templates/"

command -v python3 >/dev/null || command -v py >/dev/null || \
  echo "note: the scripts need Python 3.9+."
python3 -c "import playwright" 2>/dev/null || python3 -c "import playwright" 2>/dev/null || \
  echo "note: recon.py, shot.py and first_screen.py need Playwright: pip install playwright pillow && python -m playwright install chromium"
echo "done. Try: \"make a landing page like https://example.com for my product\" or \"check the first screen of index.html\""
