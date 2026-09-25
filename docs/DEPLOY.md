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

### Sekali saja: siapkan PAGES_TOKEN

Pages diaktifkan otomatis oleh workflow, tapi butuh satu token karena
`GITHUB_TOKEN` bawaan **tidak diizinkan** memanggil endpoint pembuatan Pages
(`POST /repos/{owner}/{repo}/pages`) berapa pun `permissions` yang ditulis di
workflow. Tokennya harus datang dari luar.

**1. Buat token.** Buka
<https://github.com/settings/personal-access-tokens/new> (Settings → Developer
settings → Personal access tokens → **Fine-grained tokens**), lalu isi:

| Kolom | Isi |
|---|---|
| Token name | `gowtennis-pages` |
| Expiration | 90 hari (atau sesuai selera) |
| Repository access | **Only select repositories** → `gowtennis` |
| Permissions → Pages | **Read and write** |
| Permissions → Administration | **Read and write** |

Dua izin itu yang diminta endpoint tersebut. Karena aksesnya dibatasi ke satu
repo, cakupannya jauh lebih sempit daripada token classic.

Klik **Generate token**, lalu salin nilainya. Token hanya tampil sekali.

**2. Simpan sebagai secret.** Buka
<https://github.com/azharkhairaa/gowtennis/settings/secrets/actions> →
**New repository secret**:

- Name: `PAGES_TOKEN`
- Secret: tempel tokennya

Tempel hanya di halaman itu. Jangan menaruhnya di berkas mana pun di repo,
jangan kirim lewat chat, dan jangan tulis di pesan commit.

**3. Jalankan ulang.** Tab **Actions** → run yang gagal → **Re-run all jobs**.

Workflow akan membuat Pages sekaligus menyetel sumbernya ke GitHub Actions
(`build_type: workflow`), jadi tidak ada yang perlu dipilih manual di Settings.

### Kalau lebih suka tanpa token

Alternatifnya cukup dua klik dan tidak perlu token sama sekali:
**Settings → Pages → Build and deployment → Source: GitHub Actions**, lalu
re-run. Workflow ini menangani keduanya — tanpa `PAGES_TOKEN`, `enablement`
otomatis dimatikan dan deploy tetap jalan memakai `GITHUB_TOKEN`.

Karena itu pula **`PAGES_TOKEN` boleh dihapus setelah deploy pertama berhasil.**
Pages hanya perlu dibuat sekali; sesudah itu workflow tidak membutuhkannya lagi.

### Kalau muncul 403 saat membuat Pages

Berarti izin tokennya kurang. Periksa bahwa **Administration: Read and write**
benar-benar tercentang, dan repo `gowtennis` ada di daftar repository access.
Kalau fine-grained tetap ditolak, token **classic** dengan scope `repo` pasti
diterima (itu yang tercantum eksplisit di dokumentasi REST) — tapi scope `repo`
berlaku untuk **semua** repo milikmu, jadi pakai itu hanya sebagai jalan
terakhir dan cabut setelah selesai.

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
