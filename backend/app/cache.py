"""Cache in-memory sederhana dengan TTL.

Dipakai supaya panggilan ke Instagram/TikTok tidak diulang setiap kali halaman
dibuka. Untuk satu proses uvicorn ini sudah cukup; kalau nanti jalan multi-worker
atau multi-instance, ganti isinya dengan Redis tanpa mengubah pemanggilnya.
"""
import threading
import time
from typing import Any, Optional, Tuple


class TTLCache:
    def __init__(self) -> None:
        self._store: dict = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Tuple[Optional[Any], bool]:
        """Kembalikan (nilai, hit). hit=False bila kosong atau sudah kedaluwarsa."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None, False
            value, expires_at = entry
            if time.time() > expires_at:
                self._store.pop(key, None)
                return None, False
            return value, True

    def set(self, key: str, value: Any, ttl: int) -> None:
        with self._lock:
            self._store[key] = (value, time.time() + ttl)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()


cache = TTLCache()
