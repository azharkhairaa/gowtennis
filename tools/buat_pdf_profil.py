#!/usr/bin/env python3
"""Bangun PDF profil Gow! Tennis dari backend/data/profile.json.

Sumber datanya sama persis dengan yang dipakai website, jadi begitu profile.json
diperbarui, jalankan ulang skrip ini dan PDF ikut menyesuaikan.

Jalankan:
    python3 tools/buat_pdf_profil.py
Hasil:
    docs/Profil-Gow-Tennis.pdf
"""
import json
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "backend" / "data" / "profile.json"
LOGO = ROOT / "tools" / "assets" / "logo-bulat.png"
OUT = ROOT / "docs" / "Profil-Gow-Tennis.pdf"

NAVY = colors.HexColor("#0D2145")
NAVY_DARK = colors.HexColor("#060E1D")
NAVY_MID = colors.HexColor("#1B3A70")
LIME = colors.HexColor("#D7E84B")
INK = colors.HexColor("#0B1B36")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#E2E8F0")
SOFT = colors.HexColor("#F4F6FA")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm


def daftarkan_font() -> tuple:
    """Pakai Arial dari sistem bila ada; kalau tidak, jatuh ke Helvetica."""
    kandidat = {
        "Body": "/System/Library/Fonts/Supplemental/Arial.ttf",
        "Body-Bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "Display": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    }
    if all(Path(p).exists() for p in kandidat.values()):
        for nama, path in kandidat.items():
            pdfmetrics.registerFont(TTFont(nama, path))
        return "Body", "Body-Bold", "Display"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Bold"


F_BODY, F_BOLD, F_DISPLAY = daftarkan_font()

S = {
    "h1": ParagraphStyle(
        "h1", fontName=F_DISPLAY, fontSize=23, leading=27, textColor=NAVY,
        spaceAfter=4,
    ),
    "h2": ParagraphStyle(
        "h2", fontName=F_DISPLAY, fontSize=14, leading=18, textColor=NAVY,
        spaceBefore=13, spaceAfter=6,
    ),
    "h3": ParagraphStyle(
        "h3", fontName=F_BOLD, fontSize=10.5, leading=14, textColor=NAVY,
        spaceAfter=2,
    ),
    "eyebrow": ParagraphStyle(
        "eyebrow", fontName=F_BOLD, fontSize=7.5, leading=10,
        textColor=NAVY_MID, spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "body", fontName=F_BODY, fontSize=9.7, leading=15, textColor=INK,
        alignment=TA_JUSTIFY, spaceAfter=7,
    ),
    "body_left": ParagraphStyle(
        "body_left", fontName=F_BODY, fontSize=9.7, leading=15, textColor=INK,
        alignment=TA_LEFT, spaceAfter=6,
    ),
    "small": ParagraphStyle(
        "small", fontName=F_BODY, fontSize=8.4, leading=12.5, textColor=MUTED,
        alignment=TA_LEFT,
    ),
    "cell": ParagraphStyle(
        "cell", fontName=F_BODY, fontSize=8.7, leading=12.5, textColor=INK,
    ),
    "cell_bold": ParagraphStyle(
        "cell_bold", fontName=F_BOLD, fontSize=8.7, leading=12.5, textColor=NAVY,
    ),
    "cell_head": ParagraphStyle(
        "cell_head", fontName=F_BOLD, fontSize=7.8, leading=11,
        textColor=colors.white,
    ),
}


# ---------------------------------------------------------------- halaman

def gambar_sampul(canvas, doc, d: dict) -> None:
    """Sampul penuh: latar navy, logo, nama, tagline."""
    canvas.saveState()
    canvas.setFillColor(NAVY_DARK)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Marka lapangan tipis sebagai tekstur latar.
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.05))
    canvas.setLineWidth(0.6)
    for i in range(1, 7):
        x = PAGE_W * i / 7
        canvas.line(x, 0, x, PAGE_H)
    for i in range(1, 10):
        y = PAGE_H * i / 10
        canvas.line(0, y, PAGE_W, y)

    # Pita lime di sisi kiri.
    canvas.setFillColor(LIME)
    canvas.rect(0, 0, 7 * mm, PAGE_H, stroke=0, fill=1)

    if LOGO.exists():
        size = 52 * mm
        canvas.drawImage(
            str(LOGO), (PAGE_W - size) / 2, PAGE_H - 108 * mm,
            width=size, height=size, mask="auto",
        )

    brand = d["brand"]
    canvas.setFillColor(colors.white)
    canvas.setFont(F_DISPLAY, 46)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 132 * mm, "GOW!")
    canvas.setFillColor(LIME)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 149 * mm, "TENNIS")

    canvas.setFillColor(colors.white)
    canvas.setFont(F_BOLD, 12.5)
    canvas.drawCentredString(
        PAGE_W / 2, PAGE_H - 163 * mm, f'"{brand["tagline"]}"'
    )

    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.6))
    canvas.setFont(F_BODY, 9.5)
    canvas.drawCentredString(
        PAGE_W / 2, PAGE_H - 174 * mm,
        f'{brand["kategori"].upper()}  ·  {brand["kota"].upper()}, '
        f'{brand["negara"].upper()}',
    )

    # Garis + angka ringkas di bawah.
    sos = d["sosial"]
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.18))
    canvas.setLineWidth(0.8)
    canvas.line(45 * mm, 62 * mm, PAGE_W - 30 * mm, 62 * mm)

    angka = [
        ("INSTAGRAM", f'{sos["instagram"]["followers"]:,}'.replace(",", ".")),
        ("TIKTOK", f'{sos["tiktok"]["followers"]:,}'.replace(",", ".")),
        ("TIKTOK LIKES", "15,4K"),
        ("PROGRAM", str(len(d["program"]))),
    ]
    lebar = (PAGE_W - 75 * mm) / len(angka)
    for i, (label, nilai) in enumerate(angka):
        x = 45 * mm + lebar * i
        canvas.setFillColor(LIME)
        canvas.setFont(F_DISPLAY, 17)
        canvas.drawString(x, 50 * mm, nilai)
        canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.5))
        canvas.setFont(F_BODY, 7)
        canvas.drawString(x, 44 * mm, label)

    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.4))
    canvas.setFont(F_BODY, 7.6)
    canvas.drawCentredString(
        PAGE_W / 2, 22 * mm,
        f'Profil Komunitas  ·  Data per {d["meta"]["tanggal_riset"]}',
    )
    canvas.restoreState()


