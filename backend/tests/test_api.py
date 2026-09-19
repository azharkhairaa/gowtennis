"""Uji endpoint utama tanpa menyentuh jaringan luar."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.cache import cache  # noqa: E402
from app.main import app  # noqa: E402
from app.services import instagram, tiktok  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def bersihkan_cache():
    cache.clear()
    yield
    cache.clear()


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_profile_lengkap():
    r = client.get("/api/profile")
    assert r.status_code == 200
    data = r.json()
    assert data["brand"]["nama"] == "Gow! Tennis"
    assert data["brand"]["kota"] == "Bandung"
    assert len(data["program"]) == 3
    # Angka yang dipakai di halaman harus konsisten dengan hasil riset.
    assert data["sosial"]["instagram"]["followers"] == 1516
    assert data["sosial"]["tiktok"]["followers"] == 1963


def test_stats_total_followers_konsisten():
    r = client.get("/api/stats")
    assert r.status_code == 200
    s = r.json()
    assert s["total_followers"] == s["instagram_followers"] + s["tiktok_followers"]


def test_programs():
    r = client.get("/api/programs")
    assert r.status_code == 200
    body = r.json()
    assert body["jumlah"] == 3
    nama = [p["nama"] for p in body["items"]]
    assert "Coaching Session" in nama
    assert "Tennis Malam Minggu" in nama


def test_feed_mode_curated_menghasilkan_embed_instagram():
    r = client.get("/api/social/feed")
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "curated"
    assert body["jumlah"] > 0
    ig = [i for i in body["items"] if i["platform"] == "instagram"]
    # Sengaja dibatasi 3 post terbaru agar halaman ringan.
    assert len(ig) == 3
    # Setiap item harus punya permalink valid dan markup embed resmi.
    for item in ig:
        assert item["url"].startswith("https://www.instagram.com/")
        assert 'class="instagram-media"' in item["embed_html"]
        assert item["id"] in item["embed_html"]


def test_feed_unggulan_tampil_lebih_dulu():
    r = client.get("/api/social/feed")
    items = r.json()["items"]
    unggulan_flags = [i["unggulan"] for i in items]
    # Tidak boleh ada item unggulan yang muncul setelah item biasa.
    assert unggulan_flags == sorted(unggulan_flags, reverse=True)


def test_feed_memperingatkan_slot_tiktok_kosong():
    r = client.get("/api/social/feed")
    peringatan = " ".join(r.json()["peringatan"])
    assert "TikTok" in peringatan


def test_feed_cache_bekerja():
    pertama = client.get("/api/social/feed").json()
    kedua = client.get("/api/social/feed").json()
    assert pertama["cache_hit"] is False
    assert kedua["cache_hit"] is True
    # refresh=true harus melewati cache
    ketiga = client.get("/api/social/feed?refresh=true").json()
    assert ketiga["cache_hit"] is False


def test_social_status_jujur_soal_otomatisasi():
    r = client.get("/api/social/status")
    body = r.json()
    # Tanpa kredensial, Instagram tidak boleh diklaim otomatis.
    assert body["instagram"]["otomatis_aktif"] is False
    assert body["tiktok"]["otomatis_aktif"] is False


def test_contact_menghasilkan_tautan_whatsapp():
    r = client.post(
        "/api/contact",
        json={
            "nama": "Azhar",
            "kontak": "081234567890",
            "program": "Coaching Session",
            "pesan": "Mau ikut kelas pemula hari Sabtu.",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    # Nomor 08xx harus dinormalkan ke format internasional 62xx.
    assert body["tindak_lanjut"].startswith("https://wa.me/6282312273282?text=")
    assert "Azhar" in body["tindak_lanjut"]
    assert "Coaching%20Session" in body["tindak_lanjut"]


def test_contact_jatuh_ke_dm_bila_nomor_belum_terkonfirmasi(tmp_path, monkeypatch):
    """Kalau nomor ditandai perlu konfirmasi, jangan kirim orang ke nomor salah."""
    import json as _json

    from app import config

    asli = config.DATA_DIR / "profile.json"
    data = _json.loads(asli.read_text(encoding="utf-8"))
    data["kontak"]["whatsapp_perlu_konfirmasi"] = True
    (tmp_path / "profile.json").write_text(
        _json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )

    from app.routers import contact as contact_router

    monkeypatch.setattr(contact_router, "DATA_DIR", tmp_path)
    r = client.post(
        "/api/contact",
        json={"nama": "Budi", "kontak": "081234567890", "pesan": "Mau coba kelas."},
    )
    assert r.status_code == 200
    assert "instagram.com" in r.json()["tindak_lanjut"]


def test_contact_menolak_input_kosong():
    r = client.post("/api/contact", json={"nama": "A", "kontak": "x", "pesan": ""})
    assert r.status_code == 422


def test_ekstraksi_id_video_tiktok():
    url = "https://www.tiktok.com/@gowtennis/video/7381360530369432838"
    assert tiktok.extract_video_id(url) == "7381360530369432838"
    assert tiktok.extract_video_id("https://www.tiktok.com/@gowtennis") is None


def test_curated_instagram_menghormati_limit():
    entries = [{"shortcode": f"AAA{i}", "tipe": "p"} for i in range(20)]
    hasil = instagram.build_curated_items(entries, limit=5)
    assert len(hasil) == 5


def test_curated_instagram_melewati_entry_tanpa_shortcode():
    entries = [{"tipe": "p"}, {"shortcode": "OK1", "tipe": "reel"}]
    hasil = instagram.build_curated_items(entries, limit=10)
    assert len(hasil) == 1
    assert hasil[0].url == "https://www.instagram.com/reel/OK1/"


def test_feed_urut_terbaru_dulu_dalam_tiap_grup():
    """Dalam grup unggulan maupun non-unggulan, post terbaru harus di atas."""
    items = client.get("/api/social/feed").json()["items"]
    unggulan = [i["tanggal"] for i in items if i["unggulan"]]
    biasa = [i["tanggal"] for i in items if not i["unggulan"]]
    assert unggulan == sorted(unggulan, reverse=True)
    assert biasa == sorted(biasa, reverse=True)
    # Post paling baru harus jadi item pertama halaman.
    assert items[0]["tanggal"] == "2026-09-15"


def test_feed_item_tanpa_tanggal_jatuh_ke_belakang():
    from app.models import FeedItem
    from app.services.feed import _sort_items

    hasil = _sort_items([
        FeedItem(platform="tiktok", id="1", url="u1"),
        FeedItem(platform="instagram", id="2", url="u2", tanggal="2026-01-01"),
    ])
    assert hasil[0].id == "2"
    assert hasil[1].id == "1"
