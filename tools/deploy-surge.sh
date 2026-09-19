#!/usr/bin/env bash
# Bangun versi statis lalu unggah ke Surge.sh.
#
# Dijalankan oleh kamu sendiri, bukan otomatis — Surge minta login sekali
# (email + password) pada pemakaian pertama.
#
# Pakai:
#   ./tools/deploy-surge.sh                    # pakai domain default
#   ./tools/deploy-surge.sh nama-lain.surge.sh # pakai domain sendiri
#
set -euo pipefail

DOMAIN="${1:-gowtennis.surge.sh}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/backend/.venv/bin/python"

if [ ! -x "$PY" ]; then
  echo "Virtualenv backend belum ada. Jalankan dulu:" >&2
  echo "  cd $ROOT/backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

echo "==> 1/3  Pre-render data jadi JSON statis"
"$PY" "$ROOT/tools/buat_static.py"

echo
echo "==> 2/3  Build frontend (mode statis)"
cd "$ROOT/frontend"
[ -d node_modules ] || npm install
npm run build:static

echo
echo "==> 3/3  Unggah ke Surge: https://$DOMAIN"
echo "         (kalau ini pertama kali, Surge akan minta email & password)"
npx --yes surge "$ROOT/frontend/dist" "$DOMAIN"

echo
echo "Selesai. Buka: https://$DOMAIN"
