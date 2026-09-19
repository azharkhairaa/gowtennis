#!/usr/bin/env python3
"""Pre-render semua endpoint GET jadi berkas JSON statis.

Surge.sh (dan static host mana pun) tidak menjalankan Python, jadi FastAPI tidak
bisa ikut ke sana. Tapi seluruh data situs ini sebenarnya statis: profil, program,
dan daftar post sosial semuanya berasal dari berkas JSON yang tidak berubah antar
permintaan.

Skrip ini memanggil aplikasi FastAPI di dalam proses (lewat TestClient, tanpa
menyalakan server) lalu menuliskan responsnya sebagai berkas .json di
frontend/public/api/. Hasilnya: frontend yang sama bisa jalan tanpa backend,
memakai logika yang persis sama karena datanya memang dihasilkan backend.

Jalankan:
    python3 tools/buat_static.py
Lalu:
    cd frontend && npm run build:static
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
TUJUAN = ROOT / "frontend" / "public" / "api"

# path endpoint -> nama berkas relatif (tanpa .json)
ENDPOINT = {
    "/api/profile": "profile",
    "/api/programs": "programs",
    "/api/stats": "stats",
    "/api/social/feed": "social/feed",
    "/api/social/status": "social/status",
    "/api/health": "health",
}


def main() -> int:
    sys.path.insert(0, str(BACKEND))
    try:
        from fastapi.testclient import TestClient

        from app.cache import cache
        from app.main import app
    except ImportError as exc:
        print(
            f"Gagal mengimpor backend: {exc}\n"
            f"Pastikan dependensi terpasang:\n"
            f"  cd {BACKEND} && .venv/bin/pip install -r requirements.txt\n"
            f"lalu jalankan skrip ini dengan interpreter venv:\n"
            f"  {BACKEND}/.venv/bin/python tools/buat_static.py",
            file=sys.stderr,
        )
        return 1

    cache.clear()
    client = TestClient(app)

    if TUJUAN.exists():
        shutil.rmtree(TUJUAN)
    TUJUAN.mkdir(parents=True)

    gagal = 0
    for path, nama in ENDPOINT.items():
        resp = client.get(path)
        if resp.status_code != 200:
            print(f"  GAGAL {path} -> HTTP {resp.status_code}", file=sys.stderr)
            gagal += 1
            continue
        data = resp.json()

        # cache_hit tidak punya arti pada berkas statis; buang supaya tidak
        # menyesatkan siapa pun yang membaca responsnya.
        if isinstance(data, dict) and "cache_hit" in data:
            data.pop("cache_hit")
            data["sumber"] = data.get("sumber", "") + " (snapshot statis)"

        berkas = TUJUAN / f"{nama}.json"
        berkas.parent.mkdir(parents=True, exist_ok=True)
        berkas.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  {path:24} -> public/api/{nama}.json  ({berkas.stat().st_size:,} bytes)")

    if gagal:
        print(f"\n{gagal} endpoint gagal.", file=sys.stderr)
        return 1

    print(f"\nSelesai. {len(ENDPOINT)} berkas ditulis ke {TUJUAN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
