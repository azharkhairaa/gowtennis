"""Perakit feed sosial: pilih sumber, gabung, urutkan, dan cache."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

import httpx

from ..cache import cache
from ..config import Settings
from ..models import FeedItem, FeedResponse
from . import instagram, tiktok

CACHE_KEY = "social_feed"


def load_feed_config(data_dir: Path) -> dict:
    with open(data_dir / "social_feed.json", encoding="utf-8") as fh:
        return json.load(fh)


def _sort_items(items: List[FeedItem]) -> List[FeedItem]:
    """Unggulan dulu, lalu yang paling baru.

    Dikerjakan dua tahap karena kunci urutnya berlawanan arah: tanggal menurun
    tapi flag unggulan menaik. Sort Python stabil, jadi tahap kedua tidak
    merusak urutan tanggal yang sudah terbentuk di tahap pertama.
    Item tanpa tanggal ("") otomatis jatuh ke belakang saat reverse=True.
    """
    per_tanggal = sorted(items, key=lambda i: i.tanggal or "", reverse=True)
    return sorted(per_tanggal, key=lambda i: not i.unggulan)


async def build_feed(settings: Settings, data_dir: Path) -> FeedResponse:
    cached, hit = cache.get(CACHE_KEY)
    if hit and cached is not None:
        return cached.model_copy(update={"cache_hit": True})

    config = load_feed_config(data_dir)
    peringatan: List[str] = []
    items: List[FeedItem] = []
    mode = settings.feed_mode
    sumber_bagian: List[str] = []

    # --- Instagram ---
    ig_entries = config.get("instagram", [])
    if mode == "api" and settings.instagram_api_ready:
        try:
            ig_items = await instagram.fetch_api_items(
                user_id=settings.ig_user_id,
                access_token=settings.ig_access_token,
                graph_version=settings.ig_graph_version,
                limit=settings.feed_limit,
            )
            items.extend(ig_items)
            sumber_bagian.append("Instagram Graph API")
        except httpx.HTTPError as exc:
            # Token kedaluwarsa atau API bermasalah: jangan matikan halaman,
            # turunkan saja ke daftar kurasi.
            peringatan.append(
                f"Instagram Graph API gagal ({exc.__class__.__name__}), "
                "dipakai daftar kurasi sebagai cadangan."
            )
            items.extend(
                instagram.build_curated_items(ig_entries, settings.feed_limit)
            )
            sumber_bagian.append("Instagram (kurasi, fallback)")
    else:
        if mode == "api" and not settings.instagram_api_ready:
            peringatan.append(
                "FEED_MODE=api tapi IG_USER_ID/IG_ACCESS_TOKEN belum diisi. "
                "Instagram memakai daftar kurasi."
            )
        items.extend(instagram.build_curated_items(ig_entries, settings.feed_limit))
        sumber_bagian.append("Instagram (kurasi + embed resmi)")

    # --- TikTok ---
    # Selalu lewat oEmbed publik. TikTok tidak menyediakan cara resmi untuk
    # mendaftar video sebuah akun tanpa Display API, jadi URL-nya tetap dikurasi.
    tt_entries = config.get("tiktok", [])
    tt_terisi = [e for e in tt_entries if (e.get("url") or "").strip()]
    if tt_terisi:
        tt_items = await tiktok.fetch_oembed_items(tt_terisi, settings.feed_limit)
        items.extend(tt_items)
        sumber_bagian.append("TikTok oEmbed")
    elif tt_entries:
        peringatan.append(
            f"{len(tt_entries)} slot TikTok belum diisi URL-nya di data/social_feed.json, "
            "jadi belum ada video TikTok yang tampil."
        )

    response = FeedResponse(
        mode=mode,
        sumber=" + ".join(sumber_bagian) if sumber_bagian else "tidak ada sumber aktif",
        diperbarui=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        cache_hit=False,
        jumlah=len(items),
        items=_sort_items(items),
        peringatan=peringatan,
    )
    cache.set(CACHE_KEY, response, settings.feed_cache_ttl)
    return response
