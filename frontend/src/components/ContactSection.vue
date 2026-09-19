<script setup>
import { reactive, ref } from 'vue'
import { STATIC_MODE, postApi } from '../composables/useApi'
import { susunTautanKontak } from '../lib/kontak'

const props = defineProps({
  kontak: { type: Object, default: null },
  program: { type: Array, default: () => [] },
})

const form = reactive({ nama: '', kontak: '', program: '', pesan: '' })
const mengirim = ref(false)
const hasil = ref(null)
const galat = ref(null)

async function kirim() {
  mengirim.value = true
  galat.value = null
  hasil.value = null
  try {
    if (STATIC_MODE) {
      // Tidak ada backend untuk dipanggil. Susun tautannya di browser dengan
      // aturan yang sama seperti endpoint /api/contact.
      hasil.value = {
        ok: true,
        pesan: `Terima kasih ${form.nama}, pesanmu sudah siap dikirim.`,
        tindak_lanjut: susunTautanKontak(form, props.kontak),
      }
    } else {
      hasil.value = await postApi('/contact', {
        nama: form.nama,
        kontak: form.kontak,
        program: form.program || null,
        pesan: form.pesan,
      })
    }
  } catch (e) {
    galat.value = e.message
  } finally {
    mengirim.value = false
  }
}
</script>

<template>
  <section id="gabung" class="section section--dark">
    <div class="wrap join">
      <div class="join__copy">
        <span class="eyebrow">Gabung</span>
        <h2 class="section-title">Datang dulu, pikir belakangan</h2>
        <p class="section-lead">
          Belum punya raket bukan alasan. Sesi pemula sudah termasuk bola,
          ballboy, dan raket pinjaman yang bisa diminta ke admin.
        </p>

        <ul class="join__steps">
          <li><strong>1.</strong> Gabung grup WhatsApp untuk lihat jadwal terbaru.</li>
          <li><strong>2.</strong> Pilih sesi yang cocok, lalu kabari admin.</li>
          <li><strong>3.</strong> Admin konfirmasi slot dan titik lapangan.</li>
        </ul>

        <a
          v-if="props.kontak?.whatsapp_group"
          class="btn btn--primary join__group"
          :href="props.kontak.whatsapp_group"
          target="_blank"
          rel="noopener noreferrer"
        >
          <span class="join__group-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <path
                d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2zm5.8 14.06c-.24.68-1.42 1.3-1.95 1.35-.5.05-.98.23-3.3-.69-2.78-1.1-4.55-3.95-4.69-4.13-.14-.18-1.12-1.49-1.12-2.85 0-1.35.71-2.02.96-2.29.25-.28.55-.35.73-.35s.37 0 .53.01c.17.01.4-.07.62.48.24.57.8 1.97.87 2.11.07.14.12.31.02.49-.09.18-.14.29-.28.45-.14.16-.29.35-.42.47-.14.14-.28.29-.12.57.16.28.72 1.18 1.54 1.92 1.06.94 1.95 1.23 2.23 1.37.28.14.44.12.6-.07.17-.19.7-.81.88-1.09.19-.28.37-.23.63-.14.25.09 1.62.76 1.9.9.28.14.46.21.53.32.07.12.07.66-.16 1.34z"
              />
            </svg>
          </span>
          Gabung Grup WhatsApp
        </a>

        <div class="join__channels">
          <a
            class="btn btn--ghost btn--sm"
            :href="props.kontak?.instagram_dm || 'https://www.instagram.com/gowtennis/'"
            target="_blank"
            rel="noopener noreferrer"
            >DM Instagram</a
          >
          <a
            class="btn btn--ghost btn--sm"
            :href="props.kontak?.tiktok || 'https://www.tiktok.com/@gowtennis'"
            target="_blank"
            rel="noopener noreferrer"
            >TikTok</a
          >
        </div>

        <p v-if="props.kontak?.whatsapp_perlu_konfirmasi" class="join__note">
          Nomor WhatsApp admin belum ditampilkan di sini karena digit terakhirnya
          terpotong pada poster sumber. Lengkapi di
          <code>backend/data/profile.json</code> lalu tombol WhatsApp akan aktif
          otomatis.
        </p>
      </div>

      <form class="join__form" @submit.prevent="kirim">
        <h3 class="join__form-title">Formulir Pendaftaran</h3>

        <label>
          <span>Nama</span>
          <input v-model.trim="form.nama" type="text" required minlength="2" placeholder="Nama kamu" />
        </label>

        <label>
          <span>WhatsApp / Email</span>
          <input v-model.trim="form.kontak" type="text" required minlength="5" placeholder="08xx atau email" />
        </label>

        <label>
          <span>Program</span>
          <select v-model="form.program">
            <option value="">Belum tahu, minta rekomendasi</option>
            <option v-for="p in props.program" :key="p.nama" :value="p.nama">
              {{ p.nama }}
            </option>
          </select>
        </label>

        <label>
          <span>Pesan</span>
          <textarea
            v-model.trim="form.pesan"
            rows="3"
            required
            minlength="5"
            placeholder="Contoh: baru pertama kali main, mau ikut kelas Sabtu."
          />
        </label>

        <button class="btn btn--primary" type="submit" :disabled="mengirim">
          {{ mengirim ? 'Menyiapkan…' : 'Kirim' }}
        </button>

        <p v-if="galat" class="join__msg join__msg--error">{{ galat }}</p>

        <div v-if="hasil" class="join__msg join__msg--ok">
          <p>{{ hasil.pesan }}</p>
          <a
            class="btn btn--primary btn--sm"
            :href="hasil.tindak_lanjut"
            target="_blank"
            rel="noopener noreferrer"
            >Lanjutkan &amp; kirim pesan</a
          >
        </div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.join {
  display: grid;
  grid-template-columns: 1fr 0.9fr;
  gap: 56px;
  align-items: start;
}

