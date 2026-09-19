# Deploy untuk Preview Online

Tujuannya: rekan bisa membuka situsnya lewat URL, tanpa perlu menjalankan
apa pun di laptop mereka.

---

## Kenapa bisa jadi statis

Situs ini punya backend FastAPI, dan **tidak ada static hosting yang menjalankan
Python** — baik GitHub Pages maupun Surge. Tapi kalau dilihat lagi, seluruh yang
dikerjakan backend saat ini sebenarnya tidak butuh server:

| Yang dilakukan backend | Butuh server? |
|---|---|
| Menyajikan `profile.json`, program, stats | Tidak, datanya tetap |
| Menyusun markup embed dari shortcode Instagram | Tidak, hasilnya tetap |
| Form kontak → tautan WhatsApp | Tidak, cukup dirakit di browser |
| Instagram Graph API (mode `api`) | **Ya** — tapi belum dipakai |

Jadi `tools/buat_static.py` memanggil FastAPI di dalam proses lalu **membekukan
respons setiap endpoint GET jadi berkas `.json`**. Frontend yang sama kemudian
membaca berkas itu, bukan API. Logikanya tidak diduplikasi — datanya tetap
dihasilkan backend, hanya dibekukan saat build.

Sudah diuji dengan backend dimatikan total: seluruh halaman, ketiga embed
Instagram, dan form kontak tetap berfungsi.

**Konsekuensinya:** setiap kali `profile.json` atau `social_feed.json` berubah,
situs harus di-build ulang. Di GitHub Pages ini otomatis setiap `git push`.

---

## Opsi A — GitHub Pages (dipakai, direkomendasikan)

Repo sudah ada: <https://github.com/azharkhairaa/gowtennis>
URL situs nantinya: **<https://azharkhairaa.github.io/gowtennis/>**

Deploy berjalan otomatis lewat `.github/workflows/deploy-pages.yml` setiap push
ke `main`. Alurnya: pre-render JSON → jalankan test backend → build → unggah.

Test ikut dijalankan supaya kalau `profile.json` rusak, ketahuan sebelum
situsnya terlanjur naik dalam keadaan pecah.

### Sekali saja: aktifkan Pages

Di GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

Tanpa langkah ini workflow akan gagal dengan error soal Pages belum aktif.

### Setelah itu

Cukup `git push`. Progresnya bisa dilihat di tab **Actions**, dan biasanya
selesai 1–2 menit.

### Catatan sub-path

GitHub Pages menyajikan project site di `/gowtennis/`, bukan di root. Semua
aset karena itu diakses lewat `base` Vite, bukan path absolut — logo diimpor
sebagai modul dan pemanggilan data memakai `import.meta.env.BASE_URL`. Nilai
`base` diisi otomatis dari output `actions/configure-pages`, jadi kalau nanti
dipasang custom domain (yang membuat situs pindah ke root), tidak ada yang
perlu diubah.

---

## Opsi B — Surge.sh

Lebih cepat kalau hanya ingin tautan sekali pakai.

```bash
./tools/deploy-surge.sh                     # ke gowtennis.surge.sh
./tools/deploy-surge.sh nama-lain.surge.sh  # domain sendiri
```

Skrip itu mengerjakan pre-render, build, lalu unggah. Pemakaian pertama Surge
meminta email dan password untuk membuat akun.

Perlu diketahui: domain `*.surge.sh` siapa saja bisa mengklaim lebih dulu, jadi
kalau namanya sudah dipakai orang lain, pilih yang lain. HTTPS pada subdomain
`surge.sh` sudah termasuk; **custom domain dengan SSL butuh paket berbayar.**

---

## Perbandingan

| | GitHub Pages | Surge.sh |
|---|---|---|
| Biaya | Gratis | Gratis |
| Deploy otomatis tiap push | **Ya** | Tidak, jalankan skrip manual |
| Riwayat versi & rollback | **Ya** | Tidak |
| Rekan bisa lihat source | **Ya** | Tidak |
| HTTPS custom domain | **Gratis** | Berbayar |
| Setup awal | Aktifkan Pages sekali | Buat akun Surge |
| Paling cocok untuk | Preview yang terus diperbarui | Tautan cepat sekali pakai |

Untuk preview yang dilihat rekan dan akan sering diperbarui, **GitHub Pages
lebih tepat**: sekali disetel, tidak ada langkah manual lagi.

---

## Kalau nanti butuh backend sungguhan

Selama feed masih mode `curated`, statis sudah cukup. Backend baru benar-benar
diperlukan kalau:

- Instagram Graph API diaktifkan (`FEED_MODE=api`) — token tidak boleh ditaruh
  di berkas statis karena akan terbaca siapa pun
- Form kontak perlu menyimpan data atau mengirim email

Kalau sampai di situ, pola yang lazim: backend di Render/Railway/Fly.io,
frontend tetap di Pages, lalu arahkan `VITE_API_BASE` ke URL backend saat build.
Perlu diingat, tier gratis layanan-layanan itu biasanya menidurkan aplikasi saat
menganggur, sehingga permintaan pertama jadi lambat.
