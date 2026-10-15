#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/pdf-answer-remover-deploy.zip"
cd "$ROOT"
zip -r "$OUT" \
  remove_red_pdf.py web_app.py requirements.txt Dockerfile \
  render.yaml templates DEPLOY.md DEPLOY-NO-CARD.md README.md \
  -x "*.pdf" -x ".venv/*" -x "output/*" -x "__pycache__/*"
echo "Created $OUT"
