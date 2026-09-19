"""Endpoint feed sosial."""
from fastapi import APIRouter, Depends, Query

from ..cache import cache
from ..config import DATA_DIR, Settings, get_settings
from ..models import FeedResponse
from ..services.feed import build_feed

router = APIRouter(tags=["sosial"])


@router.get("/social/feed", response_model=FeedResponse, summary="Feed Instagram + TikTok")
async def social_feed(
    refresh: bool = Query(default=False, description="Abaikan cache dan tarik ulang"),
    settings: Settings = Depends(get_settings),
) -> FeedResponse:
    if refresh:
        cache.clear()
    return await build_feed(settings, DATA_DIR)


@router.get("/social/status", summary="Kesiapan integrasi tiap platform")
async def social_status(settings: Settings = Depends(get_settings)) -> dict:
    """Ringkasan jujur soal apa yang sudah otomatis dan apa yang masih manual."""
    return {
        "feed_mode": settings.feed_mode,
        "instagram": {
            "otomatis_aktif": settings.feed_mode == "api" and settings.instagram_api_ready,
            "kredensial_lengkap": settings.instagram_api_ready,
            "syarat": "Akun Professional (Business/Creator) + Meta App + access token",
            "catatan": (
                "Instagram Basic Display API dimatikan 4 Desember 2024. "
                "Jalur resmi yang tersisa adalah Instagram Graph API / "
                "Instagram API with Instagram Login."
            ),
        },
        "tiktok": {
            "otomatis_aktif": False,
            "syarat": "URL video dikurasi manual, metadata diambil via oEmbed publik",
            "catatan": (
                "oEmbed tidak butuh API key tapi hanya menerjemahkan satu URL. "
                "Untuk daftar video otomatis butuh TikTok Display API (Login Kit) "
                "yang perlu persetujuan TikTok."
            ),
        },
        "cache_ttl_detik": settings.feed_cache_ttl,
    }
