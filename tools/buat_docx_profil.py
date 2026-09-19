#!/usr/bin/env python3
"""Bangun DOCX profil Gow! Tennis dari backend/data/profile.json.

Sumbernya sama persis dengan versi PDF dan website, jadi ketiganya tidak pernah
saling bertentangan. Bedanya dengan PDF: berkas ini dibuat untuk diedit lebih
lanjut di Word, sehingga memakai gaya terang, heading bawaan (biar muncul di
panel Navigation), dan tabel yang lebarnya terkunci.

Jalankan:
    python3 tools/buat_docx_profil.py
Hasil:
    docs/Profil-Gow-Tennis.docx
"""
import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "backend" / "data" / "profile.json"
LOGO = ROOT / "tools" / "assets" / "logo-bulat.png"
OUT = ROOT / "docs" / "Profil-Gow-Tennis.docx"

NAVY = RGBColor(0x0D, 0x21, 0x45)
NAVY_MID = RGBColor(0x1B, 0x3A, 0x70)
INK = RGBColor(0x0B, 0x1B, 0x36)
MUTED = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

HEX_NAVY = "0D2145"
HEX_LIME = "D7E84B"
HEX_SOFT = "F4F6FA"
HEX_LINE = "E2E8F0"

FONT = "Arial"


# ------------------------------------------------------------------ helper

def warnai_sel(cell, hex_warna: str) -> None:
    """Latar sel tabel. python-docx tidak punya API-nya, jadi sisipkan w:shd."""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_warna)
    cell._tc.get_or_add_tcPr().append(shd)


def kunci_lebar_tabel(tabel, lebar_cm: list) -> None:
    """Kunci lebar kolom.

    Mengatur cell.width saja tidak cukup: Word ikut membaca <w:tblGrid>, dan
    kalau grid-nya masih bawaan, kolom akan melar sendiri saat dibuka. Jadi
    gridnya ditulis ulang, lalu setiap sel disamakan.
    """
    tabel.autofit = False
    grid = tabel._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        tabel._tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in lebar_cm:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(Cm(w).twips)))
        grid.append(col)
    tabel._tbl.insert(0, grid)
    for baris in tabel.rows:
        for i, sel in enumerate(baris.cells):
            sel.width = Cm(lebar_cm[i])


def garis_sel(cell, sisi: str = "bottom", hex_warna: str = HEX_LINE, ukuran: int = 4) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcPr.append(borders)
    el = OxmlElement(f"w:{sisi}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(ukuran))
    el.set(qn("w:color"), hex_warna)
    borders.append(el)


def tautan(paragraf, url: str, teks: str, ukuran: float = 9.5):
    """Hyperlink asli yang bisa diklik. python-docx belum menyediakan API-nya."""
    r_id = paragraf.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    for tag, val in (("w:color", "1B3A70"), ("w:u", "single")):
        el = OxmlElement(tag)
        el.set(qn("w:val"), "single" if tag == "w:u" else val)
        if tag == "w:color":
            el.set(qn("w:val"), val)
        rPr.append(el)
    rf = OxmlElement("w:rFonts")
    rf.set(qn("w:ascii"), FONT)
    rf.set(qn("w:hAnsi"), FONT)
    rPr.append(rf)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(ukuran * 2)))
    rPr.append(sz)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = teks
    run.append(t)
    link.append(run)
    paragraf._p.append(link)
    return paragraf


def teks(paragraf, isi: str, ukuran=9.5, bold=False, warna=INK, italic=False):
    run = paragraf.add_run(isi)
    run.font.name = FONT
    run.font.size = Pt(ukuran)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = warna
    return run


def paragraf_baru(doc, isi="", ukuran=9.5, bold=False, warna=INK,
                  rata=WD_ALIGN_PARAGRAPH.LEFT, spasi_atas=0, spasi_bawah=6):
    p = doc.add_paragraph()
    p.alignment = rata
    p.paragraph_format.space_before = Pt(spasi_atas)
    p.paragraph_format.space_after = Pt(spasi_bawah)
    p.paragraph_format.line_spacing = 1.18
    if isi:
        teks(p, isi, ukuran, bold, warna)
    return p


