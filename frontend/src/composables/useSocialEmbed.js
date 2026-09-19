import { nextTick } from 'vue'

/**
 * Memuat script embed resmi Instagram & TikTok satu kali saja, lalu memicu
 * pemrosesan ulang setelah Vue selesai merender blockquote baru.
 *
 * Ini bagian yang mudah terlewat di SPA: script embed hanya memindai DOM saat
 * pertama kali dimuat. Kalau kartu dirender belakangan (setelah fetch API),
 * blockquote-nya akan diam sebagai teks biasa sampai proses ulang dipanggil.
 */
const SCRIPTS = {
  instagram: 'https://www.instagram.com/embed.js',
  tiktok: 'https://www.tiktok.com/embed.js',
}

const dimuat = new Set()

function muatScript(src) {
  return new Promise((resolve, reject) => {
    if (dimuat.has(src)) return resolve()
    const existing = document.querySelector(`script[src="${src}"]`)
    if (existing) {
      dimuat.add(src)
      return resolve()
    }
    const el = document.createElement('script')
    el.src = src
    el.async = true
    el.onload = () => {
      dimuat.add(src)
      resolve()
    }
    el.onerror = () => reject(new Error(`Gagal memuat ${src}`))
    document.head.appendChild(el)
  })
}

export async function prosesEmbed(platforms = ['instagram', 'tiktok']) {
  await nextTick()
  for (const p of platforms) {
    try {
      await muatScript(SCRIPTS[p])
    } catch {
      // Embed pihak ketiga gagal dimuat (diblokir jaringan/adblock).
      // Kartu tetap menampilkan fallback berupa tautan ke post aslinya.
      continue
    }
  }
  // Instagram menyediakan API eksplisit untuk memindai ulang DOM.
  if (window.instgrm?.Embeds?.process) {
    window.instgrm.Embeds.process()
  }
  // TikTok tidak punya API serupa; script-nya memindai saat dimuat.
  // Untuk render ulang, script perlu dipasang kembali.
  if (dimuat.has(SCRIPTS.tiktok) && !window.__tiktokReprocessed) {
    window.__tiktokReprocessed = true
    const s = document.createElement('script')
    s.src = SCRIPTS.tiktok
    s.async = true
    document.body.appendChild(s)
  }
}