def gambar_isi(canvas, doc, d: dict) -> None:
    """Header & footer tipis untuk halaman isi."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 13 * mm, PAGE_W, 13 * mm, stroke=0, fill=1)
    canvas.setFillColor(LIME)
    canvas.rect(0, PAGE_H - 13.8 * mm, PAGE_W, 0.8 * mm, stroke=0, fill=1)

    canvas.setFillColor(colors.white)
    canvas.setFont(F_DISPLAY, 9)
    canvas.drawString(MARGIN, PAGE_H - 9 * mm, "GOW! TENNIS")
    canvas.setFont(F_BODY, 7.5)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.65))
    canvas.drawRightString(
        PAGE_W - MARGIN, PAGE_H - 9 * mm, "Profil Komunitas Tenis Bandung"
    )

    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 14 * mm, PAGE_W - MARGIN, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont(F_BODY, 7.5)
    canvas.drawString(MARGIN, 9.5 * mm, "instagram.com/gowtennis  ·  tiktok.com/@gowtennis")
    canvas.drawRightString(PAGE_W - MARGIN, 9.5 * mm, f"Hal. {doc.page - 1}")
    canvas.restoreState()


# ---------------------------------------------------------------- komponen

def kotak_info(judul: str, baris: list, lebar: float) -> Table:
    """Tabel dua kolom label-nilai dengan latar lembut."""
    data = [[Paragraph(judul, S["cell_head"]), ""]]
    for label, nilai in baris:
        data.append(
            [Paragraph(label, S["cell_bold"]), Paragraph(str(nilai), S["cell"])]
        )
    t = Table(data, colWidths=[lebar * 0.32, lebar * 0.68])
    t.setStyle(
        TableStyle([
            ("SPAN", (0, 0), (1, 0)),
            ("BACKGROUND", (0, 0), (1, 0), NAVY),
            ("BACKGROUND", (0, 1), (-1, -1), SOFT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 1), (-1, -2), 0.4, colors.white),
        ])
    )
    return t


def bangun(d: dict) -> list:
    W = PAGE_W - 2 * MARGIN
    cerita = []

    # ---- Halaman: Tentang
    cerita.append(Paragraph("TENTANG", S["eyebrow"]))
    cerita.append(Paragraph("Profil Singkat", S["h1"]))
    cerita.append(Spacer(1, 7))
    cerita.append(Paragraph(d["brand"]["deskripsi_panjang"], S["body"]))

    cerita.append(Paragraph("Yang Membedakan", S["h2"]))
    sel = []
    for n in d["nilai"]:
        sel.append(
            Paragraph(
                f'<font name="{F_BOLD}" color="#0D2145">{n["judul"]}</font><br/>'
                f'<font size="9">{n["isi"]}</font>',
                S["cell"],
            )
        )
    pasangan = [sel[i:i + 2] for i in range(0, len(sel), 2)]
    for p in pasangan:
        if len(p) == 1:
            p.append("")
    t = Table(pasangan, colWidths=[W / 2 - 4, W / 2 - 4])
    t.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("LINEBELOW", (0, 0), (-1, -1), 6, colors.white),
            ("LINEAFTER", (0, 0), (0, -1), 6, colors.white),
        ])
    )
    cerita.append(t)

    cerita.append(Paragraph("Sekilas Data", S["h2"]))
    ig0, tt0 = d["sosial"]["instagram"], d["sosial"]["tiktok"]
    # Bandingkan nilai rupiahnya, bukan stringnya: "Rp115.000" < "Rp85.000"
    # secara leksikografis, yang akan salah menyebut paket termurah.
    def _rupiah(teks: str) -> int:
        angka = "".join(ch for ch in teks.split("Rp")[-1] if ch.isdigit())
        return int(angka) if angka else 10**9

    berharga = [p["harga"] for p in d["program"] if "Rp" in p.get("harga", "")]
    harga_mulai = min(berharga, key=_rupiah) if berharga else "—"
    cerita.append(
        kotak_info(
            "RINGKASAN",
            [
                ("Jenis", f'{d["brand"]["kategori"]} · komunitas tenis'),
                ("Basis", f'{d["brand"]["kota"]}, {d["brand"]["negara"]}'),
                ("Fokus level", "Beginner sampai upper beginner"),
                ("Layanan", ", ".join(p["nama"] for p in d["program"])),
                ("Lapangan", ", ".join(v["nama"] for v in d["venue"])),
                ("Biaya mulai", harga_mulai),
                (
                    "Jangkauan sosial",
                    f'{ig0["followers"]:,}'.replace(",", ".")
                    + " pengikut Instagram, "
                    + f'{tt0["followers"]:,}'.replace(",", ".")
                    + " pengikut TikTok",
                ),
                ("Pendaftaran", d["kontak"]["cara_daftar"]),
                ("Grup WhatsApp", d["kontak"].get("whatsapp_group", "—")),
            ],
            W,
        )
    )

    # ---- Halaman: Program
    cerita.append(PageBreak())
    cerita.append(Paragraph("LAYANAN", S["eyebrow"]))
    cerita.append(Paragraph("Program & Biaya", S["h1"]))
    cerita.append(Spacer(1, 4))
    cerita.append(
        Paragraph(
            "Seluruh program terbuka untuk pemain pemula. Perlengkapan dasar "
            "sudah termasuk dalam biaya, sehingga peserta baru tidak perlu "
            "membeli raket sebelum mencoba.",
            S["body"],
        )
    )
    cerita.append(Spacer(1, 4))

    kepala = ["Program", "Level", "Jadwal / Durasi", "Lokasi", "Biaya"]
    baris = [[Paragraph(h, S["cell_head"]) for h in kepala]]
    for p in d["program"]:
        waktu = p.get("jadwal") or p.get("durasi") or "—"
        if p.get("kapasitas"):
            waktu += f'<br/><font color="#64748B" size="7.6">{p["kapasitas"]}</font>'
        baris.append([
            Paragraph(p["nama"], S["cell_bold"]),
            Paragraph(p.get("level", "—"), S["cell"]),
            Paragraph(waktu, S["cell"]),
            Paragraph(p.get("lokasi", "—"), S["cell"]),
            Paragraph(f'<font name="{F_BOLD}">{p.get("harga", "—")}</font>', S["cell"]),
        ])
    t = Table(
        baris,
        colWidths=[W * 0.21, W * 0.17, W * 0.20, W * 0.24, W * 0.18],
        repeatRows=1,
    )
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT]),
            ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("LINEBELOW", (0, 0), (-1, 0), 1.6, LIME),
        ])
    )
    cerita.append(t)

    cerita.append(Paragraph("Rincian Paket", S["h2"]))
    for p in d["program"]:
        isi = [("Termasuk", ", ".join(p["termasuk"]) if p.get("termasuk") else "—")]
        if p.get("pelatih"):
            isi.append(("Pelatih", p["pelatih"]))
        isi.append(("Catatan", p.get("catatan", "—")))
        cerita.append(KeepTogether([kotak_info(p["nama"].upper(), isi, W), Spacer(1, 8)]))

    # ---- Halaman: Lapangan, kanal, kontak
    cerita.append(PageBreak())
    cerita.append(Paragraph("OPERASIONAL", S["eyebrow"]))
    cerita.append(Paragraph("Lapangan & Kanal", S["h1"]))
    cerita.append(Spacer(1, 6))

    cerita.append(Paragraph("Lapangan", S["h2"]))
    vb = [[Paragraph(h, S["cell_head"]) for h in ["Lapangan", "Tipe", "Kota", "Dipakai untuk"]]]
    for v in d["venue"]:
        vb.append([
            Paragraph(v["nama"], S["cell_bold"]),
            Paragraph(v["tipe"], S["cell"]),
            Paragraph(v["kota"], S["cell"]),
            Paragraph(v["dipakai_untuk"], S["cell"]),
        ])
    t = Table(vb, colWidths=[W * 0.33, W * 0.14, W * 0.15, W * 0.38])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT]),
            ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("LINEBELOW", (0, 0), (-1, 0), 1.6, LIME),
        ])
    )
    cerita.append(t)

    cerita.append(Paragraph("Kanal Sosial", S["h2"]))
    ig, tt = d["sosial"]["instagram"], d["sosial"]["tiktok"]
    sb = [[Paragraph(h, S["cell_head"]) for h in ["Kanal", "Handle", "Pengikut", "Catatan"]]]
    sb.append([
        Paragraph("Instagram", S["cell_bold"]),
        Paragraph(ig["handle"], S["cell"]),
        Paragraph(f'{ig["followers"]:,}'.replace(",", "."), S["cell"]),
        Paragraph(
            f'{ig["posts"]} post · kategori {ig["kategori"]} · '
            f'post terbaru {ig["post_terbaru"]}', S["cell"]
        ),
    ])
    sb.append([
        Paragraph("TikTok", S["cell_bold"]),
        Paragraph(tt["handle"], S["cell"]),
        Paragraph(f'{tt["followers"]:,}'.replace(",", "."), S["cell"]),
        Paragraph(
            f'{tt["video_publik"]} video publik · '
            f'{tt["likes"]:,}'.replace(",", ".") + " likes", S["cell"]
        ),
    ])
    t = Table(sb, colWidths=[W * 0.17, W * 0.18, W * 0.15, W * 0.50])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT]),
            ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("LINEBELOW", (0, 0), (-1, 0), 1.6, LIME),
        ])
    )
    cerita.append(t)

    cerita.append(Paragraph("Strategi Konten", S["h2"]))
    for p in d["konten"]["pilar"]:
        cerita.append(
            Paragraph(
                f'<font name="{F_BOLD}" color="#0D2145">{p["nama"]}.</font> {p["isi"]}',
                S["body_left"],
            )
        )
    cerita.append(Spacer(1, 2))
    cerita.append(
        Paragraph(
            f'<font name="{F_BOLD}" color="#0D2145">Temuan performa.</font> '
            f'{d["konten"]["performa_catatan"]}',
            S["body"],
        )
    )

    cerita.append(Paragraph("Kontak & Pendaftaran", S["h2"]))
    k = d["kontak"]
    baris_kontak = []
    if k.get("whatsapp_group"):
        baris_kontak.append(("Grup WhatsApp", k["whatsapp_group"]))
    baris_kontak += [
        ("WhatsApp Admin", k["whatsapp_admin"]),
        ("Instagram", f'{ig["handle"]} — {k["instagram_dm"]}'),
        ("TikTok", f'{tt["handle"]} — {k["tiktok"]}'),
        ("Alur", k["cara_daftar"]),
    ]
    cerita.append(kotak_info("CARA BERGABUNG", baris_kontak, W))

    # ---- Catatan metodologi
    cerita.append(Spacer(1, 14))
    cerita.append(Paragraph("Catatan Sumber Data", S["h2"]))
    cerita.append(
        Paragraph(
            f'{d["meta"]["sumber"]}. {d["meta"]["catatan"]}',
            S["small"],
        )
    )
    cerita.append(Spacer(1, 7))
    cerita.append(
        Paragraph(
            f'<font name="{F_BOLD}" color="#0D2145">Belum terverifikasi '
            f'({len(d["perlu_konfirmasi"])} hal):</font>',
            S["small"],
        )
    )
    for i, item in enumerate(d["perlu_konfirmasi"], 1):
        cerita.append(Paragraph(f"{i}. {item}", S["small"]))

    return cerita


def main() -> int:
    if not DATA.exists():
        print(f"Tidak menemukan {DATA}", file=sys.stderr)
        return 1
    d = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=22 * mm,
        bottomMargin=20 * mm,
        title="Profil Gow! Tennis — Komunitas Tenis Bandung",
        author="Gow! Tennis",
        subject="Profil komunitas tenis Bandung",
    )
    frame_kosong = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
    frame_isi = Frame(
        MARGIN, 20 * mm, PAGE_W - 2 * MARGIN, PAGE_H - 42 * mm, id="isi"
    )
    doc.addPageTemplates([
        PageTemplate(id="Sampul", frames=[frame_kosong],
                     onPage=lambda c, dd: gambar_sampul(c, dd, d)),
        PageTemplate(id="Isi", frames=[frame_isi],
                     onPage=lambda c, dd: gambar_isi(c, dd, d)),
    ])

    cerita = [NextPageTemplate("Isi"), PageBreak()] + bangun(d)
    doc.build(cerita)

    kb = OUT.stat().st_size / 1024
    print(f"PDF dibuat: {OUT}  ({kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
