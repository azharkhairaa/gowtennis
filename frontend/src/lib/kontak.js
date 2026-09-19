/**
 * Versi sisi-klien dari POST /api/contact.
 *
 * Dipakai hanya saat mode statis, ketika tidak ada backend yang bisa dipanggil.
 * Perilakunya sengaja disamakan dengan `backend/app/routers/contact.py`:
 * nomor 08xx dinormalkan ke 62xx, dan kalau nomor admin masih ditandai perlu
 * konfirmasi, pengunjung diarahkan ke DM Instagram alih-alih ke nomor yang
 * mungkin salah.
 */
export function susunTautanKontak({ nama, kontak, program, pesan }, profilKontak) {
  const prog = program || 'Coaching Session'
  const teks =
    `Halo Gow! Tennis, saya ${nama}. ` +
    `Saya tertarik ikut ${prog}. ` +
    `${pesan} ` +
    `(Kontak saya: ${kontak})`

  const wa = profilKontak?.whatsapp_admin || ''
  const digit = wa.replace(/\D/g, '')
  const perluKonfirmasi = Boolean(profilKontak?.whatsapp_perlu_konfirmasi)

  if (digit && !perluKonfirmasi) {
    const nomor = digit.startsWith('0') ? `62${digit.slice(1)}` : digit
    return `https://wa.me/${nomor}?text=${encodeURIComponent(teks)}`
  }
  return profilKontak?.instagram_dm || 'https://www.instagram.com/gowtennis/'
}
