#!/usr/bin/env bash
# Installs the lab walkthrough extension. Runs on every editor attach; safe to repeat.
DIR="$(cd "$(dirname "$0")" && pwd)"
VSIX="$DIR/race-condition-walkthrough-0.0.2.vsix"

CODE="$(command -v code || true)"
if [ -z "$CODE" ]; then
  CODE="$(find /vscode -path '*remote-cli/code' -type f 2>/dev/null | head -1)"
fi
if [ -z "$CODE" ]; then
  CODE="$(find /vscode -name code-server -type f 2>/dev/null | head -1)"
fi
if [ -z "$CODE" ]; then
  echo "Could not find the VS Code CLI; install the .vsix manually." >&2
  exit 0
fi

if "$CODE" --list-extensions 2>/dev/null | grep -qi 'race-condition-lab.race-condition-walkthrough'; then
  echo "Walkthrough extension already installed."
else
  "$CODE" --install-extension "$VSIX" --force
fi
