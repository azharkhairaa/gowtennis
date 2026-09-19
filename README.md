# Gow! Tennis — Website & Profil

Landing page dan dokumen profil untuk **Gow! Tennis**, komunitas tenis di Bandung
([Instagram](https://www.instagram.com/gowtennis/) ·
[TikTok](https://www.tiktok.com/@gowtennis)).

```
gowtennis/
├── backend/          FastAPI — API profil, program, feed sosial, form kontak
├── frontend/         Vue 3 + Vite — landing page
├── tools/            Skrip pembangkit PDF & DOCX + aset logo
├── docs/             PDF + DOCX profil & dokumentasi integrasi sosial
└── README.md
```

---

## Menjalankan

Butuh dua terminal. Backend dulu, baru frontend.

**1. Backend** (port 8010)

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/uvicorn app.main:app --reload --port 8010
```

**2. Frontend** (port 5183)

```bash
cd frontend && npm install && npm run dev
```

Buka <http://localhost:5183>. Dokumentasi API otomatis ada di
<http://127.0.0.1:8010/docs>.

> Port 8010 dan 5183 dipilih karena 8000 dan 5173 sudah dipakai project lain di
> mesin ini. Ubah di `frontend/vite.config.js` kalau mau menggeser.

**Menjalankan test:**

```bash
cd backend && .venv/bin/python -m pytest tests/ -q
```

**Build produksi frontend:**

```bash
cd frontend && npm run build
```

---

## Data profil

Website, PDF, **dan** DOCX semuanya dibaca dari satu berkas:

```
backend/data/profile.json
```

Ubah di situ, lalu jalankan ulang kedua pembangkit supaya ketiganya tetap sinkron:

```bash
python3 tools/buat_pdf_profil.py && python3 tools/buat_docx_profil.py
```

Hasilnya:

| Berkas | Halaman | Untuk apa |
|---|---|---|
| `docs/Profil-Gow-Tennis.pdf` | 5 | Versi final siap kirim/cetak, sampul gelap penuh warna |
| `docs/Profil-Gow-Tennis.docx` | 4 | Versi yang bisa diedit di Word, gaya terang, heading masuk panel Navigation, tautan bisa diklik |

Keduanya sengaja berbeda gaya: PDF untuk dibagikan apa adanya, DOCX untuk
disunting lebih lanjut.

Butuh `python-docx` dan `reportlab` (keduanya sudah terpasang di mesin ini).

---

## Menampilkan post Instagram & TikTok

Dikelola lewat `backend/data/social_feed.json`.

Ringkasnya: **Instagram bisa otomatis** (Graph API, kodenya sudah ada tinggal
diisi token), **TikTok harus disalin URL-nya manual** karena TikTok tidak
mengekspos daftar video ke pengunjung anonim. Default saat ini adalah mode
kurasi yang jalan tanpa kredensial apa pun.

Feed menampilkan **3 post Instagram terbaru** sebagai embed penuh. Saat menambah
post baru, buang entry paling lama supaya halaman tetap ringan.

Penjelasan lengkap, termasuk cara menambah post dan cara mengaktifkan Graph API:
**[docs/INTEGRASI-SOSIAL.md](docs/INTEGRASI-SOSIAL.md)**

---

## Endpoint API

| Method | Path | Fungsi |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/profile` | Profil lengkap |
| GET | `/api/programs` | Daftar program & biaya |
| GET | `/api/stats` | Angka ringkas untuk hero |
| GET | `/api/social/feed` | Feed Instagram + TikTok (`?refresh=true` lewati cache) |
| GET | `/api/social/status` | Status kesiapan integrasi tiap platform |
| POST | `/api/contact` | Validasi form, kembalikan tautan WhatsApp/DM terisi |

## Kanal pendaftaran

Urutan yang dipakai di website, PDF, dan DOCX:

1. **Grup WhatsApp** — <https://chat.whatsapp.com/HsV2Th8J7zXFpTCy1rfLe0?mode=gi_t>
2. WhatsApp admin — 082312273282
3. DM Instagram / TikTok @gowtennis

Link grup diambil dari `kontak.whatsapp_group` di `profile.json`. Kalau grupnya
diganti, ubah di sana lalu jalankan ulang kedua pembangkit dokumen — tombol di
web ikut berubah tanpa perlu menyentuh kode Vue.

---

## Yang masih perlu dilengkapi

Data di bawah ini **tidak tersedia di kanal publik** dan harus diisi pengelola
klub. Daftar ini juga tercetak di halaman terakhir PDF.

- [ ] URL tiga video TikTok (salin dari app: Share → Copy link)
- [ ] Arti singkatan "FG" pada caption TikTok
- [ ] Tahun berdiri, jumlah anggota aktif, struktur pengelola
- [ ] Alamat lengkap dan titik peta kedua lapangan
- [ ] Foto-foto asli untuk hero dan galeri (sekarang memakai logo + embed)

Sudah terverifikasi dari sumber aslinya: nomor WhatsApp admin **082312273282**,
pelatih **Coach Iwan**, harga **Rp85.000** (coaching, 2 jam, 6 orang) dan
**Rp115.000** (Tennis Malam Minggu, Sabtu 18.00–20.00 di Lapang Outdoor Pusdikku).

---

## Catatan

Form kontak **belum mengirim email atau menyimpan ke database.** Ia memvalidasi
input lalu mengembalikan tautan WhatsApp yang teksnya sudah terisi, supaya
pendaftaran tetap mengalir ke kanal yang memang dipakai klub. Kalau nanti perlu
disimpan, tempat menambahkannya ada di `backend/app/routers/contact.py`.
