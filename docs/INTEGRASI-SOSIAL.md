# Menampilkan Post Instagram & TikTok di Website

Ringkasan jawaban: **sebagian bisa otomatis, sebagian memang harus manual.**
Batasnya bukan soal kemampuan coding, tapi soal apa yang diizinkan platform.

---

## 1. Jawaban singkat

| Platform | Tarik daftar post otomatis? | Tampilkan post di web? | Syarat |
|---|---|---|---|
| Instagram | **Bisa**, lewat Instagram Graph API | Bisa | Akun Professional + Meta App + access token |
| TikTok | **Tidak bisa** tanpa persetujuan TikTok | Bisa | URL video disalin manual, sisanya otomatis |

Yang terpasang sekarang: **mode `curated`** — daftar post dikelola di satu file
JSON, tampilannya memakai embed resmi. Ini jalan tanpa kredensial apa pun.
Jalur otomatis Instagram sudah ditulis kodenya dan tinggal diaktifkan.

Feed dibatasi **3 post Instagram terbaru**, ketiganya dirender sebagai embed
penuh dalam satu baris. Batas ini disengaja: setiap embed memuat satu iframe
dari server Meta, jadi menambah banyak post membuat halaman berat dan
embed-nya memuat antre.

---

## 2. Kenapa Instagram tidak bisa asal tarik

**Instagram Basic Display API dimatikan pada 4 Desember 2024.** API itu dulunya
cara termudah menarik media akun sendiri. Sekarang API tersebut tidak melayani
akun personal sama sekali, dan integrasi lama yang masih memanggilnya gagal
total.

Penggantinya ada dua, keduanya menuntut hal yang sama: **akun harus Professional
(Business atau Creator), bukan personal.**

- **Instagram Graph API** — untuk akun Business/Creator
- **Instagram API with Instagram Login** — pengganti langsung Basic Display

Kabar baik untuk Gow! Tennis: profil `@gowtennis` menampilkan kategori
**"Community"** di bio. Kategori hanya muncul pada akun Professional, jadi
**syarat utamanya sudah terpenuhi** dan tidak perlu mengubah tipe akun.

### Yang masih perlu disiapkan

