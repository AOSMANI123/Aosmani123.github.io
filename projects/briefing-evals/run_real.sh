#!/usr/bin/env bash
# One real run of the cost and routing comparison. Costs about $1, never more than $2.
# Your API key is typed into this window, kept in memory for this run only, and never saved.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 isn't installed. Install it from python.org, then run this again."
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Setting up Python (first time only)..."
  python3 -m venv .venv
fi
.venv/bin/pip install --quiet --upgrade pip anthropic

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  read -r -s -p "Paste your Anthropic API key and press Return (it won't show on screen): " ANTHROPIC_API_KEY
  echo
  export ANTHROPIC_API_KEY
fi

.venv/bin/python real_run.py "$@"