def judul(doc, isi: str, level: int = 1):
    """Heading bawaan supaya muncul di panel Navigation, tapi fontnya dipaksa.

    Style Heading bawaan Word memakai font tema (Calibri Light) dan warna biru
    muda. Menimpanya lewat style saja sering kalah oleh tema dokumen, jadi
    diterapkan per run.
    """
    h = doc.add_heading(level=level)
    h.paragraph_format.space_before = Pt(16 if level == 1 else 12)
    h.paragraph_format.space_after = Pt(6)
    run = h.add_run(isi)
    run.font.name = FONT
    run.font.size = Pt(18 if level == 1 else 12.5)
    run.font.bold = True
    run.font.color.rgb = NAVY
    return h


def eyebrow(doc, isi: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    r = p.add_run(isi.upper())
    r.font.name = FONT
    r.font.size = Pt(7.5)
    r.font.bold = True
    r.font.color.rgb = NAVY_MID
    return p


def tabel_label_nilai(doc, kepala: str, baris: list, lebar: list):
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    hdr = t.rows[0].cells
    hdr[0].merge(hdr[1])
    p = t.rows[0].cells[0].paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    teks(p, kepala.upper(), 8, True, WHITE)
    warnai_sel(t.rows[0].cells[0], HEX_NAVY)

    for label, nilai in baris:
        sel = t.add_row().cells
        p1 = sel[0].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        teks(p1, label, 8.8, True, NAVY)
        p2 = sel[1].paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        if isinstance(nilai, tuple):  # (teks, url) -> hyperlink
            tautan(p2, nilai[1], nilai[0], 8.8)
        else:
            teks(p2, str(nilai), 8.8)
        for s in sel:
            warnai_sel(s, HEX_SOFT)
            garis_sel(s, "bottom", "FFFFFF", 6)
    kunci_lebar_tabel(t, lebar)
    return t


def tabel_data(doc, kepala: list, baris: list, lebar: list):
    t = doc.add_table(rows=1, cols=len(kepala))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(kepala):
        sel = t.rows[0].cells[i]
        p = sel.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        teks(p, h, 8, True, WHITE)
        warnai_sel(sel, HEX_NAVY)

    for n, isi_baris in enumerate(baris):
        sel = t.add_row().cells
        for i, nilai in enumerate(isi_baris):
            p = sel[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            teks(p, str(nilai), 8.6, bold=(i == 0), warna=NAVY if i == 0 else INK)
            if n % 2 == 1:
                warnai_sel(sel[i], HEX_SOFT)
            garis_sel(sel[i], "bottom", HEX_LINE, 4)
    kunci_lebar_tabel(t, lebar)
    return t


# ------------------------------------------------------------------ dokumen

def bangun(d: dict) -> Document:
    doc = Document()

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    for atr, val in (("top_margin", 2.2), ("bottom_margin", 2.0),
                     ("left_margin", 2.0), ("right_margin", 2.0)):
        setattr(sec, atr, Cm(val))
    LEBAR = 17.0  # lebar cetak efektif

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = INK

    brand, sosial, kontak = d["brand"], d["sosial"], d["kontak"]
    ig, tt = sosial["instagram"], sosial["tiktok"]

    # ---------------- Sampul
    if LOGO.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(60)
        p.paragraph_format.space_after = Pt(14)
        p.add_run().add_picture(str(LOGO), width=Cm(4.6))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("GOW! TENNIS")
    r.font.name = FONT
    r.font.size = Pt(34)
    r.font.bold = True
    r.font.color.rgb = NAVY

    paragraf_baru(doc, f'"{brand["tagline"]}"', 13, True, NAVY_MID,
                  WD_ALIGN_PARAGRAPH.CENTER, spasi_bawah=2)
    paragraf_baru(
        doc,
        f'{brand["kategori"].upper()}  ·  {brand["kota"].upper()}, {brand["negara"].upper()}',
        9, False, MUTED, WD_ALIGN_PARAGRAPH.CENTER, spasi_bawah=22,
    )

    angka = [
        ("INSTAGRAM", f'{ig["followers"]:,}'.replace(",", ".")),
        ("TIKTOK", f'{tt["followers"]:,}'.replace(",", ".")),
        ("TIKTOK LIKES", "15,4K"),
        ("PROGRAM", str(len(d["program"]))),
    ]
    t = doc.add_table(rows=2, cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (label, nilai) in enumerate(angka):
        pa = t.rows[0].cells[i].paragraphs[0]
        pa.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pa.paragraph_format.space_after = Pt(0)
        teks(pa, nilai, 17, True, NAVY)
        pb = t.rows[1].cells[i].paragraphs[0]
        pb.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pb.paragraph_format.space_after = Pt(0)
        teks(pb, label, 7, True, MUTED)
        garis_sel(t.rows[0].cells[i], "top", HEX_LIME, 18)
    kunci_lebar_tabel(t, [LEBAR / 4] * 4)

    paragraf_baru(
        doc, f'Profil Komunitas  ·  Data per {d["meta"]["tanggal_riset"]}',
        8, False, MUTED, WD_ALIGN_PARAGRAPH.CENTER, spasi_atas=26,
    )
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- Profil singkat
    eyebrow(doc, "Tentang")
    judul(doc, "Profil Singkat", 1)
    p = paragraf_baru(doc, brand["deskripsi_panjang"], 9.5, spasi_bawah=10)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    judul(doc, "Yang Membedakan", 2)
    for n in d["nilai"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(7)
        p.paragraph_format.line_spacing = 1.18
        teks(p, f'{n["judul"]}. ', 9.5, True, NAVY)
        teks(p, n["isi"], 9.5)

    judul(doc, "Sekilas Data", 2)

    def _rupiah(t_: str) -> int:
        angka_ = "".join(c for c in t_.split("Rp")[-1] if c.isdigit())
        return int(angka_) if angka_ else 10**9

    berharga = [p_["harga"] for p_ in d["program"] if "Rp" in p_.get("harga", "")]
    harga_mulai = min(berharga, key=_rupiah) if berharga else "—"

    ringkas = [
        ("Jenis", f'{brand["kategori"]} · komunitas tenis'),
        ("Basis", f'{brand["kota"]}, {brand["negara"]}'),
        ("Fokus level", "Beginner sampai upper beginner"),
        ("Layanan", ", ".join(p_["nama"] for p_ in d["program"])),
        ("Lapangan", ", ".join(v["nama"] for v in d["venue"])),
        ("Biaya mulai", harga_mulai),
        ("Jangkauan sosial",
         f'{ig["followers"]:,}'.replace(",", ".") + " pengikut Instagram, "
         + f'{tt["followers"]:,}'.replace(",", ".") + " pengikut TikTok"),
        ("Pendaftaran", kontak["cara_daftar"]),
    ]
    if kontak.get("whatsapp_group"):
        ringkas.append(("Grup WhatsApp",
                        ("Gabung grup Gow! Tennis", kontak["whatsapp_group"])))
    tabel_label_nilai(doc, "Ringkasan", ringkas, [LEBAR * 0.30, LEBAR * 0.70])

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- Program & biaya
    eyebrow(doc, "Layanan")
    judul(doc, "Program & Biaya", 1)
    paragraf_baru(
        doc,
        "Seluruh program terbuka untuk pemain pemula. Perlengkapan dasar sudah "
        "termasuk dalam biaya, sehingga peserta baru tidak perlu membeli raket "
        "sebelum mencoba.",
        9.5, spasi_bawah=10,
    )

    baris = []
    for p_ in d["program"]:
        waktu = p_.get("jadwal") or p_.get("durasi") or "—"
        if p_.get("kapasitas"):
            waktu += f' ({p_["kapasitas"]})'
        baris.append([
            p_["nama"], p_.get("level", "—"), waktu,
            p_.get("lokasi", "—"), p_.get("harga", "—"),
        ])
    tabel_data(
        doc, ["Program", "Level", "Jadwal / Durasi", "Lokasi", "Biaya"], baris,
        [LEBAR * 0.20, LEBAR * 0.17, LEBAR * 0.21, LEBAR * 0.24, LEBAR * 0.18],
    )

    judul(doc, "Rincian Paket", 2)
    for p_ in d["program"]:
        isi = [("Termasuk", ", ".join(p_["termasuk"]) if p_.get("termasuk") else "—")]
        if p_.get("pelatih"):
            isi.append(("Pelatih", p_["pelatih"]))
        isi.append(("Catatan", p_.get("catatan", "—")))
        tabel_label_nilai(doc, p_["nama"], isi, [LEBAR * 0.22, LEBAR * 0.78])
        paragraf_baru(doc, "", spasi_bawah=8)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- Lapangan, kanal, kontak
    eyebrow(doc, "Operasional")
    judul(doc, "Lapangan & Kanal", 1)

    judul(doc, "Lapangan", 2)
    tabel_data(
        doc, ["Lapangan", "Tipe", "Kota", "Dipakai untuk"],
        [[v["nama"], v["tipe"], v["kota"], v["dipakai_untuk"]] for v in d["venue"]],
        [LEBAR * 0.33, LEBAR * 0.14, LEBAR * 0.15, LEBAR * 0.38],
    )

    judul(doc, "Kanal Sosial", 2)
    tabel_data(
        doc, ["Kanal", "Handle", "Pengikut", "Catatan"],
        [
            ["Instagram", ig["handle"], f'{ig["followers"]:,}'.replace(",", "."),
             f'{ig["posts"]} post · kategori {ig["kategori"]} · post terbaru {ig["post_terbaru"]}'],
            ["TikTok", tt["handle"], f'{tt["followers"]:,}'.replace(",", "."),
             f'{tt["video_publik"]} video publik · ' + f'{tt["likes"]:,}'.replace(",", ".") + " likes"],
        ],
        [LEBAR * 0.17, LEBAR * 0.18, LEBAR * 0.15, LEBAR * 0.50],
    )

    judul(doc, "Strategi Konten", 2)
    for pilar in d["konten"]["pilar"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.18
        teks(p, f'{pilar["nama"]}. ', 9.5, True, NAVY)
        teks(p, pilar["isi"], 9.5)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6)
    teks(p, "Temuan performa. ", 9.5, True, NAVY)
    teks(p, d["konten"]["performa_catatan"], 9.5)

    judul(doc, "Kontak & Pendaftaran", 2)
    baris_kontak = []
    if kontak.get("whatsapp_group"):
        baris_kontak.append(
            ("Grup WhatsApp", ("Gabung grup Gow! Tennis", kontak["whatsapp_group"]))
        )
    baris_kontak += [
        ("WhatsApp Admin", kontak["whatsapp_admin"]),
        ("Instagram", (ig["handle"], kontak["instagram_dm"])),
        ("TikTok", (tt["handle"], kontak["tiktok"])),
        ("Alur", kontak["cara_daftar"]),
    ]
    tabel_label_nilai(doc, "Cara Bergabung", baris_kontak,
                      [LEBAR * 0.24, LEBAR * 0.76])

    judul(doc, "Catatan Sumber Data", 2)
    paragraf_baru(doc, f'{d["meta"]["sumber"]}. {d["meta"]["catatan"]}',
                  8.4, warna=MUTED, spasi_bawah=8)
    paragraf_baru(doc, f'Belum terverifikasi ({len(d["perlu_konfirmasi"])} hal):',
                  8.4, True, NAVY, spasi_bawah=4)
    for i, item in enumerate(d["perlu_konfirmasi"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(3)
        teks(p, f"{i}. {item}", 8.4, warna=MUTED)

    # ---------------- Footer di semua halaman
    ft = sec.footer.paragraphs[0]
    ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    teks(ft, "Gow! Tennis  ·  instagram.com/gowtennis  ·  tiktok.com/@gowtennis",
         7.5, warna=MUTED)

    doc.core_properties.title = "Profil Gow! Tennis — Komunitas Tenis Bandung"
    doc.core_properties.author = "Gow! Tennis"
    doc.core_properties.subject = "Profil komunitas tenis Bandung"
    return doc


def main() -> int:
    if not DATA.exists():
        print(f"Tidak menemukan {DATA}", file=sys.stderr)
        return 1
    d = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    bangun(d).save(str(OUT))
    print(f"DOCX dibuat: {OUT}  ({OUT.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
