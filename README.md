# Gow! Tennis — Website & Profil

Landing page dan dokumen profil untuk **Gow! Tennis**, komunitas tenis di Bandung
([Instagram](https://www.instagram.com/gowtennis/) ·
[TikTok](https://www.tiktok.com/@gowtennis)).

```
gowtennis/
├── backend/          FastAPI — API profil, program, feed sosial, form kontak
├── frontend/         Vue 3 + Vite — landing page
├── tools/            Skrip pembangkit PDF & DOCX, pre-render statis, deploy
├── docs/             PDF + DOCX profil & dokumentasi (integrasi sosial, deploy)
├── .github/          Workflow auto-deploy ke GitHub Pages
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

## Preview online

Situs di-deploy sebagai **situs statis** — FastAPI tidak ikut, karena seluruh
data yang dilayaninya sekarang bersifat tetap dan dibekukan saat build oleh
`tools/buat_static.py`. Sudah diuji dengan backend dimatikan: semua halaman,
embed Instagram, dan form kontak tetap jalan.

**GitHub Pages (otomatis).** Setiap push ke `main` memicu
`.github/workflows/deploy-pages.yml`.

Sekali saja, pilih salah satu:
- simpan repository secret `PAGES_TOKEN` (PAT) — Pages dibuat otomatis, atau
- aktifkan manual di **Settings → Pages → Source: GitHub Actions**

Langkah persisnya ada di [docs/DEPLOY.md](docs/DEPLOY.md).

URL: <https://azharkhairaa.github.io/gowtennis/>

**Surge.sh (manual, sekali pakai).**

```bash
./tools/deploy-surge.sh
```

Perbandingan keduanya dan penjelasan lengkap: **[docs/DEPLOY.md](docs/DEPLOY.md)**

> Karena datanya dibekukan saat build, setiap perubahan pada `profile.json` atau
> `social_feed.json` baru tampil setelah build ulang. Di Pages ini otomatis.

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

Jadwal dan tarif terkini mengikuti poster resmi klub per **25 September 2026**
(arsipnya di `docs/sumber/`):

| Hari | Kelas | Jam | Lapangan | Biaya |
|---|---|---|---|---|
| Senin | Semi-Intense | 08.00–10.00 | Indoor UPI | Rp105.000 (7 orang) |
| Selasa | Coaching Beginner | 16.00–18.00 | Outdoor UPI | Rp50.000 (10 orang) |
| Sabtu | Fun Games | 16.00–18.00 | Tennis PRV | Rp55.000 |
| Sabtu | Private | by appointment | Abadi / Secapa | Rp165.000/jam |

Kelas privat: coaching Rp330.000 per sesi 2 jam, sewa lapangan terpisah —
Abadi Rp240.000 (total Rp570.000), Secapa Rp250.000 (total Rp580.000).
Fotografer Rp100.000 by request.

WhatsApp admin **082312273282**.

---

## Catatan

Form kontak **belum mengirim email atau menyimpan ke database.** Ia memvalidasi
input lalu mengembalikan tautan WhatsApp yang teksnya sudah terisi, supaya
pendaftaran tetap mengalir ke kanal yang memang dipakai klub. Kalau nanti perlu
disimpan, tempat menambahkannya ada di `backend/app/routers/contact.py`.