.join__steps {
  list-style: none;
  margin: 28px 0;
  padding: 0;
  display: grid;
  gap: 11px;
}

.join__steps li {
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.95rem;
}

.join__steps strong {
  color: var(--lime-400);
  margin-right: 6px;
}

.join__group {
  margin-bottom: 14px;
}

.join__group-icon {
  display: inline-flex;
  align-items: center;
}

.join__channels {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.join__note {
  margin-top: 22px;
  font-size: 0.83rem;
  color: rgba(255, 255, 255, 0.5);
  max-width: 54ch;
}

.join__note code {
  background: rgba(255, 255, 255, 0.1);
  padding: 1px 6px;
  border-radius: 4px;
}

.join__form {
  background: #fff;
  color: var(--ink);
  border-radius: var(--radius-lg);
  padding: 32px 28px;
  display: grid;
  gap: 15px;
  box-shadow: var(--shadow-lg);
}

.join__form-title {
  font-size: 1.32rem;
  margin-bottom: 4px;
}

.join__form label {
  display: grid;
  gap: 6px;
}

.join__form label span {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.join__form input,
.join__form select,
.join__form textarea {
  width: 100%;
  font-family: inherit;
  font-size: 0.94rem;
  color: var(--ink);
  padding: 11px 13px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--paper-soft);
  transition: border-color 0.16s ease, box-shadow 0.16s ease;
}

.join__form textarea {
  resize: vertical;
}

.join__form input:focus,
.join__form select:focus,
.join__form textarea:focus {
  outline: none;
  border-color: var(--navy-600);
  box-shadow: 0 0 0 3px rgba(27, 58, 112, 0.12);
}

.join__form button[type='submit'] {
  margin-top: 6px;
}

.join__form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.join__msg {
  font-size: 0.89rem;
  padding: 13px 15px;
  border-radius: 10px;
  display: grid;
  gap: 11px;
  justify-items: start;
}

.join__msg--ok {
  background: rgba(215, 232, 75, 0.2);
  border: 1px solid var(--lime-500);
}

.join__msg--error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

@media (max-width: 900px) {
  .join {
    grid-template-columns: 1fr;
    gap: 36px;
  }
}
</style>