1. Buat aplikasi di [developers.facebook.com](https://developers.facebook.com)
2. Hubungkan akun Instagram ke aplikasi tersebut
3. Ambil **long-lived access token** (berlaku 60 hari)
4. Jadwalkan refresh token sebelum kedaluwarsa — kalau lewat, feed mati diam-diam

Poin 4 ini yang paling sering jadi masalah di kemudian hari, jadi backend sudah
dibuat agar **tidak mematikan halaman** kalau token bermasalah: ia otomatis
turun ke daftar kurasi dan mencatat peringatan di respons API.

---

## 3. Kenapa TikTok lebih terbatas

TikTok punya dua hal yang berbeda, dan keduanya sering tertukar:

**a. oEmbed — publik, tanpa API key.** Sudah diuji dan terbukti jalan:

```bash
curl "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@gowtennis/video/XXXXXXXXXX"
```

Mengembalikan judul, nama akun, thumbnail, dan HTML embed siap pakai.
**Tapi** oEmbed hanya menerjemahkan **satu URL yang sudah kita ketahui.**
Ia tidak bisa menjawab "berikan semua video milik akun ini".

**b. TikTok Display API (Login Kit)** — bisa mendaftar video sebuah akun, tapi
butuh pendaftaran app dan **persetujuan dari TikTok**, yang prosesnya tidak
instan dan tidak dijamin lolos.

### Kenapa tidak di-scrape saja?

Sudah dicoba saat riset ini, dan **gagal**: membuka halaman profil TikTok tanpa
login hanya menghasilkan `Something went wrong` di bagian daftar video. TikTok
memang memblokirnya. Scraping juga melanggar ToS dan gampang rusak sewaktu-waktu.

**Jadi untuk TikTok: URL video disalin manual sekali per video.** Setelah URL
masuk, judul dan thumbnail diambil otomatis lewat oEmbed.

---

## 4. Cara menambah konten sekarang

### Instagram

Buka post di Instagram, salin kodenya dari URL:

```
https://www.instagram.com/reel/DdJbG-8BhHt/
                               ^^^^^^^^^^^  ini shortcode-nya
```

Tambahkan ke `backend/data/social_feed.json`:

```json
{ "shortcode": "DdJbG-8BhHt", "tipe": "reel", "tanggal": "2026-09-11",
  "judul": "Doa Sebelum Coaching Tennis", "unggulan": true }
```

- `tipe`: `reel` untuk Reels, `p` untuk foto/carousel
- `unggulan: true` menaikkan post ke atas **dan** membuatnya dirender sebagai
  embed penuh, bukan kartu ringkas

Karena feed dibatasi 3 post, **buang entry paling lama setiap menambah yang
baru.** Kalau daftarnya dibiarkan memanjang, semua tetap tampil dan halaman
jadi berat.

### TikTok

Di aplikasi TikTok: buka video → **Share** → **Copy link**. Tempel URL-nya:

```json
{ "url": "https://www.tiktok.com/@gowtennis/video/7381360530369432838",
  "judul": "Coba Tebak Yang Mana Coachnya?", "unggulan": true }
```

Judul dan thumbnail akan ditimpa otomatis oleh oEmbed, jadi `judul` di sini
hanya cadangan kalau video dihapus atau diprivat.

Perubahan langsung terlihat setelah cache habis (15 menit), atau paksa segera:

```bash
curl "http://127.0.0.1:8010/api/social/feed?refresh=true"
```

---

## 5. Cara mengaktifkan mode otomatis Instagram

Setelah punya token, isi `backend/.env`:

```
FEED_MODE=api
IG_USER_ID=<id akun instagram>
IG_ACCESS_TOKEN=<long-lived token>
```

Restart backend. Cek statusnya:

```bash
curl http://127.0.0.1:8010/api/social/status
```

`instagram.otomatis_aktif` akan berubah jadi `true`. Kalau tetap `false`,
kredensialnya belum lengkap dan sistem tetap memakai daftar kurasi — endpoint
ini sengaja tidak mengklaim otomatis kalau kenyataannya tidak.

---

## 6. Catatan teknis yang gampang terlewat

**Script embed dan SPA.** Script `embed.js` milik Instagram hanya memindai DOM
sekali saat dimuat. Di aplikasi Vue, kartu dirender setelah data selesai
di-fetch, jadi blockquote-nya akan diam sebagai teks biasa. Solusinya ada di
`frontend/src/composables/useSocialEmbed.js`, yang memanggil
`window.instgrm.Embeds.process()` setiap kali daftar berubah.

**Embed itu berat.** Setiap embed Instagram memuat satu iframe penuh dari server
Meta. Sembilan embed sekaligus membuat halaman lambat dan memuat antre. Karena
itu feed dibatasi 3 post. Mekanisme dua tingkat tetap tersedia kalau daftarnya
nanti diperpanjang: hanya post `unggulan` yang dirender penuh, sisanya jadi
kartu ringan yang tidak memuat script pihak ketiga sama sekali, dan pengunjung
bisa menyalakan semuanya lewat toggle "Muat semua embed".

**Privasi pengunjung.** Embed resmi berarti Meta dan TikTok bisa memasang cookie
pada pengunjung website. Kalau nanti perlu patuh GDPR/kebijakan privasi, mode
kartu ringkas (tanpa embed) adalah opsi yang lebih aman.

**Cache.** Hasil feed disimpan 15 menit di memori proses. Kalau nanti jalan
multi-worker atau multi-server, ganti isi `backend/app/cache.py` dengan Redis —
antarmuka pemanggilnya sudah dipisah supaya penggantiannya tidak menyentuh kode lain.

---

## 7. Rekomendasi

**Untuk sekarang:** pakai mode `curated` apa adanya. Karena yang tampil hanya 3
post terbaru, memperbaruinya berarti mengganti satu baris JSON sesekali — jauh
lebih murah daripada mengurus token yang harus di-refresh tiap 60 hari.

**Aktifkan Graph API kalau:** frekuensi posting naik signifikan, atau ada orang
lain yang mengelola konten dan tidak mau menyentuh file JSON.

**TikTok:** tetap manual, kecuali TikTok Display API benar-benar diperlukan.
Menyalin tiga URL sekali jauh lebih cepat daripada menunggu proses persetujuan.
