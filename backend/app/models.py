"""Skema respons API. Dipakai FastAPI untuk validasi sekaligus dokumentasi OpenAPI."""
from typing import List, Optional

from pydantic import BaseModel, Field


class TarifLapangan(BaseModel):
    """Rincian biaya kelas privat per lapangan.

    Coaching dan sewa lapangan ditagih terpisah, jadi keduanya disimpan apa
    adanya berikut totalnya supaya tidak perlu dihitung ulang di tiap tampilan.
    """

    lapangan: str
    sewa_lapangan: str
    coaching: str
    total: str


class Tambahan(BaseModel):
    nama: str
    harga: str
    keterangan: Optional[str] = None


class Program(BaseModel):
    nama: str
    level: Optional[str] = None
    hari: Optional[str] = None
    lokasi: Optional[str] = None
    jadwal: Optional[str] = None
    durasi: Optional[str] = None
    kapasitas: Optional[str] = None
    harga: Optional[str] = None
    termasuk: List[str] = Field(default_factory=list)
    belum_termasuk: List[str] = Field(default_factory=list)
    tarif_lapangan: List[TarifLapangan] = Field(default_factory=list)
    tambahan: List[Tambahan] = Field(default_factory=list)
    catatan: Optional[str] = None


class Nilai(BaseModel):
    judul: str
    isi: str


class Venue(BaseModel):
    nama: str
    tipe: Optional[str] = None
    kota: str
    dipakai_untuk: str


class Brand(BaseModel):
    nama: str
    handle: str
    tagline: str
    kategori: str
    kota: str
    negara: str
    deskripsi_singkat: str
    deskripsi_panjang: str


class Profile(BaseModel):
    brand: Brand
    nilai: List[Nilai]
    program: List[Program]
    venue: List[Venue]
    sosial: dict
    kontak: dict
    konten: dict


class FeedItem(BaseModel):
    """Satu kartu di galeri sosial pada landing page."""

    platform: str = Field(description="instagram atau tiktok")
    id: str = Field(description="shortcode Instagram atau id video TikTok")
    url: str
    judul: Optional[str] = None
    tanggal: Optional[str] = None
    tipe: Optional[str] = Field(default=None, description="reel, p, atau video")
    thumbnail: Optional[str] = Field(
        default=None,
        description="Hanya terisi untuk TikTok (via oEmbed) atau Instagram Graph API.",
    )
    embed_html: Optional[str] = Field(
        default=None, description="Markup embed resmi, bila penyedia menyediakannya."
    )
    unggulan: bool = False


class FeedResponse(BaseModel):
    mode: str = Field(description="curated atau api")
    sumber: str = Field(description="Penjelasan singkat dari mana data ini berasal")
    diperbarui: str
    cache_hit: bool = False
    jumlah: int
    items: List[FeedItem]
    peringatan: List[str] = Field(default_factory=list)


class KontakRequest(BaseModel):
    nama: str = Field(min_length=2, max_length=80)
    kontak: str = Field(min_length=5, max_length=120, description="Nomor WA atau email")
    program: Optional[str] = Field(default=None, max_length=80)
    pesan: str = Field(min_length=5, max_length=1000)


class KontakResponse(BaseModel):
    ok: bool
    pesan: str
    tindak_lanjut: str
