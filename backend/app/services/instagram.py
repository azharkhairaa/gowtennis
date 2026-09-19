"""Sumber data Instagram.

Dua jalur yang disediakan:

1. ``build_curated_items`` - tanpa kredensial apa pun. Kita hanya menyusun
   permalink dan markup blockquote resmi Instagram dari daftar shortcode yang
   dikurasi manual. Script embed.js milik Instagram yang akan merender isinya
   di sisi browser.

2. ``fetch_api_items`` - menarik media otomatis lewat Instagram Graph API.
   Membutuhkan akun Professional (Business/Creator) dan access token.
   Instagram Basic Display API sudah dimatikan sejak 4 Desember 2024 dan
   tidak lagi melayani akun personal, jadi jalur inilah satu-satunya cara
   resmi untuk menarik media sendiri secara otomatis.
"""
from typing import List, Optional

import httpx

from ..models import FeedItem

PERMALINK = "https://www.instagram.com/{tipe}/{shortcode}/"


def _blockquote(url: str) -> str:
    """Markup embed resmi Instagram.

    Dirender oleh https://www.instagram.com/embed.js di sisi klien. Tidak butuh
    token, tapi setiap post harus didaftarkan satu per satu.
    """
    return (
        '<blockquote class="instagram-media" '
        f'data-instgrm-permalink="{url}" '
        'data-instgrm-version="14" '
        'style="max-width:540px;min-width:280px;width:100%;margin:0;">'
        f'<a href="{url}" target="_blank" rel="noopener noreferrer">Lihat di Instagram</a>'
        "</blockquote>"
    )


def build_curated_items(entries: List[dict], limit: int) -> List[FeedItem]:
    items: List[FeedItem] = []
    for entry in entries[:limit]:
        shortcode = entry.get("shortcode")
        if not shortcode:
            continue
        tipe = entry.get("tipe", "p")
        url = PERMALINK.format(tipe=tipe, shortcode=shortcode)
        items.append(
            FeedItem(
                platform="instagram",
                id=shortcode,
                url=url,
                judul=entry.get("judul"),
                tanggal=entry.get("tanggal"),
                tipe=tipe,
                embed_html=_blockquote(url),
                unggulan=bool(entry.get("unggulan")),
            )
        )
    return items


async def fetch_api_items(
    user_id: str,
    access_token: str,
    graph_version: str,
    limit: int,
    timeout: float = 10.0,
) -> List[FeedItem]:
    """Tarik media terbaru lewat Instagram Graph API.

    Melempar httpx.HTTPError bila gagal; pemanggil yang memutuskan fallback.
    """
    url = f"https://graph.instagram.com/{graph_version}/{user_id}/media"
    params = {
        "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp",
        "limit": str(limit),
        "access_token": access_token,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()

    items: List[FeedItem] = []
    for media in payload.get("data", [])[:limit]:
        media_type = media.get("media_type", "")
        # VIDEO punya thumbnail_url; IMAGE/CAROUSEL_ALBUM pakai media_url.
        thumbnail: Optional[str] = media.get("thumbnail_url") or media.get("media_url")
        caption = (media.get("caption") or "").strip()
        judul = caption.split("\n")[0][:120] if caption else None
        items.append(
            FeedItem(
                platform="instagram",
                id=str(media.get("id")),
                url=media.get("permalink", ""),
                judul=judul,
                tanggal=(media.get("timestamp") or "")[:10] or None,
                tipe="reel" if media_type == "VIDEO" else "p",
                thumbnail=thumbnail,
                embed_html=_blockquote(media.get("permalink", "")),
            )
        )
    return items
