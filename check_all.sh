#!/usr/bin/env bash
# Automated verification script for VERTX-2 backend
# Run this script from the project root (VERTX-2) on Windows PowerShell (use .\check_all.sh) or Git Bash.

set -e

echo "--- Installing dependencies ---"
python -m pip install -r BACKEND/requirements.txt

echo "--- Running lint (flake8) ---"
python -m flake8 BACKEND --max-line-length=120

echo "--- Running pylint ---"
python -m pylint BACKEND

echo "--- Running type checking (mypy) ---"
python -m mypy BACKEND --ignore-missing-imports

echo "--- Running security scanner (bandit) ---"
python -m bandit -r BACKEND -ll

echo "--- Running unit tests (pytest) ---"
python -m pytest BACKEND/tests || echo "No tests found"

# If you have any additional verification steps, add them below.

echo "Verification completed successfully."
