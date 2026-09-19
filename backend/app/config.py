"""Konfigurasi aplikasi, dibaca dari environment variable."""
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    app_name: str = "Gow! Tennis API"
    environment: str = Field(default="development")

    # Asal yang boleh memanggil API dari browser. Dipisah koma di .env.
    cors_origins: str = Field(default="http://localhost:5183,http://127.0.0.1:5183")

    # Mode pengambilan feed sosial:
    #   curated  -> pakai daftar manual di data/social_feed.json (default, tanpa kredensial)
    #   api      -> tarik otomatis dari Instagram Graph API bila token tersedia
    feed_mode: str = Field(default="curated")

    # Berapa lama hasil feed disimpan di cache sebelum diambil ulang (detik).
    feed_cache_ttl: int = Field(default=900)

    # Instagram Graph API. Kosongkan bila belum dipakai; aplikasi tetap jalan
    # dengan mode curated dan tidak akan gagal saat start.
    ig_user_id: Optional[str] = Field(default=None)
    ig_access_token: Optional[str] = Field(default=None)
    ig_graph_version: str = Field(default="v21.0")

    # Batas jumlah item feed yang dikembalikan ke frontend.
    feed_limit: int = Field(default=9)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def instagram_api_ready(self) -> bool:
        return bool(self.ig_user_id and self.ig_access_token)


@lru_cache
def get_settings() -> Settings:
    return Settings()
