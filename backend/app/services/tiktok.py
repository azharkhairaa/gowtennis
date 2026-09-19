"""Sumber data TikTok lewat oEmbed.

Endpoint https://www.tiktok.com/oembed bersifat publik: tidak perlu API key,
OAuth, maupun cookie, selama videonya publik. Yang dikembalikan antara lain
judul, nama author, thumbnail, dan markup embed siap pakai.

Yang TIDAK bisa dilakukan endpoint ini: mendaftar video milik sebuah akun.
oEmbed hanya menerjemahkan satu URL video yang sudah kita ketahui. Untuk
mendapat daftar video otomatis, diperlukan TikTok Display API (Login Kit)
yang butuh pendaftaran app dan persetujuan TikTok.
"""
import asyncio
import re
from typing import List, Optional

import httpx

from ..models import FeedItem

OEMBED_URL = "https://www.tiktok.com/oembed"
VIDEO_ID_RE = re.compile(r"/video/(\d+)")


def extract_video_id(url: str) -> Optional[str]:
    match = VIDEO_ID_RE.search(url or "")
    return match.group(1) if match else None


async def _fetch_one(
    client: httpx.AsyncClient, entry: dict
) -> Optional[FeedItem]:
    url = (entry.get("url") or "").strip()
    if not url:
        return None

    video_id = extract_video_id(url) or url.rsplit("/", 1)[-1]
    judul_fallback = entry.get("judul")
    unggulan = bool(entry.get("unggulan"))

    try:
        resp = await client.get(OEMBED_URL, params={"url": url})
        resp.raise_for_status()
        data = resp.json()
    except (httpx.HTTPError, ValueError):
        # oEmbed gagal (video privat, dihapus, atau jaringan bermasalah).
        # Tetap tampilkan kartunya dengan data seadanya daripada menghilang.
        return FeedItem(
            platform="tiktok",
            id=video_id,
            url=url,
            judul=judul_fallback,
            tipe="video",
            unggulan=unggulan,
        )

    return FeedItem(
        platform="tiktok",
        id=video_id,
        url=url,
        judul=data.get("title") or judul_fallback,
        tipe="video",
        thumbnail=data.get("thumbnail_url"),
        embed_html=data.get("html"),
        unggulan=unggulan,
    )


async def fetch_oembed_items(
    entries: List[dict], limit: int, timeout: float = 10.0
) -> List[FeedItem]:
    """Resolve beberapa URL TikTok sekaligus lewat oEmbed."""
    usable = [e for e in entries if (e.get("url") or "").strip()][:limit]
    if not usable:
        return []

    async with httpx.AsyncClient(timeout=timeout) as client:
        results = await asyncio.gather(
            *(_fetch_one(client, e) for e in usable), return_exceptions=True
        )

    return [r for r in results if isinstance(r, FeedItem)]
