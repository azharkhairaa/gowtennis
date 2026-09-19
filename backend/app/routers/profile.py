"""Endpoint profil klub. Membaca data/profile.json sebagai sumber tunggal."""
import json

from fastapi import APIRouter, HTTPException

from ..config import DATA_DIR

router = APIRouter(tags=["profil"])


def _load() -> dict:
    path = DATA_DIR / "profile.json"
    if not path.exists():
        raise HTTPException(status_code=500, detail="profile.json tidak ditemukan")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@router.get("/profile", summary="Profil lengkap Gow! Tennis")
async def get_profile() -> dict:
    return _load()


@router.get("/programs", summary="Daftar program & harga")
async def get_programs() -> dict:
    data = _load()
    return {"jumlah": len(data["program"]), "items": data["program"]}


@router.get("/stats", summary="Ringkasan angka untuk hero section")
async def get_stats() -> dict:
    data = _load()
    sosial = data["sosial"]
    return {
        "instagram_followers": sosial["instagram"]["followers"],
        "tiktok_followers": sosial["tiktok"]["followers"],
        "tiktok_likes": sosial["tiktok"]["likes"],
        "total_followers": sosial["total_followers"],
        "jumlah_program": len(data["program"]),
        "jumlah_venue": len(data["venue"]),
        "per_tanggal": data["meta"]["tanggal_riset"],
    }
