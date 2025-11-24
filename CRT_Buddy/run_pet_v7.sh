#!/usr/bin/env zsh
# Launch pet_window_v7 directly with ensured venv
set -e
PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
VENV_DIR="$PROJECT_DIR/.venv312"
PYTHON_BIN="/opt/homebrew/bin/python3.12"
REQ_FILE="$PROJECT_DIR/requirements.txt"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "[ERROR] python3.12 not found at $PYTHON_BIN. brew install python@3.12" >&2
  exit 1
fi
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO] Creating venv (3.12) ..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
if ! python -c "import PyQt6" 2>/dev/null; then
  echo "[INFO] Installing dependencies ..."
  python -m pip install --upgrade pip >/dev/null
  python -m pip install -r "$REQ_FILE"
fi
echo "[INFO] Running pet_window_v7 ..."
exec python "$PROJECT_DIR/core/pet_window_v7.py"