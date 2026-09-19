"""Endpoint form kontak.

Sengaja belum mengirim email atau menulis ke database. Yang dilakukan sekarang
hanya memvalidasi input dan mengembalikan tautan WhatsApp/DM yang sudah terisi,
supaya pendaftaran tetap mengalir ke kanal yang memang dipakai klub. Kalau nanti
mau disimpan, tinggal tambahkan penyimpanan di sini.
"""
import json
from urllib.parse import quote

from fastapi import APIRouter

from ..config import DATA_DIR
from ..models import KontakRequest, KontakResponse

router = APIRouter(tags=["kontak"])


@router.post("/contact", response_model=KontakResponse, summary="Kirim pesan pendaftaran")
async def kirim_kontak(payload: KontakRequest) -> KontakResponse:
    with open(DATA_DIR / "profile.json", encoding="utf-8") as fh:
        profil = json.load(fh)

    program = payload.program or "Coaching Session"
    teks = (
        f"Halo Gow! Tennis, saya {payload.nama}. "
        f"Saya tertarik ikut {program}. "
        f"{payload.pesan} "
        f"(Kontak saya: {payload.kontak})"
    )

    wa = profil["kontak"].get("whatsapp_admin", "")
    wa_digits = "".join(ch for ch in wa if ch.isdigit())
    perlu_konfirmasi = profil["kontak"].get("whatsapp_perlu_konfirmasi", False)

    if wa_digits and not perlu_konfirmasi:
        # Format internasional: 08xx -> 628xx
        nomor = "62" + wa_digits[1:] if wa_digits.startswith("0") else wa_digits
        tindak_lanjut = f"https://wa.me/{nomor}?text={quote(teks)}"
    else:
        tindak_lanjut = profil["kontak"]["instagram_dm"]

    return KontakResponse(
        ok=True,
        pesan=f"Terima kasih {payload.nama}, pesanmu sudah siap dikirim.",
        tindak_lanjut=tindak_lanjut,
    )
